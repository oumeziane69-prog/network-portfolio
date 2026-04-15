# DEX — Document d'Exploitation
# Operations Document (OD)

> **Template version :** 1.0
> **Statut :** `[DRAFT | REVIEW | APPROVED]`
> **Référence :** `DEX-[PROJET]-[PROCEDURE]-[YYYYMMDD]`
> **Auteur :** `<Nom Prénom>`
> **Validé par :** `<Nom Prénom>`
> **Date de création :** `<YYYY-MM-DD>`
> **Dernière mise à jour :** `<YYYY-MM-DD>`
> **Niveau de confidentialité :** `[Public | Interne | Confidentiel | Restreint]`

---

## 1. Objet du document / Document Purpose

> _Décrire en une phrase ce que fait cette procédure et sur quel équipement / système._

**FR** — `<Exemple : Procédure de déploiement d'une règle firewall FortiGate en production.>`

**EN** — `<Example: Procedure for deploying a FortiGate firewall rule in production.>`

---

## 2. Prérequis / Prerequisites

### 2.1 Accès requis

| Ressource | Accès requis | Justification |
|-----------|-------------|---------------|
| `<Équipement/système>` | `<SSH / HTTPS / Console / API>` | `<Pourquoi cet accès>` |
| Console d'administration | `<Admin / Read-only>` | `<Pourquoi>` |

### 2.2 Droits et habilitations

- [ ] Compte d'administration avec profil `<Nom du profil>`
- [ ] Accès VPN ou réseau de gestion (OOB)
- [ ] Validation d'un responsable `<Nom / rôle>`
- [ ] Fenêtre de maintenance approuvée : `<YYYY-MM-DD HH:MM — HH:MM>`

### 2.3 Outils nécessaires

| Outil | Version | Usage |
|-------|---------|-------|
| `<Terminal SSH>` | `<Version>` | `<Connexion à l'équipement>` |
| `<Navigateur>` | `<Version>` | `<Interface d'administration web>` |
| `<Script Python>` | `<Version>` | `<Automatisation optionnelle>` |

### 2.4 État initial attendu

> _Décrire l'état du système **avant** l'intervention. Inclure les commandes de vérification._

```bash
# Vérification de l'état initial (exemple)
<commande-verification-1>
<commande-verification-2>
```

**Résultat attendu :** `<Décrire ce que la commande doit retourner>`

---

## 3. Procédure pas à pas / Step-by-Step Procedure

> **IMPORTANT** — Lire l'intégralité de la procédure avant de commencer. Effectuer chaque étape dans l'ordre. Ne pas sauter d'étapes.

### Étape 1 — `<Titre de l'étape>`

**Durée estimée :** `<X minutes>`
**Impact :** `<Aucun / Coupure partielle / Coupure totale>`

```bash
# Commandes à exécuter
<commande-1>
<commande-2>
```

**Validation :** `<Comment vérifier que l'étape s'est bien déroulée>`

```bash
# Commande de vérification
<commande-verification>
```

**Résultat attendu :** `<Output attendu>`

---

### Étape 2 — `<Titre de l'étape>`

**Durée estimée :** `<X minutes>`
**Impact :** `<Aucun / Coupure partielle / Coupure totale>`

```bash
# Commandes à exécuter
<commande-1>
<commande-2>
```

**Validation :**

```bash
<commande-verification>
```

**Résultat attendu :** `<Output attendu>`

---

### Étape 3 — `<Titre de l'étape>`

> _Répéter le bloc ci-dessus pour chaque étape de la procédure._

---

## 4. Rollback / Rollback Procedure

> _Décrire la procédure de retour en arrière si l'intervention doit être annulée. Doit être exécutable **sans** l'auteur de la procédure._

### 4.1 Déclencheurs de rollback

Effectuer un rollback si l'une des conditions suivantes est observée :

- [ ] `<Condition 1 — ex: le service X ne répond plus après l'étape 2>`
- [ ] `<Condition 2 — ex: perte de connectivité sur le VLAN Y>`
- [ ] `<Condition 3>`

### 4.2 Procédure de rollback

**Durée estimée du rollback :** `<X minutes>`

```bash
# Étape R1 — Rétablir la configuration précédente
<commande-rollback-1>

# Étape R2 — Vérifier le retour à l'état initial
<commande-rollback-verification>
```

**Validation post-rollback :**

```bash
<commande-verification-etat-initial>
```

**Résultat attendu après rollback :** `<Décrire l'état attendu>`

---

## 5. Contrôles post-intervention / Post-Intervention Checks

> _Effectuer ces vérifications systématiquement à la fin de toute intervention, qu'elle soit nominale ou après rollback._

### 5.1 Liste de contrôle

| # | Contrôle | Commande | Résultat attendu | Statut |
|---|----------|----------|-----------------|--------|
| 1 | `<Service X actif>` | `<commande>` | `<Output attendu>` | `[ ] OK / [ ] KO` |
| 2 | `<Flux réseau Y fonctionnel>` | `<ping/curl/...>` | `<Réponse attendue>` | `[ ] OK / [ ] KO` |
| 3 | `<Log firewall sans erreur>` | `<commande>` | `<Aucune erreur critique>` | `[ ] OK / [ ] KO` |
| 4 | `<Supervision SNMP active>` | `<commande>` | `<Trap reçue>` | `[ ] OK / [ ] KO` |

### 5.2 Tests fonctionnels

```bash
# Test de connectivité de bout en bout
<commande-test-1>

# Test de la fonctionnalité principale
<commande-test-2>
```

### 5.3 Déclaration de fin d'intervention

> _Compléter après chaque intervention réelle._

| Champ | Valeur |
|-------|--------|
| Début d'intervention | `<YYYY-MM-DD HH:MM>` |
| Fin d'intervention | `<YYYY-MM-DD HH:MM>` |
| Opérateur | `<Nom Prénom>` |
| Résultat | `[Succès / Rollback / Échec]` |
| Observations | `<Commentaires libres>` |

---

## 6. Contacts escalade / Escalation Contacts

| Niveau | Rôle | Nom | Moyen de contact | Disponibilité |
|--------|------|-----|-----------------|---------------|
| N1 | Technicien réseau | `<Nom>` | `<Téléphone / Teams>` | `<Heures ouvrées>` |
| N2 | Ingénieur réseau senior | `<Nom>` | `<Téléphone / Teams>` | `<24/7 astreinte>` |
| N3 | Responsable infrastructure | `<Nom>` | `<Téléphone>` | `<Critique uniquement>` |
| Fournisseur | `<Constructeur / Opérateur>` | Support TAC | `<Numéro de contrat>` | `<24/7 selon contrat>` |

---

## 7. Historique des révisions / Revision History

| Version | Date | Auteur | Modifications |
|---------|------|--------|---------------|
| 1.0 | `<YYYY-MM-DD>` | `<Nom>` | Création initiale |
| `<X.X>` | `<YYYY-MM-DD>` | `<Nom>` | `<Description des changements>` |

---

*Document généré avec le template DEX v1.0 — network-portfolio*
