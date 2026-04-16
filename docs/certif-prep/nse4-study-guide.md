# NSE 4 — FortiGate Security Study Guide

> Fortinet Network Security Expert Level 4  
> Exam: FortiGate Security + FortiGate Infrastructure  
> Version: FortiOS 7.x

---

## Table of Contents

1. [Exam Overview](#1-exam-overview)
2. [Firewall Policies & NAT](#2-firewall-policies--nat)
3. [User Authentication](#3-user-authentication)
4. [SSL Inspection](#4-ssl-inspection)
5. [Intrusion Prevention (IPS)](#5-intrusion-prevention-ips)
6. [Application Control & Web Filtering](#6-application-control--web-filtering)
7. [Antivirus & Security Profiles](#7-antivirus--security-profiles)
8. [VPN — IPsec & SSL](#8-vpn--ipsec--ssl)
9. [Routing & SD-WAN](#9-routing--sd-wan)
10. [High Availability (HA)](#10-high-availability-ha)
11. [Logging & Monitoring](#11-logging--monitoring)
12. [FortiGate Administration](#12-fortigate-administration)

---

## 1. Exam Overview

| Item | Details |
|---|---|
| Exams | FortiGate Security (FCP_FGT_AD-7.4) + FortiGate Infrastructure (FCP_FGT_AD-7.4) |
| Format | Multiple choice, drag-and-drop |
| Duration | 60 min per exam |
| Passing score | ~70% |
| Prerequisite | NSE 1, NSE 2, NSE 3 recommended |

### Recommended Study Path

1. Fortinet Training Institute — free online courses (training.fortinet.com)
2. FortiGate Security (v7.4) — official course
3. FortiGate Infrastructure (v7.4) — official course
4. NSE 4 practice exams
5. Lab on FortiGate VM (free 15-day trial license)

---

## 2. Firewall Policies & NAT

### Firewall Policy Basics

- Policies are processed **top-down**, first match wins.
- Every policy requires: **srcintf**, **dstintf**, **srcaddr**, **dstaddr**, **service**, **action**.
- `action` can be: `accept`, `deny`, `ipsec`.
- Implicit deny-all at the bottom (invisible, not shown in GUI).

### Policy Lookup Order

```
Incoming interface → Source address → Destination address → Service → Action
```

### NAT Types

| Type | Use case | Config location |
|---|---|---|
| SNAT (IP Pool) | Outbound internet, hide internal IPs | Policy → NAT → IP Pool |
| DNAT (VIP) | Publish internal server externally | Objects → Virtual IPs |
| Central NAT | Centralized NAT table | Policy & Objects → Central SNAT |

### Virtual IPs (VIP)

- Map external IP/port to internal IP/port.
- Types: static NAT, port forwarding, load balance.
- VIPs must be referenced in firewall policy destination.

### Key CLI Commands

```bash
# List all policies
show firewall policy

# Check policy hit count
get firewall policy

# Test policy lookup
diag firewall iprope lookup <src-ip> <dst-ip> <port> <proto> <src-intf>
```

---

## 3. User Authentication

### Authentication Methods

| Method | Description |
|---|---|
| Local password | FortiGate local user database |
| LDAP | Active Directory, OpenLDAP |
| RADIUS | External RADIUS server |
| TACACS+ | Cisco-compatible AAA |
| SAML | SSO via IdP (FortiAuthenticator, Azure AD) |
| PKI/Certificate | Client certificate authentication |

### Captive Portal

- Triggers authentication for firewall policy.
- Modes: **redirect-http**, **disable** (transparent).
- Applied per policy or per interface.

### Two-Factor Authentication (2FA)

- FortiToken (hardware or mobile) — TOTP-based.
- Email-based OTP.
- Enforced per user or user group.

### Firewall Authentication Timeout

```bash
# Default auth timeout: 5 min (idle), 480 min (hard)
config user setting
    set auth-timeout 480
    set auth-timeout-type idle-timeout
end
```

---

## 4. SSL Inspection

### Inspection Modes

| Mode | Visibility | Performance impact |
|---|---|---|
| Certificate Inspection | SNI only, no decryption | Low |
| Full SSL Inspection (Deep) | Full decrypt/re-encrypt | Higher |

### Full Inspection Requirements

- FortiGate acts as MITM — re-signs certificates with its own CA.
- CA certificate must be **trusted by clients** (pushed via GPO or MDM).
- Exemptions: banking, government, medical sites (prebuilt exemption list).

### SSL/SSH Profile Components

- SSL protocol versions (TLS 1.0–1.3)
- Blocked / allowed cipher suites
- Handling of invalid certificates (block, allow, ignore)
- HTTPS, SMTPS, IMAPS, POP3S, FTPS support

### Common Issues

| Problem | Cause | Fix |
|---|---|---|
| Browser cert warning | CA not trusted | Deploy FortiGate CA to clients |
| Broken apps | Certificate pinning | Add exemption |
| Performance degradation | Too many connections decrypted | Use certificate inspection for low-risk |

---

## 5. Intrusion Prevention (IPS)

### IPS Architecture

- Signatures database updated via FortiGuard.
- Applied as **security profile** in firewall policy.
- Operates in: **detection** mode or **prevention** (inline block) mode.

### IPS Sensor Configuration

```
IPS Sensor → Signature Filters → Action (pass / block / reset / monitor)
```

- Filters by: severity (critical/high/medium/low/info), target, protocol, OS.
- Custom signatures supported.
- Rate-based signatures for DoS.

### Protocol Decoders

- FortiGate decodes application-layer protocols before inspecting.
- Anomaly detection: validates protocol compliance.

### Key CLI

```bash
# Check IPS engine status
diag ips anomaly status
diag ips signature list

# IPS engine statistics
diag ips session list
```

---

## 6. Application Control & Web Filtering

### Application Control

- Uses **Application Control** security profile.
- Application signatures from FortiGuard AppDB (10,000+).
- Actions per application/category: allow, monitor, block, quarantine, reset.
- **Application override**: override category action for specific apps.

### QUIC / HTTP/3

- FortiGate can block QUIC to force fallback to TCP (easier inspection).

### Web Filtering

| Mode | Description |
|---|---|
| FortiGuard Category | Cloud-based URL categorization |
| Static URL Filter | Manual allow/block list |
| DNS-based filter | Block at DNS resolution level |
| Safe Search | Enforce safe search on Google, Bing |

### Web Filter Actions

- Allow, Monitor, Block, Warning (user can override), Authenticate (require auth).

### Web Filter Profile Flow

```
DNS lookup → FortiGuard category check → Static URL filter → Content filter → Action
```

---

## 7. Antivirus & Security Profiles

### Antivirus Scanning Modes

| Mode | Description |
|---|---|
| Flow-based | Scan while data streams, lower latency |
| Proxy-based | Buffer full file, higher detection rate |

### Supported Protocols

- HTTP, HTTPS (with SSL inspection), FTP, SMTP, IMAP, POP3, SMB, CIFS.

### FortiSandbox Integration

- Unknown files submitted to FortiSandbox (cloud or on-prem) for analysis.
- File quarantine based on sandbox verdict.

### Security Profile Application

All security profiles (AV, IPS, AppCtrl, WebFilter, etc.) are applied **per firewall policy**.

---

## 8. VPN — IPsec & SSL

### IPsec VPN

#### Phase 1 (IKE — Key Exchange)

| Parameter | Common values |
|---|---|
| IKE version | IKEv1, IKEv2 |
| Authentication | Pre-shared key (PSK), certificates |
| Encryption | AES-128, AES-256 |
| DH Group | 14 (2048-bit), 19 (ECDH 256-bit) |
| Hash | SHA-256, SHA-384 |

#### Phase 2 (IPsec — Data Protection)

| Parameter | Common values |
|---|---|
| Protocol | ESP (Encapsulating Security Payload) |
| Encryption | AES-256-GCM |
| PFS | Enable (recommended) |
| Auto-negotiate | Enable |

#### Site-to-Site Topology

```
[HQ FortiGate] ←── IPsec tunnel ───→ [Branch FortiGate]
     wan1:x.x.x.x                          wan1:y.y.y.y
```

#### Dial-Up (Remote Access) IPsec

- Hub acts as IPsec server (accepts any peer IP).
- Spokes authenticate with PSK or certificate.
- XAUTH for additional user authentication.
- Mode Config: assign IP/DNS to spoke dynamically.

### SSL-VPN

| Mode | Description |
|---|---|
| Web mode | Clientless, browser-only access |
| Tunnel mode | Full network access via FortiClient |

#### SSL-VPN Key Settings

- Listen port: default 443 (or 10443 to avoid conflict with HTTPS admin).
- Realm: virtual SSL-VPN portal per user group.
- Split tunnel: route only VPN traffic through tunnel (or route all).
- Idle timeout / auth timeout.

```bash
# SSL-VPN session list
diag vpn ssl list
diag vpn ssl statistics
```

---

## 9. Routing & SD-WAN

### Routing Table Priority

```
Connected > Static (distance 10) > OSPF (110) > BGP (200) > RIP (120)
```

### Policy-Based Routing (PBR)

- Override routing table based on src/dst/service.
- Applied before routing table lookup.

### SD-WAN

- Combine multiple WAN links into a virtual interface.
- **Performance SLA**: health checks (ping, HTTP, DNS) per member.
- **Rules**: steer traffic based on application, src/dst, TOS.
- Load balancing algorithms: source-IP, sessions, spillover, volume.

#### SD-WAN Configuration Flow

```
1. Create SD-WAN zone
2. Add WAN interfaces as SD-WAN members
3. Configure Performance SLAs (health checks)
4. Create SD-WAN rules (traffic steering)
5. Configure firewall policies on SD-WAN zone
```

---

## 10. High Availability (HA)

### HA Modes

| Mode | Description |
|---|---|
| Active-Passive | One unit active, one standby. Failover on failure. |
| Active-Active | Load balance sessions across both units. |

### HA Key Concepts

- **FGCP** (FortiGate Clustering Protocol) — proprietary.
- Heartbeat interfaces: dedicated HA sync links.
- Session sync: active sessions synced to standby.
- **Priority**: higher value = primary (default 128, range 0–255).
- **Override**: if enabled, highest-priority unit always becomes primary.

### Failover Triggers

- Link failure (monitored interfaces)
- FortiGuard daemon failure
- Memory/CPU threshold exceeded
- Unit power loss

### HA CLI

```bash
# HA status
get system ha status
diag sys ha status

# Force failover
diag sys ha reset-uptime
```

---

## 11. Logging & Monitoring

### Log Types

| Log | Content |
|---|---|
| Traffic | All sessions (forward, local, sniffer) |
| Event | Admin actions, VPN, HA, system events |
| Security | IPS, AV, AppCtrl, WebFilter, DLP hits |
| UTM | Unified view of security logs |

### Log Destinations

- **Local disk** (if available)
- **FortiAnalyzer** (recommended for enterprise)
- **FortiCloud** (cloud-based)
- **Syslog** (external SIEM)

### Log Severity Levels

```
Emergency > Alert > Critical > Error > Warning > Notification > Information > Debug
```

### Useful CLI

```bash
# Real-time log streaming
diag log test
execute log filter category traffic
execute log display

# Top talkers / sessions
diag sys session list
diag sys session filter dport 443
```

---

## 12. FortiGate Administration

### Management Interfaces

- **GUI**: HTTPS (port 443 or custom)
- **CLI**: SSH (port 22), console cable
- **FortiManager**: centralized management
- **REST API**: `https://<ip>/api/v2/`

### Firmware Management

```bash
# Current version
get system status

# Upgrade via CLI
execute restore image tftp <filename> <tftp-server-ip>
```

### Backup & Restore

- Configuration backup: plaintext or encrypted.
- Encrypted backup requires password for restore.

### RBAC — Admin Profiles

- `super_admin`: full access.
- `prof_admin`: create custom profiles with limited permissions.
- Per-VDOM administrators: restrict admin to specific VDOM.

### FortiGuard Services

| Service | Purpose |
|---|---|
| AV/IPS updates | Signature database updates |
| Web Filtering | URL categorization |
| Application Control | App signature database |
| Anti-Spam | Email threat intelligence |
| Sandbox | File analysis |

---

## Study Resources

| Resource | URL |
|---|---|
| Fortinet Training Institute | training.fortinet.com |
| FortiGate 7.4 Admin Guide | docs.fortinet.com |
| NSE 4 Exam Blueprint | certification.fortinet.com |
| FortiGate VM Trial | support.fortinet.com (free 15-day) |

---

*Last updated: 2026-04-16 — FortiOS 7.4*
