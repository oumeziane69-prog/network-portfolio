# DAT — Dossier d'Architecture Technique
# Technical Architecture Document (TAD)

> **Template version :** 1.0
> **Statut :** `[DRAFT | REVIEW | APPROVED]`
> **Référence :** `DAT-[PROJET]-[YYYYMMDD]`
> **Auteur :** `<Nom Prénom>`
> **Validé par :** `<Nom Prénom>`
> **Date de création :** `<YYYY-MM-DD>`
> **Dernière mise à jour :** `<YYYY-MM-DD>`

---

## 1. Contexte / Context

### 1.1 Présentation du projet

> _Décrire en 2-3 paragraphes le projet, sa finalité métier, et les enjeux techniques. Préciser le commanditaire et les parties prenantes._

**FR** — `<Description du projet et de son contexte métier>`

**EN** — `<Project description and business context>`

### 1.2 Objectifs architecturaux

| Objectif | Priorité | Description |
|----------|----------|-------------|
| Disponibilité | `[Critique / Haute / Normale]` | `<SLA cible, ex: 99.9%>` |
| Sécurité | `[Critique / Haute / Normale]` | `<Niveau de classification des données>` |
| Scalabilité | `[Critique / Haute / Normale]` | `<Croissance attendue sur N ans>` |
| Performance | `[Critique / Haute / Normale]` | `<Latence max, débit min>` |

### 1.3 Contraintes

- **Techniques :** `<Équipements imposés, OS, protocoles>` 
- **Réglementaires :** `<RGPD, NIS2, IEC 62443, LPM, ...>`
- **Budgétaires :** `<Enveloppe matérielle / logicielle>`
- **Temporelles :** `<Délais de livraison>`

---

## 2. Périmètre / Scope

### 2.1 Inclus dans le périmètre

- `<Élément 1>`
- `<Élément 2>`
- `<Élément 3>`

### 2.2 Hors périmètre

- `<Élément exclu 1>`
- `<Élément exclu 2>`

### 2.3 Interfaces avec les systèmes tiers

| Système tiers | Type d'interface | Protocole | Flux |
|---------------|-----------------|-----------|------|
| `<Nom système>` | `<API / SNMP / Syslog / ...>` | `<Protocole>` | `<Entrant / Sortant>` |

---

## 3. Topologie / Topology

### 3.1 Diagramme logique

```
[Insérer ici le diagramme ASCII ou référencer un fichier image]

Exemple :
  Internet
     |
  [Firewall] (DMZ)
   /       \
 LAN       Servers
```

### 3.2 Diagramme physique

```
[Insérer ici le câblage physique ou référencer un fichier image]
```

### 3.3 Inventaire des équipements

| Équipement | Modèle | Rôle | Localisation | Redondance |
|------------|--------|------|-------------|------------|
| `<Nom>` | `<Modèle/OS>` | `<Rôle>` | `<Baie/Site>` | `<Oui/Non>` |

---

## 4. Plan d'adressage / Addressing Plan

| Réseau / VLAN | Plage IP | Masque | Passerelle | Usage |
|---------------|----------|--------|-----------|-------|
| VLAN 10 — LAN IT | `10.0.10.0` | `/24` | `10.0.10.1` | Postes utilisateurs |
| VLAN 20 — Servers | `10.0.20.0` | `/24` | `10.0.20.1` | Serveurs internes |
| VLAN 100 — DMZ | `10.0.100.0` | `/24` | `10.0.100.1` | Serveurs exposés |
| VLAN 200 — OT | `172.16.0.0` | `/24` | `172.16.0.1` | Réseau industriel |
| WAN | `<IP-HERE>` | `/30` | `<GW-HERE>` | Lien opérateur |

> **Règle :** Aucune adresse IP réelle de production ne doit figurer dans ce document si commité dans un dépôt public. Utiliser des plages RFC 1918 ou des placeholders `<IP-HERE>`.

---

## 5. Matrice de flux / Traffic Flow Matrix

| Source | Destination | Port(s) | Protocole | Action | Justification |
|--------|-------------|---------|-----------|--------|---------------|
| LAN IT | Internet | 80, 443 | TCP | Permit | Navigation web |
| LAN IT | Servers | 443 | TCP | Permit | Applications internes |
| DMZ | LAN IT | * | * | Deny | Isolation DMZ |
| OT | LAN IT | * | * | Deny | Isolation OT |
| OT | Historian (DMZ) | 443 | TCP | Permit | Remontée de données |
| Tout | Tout | * | * | Deny | Règle implicite de refus |

---

## 6. Règles firewall / Firewall Rules

### 6.1 Politique générale

> _Default deny — tout ce qui n'est pas explicitement autorisé est refusé._

### 6.2 Règles détaillées

| ID | Nom règle | Src Zone | Dst Zone | Src IP | Dst IP | Port | Proto | Action | Log |
|----|-----------|----------|----------|--------|--------|------|-------|--------|-----|
| 1 | LAN-to-Internet | LAN | WAN | `10.0.10.0/24` | Any | 80,443 | TCP | Permit | Oui |
| 2 | LAN-to-Servers | LAN | Servers | `10.0.10.0/24` | `10.0.20.0/24` | 443 | TCP | Permit | Oui |
| 99 | Implicit-Deny | Any | Any | Any | Any | Any | Any | Deny | Oui |

### 6.3 NAT

| Type NAT | Src IP | Dst IP | IP traduite | Port traduit | Commentaire |
|----------|--------|--------|------------|-------------|-------------|
| SNAT (Hide) | `10.0.10.0/24` | Internet | `<WAN-IP>` | Dynamique | Accès Internet |
| DNAT (Static) | Internet | `<WAN-IP>:443` | `10.0.100.10` | 443 | Serveur web DMZ |

---

## 7. Risques / Risks

| ID | Risque | Probabilité | Impact | Mesure de mitigation | Risque résiduel |
|----|--------|-------------|--------|---------------------|----------------|
| R01 | Défaillance du pare-feu principal | Faible | Critique | Redondance HA actif/passif | Acceptable |
| R02 | Attaque par latéralisation IT → OT | Moyenne | Critique | Segmentation stricte + IPS | À surveiller |
| R03 | Fuite de données DMZ | Faible | Haute | Filtrage sortant + DLP | Acceptable |
| R04 | `<Risque>` | `<Proba>` | `<Impact>` | `<Mitigation>` | `<Résiduel>` |

---

## 8. Annexes / Appendices

- `[ ]` Annexe A — Diagramme réseau détaillé
- `[ ]` Annexe B — Configuration équipements (sanitisée)
- `[ ]` Annexe C — Tests de validation
- `[ ]` Annexe D — Références normatives (RFC, IEC, NIST)

---

*Document généré avec le template DAT v1.0 — network-portfolio*
