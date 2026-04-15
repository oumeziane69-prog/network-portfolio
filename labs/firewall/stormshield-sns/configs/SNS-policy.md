# Stormshield SNS — Security Policy (stcli syntax)
# Stormshield Network Security — Filter Policy, NAT, VPN, and Services

> **Platform:** Stormshield SNS 4.x (SN710 ou SN2100)
> **Interface:** stcli (CLI SNS) — équivalent à la GUI SN Console
> **Contexte:** Périmètre DMZ avec zones External / DMZ / Internal — contexte CNPE EDF (souveraineté ANSSI)

---

## 1. Objects réseau / Network Objects

```bash
# ── Hosts ──────────────────────────────────────────────────────
CONFIG OBJECT HOST NEW name=Web-Server ip=172.16.50.10 comment="Serveur web DMZ"
CONFIG OBJECT HOST NEW name=SMTP-Relay ip=172.16.50.20 comment="Relai SMTP DMZ"
CONFIG OBJECT HOST NEW name=AD-Server ip=10.0.50.20 comment="Active Directory interne"
CONFIG OBJECT HOST NEW name=SMS-Host ip=10.0.50.10 comment="Station management"
CONFIG OBJECT HOST NEW name=NMS-Server ip=10.0.50.50 comment="Serveur supervision SNMP"

# ── Networks ───────────────────────────────────────────────────
CONFIG OBJECT NETWORK NEW name=Net-Internal ip=10.0.50.0 mask=255.255.255.0
CONFIG OBJECT NETWORK NEW name=Net-DMZ ip=172.16.50.0 mask=255.255.255.0
CONFIG OBJECT NETWORK NEW name=VPN-Pool ip=192.168.10.0 mask=255.255.255.0 comment="Pool SSL VPN"

# ── Interface objects (automatic from interfaces) ─────────────
# external (out) : WAN interface  → auto-object "Firewall_out"
# dmz            : DMZ interface  → auto-object "Firewall_dmz"
# internal (in)  : LAN interface  → auto-object "Firewall_in"
```

---

## 2. Services personnalisés / Custom Services

```bash
# OPC-UA (industrial)
CONFIG OBJECT SERVICE NEW name=OPC-UA proto=tcp dport=4840:4843 comment="OPC-UA (4840 plain, 4843 TLS)"

# LDAPS
CONFIG OBJECT SERVICE NEW name=LDAPS proto=tcp dport=636 comment="LDAP over SSL"

# SNMPv3
CONFIG OBJECT SERVICE NEW name=SNMPv3 proto=udp dport=161 comment="SNMPv3 management"
CONFIG OBJECT SERVICE NEW name=SNMP-Trap proto=udp dport=162 comment="SNMP traps"

# SIC Check Point (si coexistence avec SMS externe)
CONFIG OBJECT SERVICE NEW name=SIC proto=tcp dport=18211 comment="Check Point SIC"
```

---

## 3. Filter Policy / Politique de filtrage

> **Note SNS:** Les règles SNS sont numérotées explicitement. La politique est appliquée ligne par ligne (first-match). L'implicit deny est activé par défaut en fin de politique.

```bash
# ── Activer la politique de filtrage ──────────────────────────
CONFIG FILTER POLICY ACTIVATE name=Politique-1

# ── Règle 1 : Admin SSH → Firewall (accès management) ─────────
CONFIG FILTER RULE NEW \
  idx=1 \
  name="Admin-SSH-to-FW" \
  state=on \
  action=pass \
  log=yes \
  srcnet=SMS-Host \
  dstnet=Firewall_in \
  proto=tcp \
  dport=22 \
  comment="Admin SSH vers interface interne SNS"

# ── Règle 2 : Admin HTTPS → GUI SNS ───────────────────────────
CONFIG FILTER RULE NEW \
  idx=2 \
  name="Admin-HTTPS-GUI" \
  state=on \
  action=pass \
  log=yes \
  srcnet=SMS-Host \
  dstnet=Firewall_in \
  proto=tcp \
  dport=443 \
  comment="Accès interface GUI SNS depuis SMS"

# ── Règle 3 : LAN → Internet (HTTP/HTTPS/DNS) ─────────────────
CONFIG FILTER RULE NEW \
  idx=3 \
  name="LAN-to-Internet" \
  state=on \
  action=pass \
  log=yes \
  inspection=on \
  srcnet=Net-Internal \
  dstnet=Internet \
  service=http,https,domain \
  comment="Accès Internet LAN interne — inspection ASQ active"

# ── Règle 4 : Internet → Serveur Web (HTTPS) ──────────────────
CONFIG FILTER RULE NEW \
  idx=4 \
  name="Internet-to-WebServer-HTTPS" \
  state=on \
  action=pass \
  log=yes \
  inspection=on \
  alarm=high \
  srcnet=any \
  dstnet=Web-Server \
  proto=tcp \
  dport=443 \
  comment="Exposition HTTPS Web-Server — IPS actif"

# ── Règle 5 : Internet → SMTP Relay ───────────────────────────
CONFIG FILTER RULE NEW \
  idx=5 \
  name="Internet-to-SMTP-Relay" \
  state=on \
  action=pass \
  log=yes \
  srcnet=any \
  dstnet=SMTP-Relay \
  proto=tcp \
  dport=25,465 \
  comment="Mail entrant SMTP/SMTPS"

# ── Règle 6 : LAN → DMZ HTTPS ─────────────────────────────────
CONFIG FILTER RULE NEW \
  idx=6 \
  name="LAN-to-DMZ-HTTPS" \
  state=on \
  action=pass \
  log=yes \
  srcnet=Net-Internal \
  dstnet=Net-DMZ \
  proto=tcp \
  dport=443 \
  comment="LAN interne → apps DMZ en HTTPS"

# ── Règle 7 : Admin SSH → DMZ (depuis SMS uniquement) ─────────
CONFIG FILTER RULE NEW \
  idx=7 \
  name="Admin-SSH-to-DMZ" \
  state=on \
  action=pass \
  log=yes \
  alarm=medium \
  srcnet=SMS-Host \
  dstnet=Net-DMZ \
  proto=tcp \
  dport=22 \
  comment="SSH admin vers DMZ — limité à SMS"

# ── Règle 8 : Web-Server → AD (LDAP auth) ─────────────────────
CONFIG FILTER RULE NEW \
  idx=8 \
  name="WebServer-to-AD-LDAP" \
  state=on \
  action=pass \
  log=yes \
  srcnet=Web-Server \
  dstnet=AD-Server \
  service=ldap,LDAPS \
  comment="Web server → AD : authentification LDAP"

# ── Règle 9 : SNMP supervision ────────────────────────────────
CONFIG FILTER RULE NEW \
  idx=9 \
  name="SNMP-Monitoring" \
  state=on \
  action=pass \
  log=yes \
  srcnet=NMS-Server \
  dstnet=Firewall_in \
  service=SNMPv3 \
  comment="NMS → SNS : supervision SNMPv3"

# ── Règle 10 : ICMP monitoring (SMS → any) ────────────────────
CONFIG FILTER RULE NEW \
  idx=10 \
  name="ICMP-Monitoring" \
  state=on \
  action=pass \
  log=no \
  srcnet=SMS-Host \
  dstnet=any \
  proto=icmp \
  comment="Ping monitoring depuis poste admin"

# ── Règle 11 : DENY DMZ → LAN (isolation DMZ) ────────────────
CONFIG FILTER RULE NEW \
  idx=11 \
  name="DENY-DMZ-to-LAN" \
  state=on \
  action=block \
  log=yes \
  alarm=high \
  srcnet=Net-DMZ \
  dstnet=Net-Internal \
  service=any \
  comment="La DMZ ne doit pas initier vers le réseau interne"

# ── Règle 12 : DENY Internet → LAN ────────────────────────────
CONFIG FILTER RULE NEW \
  idx=12 \
  name="DENY-Internet-to-LAN" \
  state=on \
  action=block \
  log=yes \
  alarm=high \
  srcnet=any \
  dstnet=Net-Internal \
  service=any \
  comment="Protection réseau interne depuis Internet"

# ── Règle 99 : CLEANUP — tout le reste bloqué et journalisé ───
CONFIG FILTER RULE NEW \
  idx=99 \
  name="CLEANUP-DENY-ALL" \
  state=on \
  action=block \
  log=yes \
  alarm=high \
  srcnet=any \
  dstnet=any \
  service=any \
  comment="Règle implicite finale — tout flux non listé bloqué et alerté"
```

---

## 4. NAT Rules / Règles de translation

```bash
# ── SNAT — LAN → Internet (masquerade derrière IP externe) ────
CONFIG NAT RULE NEW \
  idx=1 \
  name="SNAT-LAN-to-Internet" \
  state=on \
  action=nat \
  srcnet=Net-Internal \
  dstnet=Internet \
  nat-source=Firewall_out \
  comment="SNAT (PAT) : LAN interne → Internet via IP externe"

# ── DNAT — Internet → Web Server ──────────────────────────────
CONFIG NAT RULE NEW \
  idx=2 \
  name="DNAT-WebServer-HTTPS" \
  state=on \
  action=nat \
  srcnet=any \
  dstnet=Firewall_out \
  proto=tcp \
  dport=443 \
  nat-dest=Web-Server \
  nat-dport=443 \
  comment="DNAT : HTTPS entrant → Web-Server DMZ"

# ── DNAT — Internet → SMTP Relay ──────────────────────────────
CONFIG NAT RULE NEW \
  idx=3 \
  name="DNAT-SMTP-Relay" \
  state=on \
  action=nat \
  srcnet=any \
  dstnet=Firewall_out \
  proto=tcp \
  dport=25 \
  nat-dest=SMTP-Relay \
  nat-dport=25 \
  comment="DNAT : SMTP entrant → relai SMTP DMZ"
```

---

## 5. VPN IPSec IKEv2 (site-à-site)

```bash
# ── Phase 1 (IKEv2) ───────────────────────────────────────────
CONFIG VPN IKEV2 PHASE1 NEW \
  name="VPN-Site-B" \
  peeraddr=<SITE-B-IP-HERE> \
  auth=preshared \
  psk=<PSK-HERE> \
  encryption=aes256gcm \
  integrity=sha256 \
  dhgroup=14 \
  lifetime=86400 \
  dpd=enable \
  dpd-delay=30 \
  comment="VPN site-à-site IKEv2 vers Site-B"

# ── Phase 2 (IPSec) ────────────────────────────────────────────
CONFIG VPN IKEV2 PHASE2 NEW \
  name="VPN-Site-B-P2" \
  phase1=VPN-Site-B \
  localnet=Net-Internal \
  remotenet=<SITE-B-NET-HERE> \
  encryption=aes256gcm \
  integrity=sha256 \
  lifetime=3600 \
  pfs=enable \
  dhgroup=14 \
  comment="Phase 2 : trafic LAN-Internal vers réseau Site-B"
```

---

## 6. SSL VPN (accès nomades)

```bash
# ── SSL VPN configuration ─────────────────────────────────────
CONFIG SSLVPN PORTAL NEW \
  name="Portal-Nomades" \
  address=<CLUSTER-EXT-IP-HERE> \
  port=443 \
  auth=ldap \
  ldap-server=AD-Server \
  pool=VPN-Pool \
  comment="Portail SSL VPN pour accès nomades"

# ── Règle firewall pour VPN SSL ───────────────────────────────
CONFIG FILTER RULE NEW \
  idx=15 \
  name="SSL-VPN-to-LAN" \
  state=on \
  action=pass \
  log=yes \
  srcnet=VPN-Pool \
  dstnet=Net-Internal \
  service=https,rdp,ssh \
  comment="Accès VPN nomades → LAN interne (HTTPS, RDP, SSH)"
```

---

## 7. LDAP / Active Directory Authentication

```bash
# ── Référentiel LDAP ──────────────────────────────────────────
CONFIG AUTH LDAP NEW \
  name="AD-Corp" \
  server=AD-Server \
  port=636 \
  ssl=yes \
  base="DC=lab,DC=local" \
  bind-dn="CN=svc-sns,OU=ServiceAccounts,DC=lab,DC=local" \
  bind-pw=<LDAP-BIND-PWD-HERE> \
  search-filter="(&(objectClass=user)(memberOf=CN=FW-Users,OU=Groupes,DC=lab,DC=local))" \
  comment="Authentification LDAP Active Directory pour portail SSL VPN"

# ── Test de connexion LDAP ────────────────────────────────────
AUTH LDAP TEST server=AD-Corp user=testuser password=<TEST-PASS-HERE>
# Expected: Authentication successful
```

---

## 8. SNMPv3

```bash
# ── SNMPv3 configuration ──────────────────────────────────────
CONFIG SNMP AGENT NEW \
  version=v3 \
  location="Salle-Reseau-A" \
  contact="noc@site-a.local" \
  community=<SNMP-COMMUNITY-HERE>

CONFIG SNMP USER NEW \
  name=snmpv3-nms \
  auth=sha \
  auth-pass=<SNMP-AUTH-PASS-HERE> \
  priv=aes128 \
  priv-pass=<SNMP-PRIV-PASS-HERE> \
  comment="Utilisateur SNMPv3 pour NMS"

CONFIG SNMP TRAP NEW \
  dest=NMS-Server \
  port=162 \
  user=snmpv3-nms \
  version=v3 \
  comment="Envoi de traps SNMPv3 vers NMS"
```

---

## 9. Syslog / Journalisation

```bash
# ── Syslog vers SIEM ──────────────────────────────────────────
CONFIG LOG SYSLOG NEW \
  name="SIEM-Central" \
  dest=10.0.50.100 \
  port=514 \
  proto=tcp \
  format=syslog \
  level=info \
  comment="Export syslog vers SIEM central"

# ── Audit logs ────────────────────────────────────────────────
CONFIG LOG AUDIT enable
# Active le journal d'audit des actions admin sur le SNS

# ── Niveaux de log par règle ──────────────────────────────────
# Voir log=yes / log=no dans les règles ci-dessus
# alarm=high → alerte immédiate (SNMP trap + syslog priority=crit)
# alarm=medium → alerte différée (buffer 60s)
```
