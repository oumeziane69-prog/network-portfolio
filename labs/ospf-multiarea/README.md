# Lab — OSPF Multi-Area (ABR + LSA Type 3)

## FR | Contexte

OSPF multi-area découpe le domaine de routage en zones distinctes pour limiter
la propagation des LSA de type 1/2 et réduire la charge CPU/mémoire des routeurs
non-ABR. Le **routeur ABR** (Area Border Router) génère des **LSA Type 3**
(Summary Net Link States) pour annoncer les préfixes de chaque area vers les autres.

## EN | Overview

This lab configures a single IOS-XE router as an **OSPF ABR** straddling
**Area 0** (backbone) and **Area 1** (stub extension). The ABR generates
LSA Type 3 inter-area summaries visible in both area LSDBs, confirming
correct multi-area operation.

---

## Device

| Parameter   | Value              |
|-------------|--------------------|
| Platform    | Cat8000v           |
| IOS-XE      | 17.12.2            |
| Router-ID   | 2.2.2.2            |
| OSPF PID    | 1                  |
| Role        | ABR (Area 0 + Area 1) |

---

## Interfaces & Areas

| Interface        | IP / Prefix         | Area   | Type      |
|------------------|---------------------|--------|-----------|
| GigabitEthernet1 | 10.10.20.0/24       | Area 0 | Transit   |
| Loopback2        | 2.2.2.2/32          | Area 0 | Router-ID |
| Loopback20       | 172.16.1.0/24       | Area 1 | Stub net  |
| Loopback200      | 192.168.20.0/24     | Area 1 | Stub net  |

---

## Topology

```
          Area 0 (Backbone)
  +---------------------------------------+
  |  GigabitEthernet1  10.10.20.0/24      |
  |  Loopback2         2.2.2.2/32         |
  |                                       |
  |          R2 (ABR) 2.2.2.2             |
  |                                       |
  +---------------------------------------+
              |  LSA Type 3 inter-area
              |
          Area 1
  +---------------------------------------+
  |  Loopback20        172.16.1.0/24      |
  |  Loopback200       192.168.20.0/24    |
  +---------------------------------------+
```

The ABR floods LSA Type 3 from Area 1 into Area 0 and vice versa.

---

## OSPF Configuration Summary

```
router ospf 1
 router-id 2.2.2.2
 !
 ! Area 0 — backbone
 network 10.10.20.0 0.0.0.255 area 0
 network 2.2.2.2 0.0.0.0     area 0
 !
 ! Area 1 — extension
 network 172.16.1.0 0.0.0.255 area 1
 network 192.168.20.0 0.0.0.255 area 1
```

---

## LSA Type 3 — Inter-Area Verification

### Area 0 LSDB — Summary Net Link States

```
R2# show ip ospf database summary

            OSPF Router with ID (2.2.2.2) (Process ID 1)

                Summary Net Link States (Area 0)

  LS age: ...
  Options: (No TOS-capability, DC, Upward)
  LS Type: Summary Links (Network)
  Link State ID: 172.16.1.0 (summary Network Number)
  Advertising Router: 2.2.2.2
  Network Mask: /24

  LS age: ...
  Link State ID: 192.168.20.0 (summary Network Number)
  Advertising Router: 2.2.2.2
  Network Mask: /24
```

### Area 1 LSDB — Summary Net Link States

```
                Summary Net Link States (Area 1)

  LS age: ...
  Link State ID: 10.10.20.0 (summary Network Number)
  Advertising Router: 2.2.2.2
  Network Mask: /24

  LS age: ...
  Link State ID: 2.2.2.2 (summary Network Number)
  Advertising Router: 2.2.2.2
  Network Mask: /32
```

---

## Verification Commands

```
show ip ospf
show ip ospf interface brief
show ip ospf neighbor
show ip ospf database
show ip ospf database summary
show ip route ospf
```

---

## Lab Result

| Check                                          | Result |
|------------------------------------------------|--------|
| Router-ID 2.2.2.2 active                       | ✅     |
| Gi1 + Lo2 in Area 0                            | ✅     |
| Lo20 + Lo200 in Area 1                         | ✅     |
| ABR role confirmed (show ip ospf)              | ✅     |
| LSA Type 3 generated for Area 1 → Area 0      | ✅     |
| LSA Type 3 generated for Area 0 → Area 1      | ✅     |
| Summary Net Link States verified in both areas | ✅     |

---

## Related Labs

- [OSPF Multi-Area — DevNet variant](../devnet-ospf/)
- [BGP Filtering — prefix-list / route-map](../bgp-filtering/)
- [IP SLA + Object Tracking](../ipsla/)
