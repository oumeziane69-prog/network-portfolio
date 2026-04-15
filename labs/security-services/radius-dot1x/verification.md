# 802.1X / RADIUS — Verification and Troubleshooting
# FreeRADIUS + Cisco 802.1X — Post-Configuration Verification

> **Platform:** FreeRADIUS 3.2.x + Cisco Catalyst 2960X (IOS 15.2)
> **Scope:** Commands to validate authentication flows (EAP-TLS, PEAP-MSCHAPv2), MAB, and dynamic VLAN assignment

---

## 1. FreeRADIUS — Server Status

```bash
# Check FreeRADIUS service status
systemctl status freeradius
# Expected: active (running)

# FreeRADIUS version
freeradius -v
# Expected: FreeRADIUS Version 3.2.x

# Test RADIUS locally (basic PAP test)
radtest testing <USER-PASSWORD-HERE> 127.0.0.1 0 <RADIUS-SECRET-HERE>
# Expected:
#   Sent Access-Request Id 0 from 0.0.0.0:PORT to 127.0.0.1:1812
#   Received Access-Accept Id 0 from 127.0.0.1:1812 to 0.0.0.0:PORT
#   Reply-Message = "RADIUS test account OK"
```

---

## 2. FreeRADIUS — Debug Mode (live auth trace)

```bash
# Stop service and run in debug mode (foreground)
systemctl stop freeradius
freeradius -X 2>&1 | tee /tmp/fr-debug.log

# In another terminal — trigger an auth request
radtest corp-user1 <USER-PASSWORD-HERE> 127.0.0.1 0 <RADIUS-SECRET-HERE>

# Expected debug output (PEAP-MSCHAPv2):
# (0)  Received Access-Request
# (0)    User-Name = "corp-user1"
# (0)    NAS-IP-Address = 127.0.0.1
# (0)  Processing the authorize section
# (0)    [files] = ok           ← matched users file
# (0)    Found Auth-Type = PAP (or EAP for 802.1X)
# (0)  Processing the authenticate section
# (0)    [pap] = ok
# (0)  Sending Access-Accept
# (0)    Tunnel-Type = 13
# (0)    Tunnel-Medium-Type = 6
# (0)    Tunnel-Private-Group-Id = "10"
# (0)    Reply-Message = "PEAP-MSCHAPv2 auth OK — VLAN 10"

# Restart service after debug
systemctl start freeradius
```

---

## 3. FreeRADIUS — Test EAP-TLS Authentication

```bash
# EAP-TLS test requires a client certificate
# Generate test cert (lab — not production):
openssl req -newkey rsa:2048 -nodes \
  -keyout /tmp/test-client.key \
  -x509 -days 90 \
  -subj "/CN=eap-tls-testuser/O=LAB" \
  -out /tmp/test-client.crt

# Test EAP-TLS auth with eapol_test (wpa_supplicant-utils)
cat > /tmp/eap-tls.conf << 'EOF'
network={
    eap=TLS
    identity="eap-tls-testuser"
    ca_cert="/etc/freeradius/3.0/certs/ca.pem"
    client_cert="/tmp/test-client.crt"
    private_key="/tmp/test-client.key"
}
EOF

eapol_test -c /tmp/eap-tls.conf -a 127.0.0.1 -p 1812 -s <RADIUS-SECRET-HERE>
# Expected: SUCCESS → Access-Accept with Tunnel-Private-Group-Id = "10"
```

---

## 4. FreeRADIUS — Test PEAP-MSCHAPv2

```bash
# PEAP-MSCHAPv2 test via eapol_test
cat > /tmp/peap-mschapv2.conf << 'EOF'
network={
    eap=PEAP
    identity="corp-user1"
    password="<USER-PASSWORD-HERE>"
    phase2="auth=MSCHAPV2"
    ca_cert="/etc/freeradius/3.0/certs/ca.pem"
}
EOF

eapol_test -c /tmp/peap-mschapv2.conf -a 127.0.0.1 -p 1812 -s <RADIUS-SECRET-HERE>
# Expected: SUCCESS → Access-Accept
# Verify in FreeRADIUS debug: Tunnel-Private-Group-Id = "10"
```

---

## 5. FreeRADIUS — Test MAB (MAC Auth Bypass)

```bash
# MAB uses MAC address as username (no password)
# Simulate MAB from FreeRADIUS server:
radtest aabbcc001101 aabbcc001101 127.0.0.1 0 <RADIUS-SECRET-HERE>
# Expected: Access-Accept
# Tunnel-Private-Group-Id = "30" (Voice VLAN for this MAC)

# Unknown MAC (MAB fallback — Guest VLAN 99)
radtest aabbccffffff aabbccffffff 127.0.0.1 0 <RADIUS-SECRET-HERE>
# Expected: Access-Accept with Tunnel-Private-Group-Id = "99"
```

---

## 6. Cisco Switch — Authentication Sessions

```bash
# All authenticated ports overview
show authentication sessions
# Expected output columns:
# Interface  MAC Address    Method  Domain  Status  Session-ID
# Gi0/1      aabb.cc11.0101 dot1x   DATA    Auth    ...
# Gi0/1      aabb.cc00.1101 mab     VOICE   Auth    ...

# Detailed view for a specific port
show authentication sessions interface GigabitEthernet0/1 detail
# Expected:
#   Interface: GigabitEthernet0/1
#   MAC Address: aabb.cc11.0101
#   User-Name: corp-user1
#   Status: Authorized
#   Domain: DATA
#   Oper host mode: multi-domain
#   Authorized By: Authentication Server
#   Vlan Policy: 10                ← Dynamic VLAN assigned by RADIUS
#   ACS ACL: —
#   Security Policy: Should Secure
#   Method: dot1x

# 802.1X global status
show dot1x all
# Shows: system-auth-control = enabled, per-interface config

# Per-interface 802.1X state
show dot1x interface GigabitEthernet0/1
# Shows: PAE state (Authenticating / Authenticated / Unauthorized)
# Supplicant state, auth method, max-req, timeout values

# 802.1X statistics
show dot1x statistics interface GigabitEthernet0/1
# EAP frame counters: RxStart, RxLogoff, TxReq, RxResponse, TxSuccess, TxFailure
```

---

## 7. Cisco Switch — MAB Sessions

```bash
# MAB overview
show mab
# Expected:
# Interface   MAC Address    Auth Status  Auth Method
# Gi0/10      aabb.cc33.3301 Authorized   MAB

# Detailed MAB session
show mab interface GigabitEthernet0/10 detail
# Shows MAC, VLAN assigned, session ID, policy

# Verify IP Phone authenticated via MAB on voice domain
show authentication sessions interface GigabitEthernet0/1 detail | include Domain
# Expected: DATA → VLAN 10, VOICE → VLAN 30
```

---

## 8. Cisco Switch — RADIUS Debug

```bash
# RADIUS packet trace (important: generates verbose output)
debug radius authentication
debug radius
! → Trigger authentication (plug in device or re-auth)
! Expected debug lines:
!   RADIUS(0000000): Send Access-Request to 10.0.10.100:1812
!   RADIUS: Received from id 1812:X, Access-Accept
!   RADIUS:  Tunnel-Type [64] 6 VLAN [13]
!   RADIUS:  Tunnel-Medium-Type [65] 6 802 [6]
!   RADIUS:  Tunnel-Private-Group-Id [81] 4 "10"

! Disable debug after test
no debug all
```

---

## 9. Cisco Switch — 802.1X Debug

```bash
! Real-time EAP state machine trace
debug dot1x all
! Plug in a client device — observe:
!   DOT1X-5-SUCCESS: Authentication successful for client (aabb.cc11.0101) on Gi0/1
!   VLAN assigned: 10

! EAP packet decode (for detailed troubleshooting)
debug eapol all

! After troubleshooting — disable all debug
no debug all
```

---

## 10. Dynamic VLAN Assignment Verification

```bash
! On Cisco switch — verify VLAN assigned by RADIUS:
show vlan brief
! VLAN 10: Corp-LAN — Gi0/1, Gi0/2 (authenticated ports)
! VLAN 99: Guest — Gi0/5 (unauthorized or new port)

! Verify interface is in correct VLAN after auth:
show interfaces GigabitEthernet0/1 switchport
! Access Mode VLAN: 10 (Corp-LAN)     ← assigned dynamically by RADIUS
! (Without auth: shows VLAN 99 — the default/unauthorized VLAN)

! AAA event log (Cisco IOS event history)
show authentication sessions history
! Shows recent auth/deauth events per interface
```

---

## 11. Test Full Flow — End-to-End

```bash
# Step 1: On FreeRADIUS server — run in debug mode
systemctl stop freeradius
freeradius -X 2>&1 | tee /tmp/e2e-test.log &

# Step 2: On Cisco switch — verify port is in unauthorized state
show authentication sessions interface Gi0/1
# Expected: Status = Unauthorized, Domain = DATA, VLAN = 99

# Step 3: Connect test workstation to Gi0/1
# Windows: Network adapter → 802.1X → PEAP-MSCHAPv2 → user=corp-user1

# Step 4: Monitor FreeRADIUS debug log
tail -f /tmp/e2e-test.log | grep -E "Accept|Reject|Tunnel|VLAN"
# Expected:
#   Access-Accept
#   Tunnel-Private-Group-Id = "10"

# Step 5: Verify on switch
show authentication sessions interface Gi0/1 detail
# Expected: Status=Authorized, Vlan Policy=10

# Step 6: Test IP connectivity from workstation
# ping 10.0.10.1 (switch gateway) → should reply
# ping 8.8.8.8 → should work if FGT-EDGE routing is correct
```

---

## 12. FreeRADIUS Log Files

```bash
# Authentication log (success/failure)
tail -f /var/log/freeradius/radius.log
# Format: Mon Apr 15 10:30:21 2026 : Auth: (0) Login OK: [corp-user1]
# Or: Auth: (0) Login incorrect: [baduser]

# Detail log (full RADIUS attributes per request)
tail -f /var/log/freeradius/radacct/<NAS-IP>/detail
# Full request + response attributes for accounting

# Rotate logs (logrotate config)
cat /etc/logrotate.d/freeradius
# Should be configured to rotate weekly and compress
```

---

## 13. Verification Summary

| Check | Expected Result | Command |
|-------|----------------|---------|
| FreeRADIUS running | active (running) | `systemctl status freeradius` |
| radtest localhost | Access-Accept | `radtest testing <pw> 127.0.0.1 0 <secret>` |
| dot1x system-auth-control | Enabled | `show dot1x all` |
| Port Gi0/1 mode | auto (802.1X active) | `show dot1x interface Gi0/1` |
| Corp user auth | Authorized, VLAN 10 | `show authentication sessions interface Gi0/1 detail` |
| MAB phone | Authorized, VLAN 30 | `show mab interface Gi0/1 detail` |
| IoT device | Authorized, VLAN 40 | `show authentication sessions interface Gi0/10` |
| Unknown device | Authorized, VLAN 99 (Guest) | `show authentication sessions` |
| RADIUS Access-Accept | id=X, VLAN in attributes | `debug radius authentication` |
| Dynamic VLAN correct | Access VLAN = RADIUS-assigned | `show interfaces Gi0/1 switchport` |
| EAP-TLS cert auth | ACCESS-ACCEPT | `eapol_test` with TLS config |
| PEAP-MSCHAPv2 | ACCESS-ACCEPT | `eapol_test` with PEAP config |
