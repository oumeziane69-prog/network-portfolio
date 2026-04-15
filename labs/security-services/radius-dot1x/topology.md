# Topology — RADIUS / 802.1X Lab

## Schéma logique / Logical Diagram

```
  ┌──────────────────────────────────────────────────────────────┐
  │  Server VLAN — 10.0.10.0/24                                  │
  │                                                              │
  │  ┌──────────────────┐    ┌──────────────────┐               │
  │  │  FreeRADIUS      │    │  Active Directory │               │
  │  │  Ubuntu 22.04    │    │  Windows Srv 2022 │               │
  │  │  10.0.10.100/24  │    │  10.0.10.101/24   │               │
  │  └────────┬─────────┘    └──────────┬────────┘               │
  │           │ LDAP (TCP 389/636)       │                       │
  │           └──────────────────────────┘                       │
  └─────────────────────────┬────────────────────────────────────┘
                            │ Trunk (VLAN 10/20/99 + MGMT)
                  ┌─────────┴────────────────┐
                  │  Cisco Catalyst 2960X    │
                  │  (Authenticator 802.1X)  │
                  │  MGMT: 10.0.10.200/24    │
                  │  RADIUS: 10.0.10.100     │
                  └─┬──────┬──────┬──────────┘
                    │      │      │
              Gi0/1  Gi0/2  Gi0/3
              VLAN10 VLAN20 VLAN99 (dynamic, post-auth)
                │      │      │
    ┌───────────┴──┐  ┌─┴──────────────┐  ┌──────────┐
    │ Poste Windows│  │ Imprimante     │  │ Inconnu  │
    │ (Supplicant) │  │ (MAB fallback) │  │ (Guest)  │
    │ EAP-TLS/PEAP │  │ Pas de supp.  │  │ VLAN 99  │
    │ → VLAN 10    │  │ → VLAN 20     │  │          │
    └──────────────┘  └────────────────┘  └──────────┘
```

---

## Plan d'adressage / Addressing Plan

### VLANs

| VLAN | Nom | Réseau | Passerelle | Usage |
|------|-----|--------|-----------|-------|
| 10 | Production | `10.1.10.0/24` | `10.1.10.1` | Postes authentifiés 802.1X (EAP-TLS ou PEAP) |
| 20 | Devices | `10.1.20.0/24` | `10.1.20.1` | Équipements MAB autorisés (imprimantes, IoT) |
| 30 | Auth-Fail | `10.1.30.0/24` | `10.1.30.1` | Échec d'authentification — accès limité |
| 99 | Guest | `10.1.99.0/24` | `10.1.99.1` | Invités / inconnus — Internet seulement |
| 1 | Native/MGMT | `10.0.10.0/24` | `10.0.10.1` | Management réseau + serveurs |

### Serveurs fixes / Fixed Servers

| Hôte | IP | VLAN | Rôle |
|------|----|------|------|
| FreeRADIUS | `10.0.10.100` | MGMT | Serveur RADIUS / AAA |
| Active Directory | `10.0.10.101` | MGMT | LDAP backend EAP-TLS/PEAP |
| Switch Cisco 2960X | `10.0.10.200` | MGMT | NAS / authenticator 802.1X |
| NTP server | `10.0.10.102` | MGMT | Synchronisation temps (critique EAP-TLS) |
| CA (PKI) | `10.0.10.103` | MGMT | Émission certificats EAP-TLS |

---

## Flux d'authentification / Authentication Flows

### Flux 802.1X EAP-TLS (postes managés avec certificat)

```
1. Endpoint connecte → Switch envoie EAP-Request/Identity
2. Endpoint répond avec identité (ex: user@lab.local)
3. Switch encapsule en RADIUS Access-Request → FreeRADIUS
4. FreeRADIUS démarre échange EAP-TLS :
     → Vérification certificat client (signé par CA interne)
     → Vérification certificat serveur RADIUS
5. FreeRADIUS → AD : lookup utilisateur via LDAP
6. SUCCÈS → RADIUS Access-Accept :
     Tunnel-Type = VLAN(13)
     Tunnel-Medium-Type = IEEE-802(6)
     Tunnel-Private-Group-ID = "10"
7. Switch place le port en VLAN 10
```

### Flux MAB (fallback pour imprimantes, IoT)

```
1. Timeout EAP (pas de supplicant) → Switch tente MAB
2. Switch envoie RADIUS Access-Request :
     User-Name = "<MAC-ADDRESS>"  (ex: "00-1A-2B-3C-4D-5E")
     Password  = "<MAC-ADDRESS>"
3. FreeRADIUS compare avec base MAC autorisée
   → MAC connue  → Access-Accept + VLAN 20
   → MAC inconnue → Access-Reject → VLAN 99 (Guest)
```

---

## Méthodes EAP supportées / Supported EAP Methods

| Méthode | Authentification | Sécurité | Usage |
|---------|----------------|---------|-------|
| **EAP-TLS** | Certificats X.509 (client + serveur) | Très haute | Postes managés avec PKI |
| **PEAP-MSCHAPv2** | Login/mot de passe AD (tunnel TLS) | Haute | BYOD ou postes sans PKI |
| **MAB** | Adresse MAC (fallback) | Faible | Équipements sans supplicant |

---

## Équipements simulés / Simulated Equipment

| Équipement | OS/Version | IP | Notes |
|------------|-----------|-----|-------|
| FreeRADIUS server | Ubuntu 22.04 + FreeRADIUS 3.2 | 10.0.10.100 | VM GNS3/EVE-NG |
| Active Directory | Windows Server 2022 | 10.0.10.101 | VM — AD DS + CA |
| Cisco 2960X | Cisco IOS 15.2(7)E | 10.0.10.200 | GNS3 IOS image ou EVE-NG |
| Client Windows 10 | Windows 10 21H2 | DHCP VLAN 10 | Supplicant EAP-TLS |
| Imprimante simulée | Linux (MAC fixe) | DHCP VLAN 20 | Test MAB |
