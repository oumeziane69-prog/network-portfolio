# FortiGate Verification — Post-Configuration Checklist
# FortiGate DMZ Industrial — Post-Config Verification

> **Platform:** FortiGate 7.4.x (FGT-EDGE + FGT-INTERNAL)
> **Scope:** Commands to run after initial configuration to validate system state, HA, policies, and connectivity.

---

## 1. System Status

```bash
# Version and license
get system status
# Expected: Version: FortiOS v7.4.x, License: Valid (UTM features listed)

# Resource utilization
get system performance status
# Expected: CPU < 40% idle, Memory < 70% used

# Uptime and firmware
diagnose sys top
# Real-time process list — check for abnormal CPU consumers
```

---

## 2. HA Cluster Verification (FGT-EDGE)

```bash
# HA status overview
get system ha status
# Expected:
#   Model: FortiGate-600E
#   Mode: HA A-P
#   Group: FGT-EDGE-CLUSTER
#   Master: FGT-EDGE-A (priority 150)
#   Slave: FGT-EDGE-B (priority 100)
#   Heartbeat interfaces: port4, port5

# HA synchronization check
diagnose sys ha showcsum
# Both members should show identical checksums → config is in sync

# Session synchronization
diagnose sys session stat
# "session_count" should be near identical on both nodes

# Force failover test (optional, maintenance only)
# diagnose sys ha reset-uptime
# → Active member changes — verify traffic continues (session pickup)
```

---

## 3. Interface and Routing

```bash
# Interface status
get system interface physical
# Expected: port1 WAN up, port2 DMZ-IT up, port3 LAN-IT up, port4/5 HA up

# Routing table
get router info routing-table all
# Expected: default route 0.0.0.0/0 via WAN, local routes for LAN-IT/DMZ-IT

# SD-WAN health
diagnose sys sdwan health-check
# Expected: HC-Internet → server 8.8.8.8 → alive, RTT < 100ms

# SD-WAN member status
diagnose sys sdwan member
# port1 (WAN): cost 0, status=up
```

---

## 4. Firewall Policy Verification

```bash
# List all policies (ID + name)
show firewall policy | grep "edit\|set name"
# Expected: policies 10, 20, 30, 40, 50, 99

# Policy hit counters (confirm traffic is matching rules)
diagnose firewall iprope show 100004 0
# Shows per-policy packet/byte counters

# Session table — active connections
diagnose sys session list | head -50
# Check for active sessions matching expected flows

# Session by policy
diagnose sys session filter policy-id 10
diagnose sys session list
# Shows active sessions for LAN-IT → Internet policy
```

---

## 5. NAT / VIP Verification

```bash
# VIP table
show firewall vip
# Expected: VIP-WebServer-HTTPS (DNAT 443→172.16.10.10), VIP-Jump-SSH (DNAT 2222→172.16.10.20)

# SNAT pool
show firewall ippool
# Expected: SNAT-WAN = WAN IP, type=overload (PAT)

# Active NAT sessions
diagnose sys session filter nat 1
diagnose sys session list | head -30
# Shows NAT translated sessions with original + translated tuples
```

---

## 6. IPS and UTM Verification

```bash
# IPS engine status
diagnose ips memory status
# Expected: IPS engine running, memory OK

# IPS signature database version
diagnose autoupdate status
# Check: IPS (latest), AV (latest), AppCtrl (latest) — all updated

# UTM profile applied to active sessions
diagnose sys session list | grep "proto_state"
# UTM-inspected sessions show ssl=1 or ips=1

# IPS block log (last 10 drops)
diagnose log test    ## Generate test log entry
execute log filter category 1    ## IPS logs
execute log display
```

---

## 7. SSL Deep Inspection

```bash
# SSL inspection engine status
diagnose debug application ssl -1
diagnose debug enable
# Connect from LAN-IT to HTTPS site → observe SSL handshake interception

# Certificate used for inspection
show firewall ssl-ssh-profile SSL-DEEP-INSPECT-DMZ
# Expected: caname = Fortinet_CA_SSL

# Verify CA certificate installed in LAN client browsers
# (or deployed via GPO) — if not, browser will show certificate warning
diagnose debug disable
diagnose debug reset
```

---

## 8. Application Control and Web Filter

```bash
# AppCtrl engine
diagnose sys cmdbsvr info
# Lists running services including AppCtrl daemon

# Test P2P block (from LAN client simulate BitTorrent)
# → Policy 10 log should show AppCtrl block for category 25

# Web filter test
diagnose webfilter fortiguard-cache status
# Expected: cache active, last update < 24h

# Manual category lookup
diagnose webfilter rating example.com
# Returns: category ID, block/allow decision
```

---

## 9. Connectivity Tests

```bash
# From FGT-EDGE CLI — ICMP to Internet
execute ping 8.8.8.8
# Expected: 5/5 replies, latency < 50ms

# DNS resolution
execute ping www.google.com
# Expected: resolves and replies

# Test LAN-IT connectivity (via FGT-INTERNAL side)
execute ping-options source 10.0.10.1
execute ping 172.16.10.2
# Expected: reach FGT-INTERNAL port1 (DMZ-IT-ext)

# Traceroute to Internet
execute traceroute 8.8.8.8
# Expected: hop 1 = ISP GW, then internet path
```

---

## 10. Logging and FortiAnalyzer

```bash
# FortiAnalyzer connection status
diagnose log fortianalyzer test-connectivity
# Expected: Connection to <FORTI-ANALYZER-IP>: SUCCESS

# Real-time log stream (local disk)
diagnose debug enable
diagnose debug flow filter addr 172.16.10.10
diagnose debug flow trace start 100
# Then: trigger HTTPS to web server → observe flow decision
diagnose debug flow trace stop
diagnose debug disable

# Log statistics
diagnose log stat
# Shows logs sent to FAZ vs local storage ratio

# Implicit deny logs check
execute log filter category 0
execute log filter field action deny
execute log display
# All blocked traffic should appear (fwpolicy-implicit-log = enable)
```

---

## 11. FGT-INTERNAL Specific Checks

```bash
# OT protocol services
show firewall service custom | grep "edit\|set tcp-portrange"
# Expected: Modbus-TCP (502), OPC-UA (4840-4843), S7Comm (102), DNP3 (20000)

# IPS OT strict profile
show ips sensor IPS-OT-Strict
# Expected: block critical+high+medium, log-packet = enable

# DENY-LAN-OT-Internet policy hit counter
diagnose firewall iprope show 100004 0 | grep "idx=80"
# Should show 0 hits (no OT→Internet traffic — which is correct)

# RADIUS admin auth
diagnose test authserver radius RADIUS-CORP ms_chap_v2 <test-user> <test-pass>
# Expected: Access-Accept (if RADIUS server is reachable)
```

---

## 12. Security Acceptance Summary

| Check | Expected Result | Command |
|-------|----------------|---------|
| HA active member | FGT-EDGE-A master | `get system ha status` |
| HA sync | Checksums identical | `diagnose sys ha showcsum` |
| All interfaces up | port1-5 up | `get system interface physical` |
| Default route active | 0.0.0.0/0 via WAN | `get router info routing-table all` |
| VIPs configured | 2 VIPs present | `show firewall vip` |
| IPS DB updated | Version ≥ today | `diagnose autoupdate status` |
| FAZ connected | SUCCESS | `diagnose log fortianalyzer test-connectivity` |
| Policies 10-99 active | 6 rules on FGT-EDGE | `show firewall policy \| grep edit` |
| OT services defined | 4 custom services | `show firewall service custom` |
| DENY LAN-OT→Internet | Policy 80: 0 hits | `diagnose firewall iprope show 100004 0` |
