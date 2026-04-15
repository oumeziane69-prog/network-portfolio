# Lab — OSPF Multi-Area

## Objectif / Objective

**FR** — Configurer et tester un réseau OSPF multi-aire (Area 0 backbone + areas stub/NSSA) sur routeurs Cisco IOS-XE. Le lab couvre la redistribution de routes entre areas, l'optimisation de la convergence (timers), les LSA types, et le rôle des ABR/ASBR.

**EN** — Configure and test a multi-area OSPF network (Area 0 backbone + stub/NSSA areas) on Cisco IOS-XE routers. The lab covers inter-area route redistribution, convergence optimization (timers), LSA types, and ABR/ASBR roles.

---

## Topologie prévue / Planned Topology

```
[Topology placeholder — full diagram to be added]

  Area 1 (Stub)            Area 0 (Backbone)           Area 2 (NSSA)
+──────────────+       +─────────────────────+       +──────────────+
|   R1 (LAN)  |──────►|  ABR1 ──── ABR2     |──────►|  R4 (LAN)   |
+──────────────+       |        |            |       +──────────────+
                       |       R3 (Core)     |
                       +─────────────────────+
                                 |
                           External routes
                           (ASBR redistribution)
```

**Équipements simulés / Simulated devices:** 4 × Cisco IOS-XE (GNS3 ou EVE-NG)

---

## Statut / Status

🚧 En cours de construction

---

## Technologies utilisées / Technologies Used

| Technologie | Rôle |
|-------------|------|
| Cisco IOS-XE | Plateforme de routage principale |
| OSPFv2 (IPv4) | Protocole IGP link-state |
| OSPFv3 (IPv6) | Extension dual-stack |
| GNS3 / EVE-NG | Environnement de simulation réseau |
| Python / Netmiko | Automatisation du déploiement des configs |

---

## Concepts couverts / Concepts Covered

- Types de zones : backbone (Area 0), stub, NSSA, totally stubby
- Types de LSA : 1, 2, 3, 4, 5, 7
- Rôles : DR/BDR, ABR, ASBR
- Redistribution de routes externes
- Optimisation des timers hello/dead
- Authentification MD5 entre voisins OSPF
