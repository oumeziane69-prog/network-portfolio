# Verification — Juniper JunOS Lab

Commandes de vérification post-configuration avec output attendu.
Post-configuration verification commands with expected output.

> Exécuter ces commandes en mode opérationnel JunOS (prompt `>`)

---

## 1. Vérification des interfaces / Interface Verification

### `show interfaces terse`

```
user@SRX1> show interfaces terse
Interface               Admin Link Proto    Local                 Remote
ge-0/0/0                up    up
ge-0/0/0.0              up    up   inet     10.0.12.1/30
ge-0/0/1                up    up
ge-0/0/1.0              up    up   inet     10.0.13.1/30
lo0                     up    up
lo0.0                   up    up   inet     10.255.1.1/32    --> 0/0
```

> Tous les statuts doivent être `up up`. `lo0.0` remote `0/0` est normal pour un loopback.

### `show interfaces ge-0/0/0 detail` (extrait)

```
user@SRX1> show interfaces ge-0/0/0 detail
Physical interface: ge-0/0/0, Enabled, Physical link is Up
  Description: Link to SRX2 ge-0/0/0 (AS65002) — 10.0.12.0/30
  ...
  Input errors:
    Errors: 0, Drops: 0, Framing errors: 0, ...
  Output errors:
    Carrier transitions: 1, Errors: 0, Drops: 0, ...
  Logical interface ge-0/0/0.0
    Flags: Up SNMP-Traps
    Protocol inet, MTU: 1500
      Flags: None
      Addresses, Flags: Is-Preferred Is-Primary
        Destination: 10.0.12.0/30, Local: 10.0.12.1, Broadcast: 10.0.12.3
```

---

## 2. Vérification BGP / BGP Verification

### `show bgp summary`

```
user@SRX1> show bgp summary
Threading mode: BGP I/O
Groups: 2 Peers: 2 Down peers: 0
Table          Tot Paths  Act Paths Suppressed    History Damp State    Pending
inet.0
                       2          2          0          0          0          0
Peer                     AS      InPkt     OutPkt    OutQ   Flaps Last Up/Dwn State|#Active/Received/Accepted/Damped...
10.0.12.2             65002        148        147       0       0       58:12 2/2/2/0              0/0/0/0
10.0.13.2             65003        132        135       0       0       55:30 1/1/1/0              0/0/0/0
```

> Résultat attendu :
> - `Down peers: 0` — aucun voisin en état DOWN
> - Tous les voisins ont un `State` de type `X/X/X/0` (actif/reçu/accepté/damped)
> - `Flaps: 0` ou très faible — voisins stables
> - `Last Up/Dwn` montre le temps depuis le dernier changement d'état

### `show bgp neighbor 10.0.12.2`

```
user@SRX1> show bgp neighbor 10.0.12.2
Peer: 10.0.12.2+51234 AS 65002 Local: 10.0.12.1+179 AS 65001
  Description: SRX2 (AS65002) — connected on ge-0/0/0
  Type: External    State: Established    Flags: <Sync>
  Last State: OpenConfirm   Last Event: RecvKeepAlive
  Last Error: None
  Options: <Preference LogUpDown GracefulShutdownRcv>
  Options: <Authentication>
  Authentication key is configured
  Holdtime: 90 Preference: 170+0
  Number of flaps: 0
  Peer ID: 10.255.2.1     Local ID: 10.255.1.1    Active Holdtime: 90
  Keepalive Interval: 30          Peer index: 0   AIGP originator: N/A
  ...
  Import: IMPORT-EBGP        Export: EXPORT-LOOPBACK
  ...
  BGP Output Queue[0]: 0
  Flap Statistics:
    Total: 0
    Last flap event: Opened
  Input messages:  Total 148  Updates 2  Refreshes 0  Octets 2828
  Output messages: Total 147  Updates 1  Refreshes 0  Octets 2807
  Output Queue[0]: 0
```

> Points clés à vérifier :
> - `State: Established` — session active
> - `Authentication key is configured` — MD5 en place
> - `Number of flaps: 0` — session stable
> - `Import: IMPORT-EBGP  Export: EXPORT-LOOPBACK` — politiques appliquées

### `show route protocol bgp`

```
user@SRX1> show route protocol bgp

inet.0: 7 destinations, 7 routes (7 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

10.255.2.1/32      *[BGP/170] 00:58:12, localpref 100
                    AS path: 65002 I, validation-state: unverified
                  > to 10.0.12.2 via ge-0/0/0.0
10.255.3.1/32      *[BGP/170] 00:55:30, localpref 100
                    AS path: 65003 I, validation-state: unverified
                  > to 10.0.13.2 via ge-0/0/1.0
```

> Résultat attendu :
> - SRX1 voit `10.255.2.1/32` (loopback SRX2) appris via `10.0.12.2`
> - SRX1 voit `10.255.3.1/32` (loopback R1) appris via `10.0.13.2`
> - `localpref 100` confirmé — policy IMPORT-EBGP correctement appliquée

### `show route advertising-protocol bgp 10.0.12.2`

```
user@SRX1> show route advertising-protocol bgp 10.0.12.2

inet.0: 7 destinations, 7 routes (7 active, 0 holddown, 0 hidden)
  Prefix                  Nexthop              MED     Lclpref    AS path
* 10.255.1.1/32           Self                                    I
```

> Résultat attendu : SRX1 annonce uniquement son loopback `/32` vers SRX2 — policy EXPORT-LOOPBACK correcte.

---

## 3. Vérification de la connectivité / Connectivity Check

### Ping entre loopbacks

```
user@SRX1> ping 10.255.2.1 source 10.255.1.1 count 5
PING 10.255.2.1 (10.255.2.1): 56 data bytes
64 bytes from 10.255.2.1: icmp_seq=0 ttl=64 time=1.432 ms
64 bytes from 10.255.2.1: icmp_seq=1 ttl=64 time=1.218 ms
64 bytes from 10.255.2.1: icmp_seq=2 ttl=64 time=1.344 ms
64 bytes from 10.255.2.1: icmp_seq=3 ttl=64 time=1.190 ms
64 bytes from 10.255.2.1: icmp_seq=4 ttl=64 time=1.277 ms

--- 10.255.2.1 ping statistics ---
5 packets transmitted, 5 packets received, 0% packet loss
round-trip min/avg/max/stddev = 1.190/1.292/1.432/0.083 ms
```

> Source explicite `10.255.1.1` pour tester le chemin BGP complet (loopback-to-loopback).

### Traceroute vers loopback R1

```
user@SRX1> traceroute 10.255.3.1 source 10.255.1.1
traceroute to 10.255.3.1 (10.255.3.1), 30 hops max, 52 byte packets
 1  10.0.13.2 (10.0.13.2)  1.523 ms  1.387 ms  1.456 ms
```

---

## 4. Vérification des filtres / Firewall Filter Verification

### `show firewall filter PROTECT-RE`

```
user@SRX1> show firewall filter PROTECT-RE

Filter: PROTECT-RE
Counters:
Name                                                Bytes              Packets
DENY-ALL-COUNT                                          0                    0
```

> `DENY-ALL-COUNT = 0` signifie qu'aucun paquet n'a été bloqué — état nominal.
> Si ce compteur monte, vérifier quel trafic est rejeté avec `show firewall log`.

### `show firewall log`

```
user@SRX1> show firewall log
Log :
Time      Filter    Action Interface     Protocol Src Addr        Dest Addr
00:00:00  PROTECT-RE D     ge-0/0/0.0    TCP      <attacker-IP>   10.255.1.1
```

> Affiche les paquets bloqués avec log activé.

---

## 5. Vérification commit / Commit Verification

### `show system commit`

```
user@SRX1> show system commit
0   2026-04-15 10:23:45 UTC by admin via cli
1   2026-04-15 09:50:12 UTC by admin via cli
2   2026-04-15 09:30:05 UTC by admin via cli
```

### Comparer deux versions

```
user@SRX1> show system rollback compare 0 1
[edit protocols bgp group EBGP-TO-SRX2 neighbor 10.0.12.2]
+      description "SRX2 (AS65002) — connected on ge-0/0/0";
```

---

## 6. Récapitulatif de validation / Validation Checklist

| Vérification | Commande | Résultat attendu |
|--------------|----------|-----------------|
| Interfaces up | `show interfaces terse` | Tous `up up` |
| Sessions BGP up | `show bgp summary` | `Down peers: 0`, State Established |
| Routes BGP reçues | `show route protocol bgp` | 2 loopbacks /32 dans inet.0 |
| Export policy OK | `show route advertising-protocol bgp X.X.X.X` | Uniquement le loopback propre |
| Auth MD5 active | `show bgp neighbor X.X.X.X` | `Authentication key is configured` |
| Aucun filtre bloquant | `show firewall filter PROTECT-RE` | `DENY-ALL-COUNT = 0` |
| Ping loopback-to-loopback | `ping 10.255.2.1 source 10.255.1.1` | 0% loss |
| Ping vers R1 | `ping 10.255.3.1 source 10.255.1.1` | 0% loss |
