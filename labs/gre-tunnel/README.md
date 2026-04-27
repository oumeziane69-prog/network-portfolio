# Lab — GRE Tunnel (L3 Transport + OSPF Inter-Site)

## FR | Contexte

GRE (Generic Routing Encapsulation) est un protocole de tunneling L3 qui encapsule
n'importe quel protocole réseau dans un paquet IP. Il permet de faire circuler
des protocoles de routage comme **OSPF** entre deux sites séparés par un réseau
qui ne les supporte pas nativement.

## EN | Overview

This lab configures a **GRE tunnel** between two IOS-XE routers over an IP underlay.
The tunnel interface carries OSPF adjacency traffic, enabling inter-site L3 routing
without VPN overhead. The tunnel is verified up/up with correct MTU and encapsulation.

---

## Device

| Parameter   | Value           |
|-------------|-----------------|
| Platform    | Cat8000v        |
| IOS-XE      | 17.12.2         |
| Role        | GRE tunnel head |

---

## Addressing

| Interface        | IP / Prefix         | Role                     |
|------------------|---------------------|--------------------------|
| GigabitEthernet1 | 10.10.20.48/24      | Underlay (tunnel source) |
| Tunnel0          | 192.168.100.1/30    | GRE overlay              |
| Remote peer      | 10.10.20.50         | Tunnel destination       |

---

## Topology

```
Site A                          IP Underlay                    Site B
+------------------+       10.10.20.0/24 (Gi1)       +------------------+
|  R1              |                                   |  R2              |
|  Gi1: 10.10.20.48|================================>|  Gi1: 10.10.20.50|
|  Tu0: 192.168.   |  <------- GRE Tunnel0 -------->  |  Tu0: 192.168.   |
|       100.1/30   |                                   |       100.2/30   |
+------------------+                                   +------------------+
         |                                                      |
         +------------------ OSPF (over GRE) ------------------+
```

### GRE Encapsulation

```
Outer IP header  | GRE header | Inner IP packet (OSPF / data)
src 10.10.20.48    dst 10.10.20.50
```

MTU = 1500 − 20 (outer IP) − 4 (GRE) = **1476 bytes**

---

## Tunnel0 Parameters

| Parameter          | Value             |
|--------------------|-------------------|
| IP address         | 192.168.100.1/30  |
| Tunnel source      | GigabitEthernet1  |
| Tunnel destination | 10.10.20.50       |
| Tunnel mode        | gre ip (default)  |
| MTU                | 1476 bytes        |
| Status             | up/up             |

---

## OSPF over GRE

Adding the tunnel interface to an OSPF area allows full routing protocol
adjacency across the underlay without any native multicast or routing support
from the transit network.

```
router ospf 1
 router-id 1.1.1.1
 network 192.168.100.0 0.0.0.3 area 0
 network 10.10.20.0   0.0.0.255 area 0
```

---

## Verification Commands

```
show interfaces tunnel 0
show ip interface tunnel 0
show ip route
show ip ospf neighbor
ping 192.168.100.2 source tunnel 0
```

---

## Expected Output

```
R1# show interfaces tunnel 0
Tunnel0 is up, line protocol is up
  Hardware is Tunnel
  Internet address is 192.168.100.1/30
  MTU 17916 bytes, BW 100 Kbit/sec, DLY 50000 usec,
  Tunnel source 10.10.20.48 (GigabitEthernet1), destination 10.10.20.50
  Tunnel protocol/transport GRE/IP
  Tunnel TTL 255, Fast tunneling enabled
  Tunnel transport MTU 1476 bytes
  ...

R1# show ip ospf neighbor
Neighbor ID   Pri  State    Dead Time  Address         Interface
2.2.2.2         1  FULL/DR  00:00:37   192.168.100.2   Tunnel0
```

---

## Lab Result

| Check                                        | Result |
|----------------------------------------------|--------|
| Tunnel0 configured (source Gi1, dest .50)    | ✅     |
| Tunnel IP 192.168.100.1/30                   | ✅     |
| Protocol GRE/IP confirmed                    | ✅     |
| MTU 1476 bytes                               | ✅     |
| Tunnel0 status: up/up                        | ✅     |
| OSPF neighbor FULL over tunnel               | ✅     |
| Ping 192.168.100.2 source Tunnel0 OK         | ✅     |

---

## Related Labs

- [GRE over IPSec](../routing/gre-over-ipsec/)
- [OSPF Multi-Area — ABR + LSA Type 3](../ospf-multiarea/)
- [IP SLA + Object Tracking](../ipsla/)
