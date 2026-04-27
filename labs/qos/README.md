# Lab — QoS MQC (Modular QoS CLI)

## FR | Contexte

Le **MQC** (Modular QoS CLI) est le framework IOS/IOS-XE standard pour appliquer
des politiques de qualité de service. Il s'articule en trois étapes :
1. **class-map** — classification du trafic
2. **policy-map** — actions QoS (priorité, bande passante, file d'attente)
3. **service-policy** — attachement à une interface

## EN | Overview

This lab classifies three traffic types (Management, BGP, ICMP) with **class-maps**,
applies per-class bandwidth guarantees and strict priority via a **policy-map**, then
attaches the policy outbound on GigabitEthernet1. Verified on Cat8000v IOS-XE 17.12.2.

---

## Device

| Parameter | Value       |
|-----------|-------------|
| Platform  | Cat8000v    |
| IOS-XE    | 17.12.2     |
| Interface | GigabitEthernet1 (output) |

---

## Class-Maps

| Class-Map        | Match Criterion                        | Description              |
|------------------|----------------------------------------|--------------------------|
| CM-MANAGEMENT    | ACL: TCP port 22 (SSH) + 830 (NETCONF) | Management plane traffic |
| CM-BGP           | protocol bgp                           | BGP control plane        |
| CM-ICMP          | protocol icmp                          | ICMP / OAM traffic       |
| class-default    | (everything else)                      | Best-effort              |

### ACL for CM-MANAGEMENT

```
ip access-list extended ACL-MANAGEMENT
 permit tcp any any eq 22
 permit tcp any any eq 830
```

---

## Policy-Map — PM-QOS

| Class            | Action                    | Bandwidth / Priority |
|------------------|---------------------------|----------------------|
| CM-MANAGEMENT    | priority                  | 20 % of link speed   |
| CM-BGP           | bandwidth remaining percent | 30 %               |
| CM-ICMP          | bandwidth remaining percent | 10 %               |
| class-default    | fair-queue                | remaining bandwidth  |

```
policy-map PM-QOS
 class CM-MANAGEMENT
  priority percent 20
 class CM-BGP
  bandwidth remaining percent 30
 class CM-ICMP
  bandwidth remaining percent 10
 class class-default
  fair-queue
```

---

## Service-Policy Attachment

```
interface GigabitEthernet1
 service-policy output PM-QOS
```

---

## QoS Flow Diagram

```
Outbound traffic on GigabitEthernet1
         │
         ▼
   ┌─────────────────────────────────────────────┐
   │  Scheduler (PM-QOS)                         │
   │                                             │
   │  ┌──────────────────┐  priority (20%)       │
   │  │  CM-MANAGEMENT   │  SSH/NETCONF strict   │
   │  └──────────────────┘                       │
   │  ┌──────────────────┐  bandwidth rem. 30%   │
   │  │  CM-BGP          │  BGP control plane    │
   │  └──────────────────┘                       │
   │  ┌──────────────────┐  bandwidth rem. 10%   │
   │  │  CM-ICMP         │  ICMP / OAM           │
   │  └──────────────────┘                       │
   │  ┌──────────────────┐  fair-queue (rest)    │
   │  │  class-default   │  best-effort          │
   │  └──────────────────┘                       │
   └─────────────────────────────────────────────┘
         │
         ▼
   GigabitEthernet1 (egress)
```

---

## Verification Commands

```
show policy-map interface GigabitEthernet1
show class-map
show policy-map PM-QOS
show ip access-lists ACL-MANAGEMENT
```

---

## Expected Output (excerpt)

```
R1# show policy-map interface GigabitEthernet1
 GigabitEthernet1

  Service-policy output: PM-QOS

    Class-map: CM-MANAGEMENT (match-all)
      0 packets, 0 bytes
      5 minute offered rate 0000 bps, drop rate 0000 bps
      Match: access-group name ACL-MANAGEMENT
      Priority: 20% (200000 kbps), burst bytes 5000000,
      Priority Level: 1

    Class-map: CM-BGP (match-all)
      0 packets, 0 bytes
      5 minute offered rate 0000 bps, drop rate 0000 bps
      Match: protocol bgp
      Bandwidth remaining 30%

    Class-map: CM-ICMP (match-all)
      0 packets, 0 bytes
      5 minute offered rate 0000 bps, drop rate 0000 bps
      Match: protocol icmp
      Bandwidth remaining 10%

    Class-map: class-default (match-any)
      Fair-queue
```

---

## Lab Result

| Check                                          | Result |
|------------------------------------------------|--------|
| ACL-MANAGEMENT matches port 22 + 830           | ✅     |
| CM-MANAGEMENT class-map (ACL match)            | ✅     |
| CM-BGP class-map (protocol bgp)               | ✅     |
| CM-ICMP class-map (protocol icmp)             | ✅     |
| PM-QOS: priority 20% MGMT                     | ✅     |
| PM-QOS: bandwidth remaining 30% BGP           | ✅     |
| PM-QOS: bandwidth remaining 10% ICMP          | ✅     |
| PM-QOS: fair-queue default                    | ✅     |
| service-policy output on GigabitEthernet1     | ✅     |

---

## Related Labs

- [SD-WAN Lite — PBR + IP SLA](../routing/sdwan-lite/)
- [IP SLA + Object Tracking](../ipsla/)
- [EEM — event-based automation](../eem/)
