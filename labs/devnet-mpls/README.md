# Lab — MPLS LDP (pod01 ↔ pod02)

## FR — Description

Lab MPLS avec distribution de labels via LDP (Label Distribution Protocol) entre deux routeurs Cisco IOS-XE.  
Objectif : activer MPLS LDP sur le lien de peering, vérifier la session LDP, et observer les bindings de labels pour les préfixes loopback.

### Topologie

```
  pod01                         pod02
  Lo0: 1.1.1.1/32               Lo0: 2.2.2.2/32
  Gi0/0: 10.10.20.102/30  ----  Gi0/0: 10.10.20.103/30
  LDP ID: 1.1.1.1:0             LDP ID: 2.2.2.2:0
```

### Paramètres LDP

| Paramètre              | pod01           | pod02           |
|------------------------|-----------------|-----------------|
| Router-ID / LDP ID     | 1.1.1.1:0       | 2.2.2.2:0       |
| Interface MPLS         | GigabitEthernet0/0 | GigabitEthernet0/0 |
| Transport address      | 1.1.1.1         | 2.2.2.2         |
| IGP sous-jacent        | OSPF process 1  | OSPF process 1  |

### État attendu de la session LDP

```
pod01# show mpls ldp neighbor
    Peer LDP Ident: 2.2.2.2:0; Local LDP Ident 1.1.1.1:0
        TCP connection: 2.2.2.2.646 - 1.1.1.1.12345
        State: Oper; Msgs sent/rcvd: 9/9; Downstream
        Up time: 00:01:09
        LDP discovery sources:
          GigabitEthernet0/0, Src IP addr: 10.10.20.103
        Addresses bound to peer LDP Ident:
          2.2.2.2        10.10.20.103
```

### Label bindings attendus

```
pod01# show mpls ldp bindings
  lib entry: 1.1.1.1/32, rev 2
        local binding:  label: imp-null
        remote binding: lsr: 2.2.2.2:0, label: 17
  lib entry: 2.2.2.2/32, rev 4
        local binding:  label: 17
        remote binding: lsr: 2.2.2.2:0, label: imp-null
  lib entry: 10.10.20.100/30, rev 6
        local binding:  label: imp-null
        remote binding: lsr: 2.2.2.2:0, label: imp-null

pod02# show mpls ldp bindings
  lib entry: 1.1.1.1/32, rev 2
        local binding:  label: 17
        remote binding: lsr: 1.1.1.1:0, label: imp-null
  lib entry: 2.2.2.2/32, rev 4
        local binding:  label: imp-null
        remote binding: lsr: 1.1.1.1:0, label: 17
  lib entry: 10.10.20.100/30, rev 6
        local binding:  label: imp-null
        remote binding: lsr: 1.1.1.1:0, label: imp-null
```

> **Note** : `imp-null` (label 3) = implicit-null, utilisé pour le préfixe local (PHP — Penultimate Hop Popping).  
> Le label `16` attribué à `2.2.2.2/32` peut varier selon la plateforme ; la valeur observée ici est `16`.

### Label 16 — binding de 2.2.2.2/32

Sur pod02, le préfixe `2.2.2.2/32` reçoit le label local `16` (premier label dynamique après les labels réservés 0–15) :

```
pod02# show mpls ldp bindings 2.2.2.2 32
  lib entry: 2.2.2.2/32, rev 4
        local binding:  label: 16
        remote binding: lsr: 1.1.1.1:0, label: 17
```

pod01 utilise le label `16` pour forwarder les paquets à destination de `2.2.2.2/32` vers pod02.

### Commandes de vérification

```bash
# Session LDP et état Oper
show mpls ldp neighbor
show mpls ldp neighbor detail

# Table de labels (LIB)
show mpls ldp bindings
show mpls ldp bindings 2.2.2.2 32

# Interfaces MPLS actives
show mpls interfaces

# Table de forwarding MPLS (LFIB)
show mpls forwarding-table

# OSPF sous-jacent
show ip ospf neighbor
show ip route ospf
```

---

## EN — Description

MPLS lab using LDP (Label Distribution Protocol) between two Cisco IOS-XE routers.  
Goal: enable MPLS LDP on the peering link, verify the LDP session, and observe label bindings for loopback prefixes.

### Topology

```
  pod01                         pod02
  Lo0: 1.1.1.1/32               Lo0: 2.2.2.2/32
  Gi0/0: 10.10.20.102/30  ----  Gi0/0: 10.10.20.103/30
  LDP ID: 1.1.1.1:0             LDP ID: 2.2.2.2:0
```

### LDP Parameters

| Parameter              | pod01           | pod02           |
|------------------------|-----------------|-----------------|
| Router-ID / LDP ID     | 1.1.1.1:0       | 2.2.2.2:0       |
| MPLS interface         | GigabitEthernet0/0 | GigabitEthernet0/0 |
| Transport address      | 1.1.1.1         | 2.2.2.2         |
| Underlying IGP         | OSPF process 1  | OSPF process 1  |

### Expected LDP Session State

```
pod01# show mpls ldp neighbor
    Peer LDP Ident: 2.2.2.2:0; Local LDP Ident 1.1.1.1:0
        TCP connection: 2.2.2.2.646 - 1.1.1.1.12345
        State: Oper; Msgs sent/rcvd: 9/9; Downstream
        Up time: 00:01:09
        LDP discovery sources:
          GigabitEthernet0/0, Src IP addr: 10.10.20.103
        Addresses bound to peer LDP Ident:
          2.2.2.2        10.10.20.103
```

### Expected Label Bindings

```
pod01# show mpls ldp bindings
  lib entry: 1.1.1.1/32, rev 2
        local binding:  label: imp-null
        remote binding: lsr: 2.2.2.2:0, label: 17
  lib entry: 2.2.2.2/32, rev 4
        local binding:  label: 17
        remote binding: lsr: 2.2.2.2:0, label: imp-null
  lib entry: 10.10.20.100/30, rev 6
        local binding:  label: imp-null
        remote binding: lsr: 2.2.2.2:0, label: imp-null

pod02# show mpls ldp bindings
  lib entry: 1.1.1.1/32, rev 2
        local binding:  label: 17
        remote binding: lsr: 1.1.1.1:0, label: imp-null
  lib entry: 2.2.2.2/32, rev 4
        local binding:  label: imp-null
        remote binding: lsr: 1.1.1.1:0, label: 17
  lib entry: 10.10.20.100/30, rev 6
        local binding:  label: imp-null
        remote binding: lsr: 1.1.1.1:0, label: imp-null
```

> **Note**: `imp-null` (label 3) = implicit-null, used for local prefixes (PHP — Penultimate Hop Popping).  
> The label `16` assigned to `2.2.2.2/32` may vary by platform; the observed value here is `16`.

### Label 16 — binding for 2.2.2.2/32

On pod02, prefix `2.2.2.2/32` receives local label `16` (first dynamic label after reserved labels 0–15):

```
pod02# show mpls ldp bindings 2.2.2.2 32
  lib entry: 2.2.2.2/32, rev 4
        local binding:  label: 16
        remote binding: lsr: 1.1.1.1:0, label: 17
```

pod01 uses label `16` to forward packets destined to `2.2.2.2/32` toward pod02.

### Verification Commands

```bash
# LDP session and Oper state
show mpls ldp neighbor
show mpls ldp neighbor detail

# Label Information Base (LIB)
show mpls ldp bindings
show mpls ldp bindings 2.2.2.2 32

# MPLS-enabled interfaces
show mpls interfaces

# MPLS Forwarding Table (LFIB)
show mpls forwarding-table

# Underlying OSPF
show ip ospf neighbor
show ip route ospf
```
