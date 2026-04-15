# Lab — MPLS Traffic Engineering (RSVP-TE)

## Objectif / Objective

**FR** — Mettre en oeuvre MPLS Traffic Engineering (MPLS-TE) avec RSVP comme protocole de signalisation sur un réseau Cisco IOS-XE. Le lab couvre la création de tunnels TE avec chemins explicites, la réservation de bande passante, le Fast Reroute (FRR) pour la protection des liens, et la comparaison avec LDP.

**EN** — Implement MPLS Traffic Engineering (MPLS-TE) using RSVP as signaling protocol on Cisco IOS-XE. The lab covers TE tunnel creation with explicit paths, bandwidth reservation, Fast Reroute (FRR) for link protection, and comparison with LDP.

---

## LDP vs RSVP-TE

| Aspect | LDP | RSVP-TE |
|--------|-----|---------|
| **Objectif** | Distribution d'étiquettes hop-by-hop | Ingénierie du trafic : chemins contraints |
| **Chemin** | Meilleur chemin IGP (OSPF/ISIS) | Chemin explicite ou calculé sous contraintes |
| **Réservation BW** | Aucune | Réservation de bande passante RSVP |
| **Redondance** | Convergence IGP (secondes) | Fast Reroute : < 50 ms |
| **Complexité** | Simple | Élevée (TE extensions, CSPF, RSVP) |
| **Cas d'usage** | VPN L3, routage MPLS basique | QoS critique, redondance < 50 ms, charge balancing |
| **Protocole** | LDP (UDP/TCP 646) | RSVP-TE (IP proto 46) |
| **Extensions IGP** | Aucune | OSPF-TE ou ISIS-TE obligatoires |

---

## Cas d'usage / Use Cases

- **QoS et priorisation** : Forcer un flux critique (voix, SCADA) sur un chemin avec BW réservé, indépendamment de la décision IGP
- **Redondance < 50 ms** : FRR protège un lien ou noeud défaillant — basculement sub-secondaire sans attendre OSPF
- **Load balancing** : Distribuer le trafic sur plusieurs tunnels TE (Equal/Unequal cost)
- **Backbone opérateur** : Technologie utilisée chez les opérateurs pour les VPN MPLS L3 avec SLA garanti

---

## Topologie / Topology

Voir [topology.md](topology.md)

```
PE1 (1.1.1.1) ──[Gi0/0]── P (2.2.2.2) ──[Gi0/1]── PE2 (3.3.3.3)
      \                                                   /
       \──[Gi0/1]──── Lien direct (bypass FRR) ─────[Gi0/1]
```

---

## Statut / Status

🚧 En cours de construction

---

## Technologies utilisées / Technologies Used

| Technologie | Rôle |
|-------------|------|
| Cisco IOS-XE | Plateforme PE et P |
| MPLS (LDP + RSVP-TE) | Commutation d'étiquettes et TE |
| OSPF avec extensions TE | IGP avec diffusion des capacités TE |
| RSVP-TE (RFC 3209) | Signalisation et réservation de ressources |
| CSPF (Constraint-based SPF) | Calcul des chemins TE sous contraintes |
| Fast Reroute (RFC 4090) | Protection < 50 ms des liens MPLS |
| EVE-NG / GNS3 | Environnement de simulation réseau |

---

## Fichiers du lab / Lab Files

| Fichier | Description |
|---------|-------------|
| [topology.md](topology.md) | Plan d'adressage, schéma, tunnels TE |
| [configs/PE1-TE.ios](configs/PE1-TE.ios) | Config PE1 — ingress tunnel TE + FRR |
| [configs/P-TE.ios](configs/P-TE.ios) | Config P — transit + bypass tunnel FRR |
| [configs/PE2-TE.ios](configs/PE2-TE.ios) | Config PE2 — egress tunnel TE |
| [verification.md](verification.md) | Commandes `show` avec output attendu |

---

## Concepts couverts / Concepts Covered

- OSPF TE extensions : `mpls traffic-eng area`, annonce des capacités de liens
- RSVP : messages PATH/RESV, réservation de bande passante
- Tunnel MPLS-TE : `interface Tunnel`, `tunnel mpls traffic-eng`
- Chemins explicites : `ip explicit-path`
- `autoroute announce` : intégration du tunnel dans la table de routage
- Fast Reroute : tunnel bypass, `tunnel mpls traffic-eng fast-reroute`
- `affinity` et `attribute-flags` : contraintes sur les liens
- Débogage : `debug mpls traffic-eng`, `show rsvp`
