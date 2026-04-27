# Lab — IP SLA + Object Tracking + Floating Static Route

## FR | Contexte

L'IP SLA (Service Level Agreement) est une fonctionnalité IOS/IOS-XE qui mesure la
disponibilité et les performances d'un lien en envoyant des sondes de test en continu.
Couplée à l'**Object Tracking**, elle permet de déclencher automatiquement un basculement
de route (failover) sans intervention humaine.

## EN | Overview

IP SLA probes measure link reachability in real time. Combined with **Object Tracking**
and a **floating static route**, the router automatically switches to a backup path when
the primary link goes down, then restores the primary route when the link recovers.

---

## Topology

```
                        +----------------+
                        |   R1 (IOS-XE)  |
                        +-------+--------+
                                |
               +----------------+----------------+
               |                                 |
       10.10.20.254                         10.10.20.1
     (Primary GW)                         (Backup GW)
     AD = 1 (default)                     AD = 10 (floating)
               |                                 |
               +----------------+----------------+
                                |
                         10.10.20.50
                         (SLA target)
```

---

## IP SLA 1 — ICMP Echo

| Parameter     | Value          |
|---------------|----------------|
| SLA ID        | 1              |
| Type          | icmp-echo      |
| Target IP     | 10.10.20.50    |
| Source IP     | (outbound int) |
| Frequency     | 10 s           |
| Timeout       | 5000 ms        |
| Threshold RTT | 500 ms         |
| Schedule      | start-time now / life forever |

Observed RTT: **~1 ms** (local LAN segment).

---

## Track 1 — IP SLA Reachability

| Parameter   | Value              |
|-------------|--------------------|
| Track ID    | 1                  |
| Object      | ip sla 1           |
| State       | reachability       |
| Status      | **Up** (nominal)   |

When IP SLA 1 stops receiving ICMP replies (link failure or target unreachable),
Track 1 transitions to **Down**, which removes the primary default route and installs
the floating backup.

---

## Routing — Floating Static Route

| Route           | Next-hop      | AD | Condition              |
|-----------------|---------------|----|------------------------|
| 0.0.0.0/0       | 10.10.20.254  | 1  | Active when Track 1 Up |
| 0.0.0.0/0       | 10.10.20.1    | 10 | Floating backup        |

The primary route carries `track 1` — it is withdrawn automatically if Track 1 goes Down.
The floating route (AD 10) has no tracking condition and stays in the RIB only when the
primary route is absent.

---

## Use Case — Automatic Failover

```
Normal state:
  R1 → 0.0.0.0/0 via 10.10.20.254 [1/0]   ← active, Track 1 Up

Primary link failure:
  IP SLA 1: no reply → Track 1 goes Down
  Primary route withdrawn from RIB
  R1 → 0.0.0.0/0 via 10.10.20.1   [10/0]  ← backup activated

Link recovery:
  IP SLA 1: replies resume → Track 1 goes Up
  Primary route re-installed
  R1 → 0.0.0.0/0 via 10.10.20.254 [1/0]   ← primary restored
```

No manual intervention required. Recovery is sub-minute (next SLA probe cycle).

---

## Verification Commands

```
show ip sla statistics 1
show ip sla configuration 1
show track 1
show ip route 0.0.0.0
debug ip routing
```

---

## Lab Result

| Check                              | Result |
|------------------------------------|--------|
| IP SLA 1 configured (icmp-echo)    | ✅     |
| Frequency 10 s / timeout 5000 ms   | ✅     |
| Track 1 bound to SLA 1 reachability| ✅     |
| Track 1 state: Up                  | ✅     |
| Primary route via 10.10.20.254 AD1 | ✅     |
| Floating route via 10.10.20.1 AD10 | ✅     |
| Automatic failover validated       | ✅     |

---

## Related Labs

- [SD-WAN Lite — PBR + IP SLA](../routing/)
- [EEM — event-based automation](../eem/)
