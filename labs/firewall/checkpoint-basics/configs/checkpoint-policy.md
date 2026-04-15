# Check Point Policy — Rulebase complète R81.x
# Check Point Security Policy — Full Rulebase R81.x

> **Platform :** Check Point R81.x (SmartConsole)
> **Topology :** ClusterXL A/A — 3 zones : External / DMZ / Internal
> **Note :** Check Point n'a pas de CLI flat pour les policies — elles sont gérées via SmartConsole (GUI) ou l'API REST Check Point. Ce document présente la rulebase en format tabulaire lisible.

---

## 1. Network Objects / Objets réseau

| Nom | Type | Valeur | Zone | Commentaire |
|-----|------|--------|------|-------------|
| `Cluster-VIP-External` | Host | `<CLUSTER-EXT-IP>` | External | Virtual IP cluster externe |
| `GW-A-External` | Host | `<GW-A-EXT-IP>` | External | Interface externe GW-A |
| `GW-B-External` | Host | `<GW-B-EXT-IP>` | External | Interface externe GW-B |
| `Cluster-VIP-DMZ` | Host | `172.16.50.1` | DMZ | Virtual IP cluster DMZ |
| `Cluster-VIP-Internal` | Host | `10.0.50.1` | Internal | Virtual IP cluster interne |
| `SMS-Server` | Host | `10.0.50.10` | Internal | Security Management Server |
| `AD-Server` | Host | `10.0.50.20` | Internal | Active Directory / LDAP |
| `Web-Server-DMZ` | Host | `172.16.50.10` | DMZ | Nginx HTTPS |
| `SMTP-Relay-DMZ` | Host | `172.16.50.20` | DMZ | Postfix relay |
| `Net-Internal` | Network | `10.0.50.0/24` | Internal | Réseau interne |
| `Net-DMZ` | Network | `172.16.50.0/24` | DMZ | Réseau DMZ |
| `Internet` | Domain | `0.0.0.0/0` excl. RFC1918 | External | Trafic Internet |

---

## 2. Security Rulebase (Firewall Policy)

> **Convention :** Track = `Log` (log sans alerte) / `Alert` (log + alerte SIEM) / `None`

| # | Nom règle | Source | Destination | Service | Action | Track | Commentaire |
|---|-----------|--------|-------------|---------|--------|-------|-------------|
| 1 | Allow-GW-HealthCheck | `Cluster-VIP-Internal` | `AD-Server` | LDAP, LDAPS | **Accept** | Log | GW → AD : identity check |
| 2 | Allow-SmartConsole-to-SMS | `Net-Internal` | `SMS-Server` | TCP 18190, TCP 443 | **Accept** | Log | Admin → SMS : SmartConsole |
| 3 | Allow-SMS-to-GW-SIC | `SMS-Server` | `Any` | TCP 18211 | **Accept** | Log | SMS → GW : SIC policy install |
| 4 | Allow-GW-Logs-to-SMS | `Any` | `SMS-Server` | TCP 18184, UDP 514 | **Accept** | Log | GW → SMS : logs |
| 5 | Allow-Internal-to-Internet | `Net-Internal` | `Internet` | HTTP, HTTPS, DNS | **Accept** | Log | NAT SNAT implicite |
| 6 | Allow-Internal-to-DMZ-HTTPS | `Net-Internal` | `Net-DMZ` | HTTPS | **Accept** | Log | Intranet → DMZ apps |
| 7 | Allow-Internet-to-WebServer | `Internet` | `Web-Server-DMZ` | HTTPS (443) | **Accept** | Alert | Exposition web — IPS actif |
| 8 | Allow-Internet-to-SMTP | `Internet` | `SMTP-Relay-DMZ` | SMTP (25), SMTPS (465) | **Accept** | Log | Mail entrant |
| 9 | Allow-Internal-SSH-to-DMZ | `10.0.50.10/32` | `Net-DMZ` | SSH (22) | **Accept** | Alert | Admin → DMZ : SSH limité à SMS |
| 10 | Allow-DMZ-to-Internal-app | `Web-Server-DMZ` | `AD-Server` | LDAP (389), LDAPS (636) | **Accept** | Log | Web server → AD : auth LDAP |
| 11 | Allow-ICMP-Monitoring | `SMS-Server` | `Any` | ICMP echo | **Accept** | None | Monitoring ping depuis SMS |
| 12 | Allow-SNMP | `10.0.50.50/32` | `Any` | SNMP, SNMP-Trap | **Accept** | Log | NMS → FW : supervision |
| 13 | Deny-DMZ-to-Internal | `Net-DMZ` | `Net-Internal` | Any | **Drop** | Alert | DMZ ne doit pas initier vers Internal |
| 14 | Deny-Internet-to-Internal | `Internet` | `Net-Internal` | Any | **Drop** | Alert | Protection réseau interne |
| 15 | **CLEANUP — Implicit Deny** | `Any` | `Any` | Any | **Drop** | Alert | Règle implicite finale — tout le reste est bloqué et alerté |

---

## 3. NAT Rules

| # | Nom | Original Source | Original Destination | Service | Translated Source | Translated Dest | Type |
|---|-----|----------------|---------------------|---------|-----------------|-----------------|------|
| N1 | SNAT-Internal-to-Internet | `Net-Internal` | `Internet` | HTTP, HTTPS | `Cluster-VIP-External` (Hide NAT) | Original | SNAT (PAT) |
| N2 | DNAT-WebServer-HTTPS | `Internet` | `Cluster-VIP-External` | HTTPS 443 | Original | `Web-Server-DMZ` :443 | DNAT |
| N3 | DNAT-SMTP-Relay | `Internet` | `Cluster-VIP-External` | SMTP 25 | Original | `SMTP-Relay-DMZ` :25 | DNAT |
| N4 | SNAT-DMZ-to-Internet | `Net-DMZ` | `Internet` | HTTP, HTTPS | `Cluster-VIP-External` | Original | SNAT (PAT) |

---

## 4. IPS Profile (Threat Prevention Policy)

> Dans R81.x, la Threat Prevention est une policy séparée de la Security Policy.

| Paramètre | Valeur |
|-----------|--------|
| Profile name | `TP-Profile-DMZ-Inbound` |
| Anti-Bot | Enabled — Critical, High |
| Antivirus | Enabled — HTTP, HTTPS, SMTP |
| IPS | Enabled — Prevent critical/high, Detect medium |
| Threat Emulation | Enabled (SandBlast) pour fichiers entrants |
| URL Filtering | Enabled — Block: Malware, Phishing, P2P |
| Zero Phishing | Enabled |

**Application sur les règles :**
- Règle 7 (Internet → WebServer) : `TP-Profile-DMZ-Inbound` actif
- Règle 5 (Internal → Internet) : `TP-Profile-Outbound` avec inspection SSL

---

## 5. Identity Awareness (AD Integration)

> Identity Awareness permet d'associer les connexions réseau à des utilisateurs AD.

```
SmartConsole → Gateways & Servers → GW-A → Edit
  → Identity Awareness tab → Enable
  → Active Directory: AD-Server (10.0.50.20)
  → Domain: lab.local
  → Captive Portal: Enabled on Internal interface
  → Kerberos SSO: Enabled

Policy adjustment (règle 5):
  Source: Net-Internal → Users: "Domain Users" group
  → Applies only to authenticated AD users
```

**Groupes AD utilisés dans les policies :**

| Groupe AD | Accès autorisé | Remarque |
|-----------|---------------|----------|
| `Domain Users` | Internet HTTP/HTTPS | Accès standard |
| `Admins-Reseau` | Internet + SSH → DMZ | Profil admin |
| `Service Accounts` | LDAP, HTTPS | Comptes applicatifs |
| `Contractors` | Internet HTTP uniquement | Sans accès DMZ |

---

## 6. HTTPS Inspection

```
SmartConsole → Security Policies → HTTPS Inspection → New Rule
  Name       : Inspect-Outbound-HTTPS
  Source     : Net-Internal
  Destination: Internet
  Services   : HTTPS
  Action     : Inspect
  Certificate: Check Point Internal CA (auto-signed, deployed via GPO AD)
  
  Bypass rules (exceptions — no inspection):
  - Destination: financial sites (category Banking)
  - Destination: healthcare (category Health & Medicine)
  - Source: Service accounts
```

---

## 7. ClusterXL Configuration

```
SmartConsole → Gateways & Servers → New Cluster
  Cluster Name    : FW-CLUSTER
  Cluster Type    : ClusterXL
  Mode            : Active/Active (High Availability)
  
  Members:
    GW-A: <GW-A-EXT-IP>, 172.16.50.2, 10.0.50.2
    GW-B: <GW-B-EXT-IP>, 172.16.50.3, 10.0.50.3
  
  Cluster Virtual IPs:
    External : <CLUSTER-EXT-IP>
    DMZ      : 172.16.50.1
    Internal : 10.0.50.1
  
  Sync Network : 192.168.200.0/30
    GW-A sync : 192.168.200.1
    GW-B sync : 192.168.200.2
```
