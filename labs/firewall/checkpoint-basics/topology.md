# Topology — Check Point R81.x Lab

## Schéma logique / Logical Diagram

```
  Internet (WAN)
       │ <EXT-IP>/30
       │
┌──────┴───────────────────────────────────────────────────────┐
│  ClusterXL Active/Active (GW-A + GW-B)                      │
│  ┌──────────────────┐     ┌──────────────────┐              │
│  │ GW-A (active)    │     │ GW-B (standby)   │              │
│  │ ext: <GW-A-ext>  │     │ ext: <GW-B-ext>  │              │
│  │ dmz: 172.16.50.2 │     │ dmz: 172.16.50.3 │              │
│  │ int: 10.0.50.2   │     │ int: 10.0.50.3   │              │
│  └──────────────────┘     └──────────────────┘              │
│  Cluster Virtual IPs:                                        │
│    External : <CLUSTER-EXT-IP>/30                           │
│    DMZ      : 172.16.50.1/24                                │
│    Internal : 10.0.50.1/24                                  │
│  Sync network : 192.168.200.0/30                            │
└──────┬─────────────────────┬───────────────────────────────-┘
       │ DMZ — 172.16.50.0/24│ Internal — 10.0.50.0/24
       │                     │
  ┌────┴──────────┐    ┌─────┴──────────────────────────┐
  │  DMZ servers  │    │  Internal network               │
  │  Web  :50.10  │    │  SMS (SmartConsole): 10.0.50.10 │
  │  SMTP :50.20  │    │  AD/LDAP           : 10.0.50.20 │
  │  SSH  :50.30  │    │  Client PCs        : 10.0.50.100+│
  └───────────────┘    └────────────────────────────────-┘

  SMS (Security Management Server) — 10.0.50.10
  ┌──────────────────────────────────────────────┐
  │  Check Point R81.x SMS                       │
  │  SmartConsole connection: TCP 18190, 443      │
  │  SIC (Secure Internal Comm): TCP 18211        │
  │  Log reception from GW: UDP 514 + TCP 18184   │
  └──────────────────────────────────────────────┘
```

---

## Plan d'adressage / Addressing Plan

| Zone | Réseau | Masque | Cluster VIP | Rôle |
|------|--------|--------|-------------|------|
| External | `<EXT-NET>` | `/30` | `<CLUSTER-EXT-IP>` | Interface WAN |
| DMZ | `172.16.50.0` | `/24` | `172.16.50.1` | Serveurs exposés |
| Internal | `10.0.50.0` | `/24` | `10.0.50.1` | Réseau interne |
| HA Sync | `192.168.200.0` | `/30` | — | Synchronisation cluster |

### Hôtes fixes / Fixed Hosts

| Hôte | IP | Zone | Rôle |
|------|----|------|------|
| SMS (Security Management) | `10.0.50.10` | Internal | Gestion centralisée |
| GW-A (membre cluster actif) | `10.0.50.2` | Internal | Check Point NGFW |
| GW-B (membre cluster passif) | `10.0.50.3` | Internal | Check Point NGFW |
| Active Directory | `10.0.50.20` | Internal | LDAP/Kerberos — Identity Awareness |
| Web server | `172.16.50.10` | DMZ | Nginx — HTTPS port 443 |
| SMTP relay | `172.16.50.20` | DMZ | Postfix relay |

---

## Architecture Check Point R81.x

| Composant | Rôle | Localisation |
|-----------|------|-------------|
| **SMS** (Security Management Server) | Base de données des policies, objet réseau, logs. SmartConsole se connecte ici. | VM dédiée 10.0.50.10 |
| **Security Gateway** (GW) | Applique les rules de sécurité en temps réel. Reçoit les policies depuis SMS via SIC. | Cluster GW-A + GW-B |
| **SmartConsole** | Interface graphique admin (Windows). Connexion sur SMS (TCP 18190). | Poste admin |
| **ClusterXL** | Protocole de clustering Check Point — Active/Active ou Active/Standby. | GW-A + GW-B |
| **SIC** (Secure Internal Communication) | Canal chiffré entre SMS et GW. Initialisé avec OTP `<SIC-OTP-HERE>`. | Automatique |

---

## Protocoles de gestion / Management Protocols

| Protocole | Port | Direction | Usage |
|-----------|------|-----------|-------|
| SmartConsole → SMS | TCP 18190, 443 | Admin → SMS | GUI management |
| SMS → GW (SIC) | TCP 18211 | SMS → GW | Policy install, config push |
| GW → SMS (logs) | TCP 18184, UDP 514 | GW → SMS | Log forwarding |
| SSH admin | TCP 22 | Admin → GW/SMS | Clish / expert mode |
| SNMP | UDP 161 | NMS → GW | Monitoring |
