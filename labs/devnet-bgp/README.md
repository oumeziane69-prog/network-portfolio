# Lab — DevNet BGP (Always-On Sandbox)

## Objectif / Objective

**FR** — Configurer BGP AS 65001 sur un routeur Cisco C8000V via le sandbox DevNet Always-On. Le lab couvre la déclaration du router-id, l'annonce de réseaux IPv4 en unicast address-family, et la vérification de la table BGP.

**EN** — Configure BGP AS 65001 on a Cisco C8000V router using the DevNet Always-On Sandbox. The lab covers router-id declaration, IPv4 unicast network advertisement, and BGP table verification.

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
|  BGP AS 65001             |
|  Router-ID : 1.1.1.1      |
|                           |
|  Réseaux annoncés :       |
|    1.1.1.1/32             |
|    10.100.100.0/24        |
|                           |
+---------------------------+
```

---

## Configuration BGP / BGP Configuration

| Paramètre | Valeur |
|-----------|--------|
| AS Number | 65001 |
| Router-ID | 1.1.1.1 |
| Address-Family | IPv4 Unicast |

### Réseaux annoncés / Advertised Networks

| Réseau | Masque | Description |
|--------|--------|-------------|
| 1.1.1.1 | 255.255.255.255 (/32) | Loopback0 |
| 10.100.100.0 | 255.255.255.0 (/24) | Loopback100 subnet |

---

## Configuration appliquée / Applied Configuration

Voir / See: [`bgp_config.txt`](bgp_config.txt)

```
router bgp 65001
 bgp router-id 1.1.1.1
 bgp log-neighbor-changes
 address-family ipv4
  network 1.1.1.1 mask 255.255.255.255
  network 10.100.100.0 mask 255.255.255.0
 exit-address-family
```

---

## Commandes de vérification / Verification Commands

```
show ip bgp
show ip bgp summary
show ip bgp neighbors
show ip route bgp
```

### Résultat attendu / Expected Output

`show ip bgp` doit afficher / should show:
- Table BGP avec les préfixes 1.1.1.1/32 et 10.100.100.0/24
- Status code `>` (best path) et `*` (valid)

`show ip bgp summary` doit afficher / should show:
- BGP router identifier 1.1.1.1
- Local AS number 65001

---

## Statut / Status

Complété — configuration validée sur DevNet Always-On Sandbox.

---

## Technologies utilisées / Technologies Used

| Technologie | Rôle |
|-------------|------|
| Cisco C8000V | Plateforme de routage cloud-native |
| IOS XE 17.15.04c | Système d'exploitation |
| BGP (AS 65001) | Protocole de routage EGP |
| IPv4 Unicast Address-Family | Annonce de préfixes IPv4 |
| DevNet Always-On | Sandbox de test Cisco en ligne |
| SSH / RESTCONF | Accès et automatisation |
