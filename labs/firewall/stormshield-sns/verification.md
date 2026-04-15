# Stormshield SNS — Verification and Acceptance
# SNS Post-Configuration Verification — Commands and Acceptance Procedure

> **Platform:** Stormshield SNS 4.x
> **Access:** stcli (SSH), SN Console (GUI), SN Real-Time Monitor

---

## 1. System Status

```bash
# SSH to SNS management interface
ssh admin@10.0.50.1

# System information
SYSTEM PROPERTY
# Returns: version, serial number, license status, uptime

# License status
SYSTEM LICENSE
# Expected: all features licensed (IPS, AV, URL, AppCtrl, SSL VPN)

# Hardware health
SYSTEM HEALTH
# CPU, memory, disk, temperature (for hardware appliances)

# Active processes
SYSTEM SERVICES
# List all running SNS services and their state
```

---

## 2. Interface and Network

```bash
# Interface status
MONITOR INTERFACE
# Returns: state (up/down), IP, MAC, speed, traffic counters for each interface
# Expected: out (WAN), dmz, in (LAN) — all UP

# Routing table
MONITOR ROUTES
# Expected: default 0.0.0.0/0 via WAN, DMZ and LAN routes local

# ARP table
MONITOR ARP
# List of known hosts per interface

# DNS resolution test
SYSTEM DNS RESOLVE name=www.example.com
# Expected: resolution success with IP address
```

---

## 3. Filter Policy Verification

```bash
# Display active filter policy (numbered rule list)
CONFIG FILTER POLICY SHOW name=Politique-1
# Returns all rules with idx, name, state, action, src, dst, service

# Rule hit counters
MONITOR FILTER STATS
# Per-rule: packets matched, bytes, last hit timestamp
# Expected: rules 1-10 have some hits; rules 11/12/99 may show blocked traffic

# Active connections through firewall
MONITOR CONNECTIONS
# List of established sessions: src IP/port, dst IP/port, proto, rule matched, state

# Filtered connections
MONITOR CONNECTIONS filter="src=10.0.50.100"
# All sessions from a specific host

MONITOR CONNECTIONS filter="dst=172.16.50.10"
# All sessions toward web server
```

---

## 4. NAT Verification

```bash
# NAT translation table
MONITOR NAT
# Lists active NAT sessions with original and translated addresses

# Verify SNAT active
MONITOR CONNECTIONS filter="nat=yes"
# Shows all sessions with active NAT translation

# DNAT test (from external host, telnet to WAN IP:443)
# → MONITOR CONNECTIONS should show: dst=<WAN-IP>:443 → translated to 172.16.50.10:443
```

---

## 5. IPS / ASQ Inspection

```bash
# IPS engine status
SYSTEM IPS STATUS
# Expected: engine running, signature database loaded, version current

# IPS signature database version and last update
SYSTEM UPDATE STATUS
# Check: IPS signatures, AV signatures, URL database — all up to date

# View recent IPS alerts
MONITOR ALARMS filter="type=ips" limit=20
# Returns: timestamp, src, dst, signature triggered, action (block/monitor)

# ASQ inspection statistics
MONITOR ASQ STATS
# Application detection counters by protocol/category
```

---

## 6. VPN IPSec Verification

```bash
# IKE sessions (Phase 1)
MONITOR VPN IKEV2 SA
# Expected: VPN-Site-B → state=UP, local=<SNS-IP>, remote=<SITE-B-IP>

# IPSec tunnels (Phase 2)
MONITOR VPN IPSEC SA
# Expected: VPN-Site-B-P2 → state=ESTABLISHED, traffic counters incrementing

# Re-key status
MONITOR VPN IKEV2 SA detail=yes
# Check: remaining lifetime, bytes transferred, DPD status

# DPD health check
SYSTEM VPN DPD check=VPN-Site-B
# Expected: DPD OK — peer reachable

# Ping across tunnel (from SNS internal interface)
SYSTEM PING dest=<SITE-B-HOST-IP> src=<SNS-LAN-IP>
# Expected: replies
```

---

## 7. SSL VPN Verification

```bash
# SSL VPN status
MONITOR SSLVPN SESSIONS
# List active SSL VPN user sessions: username, IP assigned, connected since

# SSL VPN user test (from external client)
# Open browser → https://<SNS-EXT-IP>/
# → Portal-Nomades login page should appear
# → Authenticate with AD credentials → should receive IP from VPN-Pool

# Check VPN pool allocation
MONITOR SSLVPN POOL
# Shows: VPN-Pool (192.168.10.0/24) — used/available IPs

# Filter rule verification
MONITOR CONNECTIONS filter="src=192.168.10.0/24"
# SSL VPN user sessions should appear with rule "SSL-VPN-to-LAN" matched
```

---

## 8. LDAP Authentication

```bash
# Test LDAP connection
AUTH LDAP TEST server=AD-Corp
# Expected: Connection to 10.0.50.20:636 → SUCCESS, LDAP bind successful

# Test user authentication
AUTH LDAP TEST server=AD-Corp user=testuser password=<TEST-PASS-HERE>
# Expected: Authentication successful, group membership returned

# Check LDAP cache
MONITOR AUTH LDAP cache
# Shows cached user entries — confirms LDAP queries are working
```

---

## 9. Log and SIEM Export

```bash
# Recent firewall logs (last 50 entries)
MONITOR LOGS filter="type=filter" limit=50
# Per-rule log entries: timestamp, rule, src, dst, action

# IPS/alarm logs
MONITOR LOGS filter="type=alarm" limit=20

# Admin audit trail
MONITOR LOGS filter="type=admin" limit=20
# Shows all admin config changes with timestamp and admin username

# Test syslog export
SYSTEM SYSLOG TEST dest=SIEM-Central
# Expected: test message sent and visible in SIEM console

# Syslog export status
CONFIG LOG SYSLOG SHOW
# Returns: SIEM-Central → status=active, last message timestamp
```

---

## 10. SNMPv3 Verification

```bash
# From NMS server — SNMP walk test
snmpwalk -v3 -u snmpv3-nms -l authPriv \
  -a SHA -A <SNMP-AUTH-PASS-HERE> \
  -x AES128 -X <SNMP-PRIV-PASS-HERE> \
  10.0.50.1 sysDescr
# Expected: Stormshield SNS product description

# SNMP trap test
SYSTEM SNMP TEST trap
# Expected: test trap sent to NMS-Server:162, visible in NMS console

# SNMP status
CONFIG SNMP AGENT SHOW
# Returns: agent enabled, community configured, location/contact set
```

---

## 11. HA Cluster Verification (if deployed)

```bash
# HA state on active node
MONITOR HA
# Expected:
#   Mode: Active/Passive
#   State: ACTIVE (local) / PASSIVE (peer)
#   Sync status: Synchronized
#   Last sync: <recent timestamp>

# Config synchronization check
SYSTEM HA SYNC CHECK
# Expected: both nodes have identical policy hash

# HA failover test (maintenance window)
# Step 1: note active node
MONITOR HA

# Step 2: force passive on current active
SYSTEM HA FAILOVER
# Step 3: verify peer is now active

# Step 4: restore (reboot or manual takeback)
# Step 5: verify sessions resumed (check MONITOR CONNECTIONS)
```

---

## 12. Connectivity Matrix Test

Run from admin workstation (10.0.50.10 = SMS-Host):

```bash
# LAN → Internet (should pass via rule 3)
curl -o /dev/null -s -w "%{http_code}" https://www.example.com
# Expected: 200

# Internet → Web Server (should pass via rule 4)
# From external test host:
curl -k https://<WAN-IP>:443
# Expected: web server response (200 or redirect)

# DMZ → LAN (should be BLOCKED by rule 11)
# From DMZ server:
curl http://10.0.50.1 --connect-timeout 3
# Expected: connection refused / timeout

# LAN → Web Server HTTPS (should pass via rule 6)
curl -k https://172.16.50.10:443
# Expected: web server response

# NMS → SNS SNMP (should pass via rule 9)
snmpwalk -v3 ... 10.0.50.1   # see section 10
# Expected: success
```

---

## 13. Security Acceptance Summary

| Check | Expected Result | Command |
|-------|----------------|---------|
| SNS version | SNS 4.x | `SYSTEM PROPERTY` |
| License | All features active | `SYSTEM LICENSE` |
| All interfaces UP | out, dmz, in: UP | `MONITOR INTERFACE` |
| Default route active | 0.0.0.0/0 via out | `MONITOR ROUTES` |
| Filter policy active | Politique-1 (12 rules) | `CONFIG FILTER POLICY SHOW` |
| NAT SNAT working | LAN sessions show NAT | `MONITOR CONNECTIONS filter="nat=yes"` |
| DNAT web server | TCP 443 → 172.16.50.10 | `MONITOR NAT` |
| IPS engine running | Active, DB current | `SYSTEM IPS STATUS` |
| VPN IPSec UP | Phase 1+2 established | `MONITOR VPN IPSEC SA` |
| SSL VPN portal | Login page accessible | browser HTTPS test |
| LDAP auth | SUCCESS | `AUTH LDAP TEST` |
| Syslog to SIEM | Last message recent | `CONFIG LOG SYSLOG SHOW` |
| SNMPv3 responding | sysDescr returned | `snmpwalk` from NMS |
| DMZ → LAN blocked | Rule 11 hit count > 0 | `MONITOR FILTER STATS` |
