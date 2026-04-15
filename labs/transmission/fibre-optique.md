# Fibre Optique — Principes, OTDR et mesures
# Fiber Optics — Principles, OTDR and Measurements

> **Contexte :** Liaisons fibre optique inter-bâtiments en environnement industriel (CNPE EDF)

---

## 1. Types de fibres optiques

### 1.1 Fibre monomode (Single-Mode — SM)

| Norme ITU-T | Nom courant | Diamètre coeur | Usage |
|-------------|-------------|----------------|-------|
| **G.652** (A/B/C/D) | SM standard | 9 µm | Liaisons longue distance (LAN, métro, backbone) |
| **G.657** (A1/A2/B2/B3) | SM bend-insensitive | 9 µm | Installation intérieure, coudes serrés |
| G.654 | SM ultra-faible atténuation | 9 µm | Sous-marin, très longue distance |
| G.655 | SM dispersion-shifted (NZDSF) | 9 µm | DWDM longue distance |

> **G.652.D** est la fibre la plus répandue en contexte CNPE et réseau d'entreprise.
> **G.657.A2** est recommandée pour les passages dans les bâtiments (tolère des rayons de courbure de 7.5 mm).

**Caractéristiques G.652.D :**
- Atténuation : ≤ 0.35 dB/km à 1310 nm, ≤ 0.20 dB/km à 1550 nm
- Dispersion chromatique : ≤ 3.5 ps/(nm·km) à 1310 nm
- Longueurs d'onde de travail : 1310 nm et 1550 nm (CWDM/DWDM jusqu'à 1625 nm)

### 1.2 Fibre multimode (Multi-Mode — MM)

| Norme ISO/IEC 11801 | Diamètre coeur | Bande passante | Distance max (10GbE) |
|---------------------|----------------|----------------|---------------------|
| OM1 | 62.5 µm | 200 MHz·km | 33 m |
| OM2 | 50 µm | 500 MHz·km | 82 m |
| OM3 | 50 µm | 2000 MHz·km | 300 m |
| OM4 | 50 µm | 4700 MHz·km | 550 m |
| OM5 | 50 µm | 28000 MHz·km | 400 m (SWDM4) |

> En contexte CNPE : la fibre **monomode G.652.D** est utilisée pour les liaisons inter-bâtiments. La multimode OM3/OM4 est réservée aux salles serveurs et câblages horizontaux courts.

---

## 2. Connecteurs

| Connecteur | Type | Usage | Ferrule |
|------------|------|-------|---------|
| **LC** (Lucent Connector) | Petit form factor | SFP, SFP+, QSFP — équipements actifs | 1.25 mm |
| **SC** (Subscriber Connector) | Standard | Panneaux de brassage, boîtiers d'épissure | 2.5 mm |
| **MPO/MTP** | Multi-fibres (8/12/24 fibres) | Backbone haute densité, 40/100GbE | Ribbons |
| **FC** | Verrouillage vissé | Mesures OTDR, environnements vibratoires | 2.5 mm |
| **ST** | Baïonnette | Équipements anciens (legacy) | 2.5 mm |

**Polissage des ferrules :**

| Polissage | Réflectance | Usage |
|-----------|-------------|-------|
| PC (Physical Contact) | −30 à −40 dB | Multimode, réseaux classiques |
| UPC (Ultra PC) | −40 à −55 dB | Monomode standard |
| APC (Angled PC, 8°) | −60 à −70 dB | CATV, WDM, mesures de précision |

> **Règle :** Ne jamais connecter un UPC avec un APC — incompatibilité physique et forte perte d'insertion.

---

## 3. OTDR — Optical Time Domain Reflectometer

### 3.1 Principe de fonctionnement

L'OTDR envoie des impulsions lumineuses dans la fibre et mesure la lumière rétrodiffusée (rétrodiffusion Rayleigh) et réfléchie (réflexions de Fresnel aux connecteurs et épissures). Le temps de retour de l'écho permet de localiser les événements sur la fibre.

```
Principe de mesure :
  OTDR ──► impulsion lumineuse ──► Fibre optique ──►
                                          │
                  Rétrodiffusion Rayleigh ◄┘ (continue, pente = atténuation)
                  Réflexion Fresnel ◄─────── (pics aux connecteurs)
```

### 3.2 Paramètres de réglage OTDR

| Paramètre | Description | Réglage typique |
|-----------|-------------|-----------------|
| Longueur d'onde (λ) | 1310 nm (dommage, splice) / 1550 nm (atténuation) | Tester les deux |
| Largeur d'impulsion | Impulsion courte = résolution, longue = portée | 10-30 ns pour < 5 km |
| Plage de mesure | Distance maximale affichée | 2× longueur estimée |
| Index de réfraction (IOR) | Spécifique au type de fibre | G.652: 1.4682 à 1310nm |
| Moyenne | Nombre de mesures moyennées | 16-64 pour une bonne courbe |

### 3.3 Événements OTDR

| Type d'événement | Représentation | Cause |
|-----------------|----------------|-------|
| Épissure (fusion splice) | Petite marche vers le bas | Soudure de deux fibres |
| Connecteur | Pic de réflexion + perte | Connecteur SC/LC/FC |
| Courbure excessive | Perte sans réflexion | Rayon de courbure trop serré |
| Cassure / rupture | Forte perte ou fin abrupte | Fibre cassée |
| Fin de fibre | Réflexion finale forte | Extrémité clivée ou connecteur |

---

## 4. Exemple de rapport OTDR — Liaison 2 km entre deux bâtiments CNPE

### 4.1 Contexte

```
Bâtiment A (Salle électrique)  ──── Câble G.652.D 12 FO ────  Bâtiment B (Salle serveurs)
Boîte d'épissure 1 (BE-01)          ~100 m        ~1000 m       Boîte d'épissure 2 (BE-02)
     |                                               |
  Splice 1                                        Splice 2+3
```

### 4.2 Trace OTDR — Wavelength 1310 nm

```
Niveau (dB)
   0 ─┐
      │ ← Pic de lancement (connecteur départ SC/APC)
  0.25─┼────────────────────────────────────────────────────
      │         Pente continue = atténuation fibre G.652.D
      │         (0.35 dB/km à 1310nm → pente ~0.35 dB/km)
  0.30─┤ ← Splice 1 à ~95 m (dans BE-01) [perte 0.04 dB]
      │
  0.50─┤ ← Splice 2 à ~540 m (jonction câble) [perte 0.07 dB]
      │
  0.73─┤ ← Splice 3 à ~1000 m (mid-span) [perte 0.05 dB]
      │
  0.95─┤ ← Splice 4 à ~1450 m [perte 0.06 dB]
      │
  1.20─┤ ← Splice 5 à ~1900 m (dans BE-02) [perte 0.03 dB]
      │
  1.49─┼── Connecteur d'arrivée SC/APC à 2000 m [perte 0.28 dB]
      │                                          [réflexion -35 dB]
  1.55─┘ END OF FIBER
       0       0.5      1.0      1.5      2.0 km
```

### 4.3 Tableau des événements / Events Table (1310 nm)

| # | Distance (km) | Type d'événement | Perte insertion (dB) | Réflexion (dB) | Acceptable ? |
|---|---------------|-----------------|---------------------|---------------|-------------|
| 1 | 0.000 | Connecteur départ (SC/APC) | 0.25 | −35.0 | ✅ < 0.5 dB |
| 2 | 0.095 | Épissure fusion (BE-01) | 0.04 | — | ✅ < 0.1 dB |
| 3 | 0.543 | Épissure fusion (jonction câble) | 0.07 | — | ✅ < 0.1 dB |
| 4 | 0.998 | Épissure fusion (mi-parcours) | 0.05 | — | ✅ < 0.1 dB |
| 5 | 1.445 | Épissure fusion (jonction câble) | 0.06 | — | ✅ < 0.1 dB |
| 6 | 1.902 | Épissure fusion (BE-02) | 0.03 | — | ✅ < 0.1 dB |
| 7 | 2.000 | Connecteur arrivée (SC/APC) | 0.28 | −34.8 | ✅ < 0.5 dB |
| — | 2.000 | FIN DE FIBRE | — | — | — |

### 4.4 Bilan optique / Optical Budget Summary

| Composante | Calcul | Valeur |
|------------|--------|--------|
| Atténuation fibre (G.652.D, 1310 nm) | 2.0 km × 0.35 dB/km | 0.70 dB |
| Pertes épissures (5 × moy. 0.05 dB) | 5 × 0.05 | 0.25 dB |
| Perte connecteur départ | — | 0.25 dB |
| Perte connecteur arrivée | — | 0.28 dB |
| **Atténuation totale mesurée** | | **1.49 dB** |
| **Budget optique disponible** | (SFP 1310nm: −3 à −8 dBm Tx, −14 dBm Rx min) | ~11 dB |
| **Marge optique** | 11 − 1.49 | **9.5 dB** ✅ |

### 4.5 Mesures à 1550 nm (comparaison)

| Composante | Calcul | Valeur |
|------------|--------|--------|
| Atténuation fibre (G.652.D, 1550 nm) | 2.0 km × 0.20 dB/km | 0.40 dB |
| Pertes épissures | 5 × 0.04 | 0.20 dB |
| Perte connecteurs | 0.25 + 0.28 | 0.53 dB |
| **Total 1550 nm** | | **1.13 dB** |

---

## 5. Seuils d'acceptabilité / Acceptance Thresholds

### 5.1 Pertes d'insertion (IL — Insertion Loss)

| Élément | Seuil acceptable | Seuil alarme |
|---------|-----------------|--------------|
| Épissure fusion (fusion splice) | ≤ 0.10 dB | > 0.10 dB |
| Épissure mécanique | ≤ 0.30 dB | > 0.30 dB |
| Connecteur SC/LC UPC | ≤ 0.50 dB | > 0.50 dB |
| Connecteur SC/LC APC | ≤ 0.30 dB | > 0.30 dB |
| Connecteur MPO | ≤ 0.60 dB (12 fibres) | > 0.60 dB |
| Atténuation fibre G.652.D 1310nm | ≤ 0.40 dB/km | > 0.40 dB/km |
| Atténuation fibre G.652.D 1550nm | ≤ 0.25 dB/km | > 0.25 dB/km |

### 5.2 Pertes de retour (RL — Return Loss / Reflectance)

| Élément | Seuil acceptable |
|---------|-----------------|
| Connecteur UPC | ≥ 40 dB (réflectance ≤ −40 dB) |
| Connecteur APC | ≥ 60 dB (réflectance ≤ −60 dB) |
| Épissure fusion | Non réflective (< −55 dB) |

---

## 6. Splice vs Connecteur

| Critère | Épissure fusion (Fusion Splice) | Connecteur (Mechanical) |
|---------|--------------------------------|------------------------|
| **Perte typique** | 0.02 — 0.10 dB | 0.15 — 0.50 dB |
| **Réflexion** | Quasi-nulle (< −60 dB) | Modérée (−30 à −55 dB) |
| **Durabilité** | Permanente (> 30 ans) | Usure des ferrules (nettoyage régulier) |
| **Démontable** | ❌ Non — soudure permanente | ✅ Oui — brassage flexible |
| **Usage** | Infrastructures permanentes (backbone) | Panneaux de brassage, équipements actifs |
| **Outillage** | Soudeuse arc (5 000 — 30 000 €) | Outil de polissage ou connecteurs préfabriqués |
| **CNPE** | Câbles enterrés, boîtes d'épissures | Baies de brassage, salles techniques |

---

## 7. Budget optique / Optical Power Budget

```
Budget optique = Puissance Tx (dBm) − Sensibilité Rx (dBm) − Marge système (dB)

Exemple : SFP 1000BASE-LX (1310 nm, 10 km)
  Puissance Tx min : −3 dBm
  Sensibilité Rx   : −19 dBm
  Budget brut      : 16 dB
  Marge système    : 3 dB (vieillissement, température)
  Budget utilisable: 13 dB

  Budget consommé par le lien 2 km : 1.49 dB
  Marge restante : 13 − 1.49 = 11.5 dB ✅ (très confortable)
```

---

## 8. Normes de câblage / Cabling Standards

| Norme | Domaine |
|-------|---------|
| **TIA-568.3-D** | Câblage fibre optique — Amérique du Nord |
| **EN 50173-1** | Infrastructure de câblage générique — Europe |
| **IEC 14763-3** | Installation et tests des câblages fibre optique |
| **IEC 61300-3-35** | Tests de propreté des connecteurs optiques |
| **IEC 61754** | Normes des connecteurs optiques (SC, LC, MPO...) |
| **ITU-T G.652** | Caractéristiques des fibres monomode G.652 |
| **ITU-T G.657** | Fibres résistantes aux courbures |
