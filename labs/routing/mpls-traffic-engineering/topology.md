# Topology — MPLS Traffic Engineering Lab

## Schéma logique / Logical Diagram

```
           Primary TE tunnel (TE-TUNNEL-TO-PE2)
           ┌─────────────────────────────────────────►
           │
PE1 ─────[Gi0/0]──── P ────[Gi0/1]──── PE2
1.1.1.1                2.2.2.2          3.3.3.3
   \                                      /
    \──[Gi0/1]────────────────[Gi0/1]───/
           Bypass tunnel (FRR path)
           (protège le lien PE1-P et le noeud P)

Légende :
  ─── : lien physique GigabitEthernet (1 Gbps)
  ───► : tunnel MPLS-TE (label-switched path)
```

---

## Plan d'adressage / Addressing Plan

### Loopbacks (Router-ID & tunnel endpoints)

| Équipement | Interface | Adresse IP | Rôle |
|------------|-----------|-----------|------|
| PE1 | Loopback0 | `1.1.1.1/32` | Ingress PE — tête de tunnel TE |
| P | Loopback0 | `2.2.2.2/32` | P-router transit |
| PE2 | Loopback0 | `3.3.3.3/32` | Egress PE — destination tunnel TE |

### Liens point-à-point / Point-to-Point Links

| Lien | Réseau | Adresses | Interfaces |
|------|--------|---------|------------|
| PE1 ↔ P | `10.0.12.0/30` | PE1: `10.0.12.1` — P: `10.0.12.2` | PE1: Gi0/0 — P: Gi0/0 |
| P ↔ PE2 | `10.0.23.0/30` | P: `10.0.23.1` — PE2: `10.0.23.2` | P: Gi0/1 — PE2: Gi0/0 |
| PE1 ↔ PE2 | `10.0.13.0/30` | PE1: `10.0.13.1` — PE2: `10.0.13.2` | PE1: Gi0/1 — PE2: Gi0/1 |

---

## Tunnels MPLS-TE

### Tunnel principal / Primary Tunnel

| Paramètre | Valeur |
|-----------|--------|
| Nom | `Tunnel0` (sur PE1) |
| Source | `1.1.1.1` (Loopback0 PE1) |
| Destination | `3.3.3.3` (Loopback0 PE2) |
| Chemin explicite | `PRIMARY-PATH` : PE1 → P (2.2.2.2) → PE2 |
| Bande passante réservée | 100 Mbps |
| Path option | 1 — explicit-path `PRIMARY-PATH` |
| Path option (backup) | 2 — dynamic (CSPF) |
| Autoroute announce | Activé — intégration dans table de routage PE1 |
| Fast Reroute | Activé |

### Tunnel bypass FRR / FRR Bypass Tunnel

| Paramètre | Valeur |
|-----------|--------|
| Nom | `Tunnel1` (sur PE1) |
| Source | `1.1.1.1` (Loopback0 PE1) |
| Destination | `3.3.3.3` (Loopback0 PE2) |
| Chemin | `BYPASS-PATH` : PE1 → PE2 direct (lien Gi0/1) |
| Type | Bypass tunnel — protège le lien PE1-P et le noeud P |
| Bande passante | 50 Mbps |

---

## OSPF avec extensions TE

| Paramètre | Valeur |
|-----------|--------|
| Protocole IGP | OSPF Process 1 |
| Area | Area 0 (backbone) |
| TE extensions | `mpls traffic-eng area 0` sur tous les routeurs |
| Router-ID | Loopback0 de chaque équipement |

### Capacités des liens / Link Bandwidth Allocation

| Lien | BW totale | BW allouable (75%) | BW réservée tunnel principal |
|------|-----------|--------------------|------------------------------|
| PE1 — P (Gi0/0) | 1000 Mbps | 750 Mbps | 100 Mbps |
| P — PE2 (Gi0/1) | 1000 Mbps | 750 Mbps | 100 Mbps |
| PE1 — PE2 (Gi0/1) | 1000 Mbps | 750 Mbps | 50 Mbps (bypass) |

---

## Comparaison avec la topologie mpls-l3vpn

Ce lab enrichit la topologie [mpls-l3vpn](../mpls-l3vpn/README.md) en ajoutant :

| Ajout | Description |
|-------|-------------|
| RSVP-TE | Remplacement de la signalisation LDP par RSVP-TE sur les PE |
| Chemins explicites | Les tunnels TE suivent des chemins déterministes, pas le meilleur IGP |
| Réservation de BW | `ip rsvp bandwidth` sur chaque interface |
| FRR | Protection < 50 ms en cas de défaillance d'un lien ou noeud |
| `autoroute announce` | Les VRF L3VPN empruntent les tunnels TE automatiquement |

---

## Notes d'installation / Setup Notes

1. Configurer OSPF + TE extensions **avant** RSVP et les tunnels
2. Vérifier `show mpls traffic-eng topology` avant de créer les tunnels
3. Les tunnels TE ne montent que si RSVP est opérationnel sur tous les liens du chemin
4. `commit` sur le chemin explicite avec `no shutdown` sur le tunnel pour déclencher la signalisation RSVP
