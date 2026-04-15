# Verification — Procédures de recette Fibre Optique & Faisceau Hertzien
# Acceptance Test Procedures — Fiber Optics & Microwave Radio

> **Usage :** Procédures à suivre lors des recettes de liaisons neuves ou rénovées.
> Ces procédures permettent de constituer les documents remis au client ou au maître d'oeuvre.

---

## 1. Recette fibre optique / Fiber Optic Acceptance

### 1.1 Prérequis

| Prérequis | Vérification |
|-----------|-------------|
| Câble tiré et épissures terminées | Visual inspection — boîtes d'épissures fermées |
| Connecteurs posés et nettoyés | Inspection avec microscope + Alcool isopropylique 99% |
| Plan de câblage disponible | Numérotation des fibres, longueurs estimées |
| Appareils calibrés | OTDR avec certificat de calibration < 1 an |
| Fiche de recette vierge | Document à compléter pendant les mesures |

### 1.2 Matériel nécessaire

| Outil | Modèle type | Usage |
|-------|-------------|-------|
| OTDR | Viavi MTS-2000 / EXFO FTB-1-Pro | Mesure des événements et atténuation |
| Source optique | EXFO FLS-300 | Mesure de perte d'insertion bidirectionnelle |
| Puissance-mètre | EXFO FPM-302 | Mesure en liaison avec la source |
| Microscope de connecteur | EXFO FIP-425B | Inspection de la propreté des ferrules |
| Kit de nettoyage | Opticspro FCC | Nettoyage des connecteurs avant mesure |
| Cordons de référence | Certifiés < 0.2 dB chacun | Cordons de lancement/réception OTDR |

### 1.3 Procédure OTDR

**Étape 1 — Préparation**

1. Nettoyer tous les connecteurs du lien à mesurer (embout + ferrule)
2. Inspecter avec le microscope : aucune égratignure sur la zone de contact, aucune poussière
3. Connecter les cordons de lancement (launch cable, ~50-100 m) pour masquer la zone morte OTDR
4. Régler l'OTDR :
   - λ = 1310 nm (mesure 1) puis 1550 nm (mesure 2)
   - Plage = 2× longueur estimée (ex: 5 km pour lien de 2 km)
   - Impulsion = 10-30 ns pour liens < 5 km
   - IOR = 1.4682 (G.652.D à 1310 nm) / 1.4676 (à 1550 nm)
   - Moyenne = 64 passes minimum

**Étape 2 — Mesure OTDR bidirectionnelle**

> La mesure doit être effectuée dans les **deux sens** (A→B puis B→A). La perte d'une épissure est la moyenne des deux mesures directionnelles.

```
Mesure A→B :
  OTDR connecté en A → mesure vers B
  Enregistrer la trace, identifier tous les événements

Mesure B→A :
  OTDR connecté en B → mesure vers A
  Enregistrer la trace, identifier tous les événements
```

**Étape 3 — Mesure de perte d'insertion (Source/Puissance-mètre)**

```
Source optique (A) ──── Lien complet ──── Puissance-mètre (B)

1. Mesurer la puissance de référence (cordon direct source → puissance-mètre) → P_ref
2. Insérer le lien à mesurer → P_lien
3. Perte d'insertion = P_ref - P_lien (en dB)
4. Répéter dans l'autre sens (B→A)
5. Résultat final = moyenne des deux mesures bidirectionnelles
```

### 1.4 Seuils de recette fibre optique

| Mesure | Critère de réception | Action si hors seuil |
|--------|---------------------|---------------------|
| Atténuation totale du lien | ≤ Budget calculé − 3 dB de marge | Identifier et reprendre l'élément défaillant |
| Perte insertion par épissure | ≤ 0.10 dB (fusion) | Refaire l'épissure |
| Perte insertion connecteur | ≤ 0.50 dB (UPC) / ≤ 0.30 dB (APC) | Nettoyer ou remplacer le connecteur |
| Atténuation /km à 1310nm | ≤ 0.40 dB/km | Vérifier le type de fibre installé |
| Atténuation /km à 1550nm | ≤ 0.25 dB/km | Vérifier la fibre + courbures excessives |
| Longueur mesurée vs plan | ≤ 5% d'écart | Vérifier le plan et l'IOR |

### 1.5 Tableau de recette OTDR — Modèle / Acceptance Record Template

```
PROCÈS-VERBAL DE RECETTE FIBRE OPTIQUE
═══════════════════════════════════════════════════════════
Projet      : ___________________________
Site A      : ___________________________
Site B      : ___________________________
Date        : ___________________________
Technicien  : ___________________________
OTDR        : Marque ____________ S/N ____________
Calibration : Valide jusqu'au _______________

CÂBLE
Type        : G.652.D  /  G.657.A2  /  OM3  /  OM4  (entourer)
Référence   : ___________________________
Longueur déclarée : _______ m
Longueur OTDR     : _______ m  (écart : _____ %)

MESURES PAR FIBRE (tableau à répéter par fibre)
─────────────────────────────────────────────────────────────
Fibre N° : _____   Couleur : _______

  Sens A→B (1310 nm)
  Atténuation totale  : _____ dB   Limite : _____ dB  [ ]OK [ ]NOK
  Nb événements       : _____
  Perte max épissure  : _____ dB   Limite : 0.10 dB   [ ]OK [ ]NOK
  Perte connecteurs   : _____ dB   Limite : 0.50 dB   [ ]OK [ ]NOK

  Sens B→A (1310 nm)
  Atténuation totale  : _____ dB   Limite : _____ dB  [ ]OK [ ]NOK
  Perte max épissure  : _____ dB   Limite : 0.10 dB   [ ]OK [ ]NOK

  Sens A→B (1550 nm)
  Atténuation totale  : _____ dB   Limite : _____ dB  [ ]OK [ ]NOK
  Perte /km           : _____ dB   Limite : 0.25 dB   [ ]OK [ ]NOK

  Résultat final      : [ ]CONFORME  [ ]NON CONFORME
─────────────────────────────────────────────────────────────

CONCLUSION
[ ] Toutes les fibres conformes — LIEN ACCEPTÉ
[ ] Non-conformités relevées — ACTIONS CORRECTIVES REQUISES

Signature technicien : ___________________  Date : _________
Signature client/MOE : ___________________  Date : _________
═══════════════════════════════════════════════════════════
```

---

## 2. Recette faisceau hertzien / Microwave Radio Acceptance

### 2.1 Prérequis

| Prérequis | Vérification |
|-----------|-------------|
| Pylônes / mâts installés et certifiés | PV de levage et certificat structural |
| Autorisation ARCEP obtenue | Numéro de licence et fréquences autorisées |
| Alignement visuel antennes | Visible à l'oeil nu / binoculaires |
| Dégagement de Fresnel > 60% | Calcul de profil avec logiciel (Pathloss, EDX) |
| Câble coaxial ou fibre interne | Installation conforme, protection UV |
| Équipements alimentés | Alimentation et mise à la terre conformes |

### 2.2 Procédure d'alignement d'antennes

```
Étape 1 — Alignement grossier
  - Utiliser une boussole et un inclinomètre pour pointer grossièrement
  - Azimut calculé (ex: 245°) — marge ±5°
  - Tilt vertical calculé selon hauteur et distance

Étape 2 — Alignement fin avec signal
  - Connecter l'RSSI (Received Signal Strength Indicator) sur l'équipement
  - Depuis le site B : monitorer le RSL en continu
  - Depuis le site A : ajuster l'azimut par pas de 0.1°, puis l'élévation
  - Chercher le RSL maximum — noter la valeur pic
  - Serrer les vis de maintien des 2 antennes
  - Vérifier que le RSL ne chute pas après serrage

Étape 3 — Vérification de la polarisation
  - H/V (Horizontal/Vertical) — configurer les deux antennes identiquement
  - Ou XPIC (Cross-Polarization Interference Cancellation) pour doublement de capacité
```

### 2.3 Mesures à effectuer

| Mesure | Méthode | Seuil acceptable |
|--------|---------|-----------------|
| RSL (Received Signal Level) | Lecture sur interface de gestion | > RSL_calculé − 3 dB |
| Marge de liaison (Fade Margin) | RSL − Seuil Rx | ≥ 30 dB (disponibilité 99.999%) |
| BER (Bit Error Rate) | Interface de gestion | ≤ 10⁻⁶ en conditions normales |
| Débit mesuré | Test iPerf ou équipement dédié | ≥ 95% du débit nominal |
| XPD (Cross-Polar Discrimination) | Si XPIC activé | ≥ 40 dB |
| Latence aller-retour | Ping avec timestamp | ≤ 2 ms pour 10 km |
| Disponibilité sur 24h | Monitoring continu | Aucune coupure > 10 s |

### 2.4 Tableau de recette FH — Modèle / FH Acceptance Record Template

```
FICHE DE RECETTE FAISCEAU HERTZIEN
═══════════════════════════════════════════════════════════
Projet         : ___________________________
Liaison        : Site A : _______  ←──→  Site B : _______
Distance       : _______ km
Fréquence Tx/Rx: _______/_______  GHz
Polarisation   : H / V / XPIC (entourer)
Modulation     : _______________  (ex: 128-QAM)
Débit nominal  : _______ Mbps
Date recette   : ___________________________
Techniciens    : ___________________________ (Site A)
                 ___________________________ (Site B)

BILAN DE LIAISON CALCULÉ
EIRP              : _______ dBm
FSL               : _______ dB
RSL calculé       : _______ dBm
Seuil Rx          : _______ dBm
Marge calculée    : _______ dB   [ ]≥30 dB ✅  [ ]<30 dB ❌

MESURES TERRAIN (Site A ←──→ Site B)
─────────────────────────────────────────────────────────
  RSL mesuré (Site A→B)  : _______ dBm   [ ]OK [ ]NOK
  RSL mesuré (Site B→A)  : _______ dBm   [ ]OK [ ]NOK
  Marge réelle           : _______ dB    [ ]≥30 dB [ ]<30 dB
  BER en conditions normales: ________   [ ]≤10⁻⁶ [ ]>10⁻⁶
  Débit mesuré (iPerf)   : _______ Mbps  [ ]≥95% du nominal

TEST DE REDONDANCE 1+1
  Bascule Radio A → Radio B  : [ ]OK < 50ms  [ ]NOK
  Bascule Radio B → Radio A  : [ ]OK < 50ms  [ ]NOK
  RSL après bascule          : _______ dBm   [ ]Stable

SYNCHRONISATION
  Mode synchronisation       : IEEE 1588 / Sync-E / GPS (entourer)
  Alarme sync               : [ ]Aucune  [ ]En cours
  MTIE mesuré (si applicable): _______ ns   [ ]≤100 ns ✅

TEST DE DISPONIBILITÉ (24h monitoring)
  Durée de test              : 24h — de _______ à _______
  Coupures > 1s             : _______ (seuil : 0 pour 99.999%)
  Disponibilité calculée     : _______ %   [ ]≥99.999% ✅

DOCUMENTS REMIS
  [ ] Traces OTDR (si liaison mixte FH + FO)
  [ ] Rapport de bilan de liaison calculé
  [ ] Certificat d'alignement des antennes (angles azimut/tilt)
  [ ] Licence ARCEP
  [ ] Plan de configuration équipements (fréquences, modulation, codes)
  [ ] Rapport de monitoring 24h

CONCLUSION
[ ] Liaison conforme — FH ACCEPTÉ
[ ] Non-conformités relevées — ACTIONS CORRECTIVES REQUISES

Observations : ________________________________________________
_______________________________________________________________

Signature technicien A : _________________  Date : ___________
Signature technicien B : _________________  Date : ___________
Signature client/MOE   : _________________  Date : ___________
═══════════════════════════════════════════════════════════
```

---

## 3. Récapitulatif des documents à produire / Deliverables Summary

| Document | Fibre optique | Faisceau hertzien |
|----------|:-------------:|:-----------------:|
| PV de recette OTDR | ✅ Obligatoire | — |
| Traces OTDR exportées (.sor) | ✅ Obligatoire | — |
| Rapport de pertes d'insertion | ✅ Obligatoire | — |
| Fiche de recette FH | — | ✅ Obligatoire |
| Bilan de liaison calculé | — | ✅ Obligatoire |
| Rapport de monitoring 24h | — | ✅ Obligatoire |
| Licence ARCEP | — | ✅ Obligatoire |
| Plan de câblage / schéma | ✅ Recommandé | ✅ Recommandé |
| Photos de l'installation | ✅ Recommandé | ✅ Obligatoire (antennes) |
| Rapport de nettoyage connecteurs | ✅ Recommandé | — |
