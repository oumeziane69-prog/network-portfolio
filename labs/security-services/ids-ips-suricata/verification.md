# Suricata IDS/IPS — Verification and Troubleshooting
# Suricata 7.x — Post-Deployment Verification

> **Platform:** Suricata 7.x on Ubuntu 22.04
> **Modes:** IDS (AF_PACKET passive) + IPS (NFQUEUE inline)

---

## 1. Service Health

```bash
# Service status
sudo systemctl status suricata
# Expected: active (running), no errors in last lines

# Suricata version and build options
sudo suricata --build-info
# Check: Version 7.x, AF_PACKET: yes, NFQUEUE: yes, Hyperscan: yes (if available)

# Running process
ps aux | grep suricata
# Expected: /usr/bin/suricata -c /etc/suricata/suricata.yaml -q 0 (IPS)
#        or: /usr/bin/suricata -c /etc/suricata/suricata.yaml -i ens4 (IDS)
```

---

## 2. Configuration Syntax Check

```bash
# Validate suricata.yaml before applying
sudo suricata -T -c /etc/suricata/suricata.yaml -q 0
# Expected: Configuration provided was successfully loaded.

# Validate with verbose output (shows all loaded rule files)
sudo suricata -T -c /etc/suricata/suricata.yaml -v 2>&1 | tail -20
# Check: no "error" or "failed" lines

# Test configuration including rules
sudo suricata -T -c /etc/suricata/suricata.yaml -v 2>&1 | grep -E "rules|loaded|error"
# Expected: X rules successfully loaded from Y rule files
```

---

## 3. Rules Loading

```bash
# Count loaded rules
sudo suricatasc -c ruleset-stats | python3 -m json.tool
# Returns: total loaded rules, rules per file, disabled rules count

# Check custom OT rules loaded
sudo grep -c "^[adp]" /etc/suricata/rules/custom-rules.rules
# Count of active rules (alert/drop/pass lines)

# Verify specific SID is loaded
sudo suricatasc -c ruleset-stats 2>/dev/null | grep "9000001"
# Or check via log after reload:
sudo suricatasc -c reload-rules
sudo grep "rules loaded" /var/log/suricata/suricata.log | tail -3
# Expected: X rules successfully loaded
```

---

## 4. Update Rules

```bash
# Update Emerging Threats Open ruleset
sudo suricata-update
# Expected: Fetching https://rules.emergingthreats.net/open/suricata-7.0/emerging.rules.tar.gz
#           ... X rules loaded, Y enabled

# List configured sources
sudo suricata-update list-sources

# Force update (ignore cache)
sudo suricata-update --no-cache

# Reload rules without restart (live reload)
sudo suricatasc -c reload-rules
# Expected: {"message": "done", "return": "OK"}

# Or via kill -USR2
sudo kill -USR2 $(cat /var/run/suricata/suricata.pid)
```

---

## 5. Alert Log Monitoring

```bash
# Real-time alert stream (human-readable)
sudo tail -f /var/log/suricata/fast.log
# Format: MM/DD/YYYY-HH:MM:SS.us [**] [SID:X:REV] MSG [**] [Classification: X] [Priority: X] {PROTO} SRC:PORT -> DST:PORT

# EVE JSON real-time stream (all events)
sudo tail -f /var/log/suricata/eve.json | python3 -m json.tool | head -50

# Filter only alerts from EVE JSON
sudo tail -f /var/log/suricata/eve.json | jq 'select(.event_type=="alert")'

# Custom OT rule alerts only (SID 9000001–9000099)
sudo tail -f /var/log/suricata/eve.json | \
  jq 'select(.event_type=="alert" and .alert.signature_id >= 9000000)'

# Alert summary by signature (last 100)
sudo tail -1000 /var/log/suricata/fast.log | grep "\[\*\*\]" | \
  awk -F'[\\[\\]]' '{print $4}' | sort | uniq -c | sort -rn | head -20
```

---

## 6. Test Rule Triggering (Lab Validation)

### 6.1 Test Rule 9 — LAN-OT → Internet (SID 9000009)

```bash
# From a host in LAN-OT (172.16.30.x) — attempt outbound TCP
# (This should be dropped by Suricata IPS before reaching FGT-INTERNAL)
ssh user@172.16.30.20     # then from HMI:
curl --connect-timeout 3 http://8.8.8.8
# Expected: Connection refused / timed out (dropped by Suricata)

# Verify on Suricata:
sudo tail -f /var/log/suricata/fast.log | grep "9000009"
# Expected: alert entry with src=172.16.30.x, dst=<external>
```

### 6.2 Test Rule 1 — Modbus Write Coils (SID 9000001)

```bash
# From a host outside OT_NET — send Modbus write to port 502
# Use mbtget (modbus test tool) or netcat:
python3 -c "
import socket, struct
s = socket.socket()
s.connect(('172.16.30.10', 502))
# Modbus Write Single Coil (FC 05) — write coil 1 to ON
pkt = struct.pack('>HHHBBHH', 1, 0, 6, 1, 5, 0, 0xFF00)
s.send(pkt)
print('Sent:', pkt.hex())
s.close()
"

# Verify alert on Suricata:
sudo tail -5 /var/log/suricata/fast.log
# Expected: [9000001:2] OT-MODBUS Unauthorized Write Coils from non-OT source
```

### 6.3 Test Rule 6 — S7Comm Stop CPU (SID 9000006)

```bash
# Simulate S7Comm Stop CPU from an unauthorized host
python3 -c "
import socket, struct
s = socket.socket()
s.connect(('172.16.30.10', 102))
# TPKT + COTP + S7 Stop CPU (simplified)
tpkt   = b'\x03\x00\x00\x1f'    # TPKT header
cotp   = b'\x02\xf0\x80'        # COTP DT Data
s7hdr  = b'\x32\x01\x00\x00'    # S7Comm header (Job)
s7fn   = b'\x00\x29'            # Function code: Stop CPU
pkt = tpkt + cotp + s7hdr + s7fn + b'\x00' * 10
s.send(pkt)
print('Sent S7Comm Stop CPU simulation')
s.close()
"

sudo tail -3 /var/log/suricata/fast.log
# Expected: [9000006:2] OT-S7COMM Stop CPU command from unauthorized host
```

---

## 7. NFQUEUE IPS Mode Verification

```bash
# Verify NFQUEUE rules are in place
sudo iptables -L FORWARD -v -n | grep NFQUEUE
# Expected: NFQUEUE  all  --  ens4  *   0.0.0.0/0  0.0.0.0/0  NFQUEUE num 0 bypass

# Verify Suricata is listening on queue 0
sudo suricatasc -c dump-counters | python3 -m json.tool | grep -i "nfq\|queue"

# Packet counter verification (traffic flowing through)
sudo suricatasc -c dump-counters | python3 -m json.tool | grep "capture.kernel_packets"
# Should increment over time → traffic is being inspected

# Bridge interfaces forwarding
bridge fdb show | head -10
# Should show MAC entries on ens4 and ens5
```

---

## 8. Performance and Stats

```bash
# Live performance stats
sudo tail -f /var/log/suricata/stats.log | grep -E "kernel_drops|capture.kernel_packets|decoder.pkts"
# Watch for:
#   capture.kernel_packets → total packets seen
#   capture.kernel_drops → packets dropped by kernel (ring buffer overflow)
#   decoder.pkts → packets decoded by Suricata

# Kernel drops should be < 0.1% of total packets
# If drops are high → increase ring-size in suricata.yaml

# Live stats via suricatasc
sudo watch -n 5 "sudo suricatasc -c iface-stat --iface ens4 2>/dev/null | python3 -m json.tool"

# CPU and memory usage
sudo suricatasc -c dump-counters | python3 -m json.tool | grep -E "flow.active|memuse"
```

---

## 9. EVE JSON Log Analysis

```bash
# Parse EVE JSON with jq — alert summary
sudo cat /var/log/suricata/eve.json | \
  jq 'select(.event_type=="alert") | {ts: .timestamp, src: .src_ip, dst: .dest_ip, sig: .alert.signature, sid: .alert.signature_id}' \
  | head -40

# DNS anomalies (potential DNS tunneling)
sudo cat /var/log/suricata/eve.json | \
  jq 'select(.event_type=="dns" and (.dns.rrname | length) > 50)' \
  | head -10
# Long DNS names (> 50 chars) may indicate DNS tunneling

# HTTP without User-Agent (scripted scanners)
sudo cat /var/log/suricata/eve.json | \
  jq 'select(.event_type=="http" and (.http.http_user_agent == null or .http.http_user_agent == ""))' \
  | head -10

# TLS SNI anomalies (connections to unusual domains)
sudo cat /var/log/suricata/eve.json | \
  jq 'select(.event_type=="tls") | .tls.sni' | sort | uniq -c | sort -rn | head -20

# Top talkers (most active source IPs)
sudo cat /var/log/suricata/eve.json | \
  jq -r 'select(.event_type=="flow") | .src_ip' | sort | uniq -c | sort -rn | head -10

# Custom OT rules hits (SID range 9000000–9000099)
sudo cat /var/log/suricata/eve.json | \
  jq 'select(.event_type=="alert" and .alert.signature_id >= 9000000) | 
      {time: .timestamp, src: .src_ip, dst: .dest_ip, msg: .alert.signature, action: .alert.action}'
```

---

## 10. ELK Stack Verification

```bash
# Elasticsearch health check
curl -u elastic:<ELASTIC-PASSWORD-HERE> http://10.0.10.120:9200/_cluster/health?pretty
# Expected: "status" : "green", "number_of_nodes" : 1+

# Check Suricata index exists and has data
curl -u elastic:<ELASTIC-PASSWORD-HERE> \
  http://10.0.10.120:9200/filebeat-suricata-*/_count?pretty
# Expected: "count" > 0

# Filebeat status (on Suricata host)
sudo filebeat test output
# Expected: Elasticsearch: http://10.0.10.120:9200... OK

# Filebeat running
sudo systemctl status filebeat
# Expected: active (running)

# Kibana access
curl -s http://10.0.10.120:5601/api/status | python3 -m json.tool | grep '"status"'
# Expected: "status": {"overall": {"level": "available"}}
```

---

## 11. Threshold and False Positive Tuning

```bash
# View threshold configuration
cat /etc/suricata/threshold.conf

# Suppress a noisy rule for a specific host (add to threshold.conf):
cat >> /etc/suricata/threshold.conf << 'EOF'
# Suppress rule 2010935 (ET SCAN) for our vulnerability scanner
suppress gen_id 1, sig_id 2010935, track by_src, ip 10.0.10.200

# Rate-limit rule 9000002 to max 1 alert per source per hour
threshold gen_id 1, sig_id 9000002, type threshold, track by_src, count 1, seconds 3600
EOF

# Reload thresholds (requires rule reload)
sudo suricatasc -c reload-rules
```

---

## 12. Verification Summary

| Check | Expected Result | Command |
|-------|----------------|---------|
| Service running | active (running) | `systemctl status suricata` |
| Config valid | "successfully loaded" | `suricata -T -c suricata.yaml -q 0` |
| Custom OT rules loaded | SIDs 9000001–9000011 | `suricatasc -c ruleset-stats` |
| ET Open rules loaded | > 10,000 rules | `suricata-update` output |
| NFQUEUE active (IPS) | iptables FORWARD NFQUEUE | `iptables -L FORWARD -n` |
| Traffic flowing (IPS) | kernel_packets > 0 | `suricatasc -c dump-counters` |
| Kernel drops < 0.1% | drops/packets ratio | `stats.log` analysis |
| EVE JSON writing | eve.json growing | `ls -lh /var/log/suricata/eve.json` |
| Filebeat shipping | count > 0 in ES | ES `_count` API |
| Kibana accessible | status: available | `curl kibana/api/status` |
| Rule 9000009 fires | LAN-OT → Internet alert | Trigger test + `fast.log` |
| Rule 9000006 fires | S7Comm Stop CPU alert | Trigger test + `fast.log` |
| SIEM alert rule | Email/Slack on critical | Kibana → Rules test |
