# Security Use Cases — Scénarios de sécurité réseau

> **Référence :** `SEC-USECASES-v1.0`
> **Auteur :** Hakim Oumeziane
> **Dernière mise à jour :** 2026-04-15
> **Statut :** En cours de rédaction

Ce document présente trois scénarios de sécurité réseau illustrant des architectures réelles. Toutes les adresses IP sont fictives (RFC 1918 ou placeholders).

---

## Scénario 1 — VPN IPSec Fortinet Site-à-Site

### 1.1 Contexte

Une entreprise possède deux sites géographiquement séparés (siège et agence) devant communiquer de façon sécurisée sur Internet. Les deux sites disposent d'un pare-feu FortiGate. Le trafic métier (RDP, partage de fichiers SMB, sauvegardes) doit transiter de manière chiffrée.

### 1.2 Architecture

```
  Siège (HQ)                              Agence (Branch)
+─────────────────────+                 +─────────────────────+
| LAN : 10.0.1.0/24  |                 | LAN : 10.0.2.0/24  |
|                     |                 |                     |
| [FortiGate HQ]      |  IPSec Tunnel   | [FortiGate Branch]  |
|  WAN : <IP-HQ>      |───────────────►|  WAN : <IP-BRANCH>  |
+─────────────────────+                 +─────────────────────+
        |                                        |
  10.0.1.0/24                             10.0.2.0/24
  (Postes, Servers)                       (Postes, Imprimantes)
```

### 1.3 Configuration IKEv2 (synthèse)

**Phase 1 (IKE SA) :**

| Paramètre | Valeur |
|-----------|--------|
| Version IKE | IKEv2 |
| Authentification | Pre-Shared Key (PSK) ou certificat X.509 |
| Chiffrement | AES-256-GCM |
| Intégrité | SHA-256 |
| DH Group | Group 14 (2048-bit MODP) |
| Lifetime | 86400 secondes |

**Phase 2 (IPSec SA) :**

| Paramètre | Valeur |
|-----------|--------|
| Protocole | ESP |
| Chiffrement | AES-256-GCM |
| PFS | Activé (Group 14) |
| Sélecteur source | `10.0.1.0/24` |
| Sélecteur destination | `10.0.2.0/24` |
| Lifetime | 3600 secondes |

### 1.4 Politiques de sécurité FortiGate

| ID | Src Zone | Dst Zone | Src Net | Dst Net | Service | Action |
|----|----------|----------|---------|---------|---------|--------|
| 10 | LAN | VPN | `10.0.1.0/24` | `10.0.2.0/24` | RDP, SMB, Backup | Accept |
| 11 | VPN | LAN | `10.0.2.0/24` | `10.0.1.0/24` | RDP, SMB | Accept |
| 99 | Any | Any | Any | Any | Any | Deny |

### 1.5 Points de vigilance

- **PSK :** Utiliser un secret fort (32+ caractères) — ne jamais committer en clair
- **DPD (Dead Peer Detection) :** Activer pour détecter les tunnels morts et déclencher la reconnexion
- **Monitoring :** Superviser le statut du tunnel via SNMP ou FortiMonitor
- **Fail-over :** Envisager un tunnel redondant sur un lien 4G/5G avec SD-WAN

---

## Scénario 2 — 802.1X RADIUS avec Fallback MAB

### 2.1 Contexte

Un réseau d'entreprise doit contrôler l'accès filaire au LAN : seuls les postes authentifiés via 802.1X (EAP-TLS avec certificats d'entreprise) peuvent accéder au VLAN de production. Les équipements sans supplicant 802.1X (imprimantes, téléphones IP, caméras) basculent automatiquement sur le MAB (MAC Authentication Bypass) et sont placés dans un VLAN restreint.

### 2.2 Architecture

```
  [Endpoint — Poste Windows]                  [Endpoint — Imprimante]
         |  EAP-TLS (802.1X)                         |  Pas de supplicant
         |                                            |
  [Cisco Catalyst — Authenticator]            [Cisco Catalyst — Authenticator]
         |                                            |
         +───────────────┬────────────────────────────+
                         | RADIUS (UDP 1812)
                  [FreeRADIUS Server]
                         | LDAP / Active Directory
                  [Windows Server AD]
```

### 2.3 Flux d'authentification

```
1. Endpoint connecte le câble réseau
2. Switch envoie EAP-Request/Identity
3. Endpoint répond avec son identité (EAP-TLS : certificat)
4. Switch transfère à FreeRADIUS via RADIUS Access-Request
5a. SUCCÈS 802.1X → FreeRADIUS valide le certificat via AD
    → RADIUS Access-Accept + attributs VLAN (VLAN 10 — Production)
    → Switch place le port dans VLAN 10
5b. ÉCHEC 802.1X (timeout supplicant) → Switch tente MAB
    → Switch envoie l'adresse MAC comme username RADIUS
    → FreeRADIUS consulte la base MAC autorisée
    → Si MAC connue → VLAN 30 (Restricted/Devices)
    → Si MAC inconnue → VLAN 99 (Guest/Quarantine)
```

### 2.4 Configuration Cisco (extrait)

```
interface GigabitEthernet0/1
 description Access port — 802.1X with MAB fallback
 switchport mode access
 switchport access vlan 99
 dot1x pae authenticator
 dot1x timeout quiet-period 10
 dot1x timeout tx-period 5
 authentication port-control auto
 authentication order dot1x mab
 authentication fallback MAB
 authentication host-mode multi-auth
 spanning-tree portfast
```

### 2.5 Attributs RADIUS pour VLAN dynamique

| Attribut RADIUS | Valeur (exemple) | Usage |
|-----------------|-----------------|-------|
| Tunnel-Type | 13 (VLAN) | Indique un VLAN dynamique |
| Tunnel-Medium-Type | 6 (802) | Médium IEEE 802 |
| Tunnel-Private-Group-ID | `"10"` | Numéro du VLAN assigné |

### 2.6 VLANs utilisés

| VLAN | Nom | Usage | Accès |
|------|-----|-------|-------|
| 10 | Production | Postes authentifiés 802.1X | Plein |
| 30 | Devices | Équipements MAB autorisés | Restreint (ports spécifiques) |
| 40 | Auth-Fail | Échec d'authentification | Internet uniquement |
| 99 | Guest | Invités / inconnusd | Internet uniquement |

---

## Scénario 3 — DMZ Multi-Niveau IT/OT avec Matrice de Flux

### 3.1 Contexte

Un site industriel (industrie manufacturière) doit interconnecter son réseau IT (bureautique, ERP) et son réseau OT (SCADA, PLCs) tout en maintenant une isolation stricte entre les deux. Une zone IDMZ (Industrial DMZ) sert de tampon contrôlé. L'architecture respecte le Modèle de Purdue et les recommandations IEC 62443.

### 3.2 Architecture multi-niveau

```
  ┌─────────────────────────────────────────────────────────┐
  │  NIVEAU 4 — Enterprise IT                               │
  │  ERP (SAP), Active Directory, Email, DNS, WSUS          │
  │  Plage : 10.0.4.0/24                                    │
  └───────────────────────┬─────────────────────────────────┘
                          │ [Firewall IT — FortiGate HQ]
  ┌───────────────────────▼─────────────────────────────────┐
  │  NIVEAU 3.5 — IDMZ (Industrial DMZ)                     │
  │  Historian (OSIsoft PI), Jump Server, Patch Server       │
  │  Plage : 10.0.35.0/24                                   │
  └───────────────────────┬─────────────────────────────────┘
                          │ [Firewall OT — FortiGate Industrial]
  ┌───────────────────────▼─────────────────────────────────┐
  │  NIVEAU 3 — Site Operations                             │
  │  MES, supervision SCADA (serveurs)                      │
  │  Plage : 172.16.3.0/24                                  │
  └───────────────────────┬─────────────────────────────────┘
                          │
  ┌───────────────────────▼─────────────────────────────────┐
  │  NIVEAU 2 — Supervisory                                 │
  │  HMI (Human Machine Interface), SCADA clients           │
  │  Plage : 172.16.2.0/24                                  │
  └───────────────────────┬─────────────────────────────────┘
                          │
  ┌───────────────────────▼─────────────────────────────────┐
  │  NIVEAU 1 — Control                                     │
  │  PLCs (Siemens S7), DCS, RTUs                           │
  │  Plage : 172.16.1.0/24                                  │
  └───────────────────────┬─────────────────────────────────┘
                          │
  ┌───────────────────────▼─────────────────────────────────┐
  │  NIVEAU 0 — Field                                       │
  │  Capteurs, actionneurs, robots                          │
  │  (réseau propriétaire / bus terrain)                    │
  └─────────────────────────────────────────────────────────┘
```

### 3.3 Matrice de flux / Traffic Flow Matrix

| Source | Destination | Port | Protocole | Action | Justification |
|--------|-------------|------|-----------|--------|---------------|
| IT (N4) | IDMZ (N3.5) | 443 | HTTPS | **Permit** | Accès Historian (lecture données) |
| IT (N4) | IDMZ (N3.5) | 22 | SSH | **Permit** | Jump Server vers OT (admin) |
| IT (N4) | OT (N3/N2) | * | * | **Deny** | Accès OT direct interdit |
| IDMZ (N3.5) | IT (N4) | 443, 8443 | HTTPS | **Permit** | Réplication Historian vers ERP |
| IDMZ (N3.5) | OT (N3) | 102 | S7Comm | **Permit** | Historian polling PLC data |
| IDMZ (N3.5) | OT (N3) | 4840 | OPC-UA | **Permit** | Acquisition OPC-UA |
| OT (N3) | IDMZ (N3.5) | 443 | HTTPS | **Permit** | Push données vers Historian |
| OT (N3) | IT (N4) | * | * | **Deny** | Flux montant OT→IT interdit |
| OT (N2) | Internet | * | * | **Deny** | Aucun accès Internet depuis OT |
| Tout | Tout | * | * | **Deny** | Règle implicite de refus |

### 3.4 Règles firewall Firewall IT (N4 ↔ N3.5)

| Règle | Src | Dst | Service | Action | Log |
|-------|-----|-----|---------|--------|-----|
| IT-to-Historian | `10.0.4.0/24` | `10.0.35.10` | HTTPS/443 | Accept | Oui |
| IT-to-JumpServer | `10.0.4.100` | `10.0.35.20` | SSH/22 | Accept | Oui |
| Historian-to-ERP | `10.0.35.10` | `10.0.4.50` | HTTPS/443 | Accept | Oui |
| Deny-IT-to-OT | `10.0.4.0/24` | `172.16.0.0/16` | Any | Deny | Oui |
| Implicit-Deny | Any | Any | Any | Deny | Oui |

### 3.5 Points de vigilance

- **Historian :** Ne jamais installer l'agent Historian directement sur un PLC — utiliser un collecteur dédié en N3
- **Jump Server :** MFA obligatoire + enregistrement de session (session recording)
- **Patch :** Les mises à jour OT doivent transiter par le Patch Server IDMZ — jamais depuis Internet
- **Protocoles OT :** Modbus/TCP et DNP3 sont non authentifiés par nature — compenser par segmentation stricte
- **Monitoring :** Déployer Suricata ou un IDS OT (ex: Claroty, Dragos) en mode passif sur les segments OT
