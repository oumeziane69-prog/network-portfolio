# IEC 62443 — Synthèse & Application contexte industriel / nucléaire
# IEC 62443 — Overview & Application in Industrial / Nuclear Context

> **Référence :** `SEC-IEC62443-v1.0`
> **Auteur :** Hakim Oumeziane
> **Dernière mise à jour :** 2026-04-15
> **Audience :** Ingénieurs réseau/sécurité, architectes OT, équipes RSSI industriels

---

## 1. Introduction

### 1.1 Qu'est-ce que l'IEC 62443 ?

L'**IEC 62443** est la norme internationale de référence pour la **cybersécurité des systèmes d'automatisation et de contrôle industriels (IACS — Industrial Automation and Control Systems)**. Elle est publiée conjointement par l'IEC (International Electrotechnical Commission) et l'ISA (International Society of Automation, série ISA-99).

Elle s'applique à tout système IACS quel que soit le secteur : énergie, eau, chimie, pétrochimie, industrie pharmaceutique, **nucléaire**, transports, et agroalimentaire.

**Objectif principal :** Définir des exigences et des bonnes pratiques pour protéger les systèmes industriels contre les cybermenaces, tout en maintenant la disponibilité et la sécurité des processus physiques.

### 1.2 Pourquoi l'IEC 62443 en contexte nucléaire ?

Dans le contexte des **Centres Nucléaires de Production d'Électricité (CNPE)** d'EDF, la convergence IT/OT impose une rigueur maximale :

- Les systèmes de contrôle-commande (DCS, PLCs) pilotent directement des processus physiques à risque
- Une cyberattaque réussie peut avoir des conséquences sur la **sûreté nucléaire** (safety) et pas seulement sur la **sécurité informatique** (security)
- L'ANSSI (Agence Nationale de la Sécurité des Systèmes d'Information) impose des exigences spécifiques aux **Opérateurs d'Importance Vitale (OIV)**, dont EDF fait partie
- La directive **NIS2** (transposée en France) renforce les obligations de sécurité pour les secteurs critiques

> **Note importante :** La norme IEC 62443 coexiste avec les exigences réglementaires nucléaires spécifiques (ASN, règles fondamentales de sûreté) qui priment toujours sur les recommandations génériques.

---

## 2. Structure de la norme IEC 62443

La norme est organisée en **4 séries** couvrant différents niveaux de l'organisation :

```
IEC 62443
├── Série 1 — Général (Fondements)
│   ├── 62443-1-1 : Terminologie, concepts et modèles
│   ├── 62443-1-2 : Glossaire de termes et abréviations
│   ├── 62443-1-3 : Métriques de conformité des systèmes
│   └── 62443-1-4 : Cycle de vie IACS et cas d'usage
│
├── Série 2 — Process (Opérateur / Asset Owner)
│   ├── 62443-2-1 : Exigences du système de management de la sécurité
│   ├── 62443-2-2 : Gestion opérationnelle de la sécurité IACS
│   ├── 62443-2-3 : Gestion des patches pour les environnements IACS
│   └── 62443-2-4 : Exigences pour les fournisseurs de services IACS
│
├── Série 3 — Système (Intégrateur système / Architecte)
│   ├── 62443-3-2 : Évaluation des risques pour la conception système
│   ├── 62443-3-3 : Exigences de sécurité système et niveaux SL ⭐
│   └── 62443-3-4 : (en développement)
│
└── Série 4 — Composant (Fabricant de produits IACS)
    ├── 62443-4-1 : Exigences du cycle de vie de développement sécurisé
    └── 62443-4-2 : Exigences de sécurité pour les composants IACS
```

> ⭐ **62443-3-3** est la partie la plus utilisée opérationnellement : elle définit les Security Levels et les Foundational Requirements.

---

## 3. Modèle de zones et conduits

### 3.1 Concept fondamental

L'IEC 62443 introduit deux concepts architecturaux centraux pour la segmentation des systèmes industriels :

**Zone :** Regroupement logique d'actifs IACS partageant le même niveau de sécurité requis et les mêmes politiques de sécurité.

**Conduit :** Canal de communication sécurisé reliant deux zones, soumis à des contrôles de sécurité spécifiques (firewall, chiffrement, filtrage protocolaire).

```
  Zone A (SL3)                   Zone B (SL2)
+─────────────+   Conduit C1    +─────────────+
│  PLCs/DCS   │◄──────────────►│  SCADA/HMI  │
│  (Contrôle) │  (Firewall +   │ (Supervision)│
+─────────────+   IDS + logs)   +─────────────+
                                      │
                               Conduit C2
                                      │
                              Zone C (SL1)
                           +─────────────────+
                           │   IT / Business  │
                           │   (ERP, AD...)   │
                           +─────────────────+
```

### 3.2 Principes de définition des zones

| Critère | Description |
|---------|-------------|
| Criticité | Les actifs avec le même niveau de criticité process sont regroupés |
| Niveau SL requis | Tous les actifs d'une zone doivent atteindre le SL cible de la zone |
| Connectivité | Les actifs qui doivent communiquer sont de préférence dans la même zone |
| Propriétaire | Actifs sous la même responsabilité opérationnelle |

---

## 4. Niveaux de sécurité (Security Levels)

### 4.1 Définition des SL

L'IEC 62443 définit quatre niveaux de sécurité (**Security Level — SL**) caractérisant la robustesse des mesures de protection en fonction de la sophistication de l'attaquant anticipé :

| Niveau | Nom | Profil d'attaquant | Description |
|--------|-----|-------------------|-------------|
| **SL 1** | Protection basique | Attaquant non ciblé, opportuniste | Protection contre les exploits génériques non intentionnels (erreur humaine, malware de masse) |
| **SL 2** | Protection contre attaquant modéré | Attaquant ciblé, moyens simples | Protection contre les attaquants qui ciblent délibérément le système avec des moyens et motivations modérés |
| **SL 3** | Protection contre attaquant sophistiqué | Attaquant ciblé, moyens importants | Protection contre des attaquants utilisant des techniques avancées, avec expertise IACS |
| **SL 4** | Protection contre État / APT | Moyens étatiques, motivation critique | Protection contre des attaquants disposant de ressources étatiques et d'une motivation extrême |

### 4.2 Les trois formes du Security Level

| Forme | Notation | Description |
|-------|----------|-------------|
| SL cible (Target) | **SL-T** | Niveau de sécurité requis par l'analyse de risques |
| SL capacité (Capability) | **SL-C** | Niveau que le composant/système peut atteindre selon ses fonctions |
| SL atteint (Achieved) | **SL-A** | Niveau réellement implémenté après déploiement et vérification |

> **Objectif :** SL-A ≥ SL-T pour chaque zone.

### 4.3 SL recommandés par zone (contexte CNPE)

| Zone | Niveau | SL-T recommandé | Justification |
|------|--------|----------------|---------------|
| N4 — IT Entreprise | IT classique | SL 1-2 | Données business, pas d'impact process direct |
| N3.5 — IDMZ | Tampon IT/OT | SL 2-3 | Zone de transition critique — exposition des deux côtés |
| N3 — Supervision OT | SCADA/MES | SL 3 | Accès à la supervision du process |
| N2 — HMI/Opérateur | Contrôle direct | SL 3 | Commandes directes sur le process |
| N1 — PLCs/DCS | Contrôle-commande | **SL 3-4** | Impact direct sur le process physique |
| N0 — Terrain | Capteurs/actionneurs | Physique | Isolation physique + SL 3 sur le réseau amont |

---

## 5. Les 7 Foundational Requirements (FR)

L'IEC 62443-3-3 définit **7 exigences fondamentales** que tout système IACS doit satisfaire selon son niveau SL cible :

| # | Foundational Requirement | Description |
|---|--------------------------|-------------|
| **FR 1** | Identification & Authentication Control (IAC) | Identification et authentification de tous les utilisateurs, processus et équipements |
| **FR 2** | Use Control (UC) | Contrôle des droits d'utilisation — principe du moindre privilège |
| **FR 3** | System Integrity (SI) | Protection de l'intégrité des communications et des logiciels |
| **FR 4** | Data Confidentiality (DC) | Protection de la confidentialité des données en transit et au repos |
| **FR 5** | Restricted Data Flow (RDF) | Segmentation réseau — limiter la propagation des flux entre zones |
| **FR 6** | Timely Response to Events (TRE) | Détection, journalisation, et réponse aux incidents de sécurité |
| **FR 7** | Resource Availability (RA) | Disponibilité des ressources — protection contre les dénis de service |

### 5.1 Exigences système (SR) associées par SL

Chaque FR se décline en **System Requirements (SR)** avec des **Requirement Enhancements (RE)** selon le SL :

```
Exemple FR 1 — IAC :
  SR 1.1 — Identification et authentification des utilisateurs humains
    SL 1 : Authentification par mot de passe
    SL 2 : + Complexité du mot de passe imposée
    SL 3 : + MFA (authentification multi-facteur)
    SL 4 : + Authentification matérielle (smartcard, PKI)
```

---

## 6. Correspondance avec le Modèle de Purdue

L'IEC 62443 ne prescrit pas de topologie réseau spécifique, mais est naturellement compatible avec le **Modèle de Purdue (ISA-95)** :

| Niveau Purdue | Zone IEC 62443 | SL-T typique | Mesures clés |
|---------------|---------------|-------------|--------------|
| N4 — Enterprise | Zone IT | SL 1-2 | AD, patch management, antivirus |
| N3.5 — IDMZ | Zone tampon | SL 2-3 | Firewall bidirectionnel, Jump Server, Historian |
| N3 — Site Ops | Zone supervision | SL 3 | Segmentation, SCADA hardening, IDS |
| N2 — HMI | Zone contrôle IHM | SL 3 | Application whitelisting, MFA opérateur |
| N1 — PLCs/DCS | Zone contrôle | SL 3-4 | Isolation physique, patch contrôlé, audit |
| N0 — Terrain | Zone terrain | Physique | Accès physique contrôlé, bus terrain isolé |

---

## 7. Applicabilité en contexte CNPE EDF

### 7.1 Enjeux spécifiques au nucléaire

| Enjeu | Description | Réponse IEC 62443 |
|-------|-------------|-------------------|
| Sûreté-sécurité (Safety-Security) | Les cyberattaques peuvent impacter la sûreté nucléaire | SL 3-4 sur les systèmes I&C de sûreté |
| Systèmes hérités (Legacy) | Nombreux équipements anciens sans capacité de patch | Compensation par segmentation (FR 5) + surveillance (FR 6) |
| Cycles de maintenance longs | Mises à jour rares — fenêtres de maintenance restreintes | Gestion des patches IEC 62443-2-3 |
| Exigences réglementaires multiples | ASN, ANSSI OIV, NIS2, INB | IEC 62443 comme cadre fédérateur |
| Indisponibilité inacceptable | Le process doit rester disponible | FR 7 — RA : haute disponibilité, redondance |

### 7.2 Articulation avec les exigences ANSSI OIV

```
Cadre réglementaire CNPE EDF
├── Loi de Programmation Militaire (LPM) / NIS2
│   └── Obligation de sécurisation des systèmes critiques (OIV)
│       └── Arrêtés sectoriels ANSSI
│           └── IEC 62443 comme standard technique de référence
│
├── Réglementation nucléaire (ASN / INB)
│   └── Règles Fondamentales de Sûreté (RFS)
│       └── Systèmes I&C de sûreté (catégories A, B, C)
│           └── IEC 62443-4-2 pour composants I&C
│
└── Guide ANSSI — Maîtrise des risques numériques pour les systèmes industriels
    └── Recommandations techniques alignées IEC 62443
```

### 7.3 Bonnes pratiques de segmentation pour CNPE

1. **Séparation physique des réseaux de sûreté** — les systèmes I&C de sûreté (catégorie A) ne doivent pas être connectés aux réseaux OT supervisory ou IT, même via un firewall
2. **IDMZ nucléaire** — la zone tampon entre IT et OT doit intégrer un Historian certifié et un Jump Server avec session recording
3. **Gestion des clés USB et médias amovibles** — procédures strictes pour le transfert de données et de patches vers les zones OT isolées
4. **Cartographie des actifs** — inventaire exhaustif obligatoire avant toute démarche IEC 62443 (62443-2-1)
5. **Plan de gestion des patches** — plan formalisé selon 62443-2-3, avec priorisation basée sur le risque
6. **Formation et sensibilisation** — tout personnel intervenant en zone OT doit être formé aux risques cybersécurité industrielle

---

## 8. Démarche de conformité IEC 62443 — Gap Analysis

### 8.1 Étapes de la démarche

```
Étape 1 — Inventaire et cartographie
  └── Identifier tous les actifs IACS (équipements, logiciels, réseaux)
      Référence : IEC 62443-2-1

Étape 2 — Analyse de risques
  └── Identifier les menaces, vulnérabilités, et impacts
      Définir le SL-T par zone
      Référence : IEC 62443-3-2

Étape 3 — Gap Analysis
  └── Comparer SL-A actuel vs SL-T requis pour chaque FR
      Identifier les écarts et les axes de remédiation

Étape 4 — Plan de remédiation
  └── Prioriser les actions par criticité et faisabilité
      Budgétiser les investissements
      Planifier les fenêtres de maintenance

Étape 5 — Implémentation
  └── Déployer les mesures techniques et organisationnelles
      Référence : IEC 62443-3-3, 62443-4-2

Étape 6 — Vérification et certification
  └── Audits internes et externes
      Certification tierce partie (optionnelle)
      Suivi continu (FR 6 — TRE)
```

### 8.2 Exemple de gap analysis simplifié (FR 1 — IAC)

| Exigence | SL-T | État actuel | Écart | Action corrective |
|----------|------|-------------|-------|------------------|
| SR 1.1 — Auth utilisateurs | SL 3 | Mot de passe simple | ❌ Écart SL2→SL3 | Déployer MFA sur tous les accès admin OT |
| SR 1.2 — Auth équipements | SL 3 | Certificats auto-signés | ⚠️ Partiel | Déployer PKI interne, certificats signés |
| SR 1.3 — Auth multi-facteur | SL 3 | Non déployé | ❌ Absent | Déployer RADIUS + TOTP pour Jump Server |
| SR 1.4 — Gestion des identifiants | SL 2 | Comptes partagés | ❌ Écart | Comptes nominatifs + PAM (Privileged Access Mgmt) |

---

## 9. Lien avec autres normes et guides

| Norme / Guide | Relation avec IEC 62443 |
|---------------|------------------------|
| **NIST SP 800-82 Rev.3** | Guide OT américain — très complémentaire, compatible |
| **ISO 27001** | Gestion de la sécurité IT — IEC 62443 est la déclinaison OT |
| **ANSSI — Guide de la sécurité des systèmes industriels** | Recommandations françaises alignées 62443, obligatoires OIV |
| **NIS2 (Directive EU)** | Obligations légales pour OES/OIV — IEC 62443 comme moyen de conformité |
| **IEC 61511 (Safety)** | Norme de sécurité fonctionnelle (SIL) — complémentaire à 62443 |
| **NERC CIP** | Norme américaine secteur électrique — similaire à 62443 appliqué à l'énergie |
| **Modèle de Purdue (ISA-95)** | Architecture de référence compatible avec les zones/conduits 62443 |

---

## 10. Ressources et labs associés

| Ressource | Lien |
|-----------|------|
| Lab pratique IEC 62443 | [labs/ot-industrial/iec62443-overview/](../labs/ot-industrial/iec62443-overview/README.md) |
| Lab segmentation Purdue | [labs/ot-industrial/purdue-model-segmentation/](../labs/ot-industrial/purdue-model-segmentation/README.md) |
| Matrice de flux IT/OT | [docs/flux-matrix-IT-OT.md](flux-matrix-IT-OT.md) |
| Scénarios de sécurité DMZ | [docs/security-usecases.md](security-usecases.md) |
| Template DAT | [docs/templates/DAT-template.md](templates/DAT-template.md) |
