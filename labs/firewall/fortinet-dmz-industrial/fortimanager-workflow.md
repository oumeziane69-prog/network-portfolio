# FortiManager Workflow — Gestion centralisée FortiGate
# FortiManager Central Management Workflow

> **Version :** FortiManager 7.4.x
> **Contexte :** Gestion centralisée de FGT-EDGE et FGT-INTERNAL depuis FortiManager

---

## 1. Architecture FortiManager

```
┌─────────────────────────────────────────────────────────┐
│  FortiManager (FortiOS-based appliance / VM)            │
│  IP: 10.0.10.60 (LAN-IT)                               │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  ADOM: DMZ   │  │  ADOM: OT    │  │  ADOM: ROOT  │  │
│  │  FGT-EDGE    │  │  FGT-INTERNAL│  │  (global)    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
         │ FGFM (FortiGate to FortiManager protocol)
         │ TCP 541 (bidirectionnel)
    ┌────┴────┐         ┌──────────────┐
    │FGT-EDGE │         │FGT-INTERNAL  │
    └─────────┘         └──────────────┘
```

**Prérequis :**
- FortiManager accessible depuis les deux FGTs (TCP 541)
- Certificats SIC générés sur chaque FGT
- Compte admin FortiManager avec profil Super_User

---

## 2. Création d'un ADOM / Create ADOM

Les **ADOM (Administrative Domains)** permettent de segmenter la gestion par zone ou par équipe.

### 2.1 Via GUI

```
FortiManager GUI → System Settings → All ADOMs → Create New
  Name        : DMZ-PERIMETER
  Description : Gestion FGT-EDGE et firewall périmètre
  Type        : FortiGate
  OS Version  : FortiOS 7.4
  Central Mgmt: Enabled
  → OK
```

### 2.2 Via CLI FortiManager

```bash
config system adom
    edit "DMZ-PERIMETER"
        set desc "Gestion FGT-EDGE — zone DMZ industrielle"
        set restricted_prds fgt
        set status enable
    next
    edit "OT-INTERNAL"
        set desc "Gestion FGT-INTERNAL — zone OT/IDMZ"
        set restricted_prds fgt
        set status enable
    next
end
```

---

## 3. Import d'un équipement / Device Import

### 3.1 Ajouter FGT-EDGE à FortiManager

**Côté FGT (à exécuter sur FGT-EDGE) :**

```bash
# Sur FGT-EDGE — enregistrer FortiManager comme gestionnaire central
config system central-management
    set type fortimanager
    set fmg "10.0.10.60"            # IP FortiManager
    set fmg-source-ip 10.0.10.1     # Source IP FGT (LAN-IT)
end

# Générer la demande d'enregistrement
execute central-mgmt register-device 10.0.10.60 <ADMIN-PASSWORD-HERE>
```

**Côté FortiManager — accepter la demande :**

```
GUI → Device Manager → ADOM: DMZ-PERIMETER → Add Device → Discover
  IP Address: 10.0.10.1 (LAN-IT interface FGT-EDGE)
  → Authorize device
  → Import configuration: Yes
  → Policy package: New — "PKG-DMZ-PERIMETER"
```

### 3.2 Vérification de la connexion

```bash
# Sur FortiManager CLI
diagnose dvm device list
# Résultat attendu:
# FGT-EDGE    10.0.10.1    MANAGED    Up    FOS 7.4.x
```

---

## 4. Policy Package — Création et gestion

### 4.1 Créer un Policy Package

```
FortiManager GUI → ADOM: DMZ-PERIMETER → Policy & Objects
  → Policy Packages → Create New
  Name        : PKG-DMZ-PERIMETER
  Type        : FortiGate
  Central NAT : Enabled
  Inspection Mode : Flow-based
```

### 4.2 Créer les objets réseau dans FortiManager

```
Policy & Objects → Object Configurations → Firewall Objects → Addresses
  → Create New → Subnet
    Name   : LAN-IT
    Subnet : 10.0.10.0/24
    → OK

  → Create New → Subnet
    Name   : DMZ-IT
    Subnet : 172.16.10.0/24
    → OK
```

### 4.3 Créer les règles dans le Policy Package

```
Policy & Objects → PKG-DMZ-PERIMETER → IPv4 Policy
  → Create New (Policy 10)
    Name        : LAN-IT-to-Internet
    Incoming    : port3 (LAN-IT)
    Outgoing    : port1 (WAN)
    Source      : LAN-IT
    Destination : all
    Service     : HTTP, HTTPS, DNS
    Action      : ACCEPT
    NAT         : Enable (SNAT)
    UTM         : AppCtrl-LAN-IT, WebFilter-LAN-IT
    Log         : All Sessions
    → OK
```

### 4.4 Comparer avant installation

```
Policy & Objects → PKG-DMZ-PERIMETER → Tools → Import Policy
  → Check diff between FortiManager config and device running config
  → Review highlighted differences
  → Accept or reject per-line
```

---

## 5. Installation de la policy sur le device / Policy Install

### 5.1 Via GUI

```
FortiManager GUI → ADOM: DMZ-PERIMETER
  → Device Manager → FGT-EDGE → Install Wizard
    Step 1: Select devices → FGT-EDGE (check)
    Step 2: Select packages → PKG-DMZ-PERIMETER
    Step 3: Preview changes → Review diff
    Step 4: Install → Confirm
```

### 5.2 Via CLI FortiManager

```bash
# Lancer une installation depuis le CLI FortiManager
execute fmpolicy install-policy DMZ-PERIMETER PKG-DMZ-PERIMETER FGT-EDGE

# Surveiller la progression
diagnose dvm task list
# Task Status: Pending → Running → Done
```

### 5.3 Vérifier l'installation

```bash
# Sur FGT-EDGE — vérifier que les policies ont bien été appliquées
show firewall policy | grep "edit\|set name"

# Sur FortiManager
diagnose dvm device list
# Column "Sync Status" doit afficher: In Sync
```

---

## 6. FortiConverter — Migration depuis Cisco ASA

**FortiConverter** est un outil de conversion automatique de configurations firewall vers FortiOS.

### 6.1 Étapes clés de migration ASA → FortiGate

```
Étape 1 — Export la config ASA courante
  ASA# show running-config > asa-config.txt
  Ou : copy running-config ftp://server/asa-config.txt

Étape 2 — Charger dans FortiConverter
  https://converter.fortinet.com (cloud) ou outil local
  → Upload: asa-config.txt
  → Source: Cisco ASA
  → Target: FortiGate (FortiOS 7.4)
  → Convert

Étape 3 — Réviser les résultats
  FortiConverter génère un rapport de conversion :
  ✅ Converted  : objets et règles traduits automatiquement
  ⚠️ Modified   : traduit avec modifications (vérification requise)
  ❌ Not Mapped : éléments sans équivalent FortiGate (action manuelle)

Étape 4 — Éléments nécessitant révision manuelle
  - ACL avec objets ASA spécifiques (object-group)  → addrgrp FortiGate
  - Crypto maps IPSec                               → FortiGate VPN IPSec
  - NAT dynamique / PAT                             → FortiGate IP Pool
  - MPF (Modular Policy Framework)                  → UTM Profiles FortiGate
  - AAA configuration                               → FortiGate RADIUS/LDAP
  - Failover (ASA) → HA FGCP                        → Config HA FortiGate

Étape 5 — Import dans FortiManager
  FortiConverter → Export → FortiManager Package (.json)
  FortiManager → ADOM → Policy Packages → Import
  → Révision et nettoyage dans FortiManager
  → Test en lab avant production

Étape 6 — Déploiement progressif
  1. Déployer en mode "monitoring" (action=monitor, log=all)
  2. Observer les logs 48-72h
  3. Identifier les faux positifs / flux légitimes bloqués
  4. Passer en mode "enforcement" règle par règle
  5. Documenter les écarts dans la matrice de flux
```

### 6.2 Correspondances Cisco ASA → FortiGate

| Concept ASA | Concept FortiGate | Notes |
|-------------|-------------------|-------|
| `access-list` + `access-group` | `firewall policy` | FortiGate = stateful par défaut |
| `object network` / `object-group` | `firewall address` / `addrgrp` | |
| `nat (inside,outside)` | `firewall vip` (DNAT) / `ippool` (SNAT) | |
| `crypto map` / `tunnel-group` | `vpn ipsec phase1/phase2` | |
| `inspect` (MPF) | UTM profiles (IPS, AppCtrl) | |
| `logging` | `log setting` + FortiAnalyzer | |
| `failover` | `system ha` FGCP | |
| `service-policy` QoS | `traffic shaper` | |

---

## 7. Révocation et rollback / Revision & Rollback

```bash
# Voir l'historique des installations sur FortiManager
execute fmpolicy revision-history DMZ-PERIMETER PKG-DMZ-PERIMETER

# Rollback vers une version précédente
execute fmpolicy revert-policy DMZ-PERIMETER PKG-DMZ-PERIMETER 3
# → Reverts to revision 3

# Sur FGT — rollback de configuration (si hors FortiManager)
execute backup config tftp fgt-edge-backup.conf 10.0.10.60
execute restore config tftp fgt-edge-backup.conf 10.0.10.60
```
