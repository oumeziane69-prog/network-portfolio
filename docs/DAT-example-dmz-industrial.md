# DAT — Architecture Technique Détaillée
# DAT — Detailed Architecture Document: DMZ Industrielle CNPE-SITE-A

> **Document type:** DAT (Document d'Architecture Technique)
> **Référence:** DAT-CNPE-SITE-A-DMZ-001
> **Version:** 1.2
> **Date:** 2026-04-15
> **Statut:** Validé — En production
> **Auteur:** Équipe Réseaux & Sécurité — Fictif (données anonymisées)
> **Classification:** INTERNE — Ne pas diffuser hors périmètre projet

---

## 1. Contexte et Objectifs

### 1.1 Contexte

Le site CNPE-SITE-A (Centre Nucléaire de Production d'Électricité fictif) exploite un système de supervision industrielle (SCADA/DCS) pour le contrôle des tranches de production. La convergence progressive des réseaux IT et OT nécessite la mise en œuvre d'une zone de démarcation sécurisée (IDMZ — Industrial DMZ) conforme aux exigences :

- **IEC 62443-3-3** (sécurité des systèmes de contrôle industriel)
- **ANSSI guide SCADA 2015** (recommandations pour la cybersécurité des systèmes industriels)
- **Politique de sécurité interne** inspirée des guides ASN (Autorité de Sûreté Nucléaire) pour la protection des systèmes numériques importants pour la sûreté (SIS)

### 1.2 Objectifs

1. Isoler le réseau OT (LAN-OT : SCADA, HMI, automates) du réseau IT (LAN-IT : bureautique, ERP, messagerie)
2. Permettre les échanges de données contrôlés IT↔OT via une IDMZ cloisonnée
3. Bloquer tout accès Internet depuis les systèmes OT
4. Assurer la traçabilité complète des flux (logging centralisé FortiAnalyzer)
5. Maintenir les performances de contrôle-commande (latence < 10ms LAN-OT interne)

### 1.3 Périmètre

| Inclus dans ce DAT | Exclus de ce DAT |
|-------------------|-----------------|
| Architecture NGFW double-pare-feu (FGT-EDGE + FGT-INTERNAL) | Réseau téléphonie (PABX, ToIP) |
| Segmentation IT / IDMZ / OT | VPN site-à-site (traité dans DAT-VPN-001) |
| Politiques de filtrage FortiGate | Sécurité physique (contrôle d'accès salles) |
| Supervision réseau (FortiAnalyzer + NMS) | Systèmes OT eux-mêmes (automates, DCS) |
| Gestion centralisée FortiManager | AAA / 802.1X (traité dans DAT-RADIUS-001) |

---

## 2. Périmètre Technique

### 2.1 Équipements concernés

| Équipement | Rôle | Plateforme | Version |
|-----------|------|-----------|---------|
| FGT-EDGE | NGFW périmètre — Internet↔DMZ-IT↔LAN-IT | FortiGate 600E | FortiOS 7.4.3 |
| FGT-INTERNAL | NGFW interne — DMZ-IT↔DMZ-OT↔LAN-OT | FortiGate 200F | FortiOS 7.4.3 |
| FMG-01 | Gestion centralisée des politiques | FortiManager VM | 7.4.3 |
| FAZ-01 | Collecte et corrélation des logs | FortiAnalyzer VM | 7.4.3 |
| NMS-01 | Supervision réseau SNMP | LibreNMS 23.x | — |
| SW-CORE-IT | Commutation LAN-IT (distribution) | Cisco Catalyst 9300 | 17.9 |
| SW-CORE-OT | Commutation LAN-OT (distribution) | Cisco IE-3400 (industrie) | 17.9 |

### 2.2 Contraintes techniques

- **Disponibilité requise:** 99,9% (8,76h de maintenance/an maximum)
- **RTO (Recovery Time Objective):** < 4h (bascule HA automatique < 1s)
- **RPO (Recovery Point Objective):** 0 (pas de perte de config — FortiManager)
- **Maintenance:** Fenêtres de maintenance planifiées (dimanche 02h–06h)
- **Réglementation OT:** Aucune modification du réseau OT sans validation ingénierie procédés

---

## 3. Topologie et Architecture

### 3.1 Schéma logique

```
                    INTERNET
                       │
              ┌────────┴────────┐
              │   FGT-EDGE      │  FortiGate 600E
              │ (NGFW périmètre)│  ClusterXL A/P
              └────┬────────────┘
                   │
       ┌───────────┼───────────┐
       │           │           │
   [WAN]       [DMZ-IT]    [LAN-IT]
               172.16.10    10.0.10.0/24
               .0/24        (Corp, IT servers)
                   │
              ┌────┴────────────┐
              │  FGT-INTERNAL   │  FortiGate 200F
              │  (NGFW interne) │  Standalone
              └────┬────────────┘
                   │
       ┌───────────┼───────────┐
       │           │           │
   [DMZ-IT-ext] [DMZ-OT]   [LAN-OT]
   172.16.10.2  172.16.20    172.16.30.0/24
   (uplink)     .0/24        (SCADA, HMI, PLC)
                (IDMZ)
```

### 3.2 Description des zones de sécurité

| Zone | Réseau | Niveau Purdue | Équipements | Niveau sécurité (IEC 62443) |
|------|--------|--------------|------------|---------------------------|
| WAN / Internet | Dynamic (ISP) | N5 — Internet | Routeur ISP | SL 0 (non contrôlé) |
| LAN-IT | 10.0.10.0/24 | N4 — IT Entreprise | PC, serveurs, AD, ERP | SL 1 |
| DMZ-IT | 172.16.10.0/24 | N3.5 — DMZ IT | Web server, Jump, Historian IT | SL 2 |
| DMZ-OT (IDMZ) | 172.16.20.0/24 | N3.5 — IDMZ | Historian OT replica, Patch server OT | SL 3 |
| LAN-OT | 172.16.30.0/24 | N1-N3 — OT | SCADA, HMI, automates, ingénierie | SL 3–4 |
| OOB Management | 192.168.0.0/24 | N4 (OOB) | Accès console OOB (IPMI, console série) | SL 2 |

### 3.3 Points de filtrage (conduits IEC 62443)

- **Conduit C1:** Internet ↔ DMZ-IT (via FGT-EDGE) — accès publics contrôlés
- **Conduit C2:** LAN-IT ↔ DMZ-IT (via FGT-EDGE) — accès IT vers DMZ applicatif
- **Conduit C3:** DMZ-IT ↔ DMZ-OT (via FGT-INTERNAL) — pont IT/OT — flux très restreints
- **Conduit C4:** DMZ-OT ↔ LAN-OT (via FGT-INTERNAL) — accès vers systèmes OT — minimal

---

## 4. Plan d'adressage

### 4.1 Interfaces FGT-EDGE

| Interface | Alias | Réseau | IP | Description |
|-----------|-------|--------|----|-------------|
| port1 | WAN | ISP | `<WAN-IP-HERE>` | Accès Internet (ISP) |
| port2 | DMZ-IT | 172.16.10.0/24 | 172.16.10.1/24 | Passerelle DMZ-IT |
| port3 | LAN-IT | 10.0.10.0/24 | 10.0.10.1/24 | Passerelle LAN-IT |
| port4 | HA-HB1 | 192.168.100.0/30 | 192.168.100.1/30 | Heartbeat HA principal |
| port5 | HA-HB2 | 192.168.101.0/30 | 192.168.101.1/30 | Heartbeat HA secondaire |

### 4.2 Interfaces FGT-INTERNAL

| Interface | Alias | Réseau | IP | Description |
|-----------|-------|--------|----|-------------|
| port1 | DMZ-IT-ext | 172.16.10.0/24 | 172.16.10.2/24 | Lien vers FGT-EDGE DMZ-IT |
| port2 | DMZ-OT | 172.16.20.0/24 | 172.16.20.1/24 | Passerelle IDMZ |
| port3 | LAN-OT | 172.16.30.0/24 | 172.16.30.1/24 | Passerelle LAN-OT |

### 4.3 Hôtes fixes

| Nom | IP | Zone | Rôle |
|-----|----|------|------|
| AD-Server | 10.0.10.101 | LAN-IT | Active Directory / DNS |
| NTP-Server | 10.0.10.102 | LAN-IT | Serveur NTP interne |
| NMS-Server | 10.0.10.50 | LAN-IT | LibreNMS (supervision SNMP) |
| FAZ-01 | 10.0.10.60 | LAN-IT | FortiAnalyzer |
| FMG-01 | 10.0.10.61 | LAN-IT | FortiManager |
| Web-Server | 172.16.10.10 | DMZ-IT | Serveur web Nginx (HTTPS) |
| Jump-Server | 172.16.10.20 | DMZ-IT | Bastion SSH/RDP vers LAN-OT |
| Historian-IT | 172.16.10.30 | DMZ-IT | Historian IT (OSIsoft PI) |
| WSUS-Mirror | 172.16.10.40 | DMZ-IT | Miroir WSUS/APT pour MAJ OT |
| OT-Historian | 172.16.20.10 | DMZ-OT | Réplica Historian OT |
| OT-Patch-Srv | 172.16.20.20 | DMZ-OT | Serveur de patchs OT (WSUS réplica) |
| SCADA-Server | 172.16.30.10 | LAN-OT | Serveur SCADA supervision |
| HMI-01 | 172.16.30.20 | LAN-OT | Poste opérateur HMI |
| Eng-WS | 172.16.30.30 | LAN-OT | Poste ingénierie (programmation PLC) |

---

## 5. Matrice de Flux

> **Convention:** ✅ Autorisé | ❌ Interdit | ⚠️ Conditionnel (maintenance uniquement)

### 5.1 Conduit C1 — Internet ↔ DMZ-IT (FGT-EDGE)

| # | Source | Destination | Service | Action | Justification |
|---|--------|-------------|---------|--------|---------------|
| F01 | Internet | Web-Server | HTTPS (443) | ✅ Accept (IPS+SSL) | Publication site web institutionnel |
| F02 | Internet | Web-Server | HTTP (80) | ✅ Accept (redirect HTTPS) | Redirection vers HTTPS |
| F03 | Internet | `<WAN-IP>`:25 | SMTP | ✅ Accept → SMTP-Relay | Messagerie entrante |
| F04 | Internet | `<WAN-IP>`:2222 | SSH | ⚠️ Accept → Jump-Server | Accès admin externe (horaires restreints) |
| F05 | Internet | LAN-IT | Tout | ❌ Deny (Alert) | Protection réseau interne |

### 5.2 Conduit C2 — LAN-IT ↔ DMZ-IT (FGT-EDGE)

| # | Source | Destination | Service | Action | Justification |
|---|--------|-------------|---------|--------|---------------|
| F06 | LAN-IT | Internet | HTTP/HTTPS/DNS | ✅ Accept (SNAT + AppCtrl) | Navigation Internet corps IT |
| F07 | LAN-IT | Jump-Server | SSH, RDP | ✅ Accept | Accès bastion pour admins |
| F08 | LAN-IT | Historian-IT | HTTPS | ✅ Accept | Consultation données process |
| F09 | LAN-IT | Web-Server | HTTPS | ✅ Accept | Intranet → applications DMZ |
| F10 | DMZ-IT | LAN-IT | Tout | ❌ Deny (Alert) | La DMZ ne peut pas initier vers IT |

### 5.3 Conduit C3 — DMZ-IT ↔ DMZ-OT (FGT-INTERNAL)

| # | Source | Destination | Service | Action | Justification |
|---|--------|-------------|---------|--------|---------------|
| F11 | Jump-Server | LAN-OT (tout) | SSH, RDP | ✅ Accept (Alert) | Accès admin OT via bastion |
| F12 | Historian-IT | OT-Historian | HTTPS (pull données) | ✅ Accept (IPS) | Lecture données procédé |
| F13 | WSUS-Mirror | OT-Patch-Srv | HTTPS, SMB | ⚠️ Accept | Réplication patches (fenêtre maintenance) |
| F14 | DMZ-OT | LAN-IT | Tout | ❌ Deny (Alert) | IDMZ ne doit pas initier vers IT |
| F15 | LAN-OT | LAN-IT | Tout | ❌ Deny (Alert) | OT ne peut pas atteindre IT directement |

### 5.4 Conduit C4 — DMZ-OT ↔ LAN-OT (FGT-INTERNAL)

| # | Source | Destination | Service | Action | Justification |
|---|--------|-------------|---------|--------|---------------|
| F16 | OT-Historian | SCADA-Server | OPC-UA (4840-4843) | ✅ Accept (IPS-OT-Strict) | Polling données temps réel |
| F17 | SCADA-Server | OT-Historian | OPC-UA, HTTPS | ✅ Accept (IPS-OT-Strict) | Push données vers réplica |
| F18 | OT-Patch-Srv | HMI-01, Eng-WS | HTTP, HTTPS, SMB | ⚠️ Accept | Déploiement patches OT (maintenance) |
| F19 | NMS-Server | LAN-OT (tout) | SNMP, ICMP | ✅ Accept | Supervision réseau depuis NMS |
| F20 | LAN-OT | Internet | Tout | ❌ Deny (Alert) | INTERDICTION ABSOLUE — exigence sûreté |

---

## 6. Règles Firewall et NAT — Résumé

### 6.1 FGT-EDGE — Politique de filtrage (résumé)

| # | Nom règle | Source | Destination | Service | Action | UTM |
|---|-----------|--------|-------------|---------|--------|-----|
| 10 | LAN-IT-to-Internet | LAN-IT | Internet | HTTP/HTTPS/DNS | Accept + SNAT | AppCtrl, WebFilter, SSL-inspect |
| 20 | LAN-IT-to-JumpServer | LAN-IT | Jump-Server | SSH, RDP | Accept | — |
| 30 | LAN-IT-to-Historian | LAN-IT | Historian-IT | HTTPS | Accept | — |
| 40 | Internet-to-WebServer | Internet | VIP-Web (DNAT) | HTTPS | Accept | IPS-DMZ, SSL-deep |
| 50 | Internet-to-JumpServer | Internet | VIP-Jump (DNAT) | SSH | Accept | IPS-DMZ |
| 99 | IMPLICIT-DENY | Any | Any | All | Deny+Log | — |

### 6.2 FGT-INTERNAL — Politique de filtrage (résumé)

| # | Nom règle | Source | Destination | Service | Action | UTM |
|---|-----------|--------|-------------|---------|--------|-----|
| 10 | JumpServer-to-LAN-OT | Jump-Server | LAN-OT | SSH, RDP | Accept | — |
| 20 | HistorianIT-to-OTHistorian | Historian-IT | OT-Historian | HTTPS | Accept | IPS-IDMZ |
| 30 | OTHistorian-poll-SCADA | OT-Historian | SCADA-Server | OPC-UA | Accept | IPS-OT-Strict |
| 40 | SCADA-push-OTHistorian | SCADA-Server | OT-Historian | OPC-UA, HTTPS | Accept | IPS-OT-Strict |
| 50 | OTPatch-to-LAN-OT | OT-Patch-Srv | HMI-01, Eng-WS | HTTP/HTTPS/SMB | Accept (maint.) | IPS-IDMZ |
| 70 | SNMP-Monitor-LAN-OT | NMS-Server | LAN-OT | SNMP | Accept | — |
| 80 | DENY-LAN-OT-Internet | LAN-OT | Any | All | Deny+Log+Alert | — |
| 90 | DENY-LAN-OT-LAN-IT | LAN-OT | LAN-IT | All | Deny+Log+Alert | — |
| 99 | IMPLICIT-DENY-ALL | Any | Any | All | Deny+Log+Alert | — |

### 6.3 NAT (FGT-EDGE)

| Type | Nom | IP publique | IP privée | Port |
|------|-----|-----------|-----------|------|
| SNAT | SNAT-WAN | `<WAN-IP-HERE>` (overload/PAT) | LAN-IT (10.0.10.0/24) | Dynamic |
| DNAT | VIP-WebServer-HTTPS | `<WAN-IP-HERE>`:443 | 172.16.10.10:443 | 443→443 |
| DNAT | VIP-Jump-SSH | `<WAN-IP-HERE>`:2222 | 172.16.10.20:22 | 2222→22 |

---

## 7. Gestion des risques

### 7.1 Risques identifiés et mesures de mitigation

| ID | Risque | Probabilité | Impact | Mesure de mitigation | Résiduel |
|----|--------|------------|--------|---------------------|----------|
| R01 | Compromission serveur Web (accès entrant HTTPS) | Moyen | Élevé | IPS actif, SSL deep inspection, isolation DMZ-IT | Faible |
| R02 | Latéralisation depuis DMZ-IT vers LAN-IT | Faible | Critique | Règle F10 Deny DMZ→LAN, alertes SIEM | Faible |
| R03 | Accès OT depuis Internet (directe ou indirecte) | Faible | Critique | Règle F20 + F05 Deny absolu, pas de flux direct | Très faible |
| R04 | Déni de service sur FGT-EDGE | Moyen | Élevé | HA A/P (basculement < 1s), rate limiting sur WAN | Faible |
| R05 | Panne FortiManager — perte gestion centralisée | Faible | Moyen | Accès CLI direct SSH sur FGT-EDGE/INTERNAL | Faible |
| R06 | Infection malware via WSUS mirror (OT) | Faible | Critique | Règle F13 conditionnel (maintenance uniquement), hash vérification | Très faible |
| R07 | Attaque protocole OT (Modbus/OPC-UA forgé) | Faible | Critique | IPS-OT-Strict avec signatures Modbus/OPC-UA activées | Faible |
| R08 | Exfiltration données via DNS (tunnel DNS) | Moyen | Moyen | DNS uniquement vers AD-Server + forwarder, inspection AppCtrl | Faible |

### 7.2 Points de surveillance prioritaires (SIEM)

```
Règles de corrélation FortiAnalyzer / SIEM à activer :

ALERTE CRITIQUE :
  - Tout flux LAN-OT → Internet (règle 80 touchée)
  - Tout flux LAN-OT → LAN-IT (règle 90 touchée)
  - Tentatives de connexion vers LAN-OT depuis Internet (règle F05)
  - IPS block sur trafic OPC-UA / Modbus anormal

ALERTE HAUTE :
  - Connexions SSH vers Jump-Server hors horaires (21h–06h)
  - Plus de 10 tentatives de connexion HTTPS sur Web-Server/minute
  - Déconnexion FGT du FortiAnalyzer (perte logs)
  - Basculement HA FGT-EDGE (failover inattendu)

ALERTE MOYENNE :
  - Nouvel équipement MAC inconnu en LAN-OT
  - Flood SNMP depuis source non autorisée
  - Dépassement de bande passante > 80% sur lien WAN
```

---

## 8. Annexes

### 8.1 Références documentaires

| Document | Référence | Localisation |
|---------|----------|-------------|
| IEC 62443-3-3 (IACS security) | IEC 62443-3-3:2013 | Bibliothèque technique |
| Guide ANSSI SCADA 2015 | ANSSI-PA-079 | anssi.fr |
| Recommandations CIS FortiGate | CIS Benchmark FortiOS v7 | cisecurity.org |
| DEX Exploitation — FGT-EDGE | DEX-CNPE-SITE-A-FGT-EDGE-001 | ITSM interne |
| DAT VPN site-à-site | DAT-CNPE-SITE-A-VPN-001 | ITSM interne |
| DAT AAA / 802.1X | DAT-CNPE-SITE-A-RADIUS-001 | ITSM interne |

### 8.2 Historique des révisions

| Version | Date | Auteur | Modifications |
|---------|------|--------|--------------|
| 1.0 | 2025-09-01 | Équipe Réseaux | Création initiale — architecture validée en lab |
| 1.1 | 2025-11-15 | Équipe Réseaux | Ajout FGT-INTERNAL, règles OT, IPS-OT-Strict |
| 1.2 | 2026-04-15 | Équipe Réseaux | MAJ matrix flux, ajout règles F19/F20, revue risques |

### 8.3 Contacts et responsabilités

| Rôle | Périmètre | Contact |
|------|-----------|---------|
| Responsable architecture réseau | FGT-EDGE, FGT-INTERNAL, FortiManager | Équipe Réseaux CNPE-SITE-A |
| Responsable sécurité OT | LAN-OT, DMZ-OT, ICS security | Équipe Sûreté Numérique |
| Exploitant N2 | Supervision quotidienne, alertes SIEM | NOC (24/7) |
| Fournisseur FortiGate | Support matériel, escalade TAC | Fortinet France — TAC |
