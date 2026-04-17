# Lab — Redistribution OSPF → BGP (pod01 AS65001)

## FR — Description

Lab de redistribution de routes OSPF dans BGP sur un routeur Cisco IOS-XE.  
Objectif : apprendre sur pod02 (AS65002) un préfixe OSPF originaire de pod01, observé avec le code d'origine `?` (incomplete), caractéristique d'une redistribution.

### Topologie

```
  pod01                         pod02
  AS65001                       AS65002
  Lo0: 1.1.1.1/32               Lo0: 2.2.2.2/32
  Gi0/0: 10.10.20.102/30  ----  Gi0/0: 10.10.20.103/30
  |
  OSPF process 1
  réseau 10.10.20.0/24
  |
  redistribué dans BGP AS65001
```

### Paramètres

| Paramètre              | pod01                   | pod02              |
|------------------------|-------------------------|--------------------|
| AS BGP                 | 65001                   | 65002              |
| Router-ID              | 1.1.1.1                 | 2.2.2.2            |
| OSPF process           | 1                       | —                  |
| Réseau OSPF            | 10.10.20.0/24           | —                  |
| Redistribution         | OSPF → BGP              | —                  |
| Peering eBGP           | 10.10.20.102            | 10.10.20.103       |

### Comportement attendu

- **Route redistribuée** : `10.10.20.0/24` visible dans la table BGP de pod02
- **Next-hop** : `10.10.20.102`
- **AS-path** : `65001`
- **Origin code** : `?` (incomplete) — comportement normal pour une redistribution (route non native BGP)
- **Reset / re-établissement** : après `clear ip bgp * soft`, l'adjacence se rétablit et la route est ré-annoncée automatiquement

### Origin codes — rappel

| Code | Signification       | Cas d'usage                          |
|------|---------------------|--------------------------------------|
| `i`  | IGP                 | Route injectée via `network`         |
| `e`  | EGP                 | Protocole EGP historique (rare)      |
| `?`  | Incomplete          | Route redistribuée depuis IGP/static |

### Commandes de vérification

```bash
# Sur pod01 — vérifier la table OSPF
show ip ospf neighbor
show ip route ospf

# Sur pod01 — vérifier la redistribution dans BGP
show ip bgp
show ip bgp 10.10.20.0/24

# Sur pod02 — vérifier la route apprise
show ip bgp
show ip bgp 10.10.20.0/24
show ip bgp neighbors 10.10.20.102 received-routes

# Reset soft (sans couper l'adjacence)
clear ip bgp * soft
```

### Sortie attendue sur pod02

```
pod02# show ip bgp
BGP table version is 4, local router ID is 2.2.2.2
Status codes: s suppressed, d damped, h history, * valid, > best, i internal
Origin codes: i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 1.1.1.1/32       10.10.20.102             0             0 65001 i
*> 10.10.20.0/24    10.10.20.102             0             0 65001 ?
*> 2.2.2.2/32       0.0.0.0                  0         32768 i
```

Le `?` sur `10.10.20.0/24` confirme que la route a été redistribuée depuis OSPF dans BGP sur pod01.

---

## EN — Description

Route redistribution lab (OSPF → BGP) on a Cisco IOS-XE router.  
Goal: have pod02 (AS65002) learn an OSPF-originated prefix from pod01, displayed with origin code `?` (incomplete) — the expected marker for redistribution.

### Topology

```
  pod01                         pod02
  AS65001                       AS65002
  Lo0: 1.1.1.1/32               Lo0: 2.2.2.2/32
  Gi0/0: 10.10.20.102/30  ----  Gi0/0: 10.10.20.103/30
  |
  OSPF process 1
  network 10.10.20.0/24
  |
  redistributed into BGP AS65001
```

### Parameters

| Parameter              | pod01                   | pod02              |
|------------------------|-------------------------|--------------------|
| BGP AS                 | 65001                   | 65002              |
| Router-ID              | 1.1.1.1                 | 2.2.2.2            |
| OSPF process           | 1                       | —                  |
| OSPF network           | 10.10.20.0/24           | —                  |
| Redistribution         | OSPF → BGP              | —                  |
| eBGP peering           | 10.10.20.102            | 10.10.20.103       |

### Expected Behaviour

- **Redistributed route**: `10.10.20.0/24` visible in pod02's BGP table
- **Next-hop**: `10.10.20.102`
- **AS-path**: `65001`
- **Origin code**: `?` (incomplete) — normal for redistribution (not a native BGP route)
- **Reset / re-establishment**: after `clear ip bgp * soft`, the session recovers and the route is re-advertised automatically

### Origin Codes — Reference

| Code | Meaning             | Use case                             |
|------|---------------------|--------------------------------------|
| `i`  | IGP                 | Route injected via `network`         |
| `e`  | EGP                 | Legacy EGP protocol (rare)           |
| `?`  | Incomplete          | Redistributed from IGP/static        |

### Verification Commands

```bash
# On pod01 — check OSPF
show ip ospf neighbor
show ip route ospf

# On pod01 — check redistribution into BGP
show ip bgp
show ip bgp 10.10.20.0/24

# On pod02 — check learned route
show ip bgp
show ip bgp 10.10.20.0/24
show ip bgp neighbors 10.10.20.102 received-routes

# Soft reset (no session teardown)
clear ip bgp * soft
```

### Expected Output on pod02

```
pod02# show ip bgp
BGP table version is 4, local router ID is 2.2.2.2
Status codes: s suppressed, d damped, h history, * valid, > best, i internal
Origin codes: i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 1.1.1.1/32       10.10.20.102             0             0 65001 i
*> 10.10.20.0/24    10.10.20.102             0             0 65001 ?
*> 2.2.2.2/32       0.0.0.0                  0         32768 i
```

The `?` on `10.10.20.0/24` confirms the route was redistributed from OSPF into BGP on pod01.
