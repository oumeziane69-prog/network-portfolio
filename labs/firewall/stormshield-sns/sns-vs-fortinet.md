# Stormshield SNS vs FortiGate — Comparison
# Stormshield SNS vs FortiGate — Comparative Analysis

> **Context:** Evaluation for regulated/OIV environments (IEC 62443, ANSSI, EDF CNPE)
> **Versions:** Stormshield SNS 4.x vs FortiGate FortiOS 7.4.x

---

## 1. Positioning and Certification

| Criterion | Stormshield SNS | FortiGate |
|-----------|----------------|-----------|
| **Country of origin** | France (Airbus CyberSecurity subsidiary) | USA/Canada (Fortinet) |
| **ANSSI qualification** | ✅ CSPN + EAL3+ (LSTI) — Standard Niveau Élevé | ❌ No ANSSI qualification |
| **ANSSI CSPN certification** | ✅ SNS 4.x series | ❌ Not applicable |
| **CC (Common Criteria)** | EAL3+ augmented | EAL4+ (some models) |
| **Recommended for OIV** | ✅ Yes — referenced by ANSSI for sensitive networks | ⚠️ Possible but not preferred for OIV/CNPE |
| **NATO/EU certification** | ✅ NATO SECRET approval (selected models) | ❌ Not applicable |
| **Product sovereignty** | ✅ Source code auditable by ANSSI | ❌ Closed-source, US Patriot Act concern |
| **Typical use case** | Critical infrastructure, government, defense, nuclear | Enterprise, MSSP, multi-site commercial |

---

## 2. Architecture and Deployment

| Criterion | Stormshield SNS | FortiGate |
|-----------|----------------|-----------|
| **Management interface** | GUI (SN Console) + stcli CLI | GUI (WebUI) + FortiOS CLI |
| **Centralized management** | SMC (Stormshield Management Center) | FortiManager |
| **Cloud management** | SMC SaaS (optional) | FortiCloud / FortiManager Cloud |
| **HA modes** | Active/Passive, Active/Active | FGCP (A/P), FGSP (A/A) |
| **Multi-VDOM equivalent** | Virtual Firewalls (VFW) — requires license | VDOM (included in most models) |
| **API** | REST API SNS | REST API FortiOS + FortiManager |
| **Automation** | SMC scripting, REST API | FortiManager + FortiOS API + Ansible |

---

## 3. Security Features / Inspection Engine

| Feature | Stormshield SNS | FortiGate |
|---------|----------------|-----------|
| **Stateful firewall** | ✅ ASQ engine (Application Scanning and Qualification) | ✅ NP ASIC accelerated stateful inspection |
| **Inspection engine** | ASQ — deep protocol analysis (L7) with TCP/UDP reassembly | FortiGate ASIC (NP7/CP9) for hardware offload + SoC |
| **Application control** | ✅ L7 protocol identification | ✅ FortiGuard AppCtrl (FortiCloud fed) |
| **IPS/IDS** | ✅ Integrated — SNORT rules + SNS signatures | ✅ FortiGuard IPS (FortiCloud subscription) |
| **Antivirus** | ✅ Bitdefender engine integrated (inline AV) | ✅ FortiGuard AV (dual-engine: Fortinet + Bitdefender) |
| **URL Filtering** | ✅ BRASSENS categorization (FR database) | ✅ FortiGuard URL Filtering (cloud) |
| **SSL/TLS inspection** | ✅ Deep inspection (with CA cert deployed) | ✅ Full SSL deep inspection |
| **Anti-spam** | ✅ Integrated | ✅ FortiMail or integrated FortiGuard spam |
| **Sandboxing** | ⚠️ Breachfighter (optional cloud sandbox) | ✅ FortiSandbox (on-prem or cloud) |

---

## 4. VPN

| Criterion | Stormshield SNS | FortiGate |
|-----------|----------------|-----------|
| **IPSec IKEv1/IKEv2** | ✅ Full — IKEv2 preferred | ✅ Full — IKEv2 + optional QKD |
| **SSL VPN** | ✅ Built-in SSL VPN portal | ✅ Built-in SSL VPN (FortiClient agent) |
| **Client software** | ✅ SN VPN Client (Windows/Linux/macOS) | ✅ FortiClient (EMS for MDM) |
| **Quantum-safe VPN** | ⚠️ Roadmap (IKEv2 + post-quantum KEM) | ⚠️ FortiGate 7.6+ experimental |
| **Crypto algorithms** | AES-256-GCM, ChaCha20-Poly1305, SHA-384 | AES-256-GCM, AES-256-CBC, SHA-256/384 |
| **FIPS 140-2/3** | ✅ FIPS mode available | ✅ FIPS mode available |
| **Multi-site VPN** | ✅ SNS Hub-and-Spoke via SMC | ✅ ADVPN / SD-WAN overlay |

---

## 5. OT / Industrial Security

| Criterion | Stormshield SNS | FortiGate |
|-----------|----------------|-----------|
| **OT/SCADA protocol inspection** | ✅ Modbus, DNP3, OPC-UA, IEC 60870-5-104 (ASQ) | ✅ FortiGuard OT signatures (subscription) |
| **Industrial certifications** | ✅ IEC 62443-4-2 (component) — listed ANSSI | ⚠️ IEC 62443 partially (FortiGate ruggedized) |
| **Ruggedized models** | ✅ SNi10, SNi20 (DIN rail, -40/+70°C, 24VDC) | ✅ FortiGate Rugged 70F/30D (-40/+75°C) |
| **EDF CNPE reference** | ✅ Preferred product — ANSSI qualification critical | ❌ Not on CNPE qualified product list |
| **IDMZ segmentation** | ✅ Multi-zone with strict inter-zone policies | ✅ Zone-based with VDOM segmentation |

---

## 6. Management and Operations

| Criterion | Stormshield SNS | FortiGate |
|-----------|----------------|-----------|
| **CLI syntax** | `CONFIG OBJECT HOST NEW name=... ip=...` (stcli) | `config firewall address / edit ... / set ...` |
| **Config backup** | `SYSTEM BACKUP` → `.na` encrypted file | `execute backup config tftp ...` |
| **Rollback** | ✅ Configuration revision management in SMC | ✅ `execute restore` + FortiManager revisions |
| **High availability failover** | < 1s (session pickup A/P) | < 1s (FGCP session pickup) |
| **Zero-touch provisioning** | ✅ SMC + HTTPS auto-registration | ✅ FortiManager ZTP (SD-WAN) |
| **Multi-admin with lock** | ✅ Session locking per object (SMC) | ✅ FortiManager policy lock |
| **Learning curve** | High — stcli syntax differs from Cisco/Fortinet | Moderate — close to IOS CLI style |

---

## 7. Logging and SIEM Integration

| Criterion | Stormshield SNS | FortiGate |
|-----------|----------------|-----------|
| **Embedded log viewer** | ✅ SN Real-Time Monitor + SN Log Viewer | ✅ FortiView (built-in dashboard) |
| **Centralized logging** | ✅ SN Reporter (on-prem) | ✅ FortiAnalyzer (on-prem or cloud) |
| **Syslog export** | ✅ CEF/Syslog — compatible SIEM (Splunk, QRadar) | ✅ Syslog/CEF/JSON — FortiSIEM integration |
| **Log format** | Stormshield proprietary + CEF | FortiOS log + CEF + JSON |
| **SIEM connectors** | ✅ QRadar, Splunk, ArcSight (official) | ✅ Same — plus FortiSIEM native |

---

## 8. Licensing and TCO

| Criterion | Stormshield SNS | FortiGate |
|-----------|----------------|-----------|
| **Base license** | Hardware appliance + perpetual SNS license | Hardware appliance — FortiCare contract |
| **UTM subscriptions** | IPS, AV, URL, AppCtrl — annual per appliance | FortiGuard bundles (UTP, ATP, ENT) — annual |
| **Support model** | Direct Stormshield or reseller (EMEA focus) | Global Fortinet TAC (24/7) |
| **Pricing segment** | Higher unit cost — smaller volume | Lower unit cost — higher volume/MSSP discounts |
| **SMC (management)** | Additional license — per-device | FortiManager — per-device license |

---

## 9. Decision Guide — When to Choose Each

### Choose Stormshield SNS when:
- **OIV/CNPE/Defense**: ANSSI qualification is a hard regulatory requirement
- **French public sector (RGS, PGSSI-S)**: Sovereign product mandate
- **Nuclear (ASN)**: CNPE equipment list compliance required
- **Classified networks (NATO/EU SECRET)**: Approved for classified processing
- **IEC 62443 SL 3-4**: Highest security level industrial environments

### Choose FortiGate when:
- **Enterprise multi-site**: SD-WAN + FortiManager scalability needed
- **MSSP**: Cost-effective multi-tenant management with FortiManager
- **FortiGate Security Fabric**: Deep integration with FortiAnalyzer/FortiSIEM/FortiClient
- **Cloud-native environments**: FortiGate VM on AWS/Azure/GCP with FortiCloud
- **Large-scale deployments**: Best TCO at volume with Fortinet ecosystem

---

## 10. CLI Syntax Comparison

| Operation | Stormshield SNS (stcli) | FortiGate (FortiOS CLI) |
|-----------|------------------------|------------------------|
| Create host object | `CONFIG OBJECT HOST NEW name=X ip=Y` | `config firewall address` / `edit X` / `set subnet Y` |
| Create filter rule | `CONFIG FILTER RULE NEW idx=N action=pass ...` | `config firewall policy` / `edit N` / `set action accept` |
| Create NAT rule | `CONFIG NAT RULE NEW action=nat nat-source=...` | `config firewall ippool` + `config firewall vip` |
| Apply/commit config | `CONFIG ACTIVATE` | `end` (auto-commit in FortiOS) |
| Backup | `SYSTEM BACKUP` | `execute backup config tftp ...` |
| View connections | `MONITOR CONNECTIONS` | `diagnose sys session list` |
| View routes | `MONITOR ROUTES` | `get router info routing-table all` |
| Debug traffic | `MONITOR PACKET interface=in filter="host X"` | `diagnose debug flow filter addr X` |
