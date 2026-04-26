# Lab BGP Filtering — Cisco Cat8k IOS-XE / BGP Filtering Lab — Cisco Cat8k IOS-XE

**Status: Completed ✅**

---

## FR — Description

Ce lab démontre les techniques de filtrage BGP sur un routeur Cisco Catalyst 8000V dans
le sandbox DevNet. Quatre mécanismes de filtrage sont illustrés : prefix-list, ACL AS-path,
route-map et communities BGP.

| Paramètre | Valeur |
|---|---|
| Plateforme | Cisco Cat8k IOS-XE 17.12.2 |
| Environnement | Cisco DevNet Sandbox |
| AS local | 65001 |
| AS pair | 65002 |
| Router-ID | 2.2.2.2 |

### Topologie

```
         AS 65001                      AS 65002
  ┌─────────────────────┐       ┌──────────────────┐
  │  Cat8k (2.2.2.2)    │       │  DevNet Peer     │
  │                     │       │  10.10.20.50     │
  │  Lo0  2.2.2.2/32    ├───────┤                  │
  │  Lo1  172.16.1.0/24 │eBGP   │                  │
  │  Lo2  192.168.20.0  │       │                  │
  │  Gi1  10.10.20.254  │       │                  │
  └─────────────────────┘       └──────────────────┘
```

### Préfixes annoncés dans BGP

| Réseau | Masque | Annoncé vers AS65002 |
|---|---|---|
| 2.2.2.2 | /32 | ✅ (via PL-OUT) |
| 172.16.1.0 | /24 | ✅ (via PL-OUT) |
| 192.168.20.0 | /24 | ❌ (bloqué par PL-OUT) |

### Techniques de filtrage

#### 1. Prefix-list `PL-OUT`

Filtre sortant : seuls `172.16.1.0/24` et `2.2.2.2/32` sont autorisés vers le pair.

```
ip prefix-list PL-OUT seq 10 permit 172.16.1.0/24
ip prefix-list PL-OUT seq 20 permit 2.2.2.2/32
ip prefix-list PL-OUT seq 30 deny 0.0.0.0/0 le 32
```

#### 2. ACL AS-path

| ACL | Regex | Usage |
|---|---|---|
| 1 | `^$` | Routes originées localement (AS65001) |
| 2 | `^65002$` | Routes reçues directement d'AS65002 |
| 3 | `_65003_` | Blocage du transit via AS65003 |

#### 3. Route-map `RM-OUT`

Appliqué en sortie vers le voisin 10.10.20.50 :
- Match `PL-OUT` → autorise les préfixes sélectionnés
- Set `local-preference 200`
- Set `community 65001:100`

#### 4. Route-map `RM-COMMUNITY`

Enrichissement des communities :
- Match `PL-OUT` → set `community 65001:200 additive`

### Vérification

```
show bgp ipv4 unicast summary
show bgp ipv4 unicast neighbors 10.10.20.50 advertised-routes
show bgp ipv4 unicast 172.16.1.0/24
show ip prefix-list PL-OUT
```

---

## EN — Description

This lab demonstrates BGP filtering techniques on a Cisco Catalyst 8000V router inside
the DevNet sandbox. Four filtering mechanisms are illustrated: prefix-list, AS-path ACL,
route-map, and BGP communities.

| Parameter | Value |
|---|---|
| Platform | Cisco Cat8k IOS-XE 17.12.2 |
| Environment | Cisco DevNet Sandbox |
| Local AS | 65001 |
| Peer AS | 65002 |
| Router-ID | 2.2.2.2 |

### Topology

```
         AS 65001                      AS 65002
  ┌─────────────────────┐       ┌──────────────────┐
  │  Cat8k (2.2.2.2)    │       │  DevNet Peer     │
  │                     │       │  10.10.20.50     │
  │  Lo0  2.2.2.2/32    ├───────┤                  │
  │  Lo1  172.16.1.0/24 │eBGP   │                  │
  │  Lo2  192.168.20.0  │       │                  │
  │  Gi1  10.10.20.254  │       │                  │
  └─────────────────────┘       └──────────────────┘
```

### Prefixes advertised into BGP

| Network | Mask | Advertised to AS65002 |
|---|---|---|
| 2.2.2.2 | /32 | ✅ (via PL-OUT) |
| 172.16.1.0 | /24 | ✅ (via PL-OUT) |
| 192.168.20.0 | /24 | ❌ (blocked by PL-OUT) |

### Filtering techniques

#### 1. Prefix-list `PL-OUT`

Outbound filter: only `172.16.1.0/24` and `2.2.2.2/32` are allowed toward the peer.

```
ip prefix-list PL-OUT seq 10 permit 172.16.1.0/24
ip prefix-list PL-OUT seq 20 permit 2.2.2.2/32
ip prefix-list PL-OUT seq 30 deny 0.0.0.0/0 le 32
```

#### 2. AS-path ACLs

| ACL | Regex | Usage |
|---|---|---|
| 1 | `^$` | Locally originated routes (AS65001) |
| 2 | `^65002$` | Routes received directly from AS65002 |
| 3 | `_65003_` | Block transit through AS65003 |

#### 3. Route-map `RM-OUT`

Applied outbound toward neighbor 10.10.20.50:
- Match `PL-OUT` → allow selected prefixes
- Set `local-preference 200`
- Set `community 65001:100`

#### 4. Route-map `RM-COMMUNITY`

Community enrichment:
- Match `PL-OUT` → set `community 65001:200 additive`

### Verification

```
show bgp ipv4 unicast summary
show bgp ipv4 unicast neighbors 10.10.20.50 advertised-routes
show bgp ipv4 unicast 172.16.1.0/24
show ip prefix-list PL-OUT
```

---

## Output example / Exemple de sortie

```
Cat8k# show bgp ipv4 unicast summary
BGP router identifier 2.2.2.2, local AS number 65001
BGP table version is 7, main routing table version 7
3 network entries using 744 bytes of memory

Neighbor        V    AS MsgRcvd MsgSent TblVer InQ OutQ Up/Down  State/PfxRcd
10.10.20.50     4 65002      12      14      7    0    0 00:08:21        2

Cat8k# show bgp ipv4 unicast neighbors 10.10.20.50 advertised-routes
   Network          Next Hop       Metric LocPrf Weight Path
*> 2.2.2.2/32       10.10.20.254        0    200  32768 i
*> 172.16.1.0/24    10.10.20.254        0    200  32768 i

Total number of prefixes 2
```
