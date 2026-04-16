# Lab — DevNet OSPF (Always-On Sandbox)

## Objectif / Objective

**FR** — Configurer OSPF Area 0 sur les interfaces loopback d'un routeur Cisco C8000V via le sandbox DevNet Always-On. Le lab démontre la mise en place d'un OSPF PID 1 avec deux loopbacks (Lo0 et Lo100) redistribuées dans l'area backbone.

**EN** — Configure OSPF Area 0 on loopback interfaces of a Cisco C8000V router using the DevNet Always-On Sandbox. The lab demonstrates setting up OSPF PID 1 with two loopbacks (Lo0 and Lo100) advertised into the backbone area.

---

## Plateforme / Platform

| Paramètre | Valeur |
|-----------|--------|
| Équipement | Cisco C8000V |
| Version IOS XE | 17.15.04c |
| Environnement | DevNet Always-On Sandbox |
| Accès | SSH / RESTCONF |

---

## Topologie / Topology

```
+---------------------------+
|   Cisco C8000V (C8KV)     |
|                           |
|  Loopback0  1.1.1.1/32    |  ─── OSPF Area 0 (PID 1)
|  Loopback100 10.100.100.1/32 |     router-id 1.1.1.1
|                           |
+---------------------------+
```

---

## Interfaces configurées / Configured Interfaces

| Interface | Adresse IP | Masque | OSPF Area |
|-----------|-----------|--------|-----------|
| Loopback0 | 1.1.1.1 | /32 (255.255.255.255) | Area 0 |
| Loopback100 | 10.100.100.1 | /32 (255.255.255.255) | Area 0 |

---

## Configuration appliquée / Applied Configuration

Voir / See: [`ospf_config.txt`](ospf_config.txt)

```
interface Loopback0
 ip address 1.1.1.1 255.255.255.255
!
interface Loopback100
 ip address 10.100.100.1 255.255.255.255
!
router ospf 1
 router-id 1.1.1.1
 network 1.1.1.1 0.0.0.0 area 0
 network 10.100.100.1 0.0.0.0 area 0
```

---

## Commandes de vérification / Verification Commands

```
show ip ospf
show ip ospf interface brief
show ip ospf neighbor
show ip route ospf
```

### Résultat attendu / Expected Output

`show ip ospf` doit afficher / should show:
- Process ID: 1
- Router ID: 1.1.1.1
- Area 0 active

`show ip ospf interface brief` doit afficher / should show:
- Loopback0 dans Area 0
- Loopback100 dans Area 0

---

## Statut / Status

Complété — configuration validée sur DevNet Always-On Sandbox.

---

## Technologies utilisées / Technologies Used

| Technologie | Rôle |
|-------------|------|
| Cisco C8000V | Plateforme de routage cloud-native |
| IOS XE 17.15.04c | Système d'exploitation |
| OSPFv2 | Protocole IGP link-state (Area 0) |
| DevNet Always-On | Sandbox de test Cisco en ligne |
| SSH / RESTCONF | Accès et automatisation |
