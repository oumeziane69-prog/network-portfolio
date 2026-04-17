# Lab — BGP Filtering : prefix-list entrant sur pod01

## FR — Description

Lab de filtrage BGP par prefix-list sur un routeur Cisco IOS-XE.  
Objectif : bloquer l'annonce `10.10.20.0/24` reçue de pod02 sur pod01, en appliquant une prefix-list en entrée, tout en laissant passer les autres préfixes.

### Topologie

```
  pod01                         pod02
  AS65001                       AS65002
  Lo0: 1.1.1.1/32               Lo0: 2.2.2.2/32
  Gi0/0: 10.10.20.102/30  ----  Gi0/0: 10.10.20.103/30
```

### Prefix-list FILTER-IN

```
ip prefix-list FILTER-IN seq 5  deny   10.10.20.0/24
ip prefix-list FILTER-IN seq 10 permit 0.0.0.0/0 le 32
```

| Séquence | Action  | Préfixe          | Effet                               |
|----------|---------|------------------|-------------------------------------|
| 5        | deny    | 10.10.20.0/24    | Bloque exactement ce préfixe        |
| 10       | permit  | 0.0.0.0/0 le 32  | Autorise tous les autres préfixes   |

> **Important** : une prefix-list a un `deny any` implicite en fin de liste.  
> La séquence 10 (`permit 0.0.0.0/0 le 32`) est indispensable pour ne pas bloquer tous les préfixes restants.

### Application sur le neighbor

```
neighbor 10.10.20.103 prefix-list FILTER-IN in
```

La prefix-list est appliquée **en entrée** sur pod01, côté peer pod02.  
Pod02 continue d'annoncer `10.10.20.0/24`, mais pod01 la rejette à la réception.

### Résultat attendu sur pod01

**Avant filtrage** (sans prefix-list) :
```
pod01# show ip bgp
   Network          Next Hop            Metric LocPrf Weight Path
*> 1.1.1.1/32       0.0.0.0                  0         32768 i
*> 2.2.2.2/32       10.10.20.103             0             0 65002 i
*> 10.10.20.0/24    10.10.20.103             0             0 65002 ?
```

**Après filtrage** (avec FILTER-IN appliquée) :
```
pod01# show ip bgp
   Network          Next Hop            Metric LocPrf Weight Path
*> 1.1.1.1/32       0.0.0.0                  0         32768 i
*> 2.2.2.2/32       10.10.20.103             0             0 65002 i
```

`10.10.20.0/24` a disparu de la table BGP de pod01 — filtrée en entrée.

### Commandes de vérification

```bash
# Table BGP — vérifier l'absence de 10.10.20.0/24
show ip bgp

# Routes reçues avant filtrage (soft-reconfig requis)
show ip bgp neighbors 10.10.20.103 received-routes

# Routes acceptées après filtrage
show ip bgp neighbors 10.10.20.103 routes

# Vérifier la prefix-list
show ip prefix-list FILTER-IN

# Vérifier l'application sur le neighbor
show ip bgp neighbors 10.10.20.103 | include prefix-list

# Appliquer le filtrage sans reset de session
clear ip bgp 10.10.20.103 soft in
```

---

## EN — Description

BGP filtering lab using a prefix-list on a Cisco IOS-XE router.  
Goal: block the `10.10.20.0/24` advertisement received from pod02 on pod01 by applying an inbound prefix-list, while allowing all other prefixes through.

### Topology

```
  pod01                         pod02
  AS65001                       AS65002
  Lo0: 1.1.1.1/32               Lo0: 2.2.2.2/32
  Gi0/0: 10.10.20.102/30  ----  Gi0/0: 10.10.20.103/30
```

### Prefix-list FILTER-IN

```
ip prefix-list FILTER-IN seq 5  deny   10.10.20.0/24
ip prefix-list FILTER-IN seq 10 permit 0.0.0.0/0 le 32
```

| Sequence | Action  | Prefix           | Effect                              |
|----------|---------|------------------|-------------------------------------|
| 5        | deny    | 10.10.20.0/24    | Blocks this exact prefix            |
| 10       | permit  | 0.0.0.0/0 le 32  | Allows all other prefixes           |

> **Important**: a prefix-list has an implicit `deny any` at the end.  
> Sequence 10 (`permit 0.0.0.0/0 le 32`) is required to avoid blocking all remaining prefixes.

### Applied to Neighbor

```
neighbor 10.10.20.103 prefix-list FILTER-IN in
```

The prefix-list is applied **inbound** on pod01, toward peer pod02.  
Pod02 still advertises `10.10.20.0/24`, but pod01 rejects it upon receipt.

### Expected Result on pod01

**Before filtering** (no prefix-list):
```
pod01# show ip bgp
   Network          Next Hop            Metric LocPrf Weight Path
*> 1.1.1.1/32       0.0.0.0                  0         32768 i
*> 2.2.2.2/32       10.10.20.103             0             0 65002 i
*> 10.10.20.0/24    10.10.20.103             0             0 65002 ?
```

**After filtering** (FILTER-IN applied):
```
pod01# show ip bgp
   Network          Next Hop            Metric LocPrf Weight Path
*> 1.1.1.1/32       0.0.0.0                  0         32768 i
*> 2.2.2.2/32       10.10.20.103             0             0 65002 i
```

`10.10.20.0/24` is gone from pod01's BGP table — filtered inbound.

### Verification Commands

```bash
# BGP table — confirm 10.10.20.0/24 is absent
show ip bgp

# Routes received before filtering (requires soft-reconfig)
show ip bgp neighbors 10.10.20.103 received-routes

# Routes accepted after filtering
show ip bgp neighbors 10.10.20.103 routes

# Check the prefix-list
show ip prefix-list FILTER-IN

# Check prefix-list applied to neighbor
show ip bgp neighbors 10.10.20.103 | include prefix-list

# Apply filtering without resetting the session
clear ip bgp 10.10.20.103 soft in
```
