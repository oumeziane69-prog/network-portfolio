# FortiGate + Suricata IPS Integration
# FortiGate IPS and Suricata — Complementary Deployment

> **Context:** FortiGate hardware IPS (NP7 ASIC) at the perimeter + Suricata software IPS at the IT/OT boundary — defense in depth.
> **FortiOS:** 7.4.x | **Suricata:** 7.x

---

## 1. Defense-in-Depth Architecture

```
INTERNET
    │
    ▼
┌──────────────────────────────────────────────────────────────────┐
│  FGT-EDGE — FortiGate 600E                                       │
│  Hardware IPS (NP7 ASIC) — Layer 1 filtering                    │
│  • Known CVE signatures (FortiGuard IPS — 20,000+ signatures)   │
│  • Protocol anomaly (HTTP/TLS/DNS/SMTP)                          │
│  • Botnet C2 blocking (FortiGuard IP reputation)                 │
│  • SSL deep inspection (inbound HTTPS)                           │
│  Throughput: up to 7 Gbps (NP7 offloaded)                       │
└──────────────────────────────────────────────────────────────────┘
    │ Filtered traffic (known attacks dropped)
    ▼
┌──────────────────────────────────────────────────────────────────┐
│  SURICATA-IPS — inline bridge (DMZ-IT → DMZ-OT boundary)        │
│  Software IPS (CPU-based) — Layer 2 filtering                   │
│  • Custom OT rules (Modbus/OPC-UA/S7Comm/DNP3/EtherNet-IP)     │
│  • Emerging Threats ruleset (ET Open)                            │
│  • Behavioral detection (threshold-based flooding, scans)        │
│  • Lateral movement detection (IT→OT direct paths)              │
│  Throughput: ~2 Gbps on 8-core VM (NFQUEUE)                    │
└──────────────────────────────────────────────────────────────────┘
    │ Deep OT-inspected traffic
    ▼
┌──────────────────────────────────────────────────────────────────┐
│  FGT-INTERNAL — FortiGate 200F                                   │
│  Policy enforcement — Layer 3 filtering                         │
│  • Zone-based policies (DMZ-OT, LAN-OT)                         │
│  • IPS-OT-Strict profile (FortiGuard OT signatures)             │
│  • Hard DENY LAN-OT → Internet/IT                               │
└──────────────────────────────────────────────────────────────────┘
```

### Division of Responsibility

| Layer | Tool | Strength | What it covers |
|-------|------|---------|----------------|
| Perimeter | FortiGate IPS (NP7) | High throughput, ASIC acceleration | Known CVEs, botnet IPs, mass-volume threats |
| IT/OT boundary | Suricata IPS | Deep OT protocol parsing, custom rules | OT-specific attacks, behavioral anomalies |
| OT enforcement | FGT-INTERNAL | Stateful policy, zone isolation | Policy violations, explicit deny rules |

---

## 2. FortiGate IPS Configuration (FGT-EDGE)

### 2.1 IPS Sensor for Inbound DMZ Traffic

```bash
# On FGT-EDGE — FortiOS CLI
config ips sensor
    edit "IPS-DMZ-Inbound-Extended"
        set comment "Extended IPS for inbound DMZ — complements Suricata"
        config entries
            edit 1
                set severity critical high
                set action block
                set status enable
                set log enable
                set log-packet enable
            next
            edit 2
                set severity medium
                set action monitor            ## Monitor only — Suricata handles blocking
                set status enable
                set log enable
            next
            edit 3
                ## OT-specific FortiGuard signatures
                set application "Modbus" "SCADA" "DNP3" "OPC"
                set action block
                set status enable
                set log enable
                set log-packet enable
            next
        end
        ## Rate-based signatures
        set scan-botnet-connections block
        set block-malicious-url enable
    next
end
```

### 2.2 Apply IPS Sensor to Policy 40 (Internet → WebServer)

```bash
config firewall policy
    edit 40
        set ips-sensor "IPS-DMZ-Inbound-Extended"
        set utm-status enable
        set logtraffic all
    next
end
```

### 2.3 FortiGate IPS Log Export to Suricata EVE-compatible SIEM

```bash
# Configure FortiAnalyzer to forward IPS events to ELK
# On FortiAnalyzer — CEF output to Logstash
config system log-forward
    edit 1
        set mode forwarding
        set fwd-max-delay realtime
        set server-name "ELK-Logstash"
        set server-addr 10.0.10.120
        set fwd-server-type syslog
        set log-field-exclusion-status disable
        set fwd-facility local7
    next
end
```

---

## 3. Suricata IPS — Linux Setup (Inline NFQUEUE Mode)

### 3.1 Prerequisites

```bash
# Install Suricata 7.x from OISF repository
sudo add-apt-repository ppa:oisf/suricata-stable
sudo apt update
sudo apt install suricata suricata-update -y

# Verify version
suricata --build-info | grep "Version\|NFQUEUE\|AF_PACKET"
# Expected: Version 7.x, NFQUEUE: yes, AF_PACKET: yes

# Install required kernel modules
sudo modprobe nfnetlink_queue
sudo modprobe xt_NFQUEUE
lsmod | grep -E "nfnetlink|NFQUEUE"
```

### 3.2 Linux Bridge Setup (bump-in-the-wire)

```bash
# Create bridge br0 between ens4 (IN from FGT-EDGE) and ens5 (OUT to FGT-INTERNAL)
sudo ip link add br0 type bridge
sudo ip link set ens4 master br0
sudo ip link set ens5 master br0
sudo ip link set br0 up
sudo ip link set ens4 up
sudo ip link set ens5 up

# Verify bridge is forwarding
bridge link show

# Persist via /etc/netplan/00-suricata-bridge.yaml
cat << 'EOF' | sudo tee /etc/netplan/00-suricata-bridge.yaml
network:
  version: 2
  ethernets:
    ens4:
      dhcp4: no
    ens5:
      dhcp4: no
  bridges:
    br0:
      interfaces: [ens4, ens5]
      dhcp4: no
      parameters:
        stp: false
        forward-delay: 0
EOF
sudo netplan apply
```

### 3.3 iptables NFQUEUE Rules

```bash
# Forward all traffic through bridge to NFQUEUE 0
# Suricata will inspect and return ACCEPT or DROP verdict

sudo iptables -I FORWARD -i ens4 -j NFQUEUE --queue-num 0 --queue-bypass
sudo iptables -I FORWARD -i ens5 -j NFQUEUE --queue-num 0 --queue-bypass

# --queue-bypass: if Suricata is not running, packets bypass queue (fail-open)
# Remove --queue-bypass for strict fail-closed behavior

# Save rules
sudo iptables-save | sudo tee /etc/iptables/rules.v4

# Verify
sudo iptables -L FORWARD -v -n
```

### 3.4 Start Suricata in IPS Mode

```bash
# Test configuration
sudo suricata -T -c /etc/suricata/suricata.yaml -q 0
# Expected: Configuration provided was successfully loaded.

# Run in IPS mode (NFQUEUE 0)
sudo suricata -c /etc/suricata/suricata.yaml -q 0 -D
# -D: daemon mode

# Or use systemd service
sudo systemctl enable suricata
sudo systemctl start suricata
sudo systemctl status suricata
```

### 3.5 Update Rules

```bash
# Update Emerging Threats Open ruleset
sudo suricata-update

# List available rulesets
sudo suricata-update list-sources

# Add ET Pro (commercial — requires subscription)
# sudo suricata-update enable-source et/pro --secret-code <ET-PRO-KEY-HERE>

# Reload rules without restart
sudo suricatasc -c reload-rules
# Returns: {"message": "done", "return": "OK"}
```

---

## 4. Suricata + FortiGate: Alert Correlation via ELK

### 4.1 Filebeat Configuration

```yaml
# /etc/filebeat/filebeat.yml
filebeat.modules:
  - module: suricata
    eve:
      enabled: true
      var.paths: ["/var/log/suricata/eve.json"]

output.elasticsearch:
  hosts: ["10.0.10.120:9200"]
  username: "filebeat_writer"
  password: "<ELASTIC-PASSWORD-HERE>"
  index: "filebeat-suricata-%{+yyyy.MM.dd}"

setup.kibana:
  host: "10.0.10.120:5601"

setup.dashboards.enabled: true    # Auto-import Suricata dashboards
```

### 4.2 Logstash Pipeline (FortiGate + Suricata unified)

```ruby
# /etc/logstash/conf.d/fortigate-suricata.conf

input {
  # Suricata EVE JSON via Filebeat
  beats {
    port => 5044
    type => "suricata"
  }
  # FortiGate CEF via syslog
  syslog {
    port => 5140
    type => "fortigate"
  }
}

filter {
  if [type] == "suricata" {
    json {
      source => "message"
    }
    date {
      match => ["timestamp", "ISO8601"]
      target => "@timestamp"
    }
    mutate {
      add_field => { "sensor" => "suricata-ips" }
      add_field => { "location" => "IT-OT-boundary" }
    }
  }

  if [type] == "fortigate" {
    # Parse FortiGate CEF log format
    grok {
      match => {
        "message" => "CEF:%{NUMBER:cef_version}\|%{DATA:device_vendor}\|%{DATA:device_product}\|%{DATA:device_version}\|%{DATA:signature_id}\|%{DATA:name}\|%{NUMBER:severity}\|%{GREEDYDATA:extensions}"
      }
    }
    kv {
      source => "extensions"
      field_split => " "
      value_split => "="
    }
    mutate {
      add_field => { "sensor" => "fortigate-ips" }
      add_field => { "location" => "perimeter" }
    }
  }

  # Normalize common fields
  mutate {
    rename => { "[src][ip]" => "source_ip" }
    rename => { "[dest][ip]" => "destination_ip" }
  }
}

output {
  elasticsearch {
    hosts => ["10.0.10.120:9200"]
    index => "security-events-%{+yyyy.MM.dd}"
  }
}
```

---

## 5. Kibana Dashboards and Alert Rules

### 5.1 Built-in Suricata Dashboards (Filebeat module)

```
Kibana → Dashboards → [Filebeat Suricata] Overview
  - Alert count by severity
  - Top source IPs (attack origins)
  - Top alert signatures (most triggered rules)
  - Geo map of source IPs
  - Protocol breakdown

Kibana → Dashboards → [Filebeat Suricata] Alerts
  - Timeline of alerts
  - Alert drill-down (src/dst/signature/payload)
```

### 5.2 Custom OT Anomaly Dashboard

```
Kibana → Create Dashboard → "OT Protocol Anomalies"

Lens panels:
  1. Count of SID 9000001–9000011 (custom OT rules) over time
  2. Top 10 source IPs triggering OT rules
  3. Rule breakdown (pie: Modbus/DNP3/S7Comm/OPC-UA/Exfil)
  4. Critical alerts: SID 9000009 (OT→Internet) + SID 9000010
  5. Table: recent alerts (timestamp, src, dst, msg, signature)
```

### 5.3 Alerting Rules (Kibana)

```
Kibana → Stack Management → Rules → Create Rule

Rule 1: OT Outbound Connection Attempt
  Type: Elasticsearch query
  Query: event.module:suricata AND alert.signature_id:(9000009 OR 9000010)
  Threshold: count > 0 in 1 minute
  Action: Email + Slack webhook (critical)

Rule 2: S7Comm Stop CPU Attempt
  Query: event.module:suricata AND alert.signature_id:9000006
  Threshold: count > 0 in 5 minutes
  Action: PagerDuty + Email (critical — potential plant shutdown)

Rule 3: Modbus Write Coils from Unauthorized Host
  Query: event.module:suricata AND alert.signature_id:9000001
  Threshold: count > 5 in 10 minutes
  Action: Slack webhook (high)
```

---

## 6. Comparison — FortiGate IPS vs Suricata

| Criterion | FortiGate IPS (NP7) | Suricata 7.x |
|-----------|-------------------|-------------|
| **Rule language** | FortiGuard binary signatures | Snort-compatible text rules (open) |
| **Throughput** | Up to 7 Gbps (ASIC) | ~2 Gbps on 8-core VM |
| **Custom OT rules** | Limited — FortiGuard OT bundle | ✅ Full — write Modbus/S7/DNP3 rules in text |
| **Update model** | FortiGuard subscription (SaaS) | suricata-update (ET Open = free) |
| **Protocol decoding** | FortiGuard decoders (closed) | Open app-layer parsers (Modbus, DNP3, ENIP, OPCUA) |
| **EVE JSON logging** | No (proprietary log format) | ✅ Standard JSON — direct ELK/Splunk ingest |
| **Community rules** | No (commercial only) | ✅ Emerging Threats Open (free), ET Pro, PTOPEN |
| **Fail-open/fail-closed** | HA failover (hardware) | Configurable (--queue-bypass) |
| **Cost** | Included in FortiGuard UTM bundle | Open-source (free) |
| **Maintenance** | FortiGate firmware updates | apt upgrade suricata + suricata-update |
| **Best for** | High-volume perimeter, known CVEs | Custom OT rules, behavioral detection, research |
