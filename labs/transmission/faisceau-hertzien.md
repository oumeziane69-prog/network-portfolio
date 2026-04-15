# Faisceau Hertzien (FH) — Principes techniques et bilan de liaison
# Microwave Radio — Technical Principles and Link Budget

> **Contexte :** Liaisons FH inter-sites pour réseaux industriels critiques (CNPE EDF, sites isolés)

---

## 1. Principes techniques du faisceau hertzien

### 1.1 Définition

Le **faisceau hertzien (FH)** est une liaison radio point-à-point utilisant des fréquences micro-ondes (typiquement 6 à 42 GHz) pour établir une connexion sans fil entre deux sites. Il est utilisé comme alternative ou complément à la fibre optique, notamment pour des sites difficiles d'accès, des traversées de routes ou de voies ferrées, ou comme liaison de secours.

### 1.2 Bandes de fréquences utilisées

| Bande | Fréquence | Distance typique | Débit typique | Conditions atmosphériques |
|-------|-----------|-----------------|---------------|--------------------------|
| 7 GHz | 7.1 — 7.9 GHz | 15 — 50 km | 155 Mbps — 1 Gbps | Résistant à la pluie |
| 13 GHz | 12.75 — 13.25 GHz | 8 — 25 km | 155 Mbps — 1 Gbps | Bon compromis |
| 18 GHz | 17.7 — 19.7 GHz | 4 — 15 km | 300 Mbps — 1 Gbps | Atténuation pluie modérée |
| 23 GHz | 21.2 — 23.6 GHz | 2 — 10 km | 300 Mbps — 1 Gbps | Sensible à la pluie |
| 38 GHz | 37 — 39.5 GHz | 1 — 5 km | 1 Gbps+ | Très sensible à la pluie |
| E-band | 71 — 86 GHz | 0.5 — 3 km | 10 Gbps+ | Très court, usage urbain |

> **CNPE EDF :** Les bandes **13 GHz et 18 GHz** sont typiquement utilisées pour les liaisons inter-bâtiments. La bande 7 GHz est préférée pour les liaisons longue distance vers le dispatching.

### 1.3 Modulations utilisées

| Modulation | Efficacité spectrale | Sensibilité | Usage |
|------------|---------------------|-------------|-------|
| QPSK | Faible | Très bonne | Longues distances, conditions dégradées |
| 16-QAM | Bonne | Bonne | Compromis distance/débit |
| 64-QAM | Très bonne | Correcte | Distances moyennes |
| 128-QAM | Excellente | Correcte | Courtes distances, bon signal |
| 256-QAM | Maximale | Faible | Très courtes distances, conditions optimales |
| 1024-QAM | Ultra-haute | Très faible | Usage spécialisé, < 2 km |

> Les équipements modernes utilisent la **modulation adaptative (ACM — Adaptive Coding and Modulation)** : la modulation s'adapte en temps réel aux conditions de propagation. Par temps clair = 1024-QAM, pluie intense = QPSK.

---

## 2. Calcul de bilan de liaison / Link Budget Calculation

Le bilan de liaison détermine si la puissance reçue est suffisante pour maintenir la liaison avec la marge souhaitée.

### 2.1 Formule générale

```
Received Signal Level (RSL) = EIRP − FSL + Rx Antenna Gain − Rx Cable Losses

Où :
  EIRP = Tx Power (dBm) + Tx Antenna Gain (dBi) − Tx Cable/Connector Losses (dB)
  FSL  = Free Space Loss (dB) = 92.4 + 20×log10(f_GHz) + 20×log10(d_km)

Link Margin (FM) = RSL − Rx Threshold (dBm)
```

### 2.2 Exemple calculé — Liaison 18 GHz, 8 km (typique CNPE)

**Paramètres d'entrée :**

| Paramètre | Valeur |
|-----------|--------|
| Fréquence | 18 GHz |
| Distance | 8 km |
| Puissance Tx | +15 dBm |
| Gain antenne Tx | 39 dBi (antenne 0.6m) |
| Pertes câbles/connecteurs Tx | 1.5 dB |
| Gain antenne Rx | 39 dBi (antenne 0.6m) |
| Pertes câbles/connecteurs Rx | 1.5 dB |
| Seuil Rx (BER 10⁻⁶, 128-QAM) | −82 dBm |
| Marge minimale requise | 30 dB (cible 99.999% dispo) |

**Calcul pas à pas :**

```
1. EIRP (Equivalent Isotropically Radiated Power)
   EIRP = Tx Power + Tx Antenna Gain − Tx Cable Losses
   EIRP = 15 + 39 − 1.5 = 52.5 dBm

2. Free Space Loss (affaiblissement en espace libre)
   FSL = 92.4 + 20×log10(18) + 20×log10(8)
   FSL = 92.4 + 20×1.255 + 20×0.903
   FSL = 92.4 + 25.1 + 18.1 = 135.6 dB

3. Received Signal Level (RSL)
   RSL = EIRP − FSL + Rx Antenna Gain − Rx Cable Losses
   RSL = 52.5 − 135.6 + 39 − 1.5
   RSL = −45.6 dBm

4. Fade Margin (marge de liaison)
   FM = RSL − Rx Threshold
   FM = −45.6 − (−82) = 36.4 dB

5. Conclusion
   FM = 36.4 dB ≥ 30 dB (requis) → LIAISON VALIDE ✓
```

**Résumé du bilan :**

| Paramètre | Valeur |
|-----------|--------|
| EIRP | +52.5 dBm |
| Affaiblissement espace libre (FSL) | −135.6 dB |
| Niveau reçu (RSL) | −45.6 dBm |
| Seuil Rx (128-QAM) | −82.0 dBm |
| **Marge de liaison (FM)** | **+36.4 dB** |
| Marge requise | +30.0 dB |
| **Statut** | **✅ Liaison valide** |

### 2.3 Atténuation par la pluie (Rain Attenuation)

En bandes > 10 GHz, la pluie introduit une atténuation supplémentaire à prendre en compte pour les liaisons longues.

| Bande | Intensité pluie 20 mm/h | Intensité pluie 50 mm/h | Impact sur 8 km |
|-------|------------------------|------------------------|-----------------|
| 13 GHz | ~1 dB/km | ~3 dB/km | 8 — 24 dB |
| 18 GHz | ~2 dB/km | ~5 dB/km | 16 — 40 dB |
| 23 GHz | ~3.5 dB/km | ~8 dB/km | 28 — 64 dB |

> Pour 18 GHz sur 8 km avec pluie intense (50 mm/h) : ~40 dB d'atténuation supplémentaire.
> La marge de 36.4 dB **ne couvre pas** les conditions extrêmes → réduire la distance ou passer en bande 7/13 GHz.

---

## 3. Redondance 1+1

### 3.1 Principe

La redondance **1+1** utilise deux émetteurs/récepteurs sur la même antenne ou sur deux antennes séparées :

| Mode | Description | Commutation |
|------|-------------|-------------|
| **Hot Standby** | Les deux radios transmettent, une est active, l'autre en veille chaude | < 50 ms |
| **Space Diversity** | Deux antennes à hauteurs différentes — réduit les évanouissements par réflexion | Continue / combinaison |
| **Frequency Diversity** | Deux fréquences légèrement différentes — réduit les évanouissements sélectifs | Continue / sélection |

**Avantage 1+1 :** Si l'équipement actif tombe en panne ou si les conditions se dégradent, la bascule vers le chemin de secours est automatique et quasi-instantanée.

### 3.2 Schéma 1+1

```
  Site A                              Site B
┌──────────────┐                   ┌──────────────┐
│  Antenne     │                   │  Antenne     │
│  (coupleur)  │                   │  (coupleur)  │
│  [Radio A1] ─┤─── Faisceau 1 ────┤─ [Radio B1] │  ← Actif
│  [Radio A2] ─┤─── Faisceau 2 ────┤─ [Radio B2] │  ← Veille (1+1 hot standby)
│              │                   │              │
│  [Switch FH] │                   │  [Switch FH] │
│  (couche 2)  │                   │  (couche 2)  │
└──────────────┘                   └──────────────┘
        │                                  │
  Réseau site A                      Réseau site B
```

---

## 4. Synchronisation

| Méthode | Description | Précision |
|---------|-------------|-----------|
| **IEEE 1588v2 (PTP)** | Protocole de temps précis sur réseau IP — synchronisation fréquence et phase | < 100 ns |
| **Sync-E (ITU-T G.8262)** | Synchronisation fréquence via couche physique Ethernet | < 1 µs |
| **GPS intégré** | Récepteur GPS dans l'équipement FH — référence absolue | < 100 ns |
| **NTP/SNTP** | Synchronisation logicielle via IP — pour les équipements non-critiques | ~1 ms |

> Pour les CNPE EDF : **IEEE 1588v2 + Sync-E** sont typiquement utilisés pour les équipements nécessitant une synchronisation fine (protection différentielle, automatismes).

---

## 5. Intégration dans un réseau MPLS

Le faisceau hertzien transporte les mêmes protocoles que la fibre. En contexte CNPE :

```
  Site A                    FH (18 GHz)                  Site B
[PE1 MPLS] ──────────── [Radio A] ─────── [Radio B] ──────────── [PE2 MPLS]
                         (L2 transparent)
                         Ethernet GigE
                         VLAN 802.1Q
                         ou MPLS directement sur GigE
```

| Paramètre | Valeur typique |
|-----------|----------------|
| Interface côté routeur | GigabitEthernet (1GbE) ou 10GbE |
| Encapsulation | Ethernet — transparent au MPLS |
| MTU | 1500 à 9000 octets (jumbo frames si supporté) |
| QoS | DSCP preservé — le FH peut appliquer QoS sur les priorités Ethernet (CoS 802.1p) |
| Latence ajoutée | < 1 ms (typiquement 200-500 µs pour 8 km) |

---

## 6. Avantages / Inconvénients vs Fibre optique

| Critère | Faisceau Hertzien (FH) | Fibre Optique |
|---------|----------------------|---------------|
| **Déploiement** | ✅ Rapide (quelques jours) | ❌ Long (travaux génie civil) |
| **Coût initial** | ✅ Faible — pas de tranchées | ❌ Élevé — génie civil, tirage |
| **Débit** | ❌ Limité (1-10 Gbps max) | ✅ Illimité (100 Gbps+ par fibre) |
| **Disponibilité** | ⚠️ Dépend conditions météo (pluie, brouillard) | ✅ Très haute — insensible aux intempéries |
| **Sécurité physique** | ⚠️ Signal interceptable (chiffrement nécessaire) | ✅ Difficile à intercepter sans détection |
| **Maintenance** | ✅ Pas de câble enterré — alignement antenne | ❌ Risque de coupure physique |
| **Dégradation** | ⚠️ Évanouissements, pluie, obstacles | ✅ Stable dans le temps |
| **Sites isolés** | ✅ Idéal (sans infrastructure civile) | ❌ Non applicable sans tranchée |
| **Longueur typique** | 2 — 50 km (selon bande) | Illimitée (régénérateurs si > 80 km) |
| **Usage CNPE** | Liaisons de secours, sites isolés | Backbone principal inter-bâtiments |

---

## 7. Normes et réglementation

| Norme / Règlement | Domaine |
|-------------------|---------|
| ETSI EN 302 217 | Caractéristiques des systèmes FH en bandes fixes |
| UIT-R F.382 | Caractéristiques des systèmes fixes par micro-ondes |
| ARCEP (France) | Attribution des fréquences FH — licence obligatoire par liaison |
| UIT-R P.530 | Propagation des ondes radio dans les liaisons terrestres |
