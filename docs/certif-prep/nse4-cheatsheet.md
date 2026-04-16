# NSE 4 — FortiGate Quick Reference Cheatsheet

> FortiOS 7.x — FortiGate Security & Infrastructure

---

## Firewall Policies

| Command | Purpose |
|---|---|
| `show firewall policy` | List all policies |
| `diag firewall iprope lookup <src> <dst> <port> <proto> <intf>` | Policy lookup test |
| `diag firewall iprope show 100004` | Show policy table |
| `get firewall policy` | Policy stats (hit count) |

**Policy matching order:** srcintf → srcaddr → dstaddr → service → schedule → action

**Implicit rule:** deny-all (not visible, always last)

---

## NAT

| Type | Object | Use |
|---|---|---|
| SNAT | IP Pool | Outbound / hide internal |
| DNAT | Virtual IP (VIP) | Publish server |
| Central SNAT | Central SNAT table | Centralized outbound NAT |

```bash
# Check NAT translations
diag firewall ippool list
diag ip router ospf show      # not NAT but routing check
```

---

## IPsec VPN

### Phase 1 — IKE

```
Encryption : AES-256
Hash       : SHA-256
DH Group   : 14 (2048-bit) or 19 (ECDH)
Auth       : PSK or Certificate
IKE        : v2 preferred
```

### Phase 2 — IPsec

```
Protocol   : ESP
Encryption : AES-256-GCM
PFS        : Enable
```

### Useful CLI

```bash
diag vpn ike gateway list          # IKE Phase 1 SAs
diag vpn tunnel list               # Phase 2 tunnels
diag debug app ike -1              # IKE debug (verbose)
diag vpn ike restart               # Restart IKE daemon
execute vpn ipsec tunnel down <name>
execute vpn ipsec tunnel up <name>
```

---

## SSL-VPN

```bash
diag vpn ssl list                  # Active SSL-VPN sessions
diag vpn ssl statistics            # Global SSL-VPN stats
diag debug app sslvpn -1           # SSL-VPN debug
```

| Setting | Default |
|---|---|
| Listen port | 443 |
| Idle timeout | 300 s |
| Auth timeout | 28800 s (8 h) |
| Tunnel mode | requires FortiClient |
| Web mode | clientless (browser) |

---

## Routing

### Administrative Distances

| Protocol | AD |
|---|---|
| Connected | 0 |
| Static | 10 |
| OSPF (internal) | 110 |
| RIP | 120 |
| BGP | 200 |

```bash
get router info routing-table all          # Full routing table
get router info routing-table database     # RIB
diag ip router ospf show                   # OSPF neighbor/state
diag ip router bgp show                    # BGP summary
```

---

## SD-WAN

```bash
diag sys virtual-wan-link status           # SD-WAN member status
diag sys virtual-wan-link sla-log <name>   # SLA health log
diag sys virtual-wan-link intf-sla-log     # Per-interface SLA
get system virtual-wan-link                # SD-WAN config
```

**Load balancing algorithms:** `source-ip-based` | `sessions` | `spillover` | `volume`

---

## SSL Inspection

| Mode | Decryption | Use case |
|---|---|---|
| Certificate Inspection | No (SNI only) | Low-risk traffic |
| Full SSL Inspection | Yes (MITM) | Security scanning |

**Full inspection requires:** FortiGate CA trusted by all clients.

**Bypass exemptions for:** certificate pinning, banking, medical.

---

## Security Profiles Summary

| Profile | Function | Applied in |
|---|---|---|
| Antivirus | Malware scan (flow/proxy) | Firewall policy |
| IPS | Exploit/anomaly detection | Firewall policy |
| Application Control | App identification & control | Firewall policy |
| Web Filter | URL/category filtering | Firewall policy |
| DNS Filter | Block domains at DNS level | Firewall policy |
| SSL Inspection | TLS decrypt | Firewall policy |
| Email Filter | Anti-spam | Firewall policy |

---

## IPS

```bash
diag ips signature list | grep <keyword>   # Find signature
diag ips anomaly status                    # Anomaly counters
diag ips session list                      # Active IPS sessions
```

**Actions:** `pass` | `monitor` | `block` | `reset` | `quarantine`

---

## High Availability

| Mode | Description |
|---|---|
| Active-Passive | Failover only |
| Active-Active | Load balanced |

```bash
get system ha status                        # HA cluster status
diag sys ha status                          # Detailed HA info
diag sys ha reset-uptime                    # Force failover (secondary becomes primary)
```

**Priority:** higher = primary (default 128). Range: 0–255.

**Monitored links:** failure triggers failover.

---

## Authentication

```bash
diag firewall auth list                     # Active auth sessions
diag test auth <server-name>               # Test LDAP/RADIUS
diagnose debug app fnbamd -1               # Auth daemon debug
```

| Method | Object |
|---|---|
| Local | `config user local` |
| LDAP | `config user ldap` |
| RADIUS | `config user radius` |
| SAML | `config user saml` |
| FortiToken | `config user fortitoken` |

---

## Logging

```bash
execute log filter category 0              # Traffic logs
execute log filter category 1             # Event logs
execute log display                        # Show filtered logs

diag log test                              # Generate test log entries
```

**Log destinations:** disk | FortiAnalyzer | FortiCloud | Syslog

---

## Sessions & Traffic Debug

```bash
diag sys session list                      # All sessions
diag sys session filter src <ip>           # Filter by source
diag sys session filter dst <ip>           # Filter by destination
diag sys session filter dport <port>       # Filter by destination port
diag sys session clear                     # Clear all sessions (!)

# Packet sniffer
diag sniffer packet <intf> '<filter>' <level> <count> l
# Example: diag sniffer packet port1 'host 10.0.0.1' 4 100 l

# Debug flow (policy decision trace)
diag debug flow filter addr <ip>
diag debug flow show console enable
diag debug enable
diag debug flow trace start 100
```

---

## System

```bash
get system status                          # FortiOS version, serial, hostname
get system performance status             # CPU, memory, sessions
get system interface                       # Interface status
diagnose hardware deviceinfo disk          # Disk info
execute factoryreset                       # Factory reset (!)
```

---

## FortiGuard

```bash
diag debug update background              # Update status
execute update-now                         # Force FortiGuard update
get system fortiguard-service             # FortiGuard config
diag autoupdate status                     # IPS/AV DB version
```

---

## Common Troubleshooting Flow

```
1. Policy lookup:  diag firewall iprope lookup ...
2. Routing:        get router info routing-table all
3. Session:        diag sys session list (filter by IP/port)
4. Sniffer:        diag sniffer packet <intf> 'host <ip>' 4 20 l
5. Debug flow:     diag debug flow filter / trace start
6. Security log:   execute log filter / log display
```

---

## Key Port Numbers

| Service | Port |
|---|---|
| HTTPS Admin | 443 (or custom) |
| SSH Admin | 22 |
| SSL-VPN (default) | 443 or 10443 |
| IKE (IPsec) | UDP 500 |
| NAT-T (IPsec) | UDP 4500 |
| ESP | IP protocol 50 |
| RADIUS | UDP 1812/1813 |
| LDAP | TCP 389 |
| LDAPS | TCP 636 |
| Syslog | UDP 514 |
| FortiAnalyzer | TCP 514 or 8514 |

---

*NSE 4 — FortiOS 7.4 — Last updated: 2026-04-16*
