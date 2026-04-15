# Suricata IDS/IPS — Lab Topology
# Suricata 7.x — IDS and Inline IPS Deployment

> **Platform:** Suricata 7.x on Ubuntu 22.04 LTS
> **Context:** Hybrid deployment — passive IDS on IT segment + inline IPS on IT/OT boundary
> **Integration:** ELK Stack (Elasticsearch + Kibana) + FortiGate IPS policy offload

---

## 1. Architecture Overview

```
                     INTERNET
                        │
               ┌────────┴────────┐
               │   FGT-EDGE      │  FortiGate 600E (perimeter NGFW)
               │  10.0.10.1      │  Hardware IPS (NP7 ASIC)
               └────────┬────────┘
                        │
               ┌────────┴────────┐  LAN-IT  10.0.10.0/24
               │   SW-CORE       │  Cisco Catalyst 9300
               │  10.0.10.200    │  SPAN port → Suricata (IDS mode)
               └─┬──────┬────────┘
                 │      │ SPAN (mirror)
           ┌─────┘      ▼
           │    ┌────────────────┐
           │    │  SURICATA-IDS  │  Ubuntu 22.04 / Suricata 7.x
           │    │  10.0.10.110   │  Mode: IDS passive (AF_PACKET)
           │    │  ens3: mgmt    │  ens4: SPAN capture (no IP)
           │    └───────┬────────┘
           │            │ EVE JSON → Filebeat
           │            ▼
           │    ┌────────────────┐
           │    │   ELK Stack    │  Elasticsearch + Kibana
           │    │  10.0.10.120   │  Dashboards: Network threats,
           │    │                │  OT anomalies, scan detection
           │    └────────────────┘
           │
    ┌──────┴──────────────────────────┐
    │   SURICATA-IPS (inline bridge)  │  Ubuntu 22.04 / Suricata 7.x
    │   Mode: IPS inline (NFQUEUE)    │  Positioned between FGT-EDGE
    │   ens3: mgmt  10.0.10.111       │  DMZ-IT and FGT-INTERNAL
    │   ens4: bridge IN  (no IP)      │
    │   ens5: bridge OUT (no IP)      │
    └───┬────────────────────────┬────┘
        │   inline bridge        │
        ▼                        ▼
  [FGT-EDGE DMZ-IT]     [FGT-INTERNAL port1]
   172.16.10.1               172.16.10.2
        │                        │
        └────────── DMZ-IT ──────┘
                 172.16.10.0/24
```

---

## 2. Deployment Modes

### 2.1 Mode IDS (passive — LAN-IT monitoring)

```
SW-CORE SPAN port → Suricata capture interface (ens4, promiscuous, no IP)
                  → AF_PACKET capture (zero-copy, kernel bypass)
                  → EVE JSON alerts → /var/log/suricata/eve.json
                  → Filebeat → Elasticsearch → Kibana
```

- **No traffic impact** — read-only mirror
- **Use case:** Threat detection on corporate LAN (port scans, brute-force, C2 callbacks, DNS tunnels)
- **Drop action:** logging only (cannot block in passive mode)

### 2.2 Mode IPS (inline — DMZ-IT/OT boundary)

```
Traffic flow: FGT-EDGE ──► ens4 (IN) ──► Suricata (NFQUEUE) ──► ens5 (OUT) ──► FGT-INTERNAL
              [Internet-facing]                                              [OT-facing]
```

- **Inline L2 bridge** — Suricata acts as transparent bump-in-the-wire
- **NFQUEUE** — Linux netfilter queues packets to Suricata for verdict (ACCEPT / DROP)
- **Drop action:** hard drop — packet never reaches destination
- **Use case:** Block OT protocol anomalies (Modbus/OPC-UA attacks), enforce IT/OT boundary

---

## 3. Network Addressing

| Host | IP | Interface | Role |
|------|----|-----------|------|
| FGT-EDGE | 172.16.10.1 | DMZ-IT | Upstream router |
| SURICATA-IPS | — (bridge) | ens4/ens5 | Inline IPS L2 bridge |
| FGT-INTERNAL | 172.16.10.2 | DMZ-IT-ext | Downstream router |
| SURICATA-IDS | 10.0.10.110 | ens3 (mgmt) | Passive IDS management |
| SURICATA-IDS capture | — (no IP) | ens4 | SPAN capture interface |
| ELK Stack | 10.0.10.120 | eth0 | Elasticsearch:9200, Kibana:5601 |
| FGT-EDGE (LAN-IT) | 10.0.10.1 | port3 | LAN-IT gateway |
| SW-CORE | 10.0.10.200 | — | SPAN source switch |

---

## 4. Log and Alert Pipeline

```
Suricata (7.x)
  └── /var/log/suricata/eve.json    ← EVE JSON (all events)
  └── /var/log/suricata/fast.log    ← Human-readable alert log
  └── /var/log/suricata/stats.log   ← Performance statistics

Filebeat (8.x)
  └── input: /var/log/suricata/eve.json
  └── module: suricata (built-in Filebeat module)
  └── output: Elasticsearch 10.0.10.120:9200

Elasticsearch (8.x)
  └── index: filebeat-suricata-*
  └── ILM policy: 30-day hot → 90-day warm → delete

Kibana (8.x)
  └── Dashboard: Suricata Overview (Filebeat module)
  └── Dashboard: OT Anomalies (custom)
  └── Alert rules: Severity High/Critical → email + Slack webhook
```

---

## 5. OT-specific Detection Scope

| Protocol | Port | Detection focus |
|----------|------|----------------|
| Modbus/TCP | 502 | Function code anomalies, write to coils (unauthorized) |
| OPC-UA | 4840/4843 | Session floods, malformed NodeId |
| DNP3 | 20000 | Unsolicited responses, broadcast commands |
| S7Comm | 102 | Stop CPU commands (Siemens) |
| EtherNet/IP | 44818 | CIP service code scanning |
| IEC 60870-5-104 | 2404 | ASDU type anomalies |

---

## 6. Simulated Equipment

| Component | Technology | Notes |
|-----------|-----------|-------|
| Suricata IDS VM | Ubuntu 22.04 + Suricata 7.x | 4 vCPU, 8 GB RAM, 2 NICs |
| Suricata IPS VM | Ubuntu 22.04 + Suricata 7.x | 4 vCPU, 8 GB RAM, 3 NICs |
| ELK Stack VM | Ubuntu 22.04 + ELK 8.x | 8 vCPU, 16 GB RAM |
| SW-CORE | Cisco Catalyst 9300 (or GNS3) | SPAN session configured |
| FortiGate | FortiOS 7.4.x | IPS offload integration |
| Test traffic | Kali Linux + Metasploit | For rule validation (lab only) |
