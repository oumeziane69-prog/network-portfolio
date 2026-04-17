# Lab — BGP Attributes : Local-Preference & MED

## FR — Description

Lab de manipulation des attributs BGP via route-maps sur deux routeurs Cisco IOS-XE.  
Objectif : configurer un Local-Preference entrant sur pod01 et un MED sortant sur pod02, puis vérifier le résultat dans la table BGP.

### Topologie

```
  pod01                         pod02
  AS65001                       AS65002
  Lo0: 1.1.1.1/32               Lo0: 2.2.2.2/32
  Gi0/0: 10.10.20.102/30  ----  Gi0/0: 10.10.20.103/30
```

### Attributs configurés

| Attribut        | Valeur | Où configuré | Direction  | Route-map         |
|-----------------|--------|--------------|------------|-------------------|
| Local-Preference | 200   | pod01        | in (depuis pod02) | SET-LOCAL-PREF |
| MED             | 100    | pod02        | out (vers pod01)  | SET-MED        |

### Local-Preference (LOCAL-PREF)

- **Scope** : interne à l'AS, non propagé aux peers eBGP
- **Usage** : influencer le chemin de sortie de l'AS pour les routes apprises
- **Valeur par défaut** : 100 — une valeur **plus élevée** est préférée
- **Ici** : pod01 applique `local-preference 200` aux routes reçues de pod02 → préférence renforcée pour `2.2.2.2/32`

### MED (Multi-Exit Discriminator)

- **Scope** : propagé au peer eBGP direct, suggère le chemin d'entrée préféré dans l'AS local
- **Usage** : influencer le chemin d'entrée vers l'AS qui annonce le MED
- **Valeur par défaut** : 0 — une valeur **plus basse** est préférée
- **Ici** : pod02 envoie `metric 100` sur `2.2.2.2/32` vers pod01

### Résultat attendu sur pod01

```
pod01# show ip bgp
BGP table version is 4, local router ID is 1.1.1.1
Status codes: s suppressed, d damped, h history, * valid, > best, i internal
Origin codes: i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 1.1.1.1/32       0.0.0.0                  0         32768 i
*> 2.2.2.2/32       10.10.20.103           100    200      0 65002 i
```

- `Metric=100` → MED positionné par pod02 via `SET-MED`
- `LocPrf=200` → Local-Preference positionné par pod01 via `SET-LOCAL-PREF`

### Commandes de vérification

```bash
# Table BGP complète
show ip bgp

# Détail du préfixe avec tous les attributs
show ip bgp 2.2.2.2/32

# Route-maps appliquées
show route-map SET-LOCAL-PREF
show route-map SET-MED

# Vérification du peer BGP
show bgp summary
show ip bgp neighbors 10.10.20.103 received-routes
```

### Sortie détaillée attendue sur pod01

```
pod01# show ip bgp 2.2.2.2/32
BGP routing table entry for 2.2.2.2/32, version 3
Paths: (1 available, best #1, table default)
  Advertised to update-groups:
     1
  Refresh Epoch 1
  65002
    10.10.20.103 from 10.10.20.103 (2.2.2.2)
      Origin IGP, metric 100, localpref 200, valid, external, best
      rx pathid: 0, tx pathid: 0x0
```

---

## EN — Description

BGP attribute manipulation lab using route-maps on two Cisco IOS-XE routers.  
Goal: configure an inbound Local-Preference on pod01 and an outbound MED on pod02, then verify the result in the BGP table.

### Topology

```
  pod01                         pod02
  AS65001                       AS65002
  Lo0: 1.1.1.1/32               Lo0: 2.2.2.2/32
  Gi0/0: 10.10.20.102/30  ----  Gi0/0: 10.10.20.103/30
```

### Configured Attributes

| Attribute        | Value | Configured on | Direction        | Route-map         |
|------------------|-------|---------------|------------------|-------------------|
| Local-Preference | 200   | pod01         | in (from pod02)  | SET-LOCAL-PREF    |
| MED              | 100   | pod02         | out (to pod01)   | SET-MED           |

### Local-Preference (LOCAL-PREF)

- **Scope**: internal to the AS, not propagated to eBGP peers
- **Usage**: influence the AS exit path for learned routes
- **Default**: 100 — a **higher** value is preferred
- **Here**: pod01 applies `local-preference 200` to routes received from pod02 → stronger preference for `2.2.2.2/32`

### MED (Multi-Exit Discriminator)

- **Scope**: propagated to the direct eBGP peer, suggests the preferred entry path into the local AS
- **Usage**: influence the entry path into the AS that advertises the MED
- **Default**: 0 — a **lower** value is preferred
- **Here**: pod02 sends `metric 100` on `2.2.2.2/32` toward pod01

### Expected Result on pod01

```
pod01# show ip bgp
BGP table version is 4, local router ID is 1.1.1.1
Status codes: s suppressed, d damped, h history, * valid, > best, i internal
Origin codes: i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 1.1.1.1/32       0.0.0.0                  0         32768 i
*> 2.2.2.2/32       10.10.20.103           100    200      0 65002 i
```

- `Metric=100` → MED set by pod02 via `SET-MED`
- `LocPrf=200` → Local-Preference set by pod01 via `SET-LOCAL-PREF`

### Verification Commands

```bash
# Full BGP table
show ip bgp

# Prefix detail with all attributes
show ip bgp 2.2.2.2/32

# Applied route-maps
show route-map SET-LOCAL-PREF
show route-map SET-MED

# BGP peer check
show bgp summary
show ip bgp neighbors 10.10.20.103 received-routes
```

### Expected Detailed Output on pod01

```
pod01# show ip bgp 2.2.2.2/32
BGP routing table entry for 2.2.2.2/32, version 3
Paths: (1 available, best #1, table default)
  Advertised to update-groups:
     1
  Refresh Epoch 1
  65002
    10.10.20.103 from 10.10.20.103 (2.2.2.2)
      Origin IGP, metric 100, localpref 200, valid, external, best
      rx pathid: 0, tx pathid: 0x0
```
