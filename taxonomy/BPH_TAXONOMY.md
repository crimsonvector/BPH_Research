# BPH & Threat Activity Enabler (TAE) Taxonomy Framework

> **Version:** 1.0 | **Last Updated:** 2026-05-16 | **Maintainer:** CrimsonVector Research
>
> This document defines the classification system used across the BPH Research repository. All provider assessments, risk ratings, and analytical products reference this taxonomy.

---

## Table of Contents

1. [Risk Tier Definitions](#1-risk-tier-definitions)
2. [Provider Type Classification](#2-provider-type-classification)
3. [Operational Pattern Taxonomy](#3-operational-pattern-taxonomy)
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
- Designated by OFAC, EU, UK OFSI, or Australian DFAT sanctions specifically for hosting/enabling cyber operations
- Subject of law enforcement seizure or takedown action targeting hosting infrastructure
- Self-advertises as "bulletproof" on underground forums with corroborating infrastructure evidence
- Recorded Future Threat Density Score in top decile with sustained concentration over 6+ months
- Multiple independent CTI vendors (3+) classify as BPH/TAE with named malware families or threat actors hosted

**Blocking Recommendation:** Block at CIDR/ASN level. Monitor for prefix migration.

**Current T1 entities (illustrative; `BPH_Master.csv` is authoritative):** Aeza International, Stark Industries Solutions, Zservers/XHOST, Media Land LLC, FUNNULL Technology/CTG Server, ELITETEAM/1337TEAM, PROSPERO OOO/Proton66, WorkTitans/THE.Hosting, Hypercore, PQ Hosting Plus, CrazyRDP (seized), Garantex (financial enabler)

---

### T2 — High Risk TAE

**Definition:** Entity exhibiting strong, consistent indicators of enabling malicious operations but lacking formal sanctions designation or confirmed law enforcement action. Distinguished from T3 by volume, persistence, and diversity of malicious activity observed.

**Criteria (meet 3+):**
- Abuse.ch ASN-DROP list inclusion or equivalent community blocklist
- Documented hosting of C2 infrastructure for 3+ distinct malware families
- No meaningful abuse response despite repeated reporting
- Corporate structure designed to obscure beneficial ownership (shell companies, nominee directors, multi-jurisdiction layering)
- Upstream for or downstream of a T1 entity with no route diversification
- RF Threat Density Score above 5% sustained for 3+ months

**Blocking Recommendation:** Block known malicious prefixes; consider ASN-level block with allowlisting for confirmed legitimate customers.

**Current T2 entities (illustrative; `BPH_Master.csv` is authoritative):** Femo IT/Defhost, Tnsecurity/EVILEMPIRE, Railnet/Virtualine, QWINS LTD, Karina Rashkovska, GCSAS, aurologic GmbH (upstream enabler), MIRhosting, PINSPB, SWISSNETWORK02/Global-Data, WAIcore, First Server Limited, UFO Hosting (evading)

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

**Current T3 entities (illustrative; `BPH_Master.csv` is authoritative):** Cloudzy/abrNOC, metaspinner net, KPROHOST, Altawk, HostSlick, StarCloud Global, Kaopu Cloud HK

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

**Current T4 entities (illustrative; `BPH_Master.csv` is authoritative):** BuyVM/Frantech, AlexHost, PrivateAlps/Private Layer, FlokiNET, Shinjiru, Phanes Networks/Flaunt7

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

**Current T5 entities (illustrative; `BPH_Master.csv` is authoritative):** CDNCloud, NECHAEVDS, NETINNOVATIONLLC, Tiger Net, HOSTYPE, 1GSERVERS, DDoS-Guard

---

### Tier Escalation / De-escalation

| Trigger | Direction | Example |
|---------|-----------|---------|
| Sanctions designation | Escalate to T1 | Aeza: T2 → T1 upon OFAC designation (July 2025) |
| LE takedown/seizure | Escalate to T1 | Zservers: T2 → T1 upon trilateral sanctions (Feb 2025) |
| New malware family attribution (3rd+) | Escalate T3 → T2 | Femo IT: accumulated 12+ malware families |
| Underground forum BPH advertising confirmed | Escalate to T2 minimum | PROSPERO: forum advertising confirmed by Intrinsec |
| abuse.ch ASN-DROP inclusion | Escalate to T2 minimum | Tnsecurity/EVILEMPIRE |
| Sustained 12-month clean period + ownership change | De-escalate one tier | (No current examples) |
| Sanctions lifted or LE clears entity | De-escalate, case-by-case | (No current examples) |
| Corporate dissolution with network still live | No de-escalation — reclassify as "dissolved" status | Silent Connection Ltd |

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

**Observed in:** Stark Industries → THE.Hosting (RDP hostname WIN-J9D866ESIJ2 reuse); Virtualine → metaspinner net pivot; Garantex → Grinex/Exved

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

**Observed in:** aurologic GmbH (LIR); Stark Industries pre-sanctions prefix transfers; Zservers post-sanctions prefix-hopping to AS213194, AS61336, AS213010

### 3.5 Prefix Hopping / ASN Migration

**Description:** Moving malicious infrastructure across different IP prefixes or autonomous systems to evade IP-based blocklists and network-level blocking. Often combined with rapid rebranding.

**Indicators:**
- Malicious activity observed migrating across /24 blocks in sequence
- New ASNs announced shortly after old ones are blocklisted
- BGP announcements appearing from previously-unannounced prefixes
- GreyNoise/Shodan scan data showing infrastructure "moving" between ASNs

**Observed in:** Zservers (AS216071 → AS213194 → AS61336 → AS213010); Virtualine shedding /24s to TELCHAK GOLD VENTURES, iHostART, metaspinner

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

**Observed in:** FUNNULL/Triad Nexus (175+ rotating CNAMEs, compromised AWS/Cloudflare/Google/Microsoft accounts); described in Silent Push April 2026

### 3.8 Residential Proxy Abuse

**Description:** Using networks of compromised home devices as proxy layers to mask the true origin of malicious traffic. Distinct from BPH in that the infrastructure is distributed across legitimate ISPs rather than concentrated in datacenter space.

**Indicators:**
- Traffic originating from residential ISP IP ranges
- Compromised IoT devices or malicious VPN applications
- Proxy-as-a-service offerings on underground forums
- Traffic patterns inconsistent with normal residential usage

**Observed in:** Described extensively in IOCTA 2026 Section 1.2; used by ransomware and malware operations for C2 anonymization

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
| **ASN-DROP inclusion** | Listed on abuse.ch or equivalent community-maintained "do not route" lists | Critical |

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

> **Auxiliary states** are also used in the database alongside the core lifecycle above: `seized` (law-enforcement seizure of infrastructure, whole or partial) and `exposed` (publicly identified as a malicious operation or front by credible research/media, but not yet formally sanctioned or seized). Both can co-occur with a risk tier.

### Status Definitions

| Status | Definition | Action Implications |
|--------|-----------|-------------------|
| `active` | Operating with no formal government adverse action. May still carry high risk tier. | Monitor per risk tier |
| `flagged` | Mounting evidence of malicious enablement from multiple sources. Under active investigation or community scrutiny. | Enhanced monitoring; prepare for escalation |
| `suspected` | Limited but credible indicators from single or few sources. Requires further investigation. | Targeted monitoring; research enrichment priority |
| `sanctioned` | Formally designated by OFAC, EU, UK OFSI, Australian DFAT, or equivalent authority. | Mandatory compliance blocking; transactions prohibited; secondary sanctions exposure |
| `evading` | Operating under a new corporate identity or through successor entities post-sanctions. Infrastructure continuity confirmed. | Track successor entities; report to OFAC/OFSI evasion units; block successor infrastructure |
| `dissolved` | Corporate entity dissolved, struck off, or otherwise legally defunct. Network infrastructure may still be operational. | Monitor for network persistence; track ASN/prefix fate |
| `seized` | Law-enforcement seizure of the entity's infrastructure (whole or partial). Operations halted or materially degraded; a clearnet storefront or re-enrollment path may persist. | Confirm infrastructure offline; track operator re-emergence; preserve seizure as an attribution anchor |
| `exposed` | Publicly identified/outed as a malicious operation or front company by credible research or media, but not (yet) formally sanctioned or seized. | Treat as high-confidence malicious; monitor for sanctions/LE follow-through and rebranding |

---

## 6. Evidence Standards

### Source Reliability Scale

| Grade | Description | Examples |
|-------|-------------|---------|
| **A — Government/Official** | Sanctions designations, LE press releases, court filings, regulatory actions | OFAC SDN entries, Europol press releases, EU Council decisions |
| **B — Established CTI Vendor** | Published research from recognized threat intelligence firms with named analysts and methodology | Recorded Future Insikt, Mandiant, CrowdStrike, Trend Micro, Unit 42, Intel 471 |
| **C — Community/Independent** | Reputable independent researchers, community blocklists, investigative journalism | Krebs on Security, abuse.ch, Spamhaus, Brian Krebs, Team Cymru |
| **D — Single Source / Unverified** | Single blog post, social media, anonymous tip, uncomfirmed OSINT | Individual Twitter/X posts, Reddit, Telegram channel claims |
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
| **OFSI** | Office of Financial Sanctions Implementation — UK equivalent of OFAC |
| **Prefix** | A block of IP addresses announced via BGP, expressed in CIDR notation |
| **RIR** | Regional Internet Registry — organization managing IP address allocation for a geographic region (RIPE NCC for Europe, ARIN for North America, etc.) |
| **TAE** | Threat Activity Enabler — Recorded Future's term for entities providing infrastructure or services that enable malicious cyber operations |
| **Threat Density Score** | Recorded Future metric: concentration of validated malicious activity relative to total IP address prefixes a network announces |

---

*This taxonomy is a living document. Update as new patterns emerge, sanctions are issued, or classification criteria require refinement.*
