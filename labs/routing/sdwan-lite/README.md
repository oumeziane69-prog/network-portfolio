# Lab — SD-WAN Lite : PBR + IP SLA + Track (Cat8000 IOS-XE)

## Objectif / Objective

**FR** — Simuler un comportement SD-WAN basique sur un routeur Cisco Catalyst 8000 en combinant IP SLA, Object Tracking et Policy-Based Routing (PBR). Le trafic entre Area 1 et Area 2 emprunte par défaut le tunnel GRE/IPSec (chemin primaire). Si le tunnel devient injoignable (Track 1 = down), le trafic bascule automatiquement sur le lien direct GigabitEthernet1 (chemin de secours).

**EN** — Simulate basic SD-WAN behavior on a Cisco Catalyst 8000 by combining IP SLA, Object Tracking, and Policy-Based Routing (PBR). Traffic between Area 1 and Area 2 uses the GRE/IPSec tunnel by default (primary path). If the tunnel becomes unreachable (Track 1 = down), traffic automatically fails over to the direct GigabitEthernet1 link (backup path).

---

## Topologie / Topology

```
  Area 1 (source)                R1 — Cat8000                Area 2 (destination)
  10.1.0.0/24 ──────────────────►  GigabitEthernet1          10.2.0.0/24
                                    10.10.20.102/24
                                         │
                        ┌────────────────┴────────────────┐
                        │          PBR + Track             │
                        │                                  │
                  PRIMARY PATH                       BACKUP PATH
              GRE/IPSec Tunnel0                  GigabitEthernet1
              172.16.0.2 (R2)                    10.10.20.103 (R2)
              Track 1 = [up]                     (used if Track 1 = [down])
                        │                                  │
                        └────────────────┬────────────────┘
                                         │
                                   R2 — Cat8000
                                    10.10.20.103/24
                                   Tu0: 172.16.0.2/30
```

**Équipement / Device:** Cisco Catalyst 8000 (IOS-XE) — s'appuie sur le tunnel GRE/IPSec du lab précédent

---

## Mécanismes / Mechanisms

| Composant     | Rôle |
|--------------|------|
| IP SLA 1      | Sonde ICMP vers 172.16.0.2 (Tunnel0 R2), toutes les 10 s |
| Track 1       | Suit la joignabilité (reachability) de l'IP SLA 1 |
| ACL-PBR       | Identifie le trafic Area 1 → Area 2 (source 10.1.0.0/24) |
| route-map RM-PBR | Redirige via 172.16.0.2 si Track 1 up, sinon 10.10.20.103 |
| service-policy (PBR) | Appliqué en entrée sur l'interface LAN/Area 1 |

---

## Configuration IOS-XE complète / Full IOS-XE Config

```ios
! --- IP SLA : sonde ICMP vers l'extrémité tunnel R2 ---
ip sla 1
 icmp-echo 172.16.0.2 source-interface Tunnel0
 frequency 10
ip sla schedule 1 life forever start-time now

! --- Object Tracking : suit la joignabilité IP SLA 1 ---
track 1 ip sla 1 reachability

! --- ACL : identifie le trafic Area1 → Area2 ---
ip access-list extended ACL-PBR
 permit ip 10.1.0.0 0.0.0.255 10.2.0.0 0.0.0.255

! --- Route-map PBR ---
route-map RM-PBR permit 10
 match ip address ACL-PBR
 set ip next-hop verify-availability 172.16.0.2 1 track 1
 set ip next-hop 10.10.20.103

! --- Application PBR en entrée (interface côté Area 1) ---
interface GigabitEthernet2
 ip policy route-map RM-PBR
```

> **Note :** GigabitEthernet2 représente l'interface LAN/Area 1 (source du trafic classifié). GigabitEthernet1 (10.10.20.102/24) reste l'interface WAN underlay et Tunnel0 le chemin primaire chiffré.

La configuration complète est disponible dans [`configs/R1.ios`](configs/R1.ios).

---

## Vérification / Verification

### Statut IP SLA / IP SLA Status

```
R1# show ip sla statistics 1

IPSLAs Latest Operation Statistics

IPSLA operation id: 1
        Latest RTT: 1 milliseconds
Latest operation start time: ...
Latest operation return code: OK
Number of successes: 10
Number of failures: 0
Operation time to live: Forever
```

### Statut Track / Track Status

```
R1# show track 1

Track 1
  IP SLA 1 reachability
  Reachability is Up
    10 changes, last change 00:xx:xx
  Latest operation return code: OK
  Latest RTT (millisecs) 1
  Tracked by:
    ROUTE-MAP 0
```

### Vérification PBR sur l'interface / PBR on interface

```
R1# show ip policy

Interface      Route map
Gi2            RM-PBR
```

### Table de routage PBR active / Active PBR routing

```
R1# show route-map RM-PBR

route-map RM-PBR, permit, sequence 10
  Match clauses:
    ip address (access-lists): ACL-PBR
  Set clauses:
    ip next-hop verify-availability 172.16.0.2 1 track 1  [up]
    ip next-hop 10.10.20.103
  Policy routing matches: x packets, x bytes
```

---

## Comportement de basculement / Failover Behavior

| État Track 1 | Chemin utilisé              | Next-hop           |
|-------------|-----------------------------|--------------------|
| **up**      | GRE/IPSec Tunnel0 (primaire)| 172.16.0.2         |
| **down**    | GigabitEthernet1 (secours)  | 10.10.20.103       |

---

## Statut / Status

✅ Terminé — IP SLA RTT 1 ms, 10 succès, Track 1 [up], basculement validé

---

## Technologies utilisées / Technologies Used

| Technologie | Rôle |
|-------------|------|
| Cisco Catalyst 8000 (IOS-XE) | Plateforme de routage principale |
| IP SLA (ICMP echo) | Sonde de joignabilité vers le tunnel |
| Object Tracking | Liaison IP SLA ↔ décision de routage |
| PBR (Policy-Based Routing) | Redirection du trafic selon la disponibilité du chemin |
| GRE/IPSec Tunnel0 | Chemin primaire chiffré (lab gre-over-ipsec) |
| `set ip next-hop verify-availability` | Basculement automatique conditionné au Track |

---

## Concepts couverts / Concepts Covered

- Architecture SD-WAN Lite : PBR + IP SLA + Track comme alternative légère à Viptela/SD-WAN
- IP SLA ICMP echo : source-interface, frequency, schedule
- Object Tracking : `track ip sla reachability` — liaison entre sonde et PBR
- `set ip next-hop verify-availability <ip> <seq> track <id>` — next-hop conditionnel
- Ordre de priorité PBR : next-hop vérifié (primaire) → next-hop fixe (secours)
- Diagnostic : `show ip sla statistics`, `show track`, `show ip policy`, `show route-map`
