# Topology — Fortinet FortiGate DMZ Industrial Lab

## Schéma logique / Logical Diagram

```
  Internet (WAN)
       │ <WAN-IP>/30
       │
┌──────┴──────────────────────────────────────────────────────┐
│  FGT-EDGE (FortiGate-600E cluster — FGCP Active/Passive)    │
│  port1 : WAN  (SNAT → Internet)                            │
│  port2 : DMZ-IT  172.16.10.1/24                            │
│  port3 : LAN-IT  10.0.10.1/24                              │
│  port4 : HA-heartbeat (192.168.100.1)                      │
└──────┬────────────────────────────────────────────────────-─┘
       │ DMZ-IT — 172.16.10.0/24
       │ ┌─────────────────────────────────┐
       │ │  DMZ-IT servers                 │
       │ │  Web server    : 172.16.10.10   │
       │ │  Jump server   : 172.16.10.20   │
       │ │  Historian     : 172.16.10.30   │
       │ │  WSUS/Patch    : 172.16.10.40   │
       │ └─────────────────────────────────┘
       │
┌──────┴──────────────────────────────────────────────────────┐
│  FGT-INTERNAL (FortiGate-200F — standalone)                 │
│  port1 : DMZ-IT-ext  172.16.10.2/24   (from FGT-EDGE)      │
│  port2 : DMZ-OT      172.16.20.1/24                        │
│  port3 : LAN-OT      172.16.30.1/24                        │
└──────┬────────────────────────────────────────────────────-─┘
       │ DMZ-OT — 172.16.20.0/24
       │ ┌─────────────────────────────────┐
       │ │  DMZ-OT (IDMZ) servers          │
       │ │  OT Historian replica : 172.16.20.10 │
       │ │  Patch server (OT)   : 172.16.20.20  │
       │ │  Antivirus mirror    : 172.16.20.30  │
       │ └─────────────────────────────────┘
       │
       │ LAN-OT — 172.16.30.0/24
       │ ┌─────────────────────────────────┐
       │ │  SCADA server   : 172.16.30.10  │
       │ │  HMI workstation: 172.16.30.20  │
       │ │  Eng. workstation: 172.16.30.30 │
       └─┤  PLCs (Modbus)  : 172.16.30.100+│
         └─────────────────────────────────┘

  LAN-IT (corporate) — 10.0.10.0/24
  ┌────────────────────────────────────┐
  │  Active Directory: 10.0.10.101     │
  │  DNS/NTP server  : 10.0.10.102     │
  │  ERP servers     : 10.0.10.50-59   │
  │  Client PCs      : 10.0.10.200-254 │
  └────────────────────────────────────┘

  HA Heartbeat (FGT-EDGE-A ↔ FGT-EDGE-B)
  port4: 192.168.100.1/30 (A) ↔ 192.168.100.2/30 (B)

  Management OOB : 192.168.0.0/24 (hors schéma — réseau dédié admin)
```

---

## Plan d'adressage / Addressing Plan

### Zones et interfaces / Zones & Interfaces

| Zone | Réseau | Masque | Gateway (FGT) | Équipements |
|------|--------|--------|---------------|-------------|
| WAN | `<WAN-IP>` | `/30` | Opérateur | FGT-EDGE port1 |
| LAN-IT | `10.0.10.0` | `/24` | `10.0.10.1` | Postes IT, AD, ERP |
| DMZ-IT | `172.16.10.0` | `/24` | `172.16.10.1` | Web, Jump, Historian, WSUS |
| DMZ-OT (IDMZ) | `172.16.20.0` | `/24` | `172.16.20.1` | Historian OT, Patch OT |
| LAN-OT | `172.16.30.0` | `/24` | `172.16.30.1` | SCADA, HMI, PLCs |
| HA heartbeat | `192.168.100.0` | `/30` | — | FGT-EDGE port4/port5 |
| OOB management | `192.168.0.0` | `/24` | `192.168.0.1` | Admin FGT, SSH |

### Serveurs fixes / Fixed Servers

| Hôte | Adresse IP | Zone | Rôle |
|------|-----------|------|------|
| FGT-EDGE-A (active) | `10.0.10.1` (cluster virtual IP) | LAN-IT | NGFW périmètre (actif) |
| FGT-EDGE-B (passive) | `10.0.10.253` (MGMT dédié) | OOB | NGFW périmètre (passif) |
| FGT-INTERNAL | `172.16.10.2` | DMZ-IT | Firewall interne IT/OT |
| Web server | `172.16.10.10` | DMZ-IT | Apache/Nginx — exposition externe |
| Jump server | `172.16.10.20` | DMZ-IT | Bastion OT — RDP/SSH admin |
| IT Historian | `172.16.10.30` | DMZ-IT | OSIsoft PI — collecte données IT |
| WSUS mirror | `172.16.10.40` | DMZ-IT | Patches Microsoft |
| OT Historian réplica | `172.16.20.10` | DMZ-OT | Réplication PI vers IT |
| OT Patch server | `172.16.20.20` | DMZ-OT | Patches OT isolés |
| SCADA server | `172.16.30.10` | LAN-OT | Wonderware/iFIX supervision |
| HMI | `172.16.30.20` | LAN-OT | IHM opérateurs |
| Active Directory | `10.0.10.101` | LAN-IT | LDAP/Kerberos auth |
| NTP/DNS | `10.0.10.102` | LAN-IT | Services réseau IT |

---

## Flux de sécurité / Security Flow Summary

```
Internet → [FGT-EDGE] → DMZ-IT
           (IPS, SSL inspection, NAT)

LAN-IT   → [FGT-EDGE] → Internet
           (SNAT, URL filtering, App Control)

LAN-IT   → [FGT-EDGE] → DMZ-IT
           (accès Jump server SSH/RDP — authentifié)

DMZ-IT   → [FGT-INTERNAL] → DMZ-OT
           (OPC-UA historian polling, SSH admin via Jump)

DMZ-OT   → [FGT-INTERNAL] → LAN-OT
           (Modbus/S7 historian, Patch déploiement)

LAN-OT   → [FGT-INTERNAL] → DMZ-OT
           (push données SCADA → Historian OT)

LAN-OT   → Internet         DENY (tous les flux)
LAN-OT   → LAN-IT           DENY (tous les flux directs)
```

---

## Équipements simulés / Simulated Equipment

| Équipement | Image | vCPU | vRAM | Notes |
|------------|-------|------|------|-------|
| FGT-EDGE-A | FortiGate-VM64 KVM 7.4 | 4 | 4 GB | EVE-NG — license trial |
| FGT-EDGE-B | FortiGate-VM64 KVM 7.4 | 4 | 4 GB | Passive HA member |
| FGT-INTERNAL | FortiGate-VM64 KVM 7.4 | 2 | 2 GB | Standalone internal FW |
| Serveurs DMZ | Linux (Debian 12) | 1 | 512 MB | Simuler Historian/Web/Jump |
| Client IT | Windows 10 | 2 | 2 GB | Test policies |
