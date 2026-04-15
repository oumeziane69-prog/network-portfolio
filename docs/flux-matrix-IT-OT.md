# Matrice de flux IT/OT — Modèle de Purdue 5 niveaux
# IT/OT Traffic Flow Matrix — Purdue Model (5 levels)

> **Référence :** `SEC-FLUX-ITOT-v1.0`
> **Auteur :** Hakim Oumeziane
> **Dernière mise à jour :** 2026-04-15
> **Périmètre :** Architecture industrielle générique — applicable CNPE / site de production
> **Principe directeur :** Default Deny — tout flux non listé explicitement est refusé.

---

## 1. Diagramme de segmentation par zone

```
┌─────────────────────────────────────────────────────────────────────────┐
│  NIVEAU 4 — Enterprise IT (Zone IT)                                     │
│  ERP, Active Directory, Email, DNS, WSUS, NTP                           │
│  Plage : 10.0.4.0/24                                                    │
│  Classification : Entreprise — Confidentiel                             │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │
                  ┌────────────▼────────────┐
                  │   FIREWALL IT / IDMZ     │
                  │   (FortiGate / Check Point)│
                  └────────────┬────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────────────┐
│  NIVEAU 3.5 — IDMZ (Industrial DMZ / Zone tampon)                       │
│  Historian (OSIsoft PI / Ignition), Jump Server, Patch Server,          │
│  Antivirus Update Mirror, Remote Access Gateway                         │
│  Plage : 10.0.35.0/24                                                   │
│  Classification : Sensible — flux IT/OT contrôlés                      │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │
                  ┌────────────▼────────────┐
                  │   FIREWALL OT / IDMZ     │
                  │   (FortiGate Rugged /    │
                  │    Stormshield SNS)      │
                  └────────────┬────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────────────┐
│  NIVEAU 3 — Site Operations (Zone Supervision)                           │
│  MES, SCADA Servers (Wonderware, iFIX), Historian Collector,            │
│  Engineering Workstations                                               │
│  Plage : 172.16.3.0/24                                                  │
│  Classification : Critique — OT supervisory                             │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │ (switch OT isolé — pas de routage direct)
┌──────────────────────────────▼──────────────────────────────────────────┐
│  NIVEAU 2 — Supervisory Control (Zone HMI)                              │
│  HMI (IHM), Postes opérateurs SCADA, Alarmes, Tendances                 │
│  Plage : 172.16.2.0/24                                                  │
│  Classification : Critique — accès opérateurs autorisés                 │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │ (bus terrain ou réseau propriétaire)
┌──────────────────────────────▼──────────────────────────────────────────┐
│  NIVEAU 1 — Basic Control (Zone Contrôle)                               │
│  PLCs (Siemens S7, Schneider, Allen-Bradley), DCS, RTUs                 │
│  Plage : 172.16.1.0/24                                                  │
│  Classification : Très critique — aucune connexion IT directe           │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │ (bus terrain : Profibus, Modbus RTU, HART)
┌──────────────────────────────▼──────────────────────────────────────────┐
│  NIVEAU 0 — Field Devices (Zone Terrain)                                │
│  Capteurs, actionneurs, variateurs, robots, transmetteurs               │
│  Réseau : bus terrain propriétaire (pas IP)                             │
│  Classification : Très critique — physiquement isolé                    │
└─────────────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────┐
  │  RÉSEAU DE MANAGEMENT HORS-BANDE (Out-of-Band / OOB)        │
  │  Ports console, IPMI/iDRAC, réseau dédié admin               │
  │  Plage : 192.168.0.0/24 (OOB dédié, non routé vers IT/OT)   │
  │  Accès : admin réseau uniquement, MFA obligatoire            │
  └──────────────────────────────────────────────────────────────┘
```

---

## 2. Matrice de flux principale / Main Flow Matrix

> **Convention :**
> - `Permit` = flux autorisé avec log obligatoire
> - `Deny` = flux bloqué avec log d'alerte
> - `*` = tous ports / tous protocoles
> - Les flux sont **unidirectionnels** sauf mention `↔` (bidirectionnel explicite)

### 2.1 Flux IT (N4) ↔ IDMZ (N3.5)

| # | Source | Destination | Port | Protocole | Action | Justification |
|---|--------|-------------|------|-----------|--------|---------------|
| F01 | N4 — IT Admin (`10.0.4.100/32`) | N3.5 — Jump Server (`10.0.35.20`) | 22 | SSH | **Permit** | Administration OT via bastion |
| F02 | N4 — IT Admin | N3.5 — Jump Server | 3389 | RDP | **Permit** | RDP vers Jump Server (admin OT) |
| F03 | N4 — Supervision | N3.5 — Historian | 443 | HTTPS | **Permit** | Lecture données Historian depuis IT |
| F04 | N3.5 — Historian | N4 — ERP (`10.0.4.50`) | 443 | HTTPS | **Permit** | Réplication données process → ERP |
| F05 | N4 — WSUS | N3.5 — Patch Server | 8530, 8531 | HTTPS | **Permit** | Synchronisation des mises à jour |
| F06 | N3.5 — Patch Server | N4 — WSUS | 8530, 8531 | HTTPS | **Permit** | Pull mises à jour depuis WSUS IT |
| F07 | N4 — NTP Server | N3.5 — All | 123 | UDP/NTP | **Permit** | Synchronisation horloge IDMZ |
| F08 | N3.5 — SNMP | N4 — Supervision | 162 | UDP/SNMP Trap | **Permit** | Remontée alarmes IDMZ vers NMS IT |
| F09 | N4 — NMS | N3.5 — All | 161 | UDP/SNMP | **Permit** | Polling supervision depuis IT |
| F10 | N4 — Tout | N3.5 — Tout | * | * | **Deny** | Tout autre flux IT→IDMZ interdit |

### 2.2 Flux IDMZ (N3.5) ↔ OT Supervision (N3)

| # | Source | Destination | Port | Protocole | Action | Justification |
|---|--------|-------------|------|-----------|--------|---------------|
| F11 | N3.5 — Historian Collector | N3 — SCADA Server | 4840 | TCP/OPC-UA | **Permit** | Acquisition données OPC-UA |
| F12 | N3.5 — Historian Collector | N3 — SCADA Server | 102 | TCP/S7Comm | **Permit** | Lecture données Siemens S7 (Historian) |
| F13 | N3 — SCADA Server | N3.5 — Historian | 443 | HTTPS | **Permit** | Push données process vers Historian |
| F14 | N3.5 — Jump Server | N3 — Eng. Workstation | 3389 | RDP | **Permit** | Accès ingénierie OT depuis bastion |
| F15 | N3.5 — Patch Server | N3 — Eng. Workstation | 445 | SMB | **Permit** | Déploiement patches OT |
| F16 | N3.5 — NTP Relay | N3 — All OT | 123 | UDP/NTP | **Permit** | Synchronisation horloge OT N3 |
| F17 | N3 — SNMP Agent | N3.5 — SNMP Collector | 162 | UDP/SNMP Trap | **Permit** | Alarmes OT N3 vers collecteur IDMZ |
| F18 | N3.5 — SNMP Collector | N3 — All OT | 161 | UDP/SNMP | **Permit** | Polling supervision équipements OT N3 |
| F19 | N3 — Tout | N4 — IT (N4) | * | * | **Deny** | Flux OT→IT direct interdit |
| F20 | N3.5 — Tout | N3 — Tout | * | * | **Deny** | Tout autre flux IDMZ→OT interdit |

### 2.3 Flux OT Supervision (N3) ↔ OT Control (N2/N1)

| # | Source | Destination | Port | Protocole | Action | Justification |
|---|--------|-------------|------|-----------|--------|---------------|
| F21 | N3 — SCADA Server | N2 — HMI | 4840 | TCP/OPC-UA | **Permit** | Remontée données procédé vers SCADA |
| F22 | N3 — SCADA Server | N1 — PLC | 502 | TCP/Modbus | **Permit** | Lecture registres Modbus (polling) |
| F23 | N3 — SCADA Server | N1 — PLC | 102 | TCP/S7Comm | **Permit** | Lecture/écriture PLC Siemens S7 |
| F24 | N3 — SCADA Server | N1 — RTU | 20000 | TCP/DNP3 | **Permit** | Polling DNP3 (télégestion RTU) |
| F25 | N2 — HMI | N1 — PLC | 502 | TCP/Modbus | **Permit** | Commandes opérateur HMI → PLC |
| F26 | N2 — HMI | N1 — PLC | 102 | TCP/S7Comm | **Permit** | Commandes HMI vers automates Siemens |
| F27 | N1 — PLC | N3 — SCADA | 4840 | TCP/OPC-UA | **Permit** | Push alarmes et événements critiques |
| F28 | N3 — Eng. WS | N1 — PLC | 102 | TCP/S7Comm | **Permit** | Programmation/debug PLC (fenêtres de maintenance uniquement) |
| F29 | N1 — PLC | N3 — Tout | * | * | **Deny** | Flux PLC→réseau supervision non listés : interdits |
| F30 | N3 — Tout | N0 — Field | * | * | **Deny** | Accès IP direct aux capteurs/actionneurs interdit |

### 2.4 Flux de management hors-bande (OOB)

| # | Source | Destination | Port | Protocole | Action | Justification |
|---|--------|-------------|------|-----------|--------|---------------|
| F31 | OOB Admin (`192.168.0.10`) | Firewall IT | 22, 443 | SSH / HTTPS | **Permit** | Administration firewall IT |
| F32 | OOB Admin | Firewall OT | 22, 443 | SSH / HTTPS | **Permit** | Administration firewall OT |
| F33 | OOB Admin | Switches OT | 22 | SSH | **Permit** | Administration switches OT |
| F34 | OOB Admin | PLCs (console) | Console physique | — | **Permit** | Accès console physique (câble RS-232/USB) |
| F35 | OOB Admin | IPMI / iDRAC | 443, 623 | HTTPS / IPMI | **Permit** | Administration BMC serveurs |
| F36 | OOB — Tout | IT/OT réseau prod | * | * | **Deny** | Réseau OOB isolé — aucun routage vers production |

---

## 3. Flux de protocoles OT détaillés

### 3.1 Modbus TCP (port 502)

| Paramètre | Valeur |
|-----------|--------|
| Port | 502/TCP |
| Direction | Client (SCADA/HMI) → Serveur (PLC/RTU) |
| Authentification | **Aucune** (protocole non sécurisé par nature) |
| Chiffrement | **Aucun** |
| Compensation | Isolation réseau stricte + ACL sur switch OT |
| Zones autorisées | N3 → N1, N2 → N1 uniquement |

### 3.2 DNP3 (port 20000)

| Paramètre | Valeur |
|-----------|--------|
| Port | 20000/TCP (ou UDP) |
| Direction | Master (SCADA) → Outstation (RTU/PLC) |
| Authentification | DNP3 Secure Authentication (SA) v5 si disponible |
| Chiffrement | Non natif — tunneler dans VPN si besoin |
| Compensation | Segmentation + surveillance IDS (signatures DNP3) |
| Zones autorisées | N3 → N1 uniquement |

### 3.3 OPC-UA (port 4840)

| Paramètre | Valeur |
|-----------|--------|
| Port | 4840/TCP (ou 4843 pour OPC-UA/TLS) |
| Direction | Bidirectionnel Client ↔ Server |
| Authentification | Certificats X.509 ou username/password |
| Chiffrement | TLS 1.2/1.3 avec `SecurityPolicy: Basic256Sha256` |
| Recommandation | Toujours utiliser OPC-UA avec TLS en production |
| Zones autorisées | N3.5 → N3, N3 → N2/N1 |

### 3.4 SNMP (ports 161/162)

| Paramètre | Valeur |
|-----------|--------|
| Ports | 161/UDP (polling), 162/UDP (traps) |
| Version | **SNMPv3 obligatoire** (authPriv — SHA-256 + AES-256) |
| Ne pas utiliser | SNMPv1 / SNMPv2c (communautés en clair) |
| Compensation SNMPv1/v2 | ACL source strict + VLAN management isolé |
| Community string | `<COMMUNITY-HERE>` — jamais `public` / `private` |

---

## 4. Règles globales et principes de sécurité

### 4.1 Default Deny

> **Tout flux non explicitement autorisé dans cette matrice est refusé** par la règle implicite de refus (règle ID 99) sur chaque firewall de zone.

```
Règle implicite (tous les firewalls) :
  Source : Any
  Destination : Any
  Service : Any
  Action : DENY
  Log : YES (obligatoire)
```

### 4.2 Règles bi-directionnelles

Les flux bidirectionnels (↔) doivent faire l'objet de **deux règles distinctes** sur le firewall, une pour chaque sens, avec les logs activés sur les deux. Ne jamais créer une règle `any-to-any` pour simplifier un flux bidirectionnel.

### 4.3 Règles de management hors-bande (OOB)

- Le réseau OOB ne doit **jamais** être routé vers les réseaux de production IT ou OT.
- Les accès administration (SSH, HTTPS, console) passent **exclusivement** par le réseau OOB.
- MFA (authentification multi-facteur) obligatoire sur tous les accès admin OOB.
- Les sessions d'administration doivent être journalisées (session recording sur le Jump Server).

### 4.4 Protocoles interdits

| Protocole | Raison | Alternative |
|-----------|--------|-------------|
| Telnet (23) | Credentials en clair | SSH v2 |
| FTP (21) | Données en clair | SFTP (22) ou FTPS (990) |
| SNMPv1/v2c | Community en clair | SNMPv3 authPriv |
| HTTP (80) | Trafic non chiffré | HTTPS (443) avec TLS 1.2+ |
| RDP sans MFA | Brute-force, latéralisation | RDP + NLA + MFA via Jump Server |

### 4.5 Logging et supervision

- Tous les flux `Permit` doivent générer un log horodaté avec source, destination, port, et utilisateur si disponible.
- Tous les flux `Deny` doivent générer une **alerte** remontée vers le SIEM ou le NMS.
- La rétention des logs firewall est de **minimum 90 jours** (6 mois recommandé en contexte nucléaire/IEC 62443).
- Un IDS passif (ex: Suricata ou Claroty) est recommandé sur les segments OT N2/N3 pour détecter les anomalies protocolaires Modbus/DNP3/OPC-UA.

---

## 5. Références

| Référence | Description |
|-----------|-------------|
| IEC 62443-3-3 | System Security Requirements and Security Levels |
| NIST SP 800-82 Rev.3 | Guide to OT Security |
| ANSSI — Guide de la sécurité des systèmes industriels | Recommandations ANSSI pour les SCADA/ICS |
| ISA-95 / ISA-99 | Modèle de Purdue et architecture de référence |
| [labs/ot-industrial/purdue-model-segmentation/](../labs/ot-industrial/purdue-model-segmentation/README.md) | Lab pratique associé |
| [docs/iec62443-overview.md](iec62443-overview.md) | Synthèse IEC 62443 |
| [docs/security-usecases.md](security-usecases.md) | Scénarios DMZ IT/OT détaillés |
