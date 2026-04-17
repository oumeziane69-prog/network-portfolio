# Lab — DevNet OSPF VPN Sandbox (Cat8kv, 2 Pods)

## Objectif / Objective

**FR** — Valider une adjacence OSPF Area 0 entre deux pods Cisco Catalyst 8000V (IOS XE 17.09.02a) dans le sandbox VPN DevNet. Le lab démontre l'établissement d'une relation de voisinage FULL/DR et l'apprentissage de routes OSPF inter-pods via OpenConnect VPN.

**EN** — Validate an OSPF Area 0 adjacency between two Cisco Catalyst 8000V pods (IOS XE 17.09.02a) in the DevNet VPN Sandbox. The lab demonstrates establishing a FULL/DR neighbor relationship and learning inter-pod OSPF routes over an OpenConnect VPN connection.

---

## Plateforme / Platform

| Paramètre | Valeur |
|-----------|--------|
| Équipement | Cisco Catalyst 8000V (Cat8kv) |
| Version IOS XE | 17.09.02a |
| Pods | pod01 · pod02 |
| Environnement | DevNet VPN Sandbox |
| Accès | OpenConnect VPN → devbox SSH → telnet 2222 / 2223 |

---

## Accès au sandbox / Sandbox Access

```
[Poste local]
    │
    │  OpenConnect VPN  (anyconnect-devnet.cisco.com)
    ▼
[devbox]  <IP-DEVBOX-HERE>
    │
    ├─ telnet 127.0.0.1 2222  ──►  pod01  (IOS XE 17.09.02a)
    └─ telnet 127.0.0.1 2223  ──►  pod02  (IOS XE 17.09.02a)
```

**Étapes de connexion / Connection steps:**

1. Se connecter au VPN DevNet avec OpenConnect :
   ```
   sudo openconnect <VPN-HOST-HERE> --user=<USERNAME-HERE>
   ```
2. Se connecter en SSH à la devbox :
   ```
   ssh developer@<IP-DEVBOX-HERE>
   ```
3. Accéder aux pods via telnet :
   ```
   telnet 127.0.0.1 2222   # pod01
   telnet 127.0.0.1 2223   # pod02
   ```

---

## Topologie / Topology

```
        OSPF Area 0 (PID 1)
        ─────────────────────────────────────
        pod01                    pod02
     router-id 1.1.1.1        router-id 2.2.2.2
                                          
  Lo0 1.1.1.1/32            Lo0 2.2.2.2/32
        │                          │
  Gi1 192.168.100.1/30 ─── Gi1 192.168.100.2/30
        │                          │
        └──── Segment broadcast ───┘
               (DR: pod01 · BDR: pod02)
```

---

## Adressage / Addressing

| Équipement | Interface | Adresse IP | Masque | OSPF Area |
|-----------|-----------|-----------|--------|-----------|
| pod01 | Loopback0 | 1.1.1.1 | /32 | Area 0 |
| pod01 | GigabitEthernet1 | 192.168.100.1 | /30 | Area 0 |
| pod02 | Loopback0 | 2.2.2.2 | /32 | Area 0 |
| pod02 | GigabitEthernet1 | 192.168.100.2 | /30 | Area 0 |

---

## Configuration appliquée / Applied Configuration

Voir / See: [`ospf_config.txt`](ospf_config.txt)

**pod01 (extrait / excerpt):**
```
interface Loopback0
 ip address 1.1.1.1 255.255.255.255
!
interface GigabitEthernet1
 ip address 192.168.100.1 255.255.255.252
 ip ospf 1 area 0
!
router ospf 1
 router-id 1.1.1.1
 network 1.1.1.1 0.0.0.0 area 0
```

**pod02 (extrait / excerpt):**
```
interface Loopback0
 ip address 2.2.2.2 255.255.255.255
!
interface GigabitEthernet1
 ip address 192.168.100.2 255.255.255.252
 ip ospf 1 area 0
!
router ospf 1
 router-id 2.2.2.2
 network 2.2.2.2 0.0.0.0 area 0
```

---

## Commandes de vérification / Verification Commands

```
show ip ospf neighbor
show ip ospf interface GigabitEthernet1
show ip route ospf
show ip ospf database
```

### Résultats obtenus / Observed Results

**`show ip ospf neighbor` sur pod01 / on pod01:**

```
Neighbor ID     Pri   State           Dead Time   Address         Interface
2.2.2.2           1   FULL/DR         00:00:39    192.168.100.2   GigabitEthernet1
```

> Adjacence FULL/DR établie — pod02 est DR, pod01 est BDR.
> FULL/DR adjacency established — pod02 is DR, pod01 is BDR.

**`show ip route ospf` sur pod01 / on pod01:**

```
O        2.2.2.2 [110/2] via 192.168.100.2, 00:05:14, GigabitEthernet1
```

> Route OSPF 2.2.2.2/32 apprise avec distance administrative 110, métrique 2.
> OSPF route 2.2.2.2/32 learned with administrative distance 110, metric 2.

---

## Statut / Status

Complété — adjacence FULL/DR validée, route O 2.2.2.2 [110/2] apprise sur pod01.

---

## Technologies utilisées / Technologies Used

| Technologie | Rôle |
|-------------|------|
| Cisco Cat8kv | Plateforme de routage virtuelle cloud-native |
| IOS XE 17.09.02a | Système d'exploitation |
| OSPFv2 | Protocole IGP link-state (Area 0) |
| OpenConnect VPN | Accès sécurisé au sandbox DevNet |
| DevNet VPN Sandbox | Environnement de lab Cisco multi-pods |
| SSH / Telnet | Accès aux pods via devbox |
