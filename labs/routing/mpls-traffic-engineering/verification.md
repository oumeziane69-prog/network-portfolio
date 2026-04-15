# Verification — MPLS Traffic Engineering Lab

Commandes de vérification post-configuration avec output attendu.
Run on PE1 (ingress) unless otherwise specified.

---

## 1. Vérification OSPF TE / OSPF TE Verification

### `show mpls traffic-eng topology`

```
PE1# show mpls traffic-eng topology

My_System_id: 1.1.1.1 (OSPF 1 area 0)
...
  Link[0]: Point-to-Point, Nbr Node id 2, gen 6
    Frag id 0, Intf Address: 10.0.12.1, Nbr Intf Address: 10.0.12.2
    TE Metric: 1, IGP Metric: 1, Attribute Flags: 0x0
    Attribute Names:
    Physical BW: 1000000 kbits/sec, Max Reservable BW Global: 750000 kbits/sec
    Max Reservable BW Sub: 750000 kbits/sec
      [ 0] Reservable Global BW:  650000 kbits/sec (after 100000 reserved)
      [ 1] Reservable Global BW:  750000 kbits/sec
      ...
  Link[1]: Point-to-Point, Nbr Node id 3, gen 5
    Frag id 0, Intf Address: 10.0.13.1, Nbr Intf Address: 10.0.13.2
    TE Metric: 1, IGP Metric: 1, Attribute Flags: 0x0
    Physical BW: 1000000 kbits/sec, Max Reservable BW Global: 750000 kbits/sec
    ...
```

> Vérifier que tous les liens apparaissent avec leur BW physique et réservable.
> `Max Reservable BW Global: 750000` confirme que `ip rsvp bandwidth 750000` est actif.

---

## 2. Vérification des tunnels TE / TE Tunnel Verification

### `show mpls traffic-eng tunnels`

```
PE1# show mpls traffic-eng tunnels

Name:PE1_t0                          (Tunnel0) Destination: 3.3.3.3
  Status:
    Admin: up         Oper: up     Path: valid       Signalling: connected
    path option 1, type explicit PRIMARY-PATH (Basis for Setup, path weight 2)
  Config Parameters:
    Bandwidth: 100000      kbps (Global)  Priority: 7  0   Affinity: 0x0/0xFFFF
    Metric Type: TE (default)
    AutoRoute: enabled  LockDown: disabled  Loadshare: 100  bw-based
    auto-bw: disabled
  Active Path Option Parameters:
    State: explicit path option 1 is active
    BandwidthOverride: disabled  LockDown: disabled  Verbatim: disabled
  InLabel  :  -
  OutLabel : GigabitEthernet0/0, 18
  RSVP Signalling Info:
       Src 1.1.1.1, Dst 3.3.3.3, Tun_Id 0, Tun_Instance 37
       RSVP Path Info:
         My Address: 10.0.12.1
         Explicit Route: 10.0.12.2 10.0.23.2 3.3.3.3
         Record   Route:  NONE
         Tspec: ave rate=100000 kbits, burst=1000 bytes, peak rate=100000 kbits
       RSVP Resv Info:
         Record   Route:  NONE
         Fspec: ave rate=100000 kbits, burst=1000 bytes, peak rate=100000 kbits
  Shortest Unconstrained Path Info:
    Path Weight: 2 (TE)
    Explicit Route: 10.0.12.2 3.3.3.3

Name:PE1_t1                          (Tunnel1) Destination: 3.3.3.3
  Status:
    Admin: up         Oper: up     Path: valid       Signalling: connected
    path option 1, type explicit BYPASS-PATH
  ...
  OutLabel : GigabitEthernet0/1, 22
```

> Résultats attendus :
> - `Oper: up` pour les deux tunnels
> - `Path: valid` — chemin RSVP établi
> - `Explicit Route` correspond au chemin configuré
> - `OutLabel` montre l'étiquette MPLS attribuée par RSVP

### `show mpls traffic-eng tunnels brief`

```
PE1# show mpls traffic-eng tunnels brief

                          Tunnel   Destination   Admin  Oper   Path   BW(Kbps)
Name               Intf   State    Address       State  State  Type   Allocated
-----------------------------------------------------------------------------------
PE1_t0             Tu0    up       3.3.3.3       up     up     Exp    100000
PE1_t1             Tu1    up       3.3.3.3       up     up     Exp    50000
```

---

## 3. Vérification RSVP / RSVP Verification

### `show ip rsvp neighbors`

```
PE1# show ip rsvp neighbors

Address          Interface        Messages  Refresh  Timeouts  HelloInt  HelloMisses  HelloState
10.0.12.2        Gi0/0            47        45       0         10000     4            UP
10.0.13.2        Gi0/1            23        21       0         10000     4            UP
```

> `HelloState: UP` pour chaque voisin RSVP — les hellos fonctionnent (requis pour FRR).

### `show ip rsvp installed`

```
PE1# show ip rsvp installed

RSVP: Gi0/0 has the following installed reservations
RSVP Reservation. Destination is 3.3.3.3. Source is 1.1.1.1,
  Protocol is IP, Destination port is 0, Source port is 0
  Reserved bandwidth: 100K bits/sec, Maximum burst: 1000 bytes, Peak rate: 100K
  Min Policed Unit: 0 bytes, Max Pkt Size: 1500 bytes

RSVP: Gi0/1 has the following installed reservations
RSVP Reservation. Destination is 3.3.3.3. Source is 1.1.1.1,
  Protocol is IP, Destination port is 0, Source port is 0
  Reserved bandwidth: 50K bits/sec, Maximum burst: 1000 bytes, Peak rate: 50K
```

### `show mpls traffic-eng link-management bandwidth-allocation`

```
PE1# show mpls traffic-eng link-management bandwidth-allocation

  System Information::
    Links (with RSVP): 2
    Maximum Tunnels: 5

  Link ID:: Gi0/0 (10.0.12.1)
    Physical Bandwidth    : 1000000 kbits/sec
    Maximum Reservable BW : 750000  kbits/sec
    Soft Preempted BW     : 0       kbits/sec
    Global Pool           :
      BW Allocated : 100000 kbits/sec   (13% of reservable)
      BW Soft Preempted : 0 kbits/sec
      Priority Allocations (kbits/sec):
        [0]:100000 [1]:0 [2]:0 [3]:0 [4]:0 [5]:0 [6]:0 [7]:0

  Link ID:: Gi0/1 (10.0.13.1)
    Physical Bandwidth    : 1000000 kbits/sec
    Maximum Reservable BW : 750000  kbits/sec
    BW Allocated : 50000 kbits/sec    (6% of reservable)
```

---

## 4. Vérification de la table de routage / Routing Table

### `show ip route 3.3.3.3`

```
PE1# show ip route 3.3.3.3

Routing entry for 3.3.3.3/32
  Known via "ospf 1", distance 110, metric 2, type intra area
  Routing Descriptor Blocks:
  * 10.0.12.2, from 3.3.3.3, via GigabitEthernet0/0
      Route metric is 2, traffic share count is 1
  via Tunnel0, from 3.3.3.3
      Route metric is 10, traffic share count is 1

```

> `via Tunnel0` confirme que `autoroute announce` a injecté le tunnel dans la table de routage.
> Le trafic vers PE2 (3.3.3.3) utilisera le tunnel TE (Tunnel0) et non le chemin IGP direct.

### `show mpls forwarding-table`

```
PE1# show mpls forwarding-table

Local  Outgoing    Prefix            Bytes Label  Outgoing   Next Hop
Label  Label       or Tunnel Id      Switched      interface
16     Pop Label   10.0.12.0/30      0             Gi0/0      10.0.12.2
17     Pop Label   10.0.13.0/30      0             Gi0/1      10.0.13.2
18     18          3.3.3.3/32 [T]    2847360       Gi0/0      10.0.12.2
22     22          3.3.3.3/32 [T]    0             Gi0/1      10.0.13.2
```

> `[T]` = entrée TE tunnel. Label 18 sur Gi0/0 = tunnel Tunnel0 (primary). Label 22 sur Gi0/1 = Tunnel1 (bypass).

---

## 5. Test du Fast Reroute / FRR Test

### Simuler une panne / Simulate failure

```
P(config)# interface GigabitEthernet0/0
P(config-if)# shutdown
```

### Observer le basculement sur PE1

```
PE1# show mpls traffic-eng tunnels

Name:PE1_t0                          (Tunnel0) Destination: 3.3.3.3
  Status:
    Admin: up         Oper: up     Path: valid       Signalling: connected
    path option 2, type dynamic (Basis for Setup, path weight 2)  ← BACKUP PATH NOW ACTIVE
```

> `path option 2, type dynamic` indique que le tunnel a basculé sur l'option de chemin dynamique (via BYPASS).
> En FRR réel, le basculement se fait en < 50 ms avant même la reconvergence OSPF.

### Vérifier les logs de basculement

```
PE1# show logging | include Tunnel0|RSVP|FRR
*Apr 15 10:35:22.443: %MPLS_TE-5-TUNNEL_REROUTED: Tunnel0: Fast Rerouted
*Apr 15 10:35:22.451: %MPLS_TE-5-TUNNEL_REROUTED: Tunnel0 rerouted to bypass Tunnel1
```

---

## 6. Récapitulatif de validation / Validation Checklist

| Vérification | Commande | Résultat attendu |
|--------------|----------|-----------------|
| OSPF TE topology complète | `show mpls traffic-eng topology` | Tous les liens avec BW visible |
| Tunnels TE operationnels | `show mpls traffic-eng tunnels brief` | `Oper: up` pour Tunnel0 et Tunnel1 |
| RSVP voisins up | `show ip rsvp neighbors` | `HelloState: UP` pour P et PE2 |
| BW réservée correcte | `show mpls traffic-eng link-management bandwidth-allocation` | 100000 kbps sur Gi0/0 |
| Autoroute injecté | `show ip route 3.3.3.3` | `via Tunnel0` dans la table |
| LFIB populée | `show mpls forwarding-table` | Entrées `[T]` pour les tunnels |
| FRR bascule < 50ms | `shutdown` Gi0/0 sur P | `path option 2, dynamic` actif sur PE1 |
