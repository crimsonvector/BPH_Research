# BPH & Threat Activity Enabler (TAE) Taxonomy Framework

> **Version:** 1.3 | **Last Updated:** 2026-09-25 | **Maintainer:** CrimsonVector Research
>
> This document defines the classification system used across the BPH Research repository. All provider assessments, risk ratings, and analytical products reference this taxonomy.

---

## Table of Contents

1. [Risk Tier Definitions](#1-risk-tier-definitions)
2. [Provider Type Classification](#2-provider-type-classification)
3. [Operational Pattern Taxonomy](#3-operational-pattern-taxonomy) (incl. 3.9 ASN recycling, 3.10 actor-preferred providers)
4. [Identification Signals Matrix](#4-identification-signals-matrix)
5. [Status Lifecycle Model](#5-status-lifecycle-model)
6. [Evidence Standards](#6-evidence-standards)
7. [Glossary](#7-glossary)

---

## 1. Risk Tier Definitions

Providers are assigned to one of five risk tiers based on the weight and recency of evidence. Tier assignment drives prioritization for monitoring, blocking recommendations, and sanctions-tracking workflows.

### T1 — Confirmed BPH / Confirmed TAE

**Definition:** Entity whose primary or predominant business function is enabling malicious cyber operations. Confirmed through sanctions designations, law enforcement actions, or overwhelming convergent intelligence from multiple independent sources.

**Criteria (meet ANY):**
- Designated by OFAC, the EU, the UK (FCDO; implemented by OFSI), or Australian DFAT sanctions specifically for hosting/enabling cyber operations
- Subject of law enforcement seizure or takedown action targeting hosting infrastructure
- Self-advertises as "bulletproof" on underground forums with corroborating infrastructure evidence
- Recorded Future Threat Density Score in top decile with sustained concentration over 6+ months
- Multiple independent CTI vendors (3+) classify as BPH/TAE with named malware families or threat actors hosted

**Blocking Recommendation:** Block at CIDR/ASN level. Monitor for prefix migration.

**Current T1 entities (illustrative; `BPH_Master.csv` is authoritative — 24 rows):** Aeza International / Aeza Group, Stark Industries Solutions (dissolved), Zservers/XHOST, Media Land LLC, FUNNULL Technology, CTG Server Limited (FUNNULL hosting ASN), ELITETEAM/1337TEAM (dormant), PROSPERO OOO/Proton66, WorkTitans/THE.Hosting, Hypercore, Datavice, PQ Hosting Plus (evading; not itself listed), Railnet/Virtualine, Femo IT/Defhost, Kaopu Cloud HK, PrivateAlps/Private Layer, MIRhosting (WorkTitans' upstream), CrazyRDP (seized), BtHoster, First VPN Service/1VPNS and QTFY/QTRouter (anonymization enablers), Garantex / Grinex / A7A5-Old Vector (financial enablers)

---

### T2 — High Risk TAE

**Definition:** Entity exhibiting strong, consistent indicators of enabling malicious operations but lacking formal sanctions designation or confirmed law enforcement action. Distinguished from T3 by volume, persistence, and diversity of malicious activity observed.

**Criteria (meet 3+):**
- Spamhaus ASN-DROP list inclusion or equivalent community blocklist
- Documented hosting of C2 infrastructure for 3+ distinct malware families
- No meaningful abuse response despite repeated reporting
- Corporate structure designed to obscure beneficial ownership (shell companies, nominee directors, multi-jurisdiction layering)
- Upstream for or downstream of a T1 entity with no route diversification
- RF Threat Density Score above 5% sustained for 3+ months

**Blocking Recommendation:** Block known malicious prefixes; consider ASN-level block with allowlisting for confirmed legitimate customers.

**Current T2 entities (illustrative; `BPH_Master.csv` is authoritative — 25 rows):** Tnsecurity/EVILEMPIRE (defunct), QWINS LTD, GCSAS, Karina Rashkovska (defunct), KPROHOST, Altawk, aurologic GmbH and UAB Host Baltic (upstream enablers), PINSPB, SWISSNETWORK02/Global-Data (dormant), WAIcore, First Server Limited, Pfcloud UG, Chang Way Technologies, VPSVault.host, Feo Prest, SHANGXING TECH LIMITED (HK reseller ASN), UFO Hosting (evading), Asocks / NetNut-Alarum / IPIDEA (proxy enablers), Nobitex / Dabai Guarantee / Tudou Guarantee / H-Pay Service PLC (financial enablers)

---

### T3 — Suspected TAE

**Definition:** Entity with credible but limited indicators of enabling malicious operations. Evidence may come from a single source, be temporally limited, or lack confirmation of deliberate enablement versus negligence.

**Criteria (meet 2+):**
- Single CTI vendor attribution to malicious hosting with named indicators
- Malicious traffic concentration above baseline but below T2 threshold
- Corporate registration patterns matching known BPH shells (offshore LLP/LLC with minimal filings)
- Forum advertising presence on cybercriminal platforms (BreachForums, cracked.io, etc.)
- Operates as downstream of known enabler with limited route diversification
- Known association with sanctioned or flagged personnel

**Blocking Recommendation:** Monitor and alert. Block specific confirmed-malicious IPs. Reassess quarterly.

**Current T3 entities (illustrative; `BPH_Master.csv` is authoritative — 11 rows):** Cloudzy/abrNOC, metaspinner-named AS209800 (defunct Virtualine front), HostSlick, StarCloud Global, NECHAEVDS, NETINNOVATIONLLC, Tiger Network Limited, Silent Connection (dissolved), Wallex / Bitpin / Ramzinex (financial enablers)

---

### T4 — Gray Zone / BPH-Adjacent

**Definition:** Entity operating in a legitimacy gray area. Provides hosting services that may facilitate abuse through permissive policies, slow abuse response, or privacy-focused positioning, but whose infrastructure is not predominantly malicious. Often markets "freedom of speech" or "DMCA-ignored" services.

**Criteria (meet 2+):**
- Markets DMCA-ignored, "offshore," or "privacy-focused" hosting with anonymous/crypto payment
- Documented slow or selective abuse response, but some enforcement exists
- Permits Tor exit relays or explicitly caters to anonymity-focused use cases
- Presence on both legitimate hosting forums (LowEndTalk, WebHostingTalk) and gray-area platforms
- Malicious traffic concentration at or slightly above industry baseline
- No sanctions, no LE action, no underground forum BPH advertising

**Blocking Recommendation:** No blanket blocking. Monitor for escalation. Flag in threat intel enrichment.

**Current T4 entities (illustrative; `BPH_Master.csv` is authoritative — 6 rows):** BuyVM/Frantech, AlexHost, FlokiNET, Shinjiru, Phanes Networks/Flaunt7, HostZealot (HZ Hosting Ltd)

---

### T5 — Watch List

**Definition:** Entity with minimal current evidence of malicious enablement but included in tracking due to structural characteristics, geographic positioning, or association with entities of interest. May be newly identified, under-researched, or historically problematic but currently quiescent.

**Criteria (meet 1+):**
- Named in a single report without corroborating evidence
- Newly registered ASN/entity matching known BPH patterns but no observed malicious activity yet
- Historically associated with abuse but under new management or restructured
- Dual-use service with legitimate primary function but periodic abuse (DDoS mitigation, CDN, exchange)
- Insufficient data for higher-tier classification

**Blocking Recommendation:** No blocking. Passive monitoring. Reassess upon new intelligence.

**Current T5 entities (illustrative; `BPH_Master.csv` is authoritative — 4 rows):** HOSTYPE (dormant), 1GSERVERS, DDoS-Guard, Dolphon 1337 (ASN recycled)

---

### Tier Escalation / De-escalation

| Trigger | Direction | Example |
|---------|-----------|---------|
| Sanctions designation **for hosting/enabling cyber operations** | Escalate to T1 | Aeza: T2 → T1 upon OFAC designation (July 2025) |
| Sanctions designation **on other grounds** (terror finance, sectoral, non-cyber) | No automatic escalation — tier on the cyber-enablement evidence alone; set `status` to `sanctioned` regardless | Nobitex (OFAC June 2026, terror finance + Iran financial sector) remains T2: designated, but not *for* enabling cyber operations |
| LE takedown/seizure | Escalate to T1 | Zservers: T2 → T1 upon trilateral sanctions (Feb 2025) |
| New malware family attribution (3rd+) | Escalate T3 → T2 | Femo IT: accumulated 12+ malware families |
| Underground forum BPH advertising confirmed | Escalate to T2 minimum | PROSPERO: forum advertising confirmed by Intrinsec |
| Spamhaus ASN-DROP inclusion | Escalate to T2 minimum | Tnsecurity/EVILEMPIRE |
| Sustained 12-month clean period + ownership change | De-escalate one tier | (No current examples) |
| Sanctions lifted or LE clears entity | De-escalate, case-by-case | (No current examples) |
| Corporate dissolution with network still live | No de-escalation — reclassify as "dissolved" status | Stark Industries Solutions (dissolved 2025-09-16; network lives on as WorkTitans/THE.Hosting) |
| ASN returned and re-issued to an unrelated holder | Mark the ASN `historical; reassigned to X - do not block` in the CSV; if no successor network is identifiable, set status `dissolved` (network defunct) and keep the tier as a historical record | Karina Rashkovska (AS215789 now BLIK); Tnsecurity (AS216309); CrazyRDP (AS394711, AS211252) |
| Network announces nothing for 6+ months with no new reporting, and the entity is not dissolved, sanctioned or seized | No de-escalation — set status `dormant` and keep the tier; re-announcement or an ASN transfer means reassessing and restoring an operating status | ELITETEAM/1337TEAM (AS51381, AS56873 registered but unrouted); HOSTYPE (AS49217); SWISSNETWORK02/Global-Data |

---

## 2. Provider Type Classification

Each entity is assigned one primary type and may carry secondary type tags where applicable.

### 2.1 Pure BPH

**Definition:** Entity whose core business model is providing hosting infrastructure specifically marketed to or predominantly used by cybercriminals. Openly advertises bulletproof services, ignores abuse reports by policy, and accepts anonymous/cryptocurrency payment as standard.

**Distinguishing Characteristics:**
- Advertises on Russian-language or English-language underground forums (XSS, Exploit, BreachForums)
- Uses terms like "bulletproof," "abuse-proof," "100% ignore Spamhaus," "no logs"
- Often small operator: single maintainer in RIPE, 1-3 ASNs, limited prefix diversity
- Payment exclusively via cryptocurrency or anonymous methods

**Examples:** PROSPERO/BEARHOST, ELITETEAM/1337TEAM, Zservers, Media Land

### 2.2 BPH-Adjacent / Permissive Hoster

**Definition:** Entity operating as a legitimate hosting provider but whose permissive policies, lax abuse enforcement, or "privacy-first" positioning results in disproportionate concentration of malicious infrastructure. Maintains plausible deniability through formal AUPs that prohibit abuse but are weakly enforced.

**Distinguishing Characteristics:**
- Has a public website, formal terms of service, and some legitimate customer base
- Markets "DMCA-ignored," "offshore hosting," or "freedom of speech" hosting
- Abuse response exists but is slow, selective, or complaint-driven
- Mixed presence: legitimate forums + gray-area platforms
- May accept both traditional and cryptocurrency payment

**Examples:** AlexHost, BuyVM/Frantech, PrivateAlps, Shinjiru, HostSlick, FlokiNET

### 2.3 Upstream Enabler

**Definition:** Entity that provides transit, peering, or upstream bandwidth to multiple BPH or high-risk downstream networks. May not itself host malicious content but enables BPH operations through its network connectivity. Often operates as a Local Internet Registry (LIR) with direct control over IP resources.

**Distinguishing Characteristics:**
- Provides upstream/transit for 3+ entities classified T1-T3
- Often operates as LIR with ability to allocate/transfer IP resources
- May have high aggregate malicious traffic volume despite individual downstream diversity
- Single point of failure: disrupting the upstream would impact multiple downstream BPH operations
- Often claims ignorance of downstream abuse or contractual inability to intervene

**Examples:** aurologic GmbH (AS30823), DDoS-Guard (dual-use)

### 2.4 Financial Enabler

**Definition:** Entity (exchange, mixer, payment processor) that provides the financial infrastructure enabling BPH operations and the broader cybercrime ecosystem. Not a hosting provider but essential to the BPH payment chain.

**Distinguishing Characteristics:**
- Processes payments for sanctioned or high-risk hosting providers
- Inadequate or absent KYC/AML enforcement
- Often operates in jurisdictions with loose financial regulation
- May be sanctioned specifically for enabling cybercrime financial flows

**Examples:** Garantex/Grinex, Cryptomixer (seized)

### 2.5 Corporate Shell

**Definition:** Legal entity created primarily to provide corporate distance between BPH infrastructure and its actual operators. Typically a thin incorporation in a business-friendly jurisdiction (UK LLP, US LLC, Seychelles) with nominee directors, minimal filings, and no genuine business operations.

**Distinguishing Characteristics:**
- Recent incorporation (often <2 years before first malicious activity observed)
- Minimal corporate filings beyond statutory minimum
- Nominee or short-tenure directors (6-month rotations)
- Registered at virtual office or formation agent address
- No website, employees, or visible business operations beyond ASN registration
- Often UK LLP (no financial filing requirements) or US LLC (minimal disclosure states: Wyoming, Kentucky, Delaware)

**Examples:** GCSAS (UK LLP), XHOST Internet Solutions LP, Hypercore LTD, Dolphon 1337 Ltd

### 2.6 Sanctions-Evasion Vehicle

**Definition:** Entity created specifically to continue operations of a sanctioned provider under a new corporate identity. Distinguished from normal business succession by timing (created immediately before or after sanctions), shared infrastructure/personnel, and traceable continuity of operations.

**Distinguishing Characteristics:**
- Created within weeks of a sanctions action against a related entity
- Shares ASN, IP prefixes, technical fingerprints, or personnel with sanctioned entity
- Corporate ownership traces back to associates of sanctioned individuals
- Rapid migration of infrastructure from sanctioned to successor entity
- May use intermediary jurisdictions to create additional legal distance

**Examples:** WorkTitans B.V./THE.Hosting (Stark successor), PQ Hosting Plus S.R.L. (Stark Moldova arm), UFO Hosting (Stark Russian prefix vehicle), Hypercore LTD (Aeza successor), Grinex/Exved (Garantex successors)

### 2.7 Anonymization / Proxy Enabler

**Definition:** Entity that provides the anonymization and traffic-obfuscation layer enabling malicious operations — criminal VPNs, residential-proxy networks, and proxy-as-a-service platforms — rather than the hosting itself. Distinct from Pure BPH in that the infrastructure is distributed across legitimate residential/mobile ISP space (or a botnet of compromised devices) rather than concentrated in datacenter space, which is what lets it defeat IP-reputation and geolocation controls. Ranges from openly criminal (no-log VPNs advertised on forums) to nominally commercial providers whose exit-node supply is botnet-sourced.

**Distinguishing Characteristics:**
- Sells proxy/VPN egress rather than compute or storage
- Exit nodes sit in residential/mobile ISP ranges or on compromised IoT/mobile devices
- May enroll devices covertly via malicious SDKs or bundled apps (proxyware)
- Advertised for "bypass geo-blocks / anti-detect / undetectable" use, or forum-advertised as a no-log criminal VPN
- Blurs into legitimacy: some operate as public companies with a legitimate customer base while their egress pool is criminally sourced

**Examples:** Asocks (residential-proxy botnet, LE-disrupted), First VPN Service/1VPNS (OFAC-sanctioned no-log criminal VPN), NetNut/Alarum Technologies (commercial residential-proxy platform, FBI/Google-seized; Popa botnet exit nodes)

> **Note:** This type was added 2026-07-17 after the 1VPNS designation and the NetNut/Popa takedown surfaced enablers that the original six types did not cleanly cover. Because the database encodes provider type as a parenthetical qualifier on the `risk_tier` column rather than a dedicated field, only entities where the type is analytically salient carry the tag; the tag is not exhaustive across the dataset.

---

## 3. Operational Pattern Taxonomy

These are the recurring operational techniques observed across BPH and TAE networks. Multiple patterns may apply to a single entity.

### 3.1 Corporate Shell Games

**Description:** Establishing front companies across multiple jurisdictions to create legal distance between the infrastructure and operators. Often involves UK LLPs (no financial filing requirements), US LLCs (minimal disclosure), or offshore jurisdictions (Seychelles, BVI).

**Indicators:**
- Multi-jurisdiction incorporation chain
- Nominee directors with short tenures
- Virtual office registration addresses
- Formation agent addresses shared with many other entities
- No employees, revenue, or visible business beyond ASN registration

**Observed in:** Stark Industries → WorkTitans chain; ELITETEAM (Seychelles); QWINS LTD (UK)

### 3.2 Rapid Rebranding

**Description:** When a network becomes "too hot" due to scrutiny, sanctions, or takedowns, TAEs rapidly transfer IP address prefixes to a newly registered, clean-looking entity. The underlying infrastructure (physical servers, routing, peering) remains unchanged.

**Indicators:**
- New entity registration within weeks of adverse action against predecessor
- RIPE/ARIN resource transfers from flagged to new entity
- Identical BGP routing patterns, peering relationships, or upstreams post-transfer
- Shared technical fingerprints (RDP hostnames, TLS certificates, server configurations)

**Observed in:** Stark Industries → THE.Hosting (RDP hostname WIN-J9D866ESIJ2 reuse); Virtualine → metaspinner-named AS209800 → OMEGATECH (AS202412); Garantex → Grinex

### 3.3 Sub-Sub-Leasing (Infrastructure Nesting)

**Description:** Creating multiple layers of leasing arrangements between the bare-metal datacenter and the end-user criminal. Each layer introduces a new jurisdiction and legal entity, complicating judicial requests and evidence chains.

**Indicators:**
- 3+ corporate entities between datacenter and end user
- Each layer in a different jurisdiction
- Abuse complaints redirected to intermediaries who redirect further
- Data retention gaps between layers

**Observed in:** Described broadly in IOCTA 2026 as growing trend; aurologic → downstream → sub-customer chains

### 3.4 LIR Manipulation / Strategic Resource Control

**Description:** Operating as or through a Local Internet Registry (LIR) to maintain direct control over IP address resources and autonomous systems. Enables rapid allocation, reallocation, and transfer of IP blocks without relying on third-party providers.

**Indicators:**
- Entity operates as RIPE LIR or sponsors RIPE membership for related entities
- Frequent IP prefix transfers between related entities
- New ASN registrations correlated with adverse events against existing ASNs
- Control over number resources used to evade blocklists by rotating prefixes

**Observed in:** aurologic GmbH (LIR); Stark Industries pre-sanctions AS44477 transfer (2025-05-16, four days before the EU listing); Zservers post-sanctions prefix-hopping to AS213194, AS61336, AS213010

### 3.5 Prefix Hopping / ASN Migration

**Description:** Moving malicious infrastructure across different IP prefixes or autonomous systems to evade IP-based blocklists and network-level blocking. Often combined with rapid rebranding.

**Indicators:**
- Malicious activity observed migrating across /24 blocks in sequence
- New ASNs announced shortly after old ones are blocklisted
- BGP announcements appearing from previously-unannounced prefixes
- GreyNoise/Shodan scan data showing infrastructure "moving" between ASNs

**Observed in:** Zservers (AS197414 → AS213194 → AS61336 → AS213010, per Intrinsec); Virtualine shedding /24s to TELCHAK GOLD VENTURES, iHostART and the metaspinner-named AS209800, then to OMEGATECH (AS202412); Aeza → Hypercore (AS211522)

### 3.6 Proprietary Infrastructure Deployment

**Description:** Criminal networks bypassing third-party hosting entirely by deploying their own hardware in colocation facilities or private locations. Eliminates the traditional evidence chain that runs through hosting providers.

**Indicators:**
- No hosting provider in the infrastructure chain — entity owns the hardware
- Colocation agreements in name of shell companies
- Hardware purchased with cryptocurrency or through intermediaries
- No standardized server management platform (custom deployments)

**Observed in:** Described in IOCTA 2026 Section 1.2; some OFS networks deploying proprietary infrastructure (Section 2.4)

### 3.7 Infrastructure Laundering

**Description:** Routing malicious traffic through compromised accounts at legitimate cloud providers (AWS, Cloudflare, Google Cloud, Microsoft Azure) to avoid detection and leverage the reputation of trusted networks.

**Indicators:**
- Malicious domains resolving to IP space of major cloud providers
- Compromised or fraudulently-registered cloud accounts used for hosting
- Rapidly rotating CNAMEs pointing to legitimate CDN infrastructure
- Geofencing (returning 451 errors to investigator IP ranges)

**Observed in:** FUNNULL/Triad Nexus (FBI: 548 FUNNULL CNAMEs linked to 332,000+ domains since Jan 2025; accounts at AWS/Cloudflare/Google/Microsoft; pre-sanction 'clean' front brands per Silent Push, April 2026)

### 3.8 Residential Proxy Abuse

**Description:** Using networks of compromised home devices as proxy layers to mask the true origin of malicious traffic. Distinct from BPH in that the infrastructure is distributed across legitimate ISPs rather than concentrated in datacenter space.

**Indicators:**
- Traffic originating from residential ISP IP ranges
- Compromised IoT devices or malicious VPN applications
- Proxy-as-a-service offerings on underground forums
- Traffic patterns inconsistent with normal residential usage

**Observed in:** Described extensively in IOCTA 2026 Section 1.2; enforcement lineage 911 S5 (2024) → Moonlander/5socks (2025) → SocksEscort (Mar 2026) → IPIDEA (Jan 2026, Google) → Asocks (May 2026) → NetNut/Popa (Jul 2026) → QTFY/QTRouter (Aug 2026, a PRC state-enablement ORB that bought commercial proxy subscriptions)

### 3.9 ASN Recycling and Re-issue

**Description:** When a shell is struck off or abandoned, its RIPE/ARIN/APNIC number resources are returned and later re-issued to unrelated organisations, sometimes within months. The historical ASN keeps its reputation in blocklists and in this database long after it has changed hands.

**Indicators:**
- Registry holder name no longer matches the tracked entity (check the current RIR/ipverse holder before any ASN-level action)
- ASN announces nothing for months, then reappears under a new org handle
- Spamhaus ASN-DROP delists the ASN while a sibling ASN under the same `domain` field appears
- Former prefixes surface under a different, often also-listed, ASN

**Observed in (2026-09-25 audit):** AS215789 (Karina Rashkovska → BLIK); AS216309 (Tnsecurity → InvisionTech); AS209800 (metaspinner front → ZEMA GbR); AS208046 (HostSlick/ColocationX → a French individual); AS203727 (Altawk → byon); AS210281, AS202973, AS206425 (WAIcore); AS215208 (Dolphon 1337 → an Indonesian ISP); AS215240 (Silent Connection → Microdex UG); AS394711 and AS211252 (CrazyRDP); AS198465 (BtHoster). Separately, two ASNs in this database had simply been mis-attributed (AS216071 for Zservers is VDSina; AS215552 for Hypercore is a Romanian individual).

**Handling:** Keep the ASN in the CSV only with a `historical; reassigned to X - do not block` qualifier, verify every ASN against the registry and `asndrop.json` before publishing blocklists, and treat Spamhaus's `domain` field as an attribution anchor for successor ASNs. An ASN still registered to the tracked entity but announcing nothing has not been recycled: keep it attributed, and when all of an entity's ASNs have been in that state for 6+ months with no new reporting, set its status to `dormant` (§5).

### 3.10 Actor-Preferred Mainstream-Adjacent Providers (Repeat Tenancy)

**Description:** Some capable actors return to the same commercial hosts across campaigns even though those hosts are not bulletproof - they run KYC and an AUP, are absent from DROP/ASN-DROP and show ordinary reputation density. The hoster is chosen for availability, locations and payment convenience, and the actor rents fresh VPS in the same blocks each time, so exact IPs burn but /24s and ASNs recur.

**Indicators:**
- The same provider appears in several independent campaign IOC lists years apart, usually at different exact IPs
- Reuse clusters at /22-/24 level inside a few provider blocks
- Multiple unrelated advanced actors share the provider (espionage and ransomware)
- No evidence of deliberate enablement (no forum advertising, KYC present)

**Observed in:** HostZealot / HZ Hosting Ltd - 4 of 10 Cl0p mass-exploitation campaigns (Accellion 2020, GoAnywhere and MOVEit 2023, Cleo 2024), plus SideWinder, Akira/Fog and DanaBot tenants; see `analysis/CL0P_HOSTZEALOT_REUSE.md`. Also ReliableSite, Datahome and Data Campus in the Cl0p data.

**Handling:** Classify on enablement evidence (usually T4/T5), but use the actor-specific blocks as a watchlist and risk-scoring input for 2-3 years after they burn rather than for blanket blocking.

---

## 4. Identification Signals Matrix

Based on Recorded Future's TAE framework, adapted and expanded for BPH-specific assessment. Use this matrix when evaluating an unknown hosting provider.

### Operational Signals (How the entity conducts business)

| Signal | Description | Weight |
|--------|-------------|--------|
| **No formal storefront** | Operates without a formal physical or virtual business presence; no verifiable office, datacenter tours, or public-facing team | High |
| **Messaging-only business** | Conducts business exclusively via email, Telegram, or encrypted messaging — no phone, no ticketing system, no formal sales process | High |
| **No KYC enforcement** | Does not verify customer identity; accepts anonymous registrations and cryptocurrency-only payment | High |
| **Underground forum presence** | Actively advertises on cybercriminal forums (XSS, Exploit, BreachForums, cracked.io) | Critical |
| **Anonymous payment only** | Accepts only cryptocurrency (especially Monero/privacy coins) with no fiat payment option | Medium |
| **Short corporate history** | Entity incorporated within last 24 months with immediate high-volume hosting operations | Medium |

### Technical Signals (What the network looks like)

| Signal | Description | Weight |
|--------|-------------|--------|
| **High malicious traffic ratio** | Disproportionate concentration of validated malicious activity relative to total IP space | Critical |
| **Selective abuse response** | Responds to some abuse reports but not others, or responds only to threats of upstream disconnection | High |
| **Bulletproof self-identification** | Explicitly markets as "bulletproof," "abuse-proof," or "we ignore Spamhaus/abuse reports" | Critical |
| **No route diversification** | All prefixes routed through a single upstream, especially if that upstream is a known enabler | High |
| **Frequent prefix churn** | IP prefixes being announced and withdrawn at rates inconsistent with normal business operations | High |
| **ASN-DROP inclusion** | Listed on Spamhaus ASN-DROP (`spamhaus.org/drop/asndrop.json`) or an equivalent community-maintained "do not route" list. Query the JSON feed — the legacy `.txt` returns zero listings while still looking fresh, which silently turns this criterion off | Critical |

### Governance Signals (How the entity is structured)

| Signal | Description | Weight |
|--------|-------------|--------|
| **Anonymity over compliance** | Prioritizes customer anonymity over regulatory compliance (no data retention, no LE cooperation) | High |
| **Non-cooperative with LE** | Ignores or systematically delays law enforcement requests; located in non-cooperative jurisdiction | High |
| **Shell company structure** | Corporate registration consistent with obfuscation (nominee directors, virtual offices, offshore) | Medium |
| **Sanctioned personnel** | Officers, directors, or beneficial owners appear on OFAC SDN, EU consolidated list, or equivalent | Critical |
| **Dissolved-but-live** | Corporate entity dissolved or struck off but ASN/network continues to operate | High |

### Signal Scoring Guide

| Signals Present | Assessment |
|----------------|------------|
| 1 Critical + 2 High | Minimum T2 classification |
| 2+ Critical | Minimum T1 classification pending corroboration |
| 3+ High (no Critical) | T3 classification |
| 2 High or 2+ Medium | T4 classification |
| 1 Medium or 1 High | T5 classification |

---

## 5. Status Lifecycle Model

Each provider carries a **status** reflecting its current operational and legal state, independent of its risk tier.

```
                    +-----------+
                    |  ACTIVE   |  Operating, no formal adverse action
                    +-----+-----+
                          |
            +-------------+-------------+
            |                           |
      +-----v-----+             +------v------+
      |  FLAGGED   |             |  SUSPECTED  |
      | Evidence   |             | Limited     |
      | mounting   |             | indicators  |
      +-----+------+             +------+------+
            |                           |
            +-------------+-------------+
                          |
                    +-----v-----+
                    | SANCTIONED|  Formal designation by government authority
                    +-----+-----+
                          |
            +-------------+-------------+
            |                           |
      +-----v-----+             +------v------+
      |  EVADING   |             |  DISSOLVED  |
      | Operating  |             | Corporate   |
      | under new  |             | entity dead |
      | identity   |             | Network may |
      +------------+             | persist     |
                                 +-------------+
```

> **Auxiliary states** are also used in the database alongside the core lifecycle above: `seized` (law-enforcement seizure of infrastructure, whole or partial), `exposed` (publicly identified as a malicious operation or front by credible research/media, but not yet formally sanctioned or seized) and `dormant` (network resources still held, but nothing announced and no new reporting for 6+ months; added 2026-09-25). All three can co-occur with any risk tier. When a `dormant` network re-announces prefixes or its ASN changes hands, reassess and restore an operating status (`active`, `flagged` or `suspected`) or apply §3.9.

### Status Definitions

| Status | Definition | Action Implications |
|--------|-----------|-------------------|
| `active` | Operating with no formal government adverse action. May still carry high risk tier. | Monitor per risk tier |
| `flagged` | Mounting evidence of malicious enablement from multiple sources. Under active investigation or community scrutiny. | Enhanced monitoring; prepare for escalation |
| `suspected` | Limited but credible indicators from single or few sources. Requires further investigation. | Targeted monitoring; research enrichment priority |
| `sanctioned` | Formally designated by OFAC, the EU, the UK (FCDO), Australian DFAT, or an equivalent authority. | Mandatory compliance blocking; transactions prohibited; secondary sanctions exposure |
| `evading` | Operating under a new corporate identity or through successor entities post-sanctions. Infrastructure continuity confirmed. | Track successor entities; report to OFAC/OFSI evasion units; block successor infrastructure |
| `dissolved` | Corporate entity dissolved, struck off, or otherwise legally defunct. Network infrastructure may still be operational. | Monitor for network persistence; track ASN/prefix fate |
| `seized` | Law-enforcement seizure of the entity's infrastructure (whole or partial). Operations halted or materially degraded; a clearnet storefront or re-enrollment path may persist. | Confirm infrastructure offline; track operator re-emergence; preserve seizure as an attribution anchor |
| `exposed` | Publicly identified/outed as a malicious operation or front company by credible research or media, but not (yet) formally sanctioned or seized. | Treat as high-confidence malicious; monitor for sanctions/LE follow-through and rebranding |
| `dormant` | Entity still holds its network resources (ASN registered to it; company not dissolved) but announces no prefixes and has drawn no new reporting for 6+ months, and no dissolution, sanction or seizure explains the silence. The risk tier is kept. | Keep ASN watch rules for re-announcement or transfer; move historical-prefix blocks to the hunt tier (Playbook §8.2); reassess before any de-escalation |

---

## 6. Evidence Standards

### Source Reliability Scale

| Grade | Description | Examples |
|-------|-------------|---------|
| **A — Government/Official** | Sanctions designations, LE press releases, court filings, regulatory actions | OFAC SDN entries, Europol press releases, EU Council decisions |
| **B — Established CTI Vendor** | Published research from recognized threat intelligence firms with named analysts and methodology | Recorded Future Insikt, Mandiant, CrowdStrike, Trend Micro, Unit 42, Intel 471 |
| **C — Community/Independent** | Reputable independent researchers, community blocklists and registry mirrors, investigative journalism | Krebs on Security, abuse.ch, Spamhaus, Team Cymru, Qurium, ipverse/RIR-derived registry mirrors |
| **D — Single Source / Unverified** | Single blog post, social media, anonymous tip, unconfirmed OSINT | Individual Twitter/X posts, Reddit, Telegram channel claims |
| **E — Self-Reported / Marketing** | Provider's own marketing materials, forum posts, AUP text | "We are bulletproof" forum ads, provider websites |

### Minimum Evidence for Tier Assignment

| Tier | Minimum Evidence Requirement |
|------|----------------------------|
| T1 | Grade A source OR 3+ independent Grade B/C sources with convergent findings |
| T2 | 2+ independent Grade B/C sources with specific technical indicators (IPs, domains, malware hashes) |
| T3 | 1 Grade B source with specific indicators OR 2+ Grade C sources with convergent findings |
| T4 | 1 Grade B/C source with behavioral indicators OR documented marketing/policy patterns |
| T5 | Any credible source with structural indicators warranting monitoring |

---

## 7. Glossary

| Term | Definition |
|------|-----------|
| **ASN** | Autonomous System Number — unique identifier for a network's routing policy on the internet |
| **BPH** | Bullet-Proof Hosting — hosting services designed to resist takedown by ignoring abuse reports, operating in non-cooperative jurisdictions, and/or rapidly migrating infrastructure |
| **C2** | Command and Control — server infrastructure used by malware to receive instructions and exfiltrate data |
| **CIDR** | Classless Inter-Domain Routing — IP address range notation (e.g., 185.215.113.0/24) |
| **CaaS** | Crime-as-a-Service — criminal business model where tools, infrastructure, or services are offered to other criminals on a subscription or per-use basis |
| **KYC** | Know Your Customer — identity verification requirements for financial and business services |
| **LIR** | Local Internet Registry — organization allocated IP address space by a Regional Internet Registry (RIR) for assignment to end users |
| **OFAC** | Office of Foreign Assets Control — US Treasury department administering sanctions |
| **OFSI** | Office of Financial Sanctions Implementation — HM Treasury body that implements and enforces UK financial sanctions. Designations are made by the FCDO and published on the **UK Sanctions List**, which replaced OFSI's Consolidated List on 2026-01-28 |
| **Prefix** | A block of IP addresses announced via BGP, expressed in CIDR notation |
| **RIR** | Regional Internet Registry — organization managing IP address allocation for a geographic region (RIPE NCC for Europe, ARIN for North America, etc.) |
| **TAE** | Threat Activity Enabler — Recorded Future's term for entities providing infrastructure or services that enable malicious cyber operations |
| **Threat Density Score** | Recorded Future metric: concentration of validated malicious activity relative to total IP address prefixes a network announces |

---

> **Evidence floor on escalation (2026-09-25).** The escalation triggers above never override §6. Where the only independent B/C source is the Spamhaus listing itself, hold the entity at T3 with status `flagged` and record the pending escalation in `notes` (as of 2026-09-25: NETINNOVATIONLLC, Tiger Network Limited, HostSlick). Where Spamhaus plus one independent vendor provide specific indicators, apply T2 (e.g. VPSVault.host, Feo Prest with GreyNoise).

*This taxonomy is a living document. Update as new patterns emerge, sanctions are issued, or classification criteria require refinement.*
