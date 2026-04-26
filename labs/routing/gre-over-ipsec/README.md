# Lab — GRE over IPSec (IKEv2 — AES-256)

## Objectif / Objective

**FR** — Mettre en oeuvre un tunnel GRE chiffré par IPSec (mode transport, IKEv2) entre deux routeurs Cisco IOS-XE. Le lab couvre la négociation IKEv2 avec clé pré-partagée, le profil IPSec en mode transport associé à l'interface Tunnel0, et la validation de la connectivité via le tunnel chiffré.

**EN** — Deploy a GRE tunnel encrypted by IPSec (transport mode, IKEv2) between two Cisco IOS-XE routers. The lab covers IKEv2 negotiation with pre-shared key, IPSec transport-mode profile bound to Tunnel0, and connectivity validation across the encrypted tunnel.

---

## Topologie / Topology

```
        Underlay — 10.10.20.0/24
  ┌──────────────────────────────────────────┐
  │                                          │
[R1]                                        [R2]
Gi1: 10.10.20.102/24              Gi1: 10.10.20.103/24
Tu0: 172.16.0.1/30                Tu0: 172.16.0.2/30
  │                                          │
  └══════════════════════════════════════════┘
       GRE Tunnel0 (172.16.0.0/30)
       Protected by IPSec IKEv2 + ESP
```

**Équipements / Devices:** 2 × Cisco IOS-XE — simulation sur pont virtuel

---

## Adressage / Addressing

| Interface         | Router | Adresse IP         | Rôle                   |
|------------------|--------|--------------------|------------------------|
| GigabitEthernet1  | R1     | 10.10.20.102/24    | Underlay (transport)   |
| GigabitEthernet1  | R2     | 10.10.20.103/24    | Underlay (transport)   |
| Tunnel0           | R1     | 172.16.0.1/30      | GRE overlay endpoint   |
| Tunnel0           | R2     | 172.16.0.2/30      | GRE overlay endpoint   |

---

## Paramètres IKEv2 / IKEv2 Parameters

| Paramètre        | Valeur              |
|-----------------|---------------------|
| Encryption       | AES-CBC-256         |
| Integrity        | SHA-256             |
| DH Group         | Group 14 (2048-bit) |
| Authentication   | Pre-Shared Key (PSK)|
| Lifetime SA      | Default (86400 s)   |

## Paramètres IPSec / IPSec Parameters

| Paramètre        | Valeur                  |
|-----------------|-------------------------|
| Protocol         | ESP                     |
| Encryption       | esp-aes 256             |
| Integrity        | esp-sha256-hmac         |
| Mode             | Transport               |
| Profile binding  | Tunnel0 (GRE interface) |

---

## Configuration

### R1 — 10.10.20.102

```ios
! --- IKEv2 ---
crypto ikev2 proposal GRE-IPSEC-PROP
 encryption aes-cbc-256
 integrity sha256
 group 14
!
crypto ikev2 policy GRE-IPSEC-POL
 proposal GRE-IPSEC-PROP
!
crypto ikev2 keyring GRE-IPSEC-KR
 peer R2
  address 10.10.20.103
  pre-shared-key <PSK-HERE>
!
crypto ikev2 profile GRE-IPSEC-PROF
 match identity remote address 10.10.20.103 255.255.255.255
 authentication remote pre-share
 authentication local pre-share
 keyring local GRE-IPSEC-KR
!
! --- IPSec ---
crypto ipsec transform-set GRE-TS esp-aes 256 esp-sha256-hmac
 mode transport
!
crypto ipsec profile GRE-IPSEC-PROFILE
 set transform-set GRE-TS
 set ikev2-profile GRE-IPSEC-PROF
!
! --- Interfaces ---
interface GigabitEthernet1
 ip address 10.10.20.102 255.255.255.0
 no shutdown
!
interface Tunnel0
 ip address 172.16.0.1 255.255.255.252
 tunnel source GigabitEthernet1
 tunnel destination 10.10.20.103
 tunnel protection ipsec profile GRE-IPSEC-PROFILE
```

### R2 — 10.10.20.103

```ios
! --- IKEv2 ---
crypto ikev2 proposal GRE-IPSEC-PROP
 encryption aes-cbc-256
 integrity sha256
 group 14
!
crypto ikev2 policy GRE-IPSEC-POL
 proposal GRE-IPSEC-PROP
!
crypto ikev2 keyring GRE-IPSEC-KR
 peer R1
  address 10.10.20.102
  pre-shared-key <PSK-HERE>
!
crypto ikev2 profile GRE-IPSEC-PROF
 match identity remote address 10.10.20.102 255.255.255.255
 authentication remote pre-share
 authentication local pre-share
 keyring local GRE-IPSEC-KR
!
! --- IPSec ---
crypto ipsec transform-set GRE-TS esp-aes 256 esp-sha256-hmac
 mode transport
!
crypto ipsec profile GRE-IPSEC-PROFILE
 set transform-set GRE-TS
 set ikev2-profile GRE-IPSEC-PROF
!
! --- Interfaces ---
interface GigabitEthernet1
 ip address 10.10.20.103 255.255.255.0
 no shutdown
!
interface Tunnel0
 ip address 172.16.0.2 255.255.255.252
 tunnel source GigabitEthernet1
 tunnel destination 10.10.20.102
 tunnel protection ipsec profile GRE-IPSEC-PROFILE
```

> **Note sécurité / Security note:** Remplacer `<PSK-HERE>` par une valeur tirée d'un fichier `.env` non commité. Ne jamais commiter de clé PSK réelle dans le dépôt.

Les configs complètes sont disponibles dans [`configs/R1.ios`](configs/R1.ios) et [`configs/R2.ios`](configs/R2.ios).

---

## Vérification / Verification

### IKEv2 SA — État READY / IKEv2 SA — READY State

```
R1# show crypto ikev2 sa

 IPv4 Crypto IKEv2  SA

Tunnel-id Local                 Remote                fvrf/ivrf            Status
1         10.10.20.102/500      10.10.20.103/500      none/none            READY
      Encr: AES-CBC, keysize: 256, PRF: SHA256, Hash: SHA256, DH Grp:14, Auth sign: PSK, Auth verify: PSK
      Life/Active Time: 86400/xxx sec
```

### Ping Tunnel / Tunnel Ping (5/5)

```
R1# ping 172.16.0.2 source Tunnel0 repeat 5

Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 172.16.0.2, timeout is 2 seconds:
Packet sent with a source address of 172.16.0.1
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/2/3 ms
```

### Compteurs ESP / ESP Counters

```
R1# show crypto ipsec sa | include encaps|decaps

    #pkts encaps: 5, #pkts encrypt: 5, #pkts digest: 5
    #pkts decaps: 5, #pkts decrypt: 5, #pkts verify: 5
```

---

## Statut / Status

✅ Terminé — Tunnel GRE/IPSec fonctionnel, IKEv2 SA READY, ping 5/5

---

## Technologies utilisées / Technologies Used

| Technologie | Rôle |
|-------------|------|
| Cisco IOS-XE | Plateforme de routage principale |
| GRE (Generic Routing Encapsulation) | Tunnel overlay point-à-point |
| IKEv2 (RFC 7296) | Négociation et gestion des SA IPSec |
| IPSec ESP — mode transport | Chiffrement AES-256 + intégrité SHA-256 |
| Tunnel protection profile | Liaison GRE ↔ IPSec sur IOS-XE |

---

## Concepts couverts / Concepts Covered

- Architecture GRE over IPSec : underlay / overlay, mode transport vs tunnel
- IKEv2 : proposal, policy, keyring PSK, profil d'identité remote
- IPSec transform-set : ESP AES-256 + SHA-256-HMAC, mode transport
- `tunnel protection ipsec profile` — binding entre Tunnel0 et le profil IPSec
- Diagnostic : `show crypto ikev2 sa`, `show crypto ipsec sa`, ping source Tunnel0
- Sécurité : utilisation de placeholders PSK, pas de clés réelles en dépôt
