# Lab — QoS MQC (LLQ + CBWFQ — Cat8000 IOS-XE)

## Objectif / Objective

**FR** — Configurer et valider une politique QoS basée sur le modèle MQC (Modular QoS CLI) sur un routeur Cisco Catalyst 8000. Le lab couvre la classification du trafic voix et données par ACL, la mise en file d'attente prioritaire (LLQ) pour la voix, la bande passante garantie (CBWFQ) pour les données, et l'application de la politique en sortie sur GigabitEthernet1.

**EN** — Configure and validate a MQC-based (Modular QoS CLI) QoS policy on a Cisco Catalyst 8000 router. The lab covers traffic classification of voice and data via ACLs, priority queuing (LLQ) for voice, guaranteed bandwidth (CBWFQ) for data, and outbound service-policy applied on GigabitEthernet1.

---

## Topologie / Topology

```
                        QoS applied outbound
                        service-policy output
                              │
  [LAN / Source]──────[Cat8000 — R1]──────[WAN / Destination]
                        GigabitEthernet1
                              │
                    ┌─────────┴──────────┐
                    │   Policy-map PM-QOS │
                    ├────────────────────┤
                    │  CM-VOIP  → LLQ    │  priority 128 kbps
                    │  CM-DATA  → CBWFQ  │  bandwidth 256 kbps
                    │  class-default     │  fair-queue
                    └────────────────────┘
```

**Équipement / Device:** 1 × Cisco Catalyst 8000 (IOS-XE)

---

## Classification du trafic / Traffic Classification

| ACL             | Protocole | Port / Critère      | Trafic ciblé          |
|----------------|-----------|---------------------|-----------------------|
| ACL-VOIP        | UDP       | 16384 – 32767       | RTP (voix, vidéo)     |
| ACL-DATA        | TCP       | any                 | Données applicatives  |

| Class-map   | Match type | ACL associée |
|-------------|------------|--------------|
| CM-VOIP     | match-all  | ACL-VOIP     |
| CM-DATA     | match-all  | ACL-DATA     |

---

## Politique QoS / QoS Policy

| Classe         | Mécanisme | Paramètre          | Comportement                        |
|---------------|-----------|--------------------|------------------------------------|
| CM-VOIP       | LLQ       | priority 128 kbps  | File prioritaire stricte — voix    |
| CM-DATA       | CBWFQ     | bandwidth 256 kbps | Bande passante garantie — données  |
| class-default | WFQ       | fair-queue         | Trafic résiduel équitable           |

---

## Configuration IOS-XE complète / Full IOS-XE Config

```ios
! --- ACLs de classification ---
ip access-list extended ACL-VOIP
 permit udp any any range 16384 32767

ip access-list extended ACL-DATA
 permit tcp any any

! --- Class-maps ---
class-map match-all CM-VOIP
 match access-group name ACL-VOIP

class-map match-all CM-DATA
 match access-group name ACL-DATA

! --- Policy-map ---
policy-map PM-QOS
 class CM-VOIP
  priority 128
 class CM-DATA
  bandwidth 256
 class class-default
  fair-queue

! --- Application en sortie sur GigabitEthernet1 ---
interface GigabitEthernet1
 service-policy output PM-QOS
```

La configuration complète est disponible dans [`configs/R1.ios`](configs/R1.ios).

---

## Vérification / Verification

### Politique appliquée sur l'interface / Policy applied on interface

```
R1# show policy-map interface GigabitEthernet1

 GigabitEthernet1

  Service-policy output: PM-QOS

    Class-map: CM-VOIP (match-all)
      0 packets, 0 bytes
      5 minute offered rate 0000 bps, drop rate 0000 bps
      Match: access-group name ACL-VOIP
      Priority: 128 kbps, burst bytes 3200, b/w exceed drops: 0

    Class-map: CM-DATA (match-all)
      0 packets, 0 bytes
      5 minute offered rate 0000 bps, drop rate 0000 bps
      Match: access-group name ACL-DATA
      Queueing
        Output Queue: Conversation 265
        Bandwidth 256 kbps
        (pkts matched/bytes matched) 0/0
        (depth/total drops/no-buffer drops) 0/0/0

    Class-map: class-default (match-any)
      0 packets, 0 bytes
      5 minute offered rate 0000 bps, drop rate 0000 bps
      Match: any
      Fair-queue: per-flow queue limit 64 packets
```

### Vérification des class-maps / Class-map verification

```
R1# show class-map

 Class Map match-all CM-VOIP (id 1)
   Match access-group name ACL-VOIP

 Class Map match-all CM-DATA (id 2)
   Match access-group name ACL-DATA
```

---

## Statut / Status

✅ Terminé — Politique QoS active, `show policy-map interface` confirmé

---

## Technologies utilisées / Technologies Used

| Technologie | Rôle |
|-------------|------|
| Cisco Catalyst 8000 (IOS-XE) | Plateforme de routage principale |
| MQC (Modular QoS CLI) | Framework de configuration QoS IOS-XE |
| LLQ (Low Latency Queuing) | File prioritaire stricte pour la voix (RTP) |
| CBWFQ (Class-Based WFQ) | Bande passante garantie par classe de trafic |
| ACL étendues (Extended ACL) | Classification du trafic par protocole / port |

---

## Concepts couverts / Concepts Covered

- Modèle MQC : ACL → class-map → policy-map → service-policy
- LLQ : priority queue stricte, protection contre la latence et la gigue voix
- CBWFQ : garantie de bande passante minimale par classe
- class-default + fair-queue : traitement équitable du trafic non classifié
- Plage de ports RTP : UDP 16384–32767 (RFC 3550)
- Diagnostic : `show policy-map interface`, `show class-map`, `show policy-map`
