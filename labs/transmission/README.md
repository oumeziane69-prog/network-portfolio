# Labs — Transmission (Faisceau Hertzien & Fibre Optique)

## Objectif / Objective

**FR** — Comprendre et maîtriser les technologies de transmission utilisées pour les liaisons inter-sites dans des environnements industriels critiques. Ce lab couvre les deux grands médias de transmission : le **faisceau hertzien (FH)** pour les liaisons point-à-point sans fil, et la **fibre optique** pour les liaisons câblées haute performance. Le contexte principal est celui des **Centres Nucléaires de Production d'Électricité (CNPE) d'EDF**, où la fiabilité et la redondance des liaisons sont critiques.

**EN** — Understand and master the transmission technologies used for inter-site links in critical industrial environments. This lab covers the two main transmission media: **microwave radio (FH — faisceau hertzien)** for wireless point-to-point links, and **fiber optics** for high-performance wired links. The primary context is **EDF Nuclear Power Plants (CNPE)**, where link reliability and redundancy are critical.

---

## Contexte CNPE EDF / CNPE EDF Context

Les CNPE EDF disposent de plusieurs types de liaisons de transmission :

| Type de liaison | Usage typique | Redondance |
|-----------------|---------------|------------|
| Fibre optique multi-fibres | Backbone inter-bâtiments | Active/Active, boucle physique |
| Faisceau hertzien | Liaison de secours ou site isolé | 1+1 (protection de chemin) |
| Fibre optique longue distance | Liaison CNPE ↔ Dispatching EDF | DWDM, 1+1 |
| Cuivre / paire torsadée | Réseaux téléphonie / supervision hérités | — |

**Contraintes spécifiques CNPE :**
- **Disponibilité requise :** 99.999% (5 nines) pour les liaisons critique-sûreté
- **Environnement électromagnétique :** Interférences possibles depuis les équipements haute tension
- **Distances :** Quelques centaines de mètres à quelques kilomètres entre bâtiments
- **Températures :** Câbles et équipements dimensionnés pour -20°C à +70°C
- **Sécurité physique :** Toute infrastructure passive (chemins de câbles, boîtes d'épissures) en zone contrôlée

---

## Statut / Status

✅ Complété

---

## Technologies couvertes / Technologies Covered

| Technologie | Document |
|-------------|----------|
| Faisceau hertzien (FH) | [faisceau-hertzien.md](faisceau-hertzien.md) |
| Fibre optique (FO) | [fibre-optique.md](fibre-optique.md) |
| Procédures de recette | [verification.md](verification.md) |

---

## Liens avec d'autres labs / Related Labs

- [labs/routing/mpls-l3vpn/](../mpls-l3vpn/README.md) — Les liaisons FH/FO portent souvent un backbone MPLS
- [docs/flux-matrix-IT-OT.md](../../docs/flux-matrix-IT-OT.md) — Les liaisons inter-sites portent les flux IT/OT documentés dans la matrice
