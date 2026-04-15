# Lab — BGP iBGP / eBGP

## Objectif / Objective

**FR** — Implémenter des sessions BGP internes (iBGP) et externes (eBGP) entre plusieurs systèmes autonomes (AS). Le lab couvre les route reflectors, le filtrage de préfixes (prefix-list, route-map), et la manipulation d'attributs (MED, Local Preference, AS-Path, Communities).

**EN** — Implement internal (iBGP) and external (eBGP) BGP sessions across multiple autonomous systems (AS). The lab covers route reflectors, prefix filtering (prefix-list, route-map), and attribute manipulation (MED, Local Preference, AS-Path, Communities).

---

## Topologie prévue / Planned Topology

```
[Topology placeholder — full diagram to be added]

  AS 65001                                    AS 65002
+──────────────────────────+        +──────────────────────────+
|  R1 ────iBGP──── R2 (RR) |──eBGP──| R3 ────iBGP──── R4      |
|          ↑               |        |                          |
|       iBGP client        |        |                          |
+──────────────────────────+        +──────────────────────────+
                                            |
                                       AS 65003
                                        [R5] (transit)
```

**Équipements simulés / Simulated devices:** 5 × Cisco IOS-XE ou Juniper vMX (GNS3 / EVE-NG)

---

## Statut / Status

🚧 En cours de construction

---

## Technologies utilisées / Technologies Used

| Technologie | Rôle |
|-------------|------|
| Cisco IOS-XE / Juniper vMX | Plateformes de routage |
| BGP-4 (RFC 4271) | Protocole de routage inter-AS |
| Route Reflector (RFC 4456) | Scalabilité iBGP full-mesh |
| Prefix-list / Route-map | Filtrage et manipulation de routes |
| GNS3 / EVE-NG | Environnement de simulation réseau |

---

## Concepts couverts / Concepts Covered

- Sessions eBGP (multi-hop) et iBGP
- Route Reflector et Cluster-ID
- Attributs BGP : MED, Local Preference, AS-Path prepending, Communities
- Filtrage entrant/sortant avec prefix-list et route-map
- BGP graceful restart
- Convergence et stabilité (route dampening)
