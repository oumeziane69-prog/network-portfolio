# Lab — BGP eBGP (pod01 ↔ pod02)

## FR — Description

Lab de routage BGP externe (eBGP) entre deux routeurs Cisco IOS-XE virtualisés.  
Objectif : établir une adjacence BGP inter-AS, annoncer un préfixe loopback et vérifier l'AS-path sur le pair distant.

### Topologie

```
  pod01                         pod02
  AS65001                       AS65002
  Lo0: 1.1.1.1/32               Lo0: 2.2.2.2/32
  Gi0/0: 10.10.20.102/30  ----  Gi0/0: 10.10.20.103/30
```

### Paramètres BGP

| Paramètre        | pod01           | pod02           |
|------------------|-----------------|-----------------|
| AS local         | 65001           | 65002           |
| Router-ID        | 1.1.1.1         | 2.2.2.2         |
| Loopback0        | 1.1.1.1/32      | 2.2.2.2/32      |
| IP peering       | 10.10.20.102    | 10.10.20.103    |
| Peer déclaré     | 10.10.20.103    | 10.10.20.102    |
| Remote-AS        | 65002           | 65001           |

### État attendu

- Adjacence eBGP : **Established**
- pod02 apprend **1.1.1.1/32** via `10.10.20.102` (next-hop)
- AS-path visible sur pod02 : `65001`

### Commandes de vérification

```bash
# Adjacence
show bgp summary

# Table BGP complète
show ip bgp

# Préfixe spécifique avec AS-path
show ip bgp 1.1.1.1/32

# Routes reçues du pair
show ip bgp neighbors 10.10.20.102 received-routes
```

### Sortie attendue sur pod02

```
pod02# show ip bgp
BGP table version is 3, local router ID is 2.2.2.2
Status codes: s suppressed, d damped, h history, * valid, > best, i internal
Origin codes: i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 1.1.1.1/32       10.10.20.102             0             0 65001 i
*> 2.2.2.2/32       0.0.0.0                  0         32768 i
```

---

## EN — Description

External BGP (eBGP) routing lab between two virtualised Cisco IOS-XE routers.  
Goal: bring up a BGP inter-AS adjacency, advertise a loopback prefix, and verify the AS-path on the remote peer.

### Topology

```
  pod01                         pod02
  AS65001                       AS65002
  Lo0: 1.1.1.1/32               Lo0: 2.2.2.2/32
  Gi0/0: 10.10.20.102/30  ----  Gi0/0: 10.10.20.103/30
```

### BGP Parameters

| Parameter        | pod01           | pod02           |
|------------------|-----------------|-----------------|
| Local AS         | 65001           | 65002           |
| Router-ID        | 1.1.1.1         | 2.2.2.2         |
| Loopback0        | 1.1.1.1/32      | 2.2.2.2/32      |
| Peering IP       | 10.10.20.102    | 10.10.20.103    |
| Declared peer    | 10.10.20.103    | 10.10.20.102    |
| Remote-AS        | 65002           | 65001           |

### Expected State

- eBGP adjacency: **Established**
- pod02 learns **1.1.1.1/32** via `10.10.20.102` (next-hop)
- AS-path visible on pod02: `65001`

### Verification Commands

```bash
# Adjacency
show bgp summary

# Full BGP table
show ip bgp

# Specific prefix with AS-path
show ip bgp 1.1.1.1/32

# Routes received from peer
show ip bgp neighbors 10.10.20.102 received-routes
```

### Expected Output on pod02

```
pod02# show ip bgp
BGP table version is 3, local router ID is 2.2.2.2
Status codes: s suppressed, d damped, h history, * valid, > best, i internal
Origin codes: i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 1.1.1.1/32       10.10.20.102             0             0 65001 i
*> 2.2.2.2/32       0.0.0.0                  0         32768 i
```
