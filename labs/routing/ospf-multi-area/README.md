# Lab — OSPF Multi-Area (Cat8000 — NBMA Non-Broadcast)

## Objectif / Objective

**FR** — Configurer et valider un réseau OSPF multi-aire sur deux routeurs Cisco Catalyst 8000 (IOS-XE). Le lab couvre la segmentation en trois aires (Area 0 backbone, Area 1, Area 2), le rôle ABR, l'élection DR/BDR, et le type de réseau NBMA non-broadcast requis lorsque le multicast n'est pas supporté sur le pont virtuel de simulation.

**EN** — Configure and validate a multi-area OSPF network on two Cisco Catalyst 8000 routers (IOS-XE). The lab covers three-area segmentation (Area 0 backbone, Area 1, Area 2), ABR role, DR/BDR election, and NBMA non-broadcast network type required when multicast is unsupported on the virtual bridge in the simulation environment.

---

## Topologie / Topology

```
  Area 1                      Area 0 (Backbone — Gi1)                   Area 2
+──────────────+    +──────────────────────────────────────+    +──────────────+
|  R1 — Lo1   |    |  R1 (Cat8000)        R2 (Cat8000)    |    |  R2 — Lo1   |
|  10.1.0.1/24|────|  Gi1: 10.0.12.1      Gi1: 10.0.12.2  |────|  10.2.0.1/24|
|  Lo0: 1.1.1.1    |  router-id: 1.1.1.1  router-id: 2.2.2.2   |  Lo0: 2.2.2.2
+──────────────+    |  Role: BDR (pri 50)  Role: DR (pri 100)|   +──────────────+
                    |    NBMA non-broadcast — neighbor unicast   |
                    +──────────────────────────────────────+
```

**Équipements / Devices:** 2 × Cisco Catalyst 8000 (IOS-XE) — simulation sur pont virtuel

---

## Adressage / Addressing

| Interface         | Router | Adresse IP       | Area   |
|------------------|--------|-----------------|--------|
| Loopback0         | R1     | 1.1.1.1/32      | Area 0 |
| Loopback0         | R2     | 2.2.2.2/32      | Area 0 |
| GigabitEthernet1  | R1     | 10.0.12.1/24    | Area 0 |
| GigabitEthernet1  | R2     | 10.0.12.2/24    | Area 0 |
| Loopback1         | R1     | 10.1.0.1/24     | Area 1 |
| Loopback1         | R2     | 10.2.0.1/24     | Area 2 |

---

## Configuration

### R1 — router-id 1.1.1.1 (BDR)

```ios
interface Loopback0
 ip address 1.1.1.1 255.255.255.255
!
interface Loopback1
 ip address 10.1.0.1 255.255.255.0
!
interface GigabitEthernet1
 ip address 10.0.12.1 255.255.255.0
 ip ospf network non-broadcast
 ip ospf priority 50
!
router ospf 1
 router-id 1.1.1.1
 network 1.1.1.1 0.0.0.0 area 0
 network 10.0.12.0 0.0.0.255 area 0
 network 10.1.0.0 0.0.0.255 area 1
 neighbor 10.0.12.2
```

### R2 — router-id 2.2.2.2 (DR)

```ios
interface Loopback0
 ip address 2.2.2.2 255.255.255.255
!
interface Loopback1
 ip address 10.2.0.1 255.255.255.0
!
interface GigabitEthernet1
 ip address 10.0.12.2 255.255.255.0
 ip ospf network non-broadcast
 ip ospf priority 100
!
router ospf 1
 router-id 2.2.2.2
 network 2.2.2.2 0.0.0.0 area 0
 network 10.0.12.0 0.0.0.255 area 0
 network 10.2.0.0 0.0.0.255 area 2
 neighbor 10.0.12.1
```

---

## Problème résolu / Key Fix

**FR** — Sur un pont virtuel (environnement de simulation), le multicast OSPF (224.0.0.5 / 224.0.0.6) n'est pas acheminé. Les voisins OSPF ne s'établissent pas avec le type de réseau broadcast par défaut. Solution : `ip ospf network non-broadcast` sur GigabitEthernet1 et déclaration explicite des voisins en unicast avec la commande `neighbor`.

**EN** — On a virtual bridge (simulation environment), OSPF multicast (224.0.0.5 / 224.0.0.6) is not forwarded. OSPF neighbors fail to establish with the default broadcast network type. Fix: set `ip ospf network non-broadcast` on GigabitEthernet1 and declare explicit unicast neighbors with the `neighbor` command under `router ospf`.

| Symptôme / Symptom | Cause | Solution |
|---|---|---|
| Voisins bloqués en INIT/EXSTART | Multicast non acheminé sur pont virtuel | `ip ospf network non-broadcast` |
| Pas d'adjacence OSPF | Pas de repli unicast par défaut | `neighbor <peer-ip>` sous `router ospf` |

---

## Vérification / Verification

### Table de routage OSPF — R1 / OSPF Routing Table — R1

```
R1# show ip route ospf

      2.0.0.0/32 is subnetted, 1 subnets
O        2.2.2.2 [110/2] via 10.0.12.2, GigabitEthernet1
      10.0.0.0/8 is variably subnetted
O IA     10.2.0.1/32 [110/2] via 10.0.12.2, GigabitEthernet1
```

- `O 2.2.2.2` — route intra-area (Area 0) vers Loopback0 de R2
- `O IA 10.2.0.1/32` — route inter-area (Area 2 → Area 0) vers Loopback1 de R2

### Voisins OSPF / OSPF Neighbors

```
R1# show ip ospf neighbor

Neighbor ID     Pri   State           Dead Time   Address         Interface
2.2.2.2          100   FULL/DR         00:01:58    10.0.12.2       GigabitEthernet1
```

### Statut DR/BDR / DR/BDR Status

```
R1# show ip ospf interface GigabitEthernet1

GigabitEthernet1 is up, line protocol is up
  Internet Address 10.0.12.1/24, Area 0
  Network Type NON_BROADCAST, Cost: 1
  ...
  DR is 10.0.12.2, BDR is 10.0.12.1
```

---

## Statut / Status

✅ Terminé — Lab fonctionnel et validé

---

## Technologies utilisées / Technologies Used

| Technologie | Rôle |
|-------------|------|
| Cisco Catalyst 8000 (IOS-XE) | Plateforme de routage principale |
| OSPFv2 — Multi-Area | Protocole IGP link-state |
| NBMA Non-Broadcast | Type réseau adapté (pont virtuel sans multicast) |
| DR/BDR Election | Réduction des adjacences sur réseau multi-accès |
| ABR (Area Border Router) | R1 et R2 relient Area 0 à leurs aires respectives |

---

## Concepts couverts / Concepts Covered

- Architecture OSPF multi-aire : Area 0 backbone, Area 1, Area 2
- Rôle ABR : génération des LSA Type 3 (Summary LSA) entre aires
- Élection DR/BDR : priorité OSPF et tie-break router-id
- Type de réseau NBMA non-broadcast : voisins unicast explicites
- Routes intra-area (`O`) vs inter-area (`O IA`) dans la table de routage
- Diagnostic : `show ip ospf neighbor`, `show ip ospf interface`, `show ip route ospf`
