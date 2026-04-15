# Check Point Verification — Post-Deployment Checklist
# Check Point R81.x — Post-Deploy Verification Commands

> **Platform:** Check Point R81.x — SMS + ClusterXL Gateway
> **Scope:** Commands to run from SMS CLI, gateway CLI, and SmartConsole to validate a freshly installed policy.

---

## 1. SMS Health Check

```bash
# SSH to SMS (10.0.50.10)
ssh admin@10.0.50.10

# Check management server status (SmartCenter processes)
cpstat mg
# Expected: All daemons running (FWM, FWLOG, CPD, etc.)
# Lines like: Policy: installed, Connections: X active admins

# Check CPD (Check Point daemon) status
cpwd_admin list
# Lists all running CP processes and their PID/status

# Check SIC (Secure Internal Communication) status
cpca_client lscert -kind SIC
# Lists SIC certificates for all registered gateways

# Management API status
api status
# Expected: API is started and ready on port 443
```

---

## 2. Gateway SIC and Connection

```bash
# On SMS — verify gateways are connected
cpstat -f all mg | grep -A5 "Gateway"

# On GW-A (SSH to GW-A IP)
ssh admin@<GW-A-MGMT-IP>
expert

# SIC status (should show "communicating")
cpstat os | grep -i sic

# Policy installation status
fw stat -l
# Expected output:
# HOST          POLICY          DATE                INTERFACE
# localhost     Standard        15Apr2026 10:30:21  All
```

---

## 3. ClusterXL Status

```bash
# On GW-A — cluster state
cphaprob stat
# Expected:
# Cluster Mode:   High Availability (Active Up) with IGMP Membership
# Number         Unique Address  Assigned Load  State
# 1 (local)      <GW-A-IP>        100%           ACTIVE
# 2              <GW-B-IP>          0%           STANDBY

# Cluster interfaces
cphaprob -a if
# Lists all cluster interfaces and their state (operational/failed)

# Cluster synchronization
cphaprob -l list
# Lists configured probes and their status

# On SMS — ClusterXL state from management perspective
SmartConsole → Gateways & Servers → FW-CLUSTER → double-click
# Cluster page shows member states, sync status
```

---

## 4. Policy Verification

```bash
# On GW-A — installed policy name and date
fw stat
# Output: Policy name = "Standard", install timestamp

# Full policy stats
fw stat -l
# Interface list + policy per interface

# Rule base loaded in kernel
fw ctl get int fwaccel_enabled
# Should return 0 if SecureXL acceleration enabled check is needed

# Policy compilation check (on SMS)
$FWDIR/bin/fwm verify Standard
# Returns: policy verified OK, no compilation errors
```

---

## 5. Traffic and Session Table

```bash
# On GW-A — connection table (kernel connections)
fw tab -t connections -s
# Returns: connections count (number of tracked sessions)

# View active connections
fw tab -t connections -f | head -30
# Format: src IP, dst IP, proto, state

# Per-interface stats
fw ctl iflist
# Lists interfaces registered in CP kernel

fw ctl pstat
# Kernel statistics: inspected packets, connections, NAT entries

# Real-time connection monitoring
fw monitor -e "accept;" -o /tmp/fw-capture.pcap
# Capture all accepted traffic (CTRL+C to stop)
# Review: tcpdump -r /tmp/fw-capture.pcap | head -20
```

---

## 6. NAT Verification

```bash
# NAT table
fw tab -t fwx_cache -s
# Shows NAT translation entries count

# Detailed NAT entries
fw tab -t fwx_cache -f | head -20
# Source/translated address pairs

# Verify SNAT working (from Internal client)
# On SMS CLI:
fw monitor -e "host 10.0.50.100 and accept;" -o /tmp/nat-test.pcap
# → Trigger HTTP from 10.0.50.100 → observe SNAT to cluster VIP in capture

# On GW-A — verify SNAT pool active
fw tab -t fwx_alloc -s
```

---

## 7. Logs and Monitoring

```bash
# On GW-A — real-time log stream
fw log -t -n
# Output: timestamp | action | src | dst | proto | rule | service

# Filtered logs — see all drops
fw log -t -n | grep "DROP"

# Logs for specific host
fw log -t -n | grep "10.0.50.100"

# Logs archive list
ls -la $FWDIR/log/
# fw.log = current, fw.log.YYYYMMDD = archives

# From SmartConsole — Logs & Monitor
# Filter: Action:Drop → blocked traffic
# Filter: Blade:Firewall → policy decisions
# Filter: Source:10.0.50.100 → per-host audit
```

---

## 8. Threat Prevention (IPS/AV/Anti-Bot)

```bash
# Threat Prevention status (on GW-A)
cpstat blades | grep -i "threat\|ips\|av"
# Expected: IPS: Active, AV: Active, Anti-Bot: Active

# IPS engine status
ips stat
# Shows: IPS updates version, engine status, active profile

# IPS update check (on SMS)
cpinfo -y all | grep -i ips
# IPS signature database version + last update

# Anti-Bot database
cpstat ab
# Expected: database loaded, last update recent

# URL Filtering category test (from SMS)
SmartConsole → Security Policies → Threat Prevention → check profile TP-Profile-DMZ-Inbound
```

---

## 9. Identity Awareness Check

```bash
# On GW-A — Identity Awareness status
pdp status
# Expected: PDP (Policy Decision Point) running, connected to AD

# LDAP connection
pdp connections
# Shows AD server connections: lab.local → 10.0.50.20 → Connected

# PDP entries (users identified)
pdp monitor user all | head -20
# Shows: username, IP, AD groups, login time

# SmartConsole — Identity Awareness logs
Logs & Monitor → new tab → filter: Blade:Identity Awareness
# Verify: login events from AD domain
```

---

## 10. HTTPS Inspection

```bash
# HTTPS Inspection status (on GW-A)
cpstat blades | grep HTTPS
# Expected: HTTPS Inspection: Active

# Inspection log (see inspected flows)
fw log -t -n | grep "HTTPS_INSPECTION"

# Bypass check (banking sites should NOT be inspected)
# Generate traffic from Internal client to a banking site
# In SmartConsole Logs: Action = "Accept", Blade = HTTPS, 
#   look for "HTTPS Inspection Bypass" in rule match

# Certificate chain — verify CP internal CA is trusted by browsers
SmartConsole → Manage & Settings → Blades → HTTPS Inspection
→ CA Certificate → Export → compare thumbprint with client browser
```

---

## 11. High Availability Failover Test

```bash
# Planned failover procedure (maintenance)

# Step 1 — On SMS, note current active member
cphaprob stat

# Step 2 — On GW-A (current active), simulate failover
cphaprob -d <critical-device> -s problem -t 0 report
# → GW-B becomes active

# Step 3 — Verify GW-B is now active
# SSH to GW-B: cphaprob stat → shows GW-B as ACTIVE

# Step 4 — Test traffic continuity during failover
# Ping flood from client: ping -t 8.8.8.8
# Expected: < 3 packet loss during failover (session pickup)

# Step 5 — Restore GW-A as active
cphaprob -d <critical-device> -s ok report
# GW-A priority 150 > GW-B priority 100 → GW-A reclaims active

# Step 6 — Verify policy reinstalled correctly
fw stat -l   # on both members
```

---

## 12. cpinfo — Full System Diagnostic

```bash
# Generate full system diagnostic package (on SMS or GW)
cpinfo -o /tmp/cpinfo-$(hostname)-$(date +%Y%m%d).tar.gz
# → Creates compressed archive with all system info, logs, config

# Key files included:
#   /opt/CPshared/5.0/conf/   — CP shared config
#   $FWDIR/conf/              — FW config files
#   $FWDIR/log/               — log files (sampled)
#   /var/log/messages         — syslog

# Quick health report only
cpinfo -y all 2>&1 | tee /tmp/health-$(date +%Y%m%d).txt
```

---

## 13. Security Acceptance Summary

| Check | Expected Result | Command |
|-------|----------------|---------|
| SMS processes | All running | `cpstat mg` |
| GW-A SIC | Communicating | `cpstat os \| grep sic` |
| GW-B SIC | Communicating | same on GW-B |
| Policy installed | Standard (latest date) | `fw stat -l` |
| ClusterXL GW-A | ACTIVE (100%) | `cphaprob stat` |
| ClusterXL GW-B | STANDBY (0%) | `cphaprob stat` |
| HA sync | No sync errors | `cphaprob -l list` |
| IPS active | IPS: Active | `cpstat blades` |
| Anti-Bot active | AB: Active | `cpstat blades` |
| Identity Awareness | PDP connected to AD | `pdp status` |
| HTTPS Inspection | Active | `cpstat blades \| grep HTTPS` |
| Connections in kernel | > 0 (live traffic) | `fw tab -t connections -s` |
| Logs streaming to SMS | fw.log growing | `ls -la $FWDIR/log/` |
