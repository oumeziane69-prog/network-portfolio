# Lab — MPLS L3VPN

## Objectif / Objective

**FR** — Mettre en oeuvre un réseau MPLS avec VPN de couche 3 (L3VPN) entre sites clients, incluant la signalisation LDP, les VRF par client, et l'échange de routes MP-BGP entre PE. Validation de l'isolation du trafic entre VRF.

**EN** — Deploy an MPLS network with Layer 3 VPNs (L3VPN) between customer sites, including LDP signaling, per-customer VRF, and MP-BGP route exchange between PE routers. Validate traffic isolation between VRFs.

---

## Topologie prévue / Planned Topology

```
[Topology placeholder — full diagram to be added]

 Site A (Client 1)                              Site B (Client 1)
   [CE1]────────[PE1]────[P1]────[P2]────[PE2]────────[CE2]
                   \                       /
                    ──────────────────────
                    MP-BGP (VPNv4 routes)

   VRF CUST1 on PE1 ←──────────────────→ VRF CUST1 on PE2
   VRF CUST2 on PE1 ←──────────────────→ VRF CUST2 on PE2
   (traffic isolation enforced)
```

**Équipements simulés / Simulated devices:** 6 × Cisco IOS-XE (CE × 2, PE × 2, P × 2)

---

## Statut / Status

🚧 En cours de construction

---

## Technologies utilisées / Technologies Used

| Technologie | Rôle |
|-------------|------|
| Cisco IOS-XE | Plateforme PE/P/CE |
| MPLS / LDP | Commutation d'étiquettes et signalisation |
| MP-BGP (VPNv4) | Distribution des routes VPN |
| VRF (Virtual Routing & Forwarding) | Isolation par client |
| OSPF / ISIS | IGP backbone MPLS |
| GNS3 / EVE-NG | Environnement de simulation réseau |

---

## Concepts couverts / Concepts Covered

- Architecture MPLS : PE, P, CE — rôles et responsabilités
- LDP (Label Distribution Protocol) — échange d'étiquettes
- VRF : import/export de routes, Route Distinguisher (RD), Route Target (RT)
- MP-BGP address family VPNv4
- Traceroute MPLS et débogage de la table LFIB
- Isolation du trafic inter-clients
- MPLS TE (Traffic Engineering) — introduction
