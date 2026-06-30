# BPH & TAE Ecosystem Map

> **Version:** 1.1 | **Last Updated:** 2026-06-29 | **Maintainer:** CrimsonVector Research
>
> This document maps the bullet-proof hosting (BPH) and Threat Activity Enabler (TAE) ecosystem, charting the supply chain from bare metal to criminal end-user, the geographic clusters where these operations concentrate, the corporate relationship networks that sustain them, and the financial infrastructure that monetizes them. Risk tier references follow the classification system defined in [`taxonomy/BPH_TAXONOMY.md`](../taxonomy/BPH_TAXONOMY.md).

---

> **2026-06 update:** This narrative map predates the June-2026 refresh; `BPH_Master.csv` is the authoritative entity list (now 60 rows). Newly tracked clusters not yet diagrammed below: the **Garantex -> Grinex / A7A5 (Old Vector)** financial-evasion rails (now OFAC-sanctioned); the **SEA guarantee-marketplace** economy (**Huione -> Tudou -> H-Pay Service PLC**; **Dabai Guarantee**); **BtHoster** (UK-shell AS-leasing via Skynet AS214295 / Inside Network AS215476, upstream UAB Host Baltic AS209605); **Pfcloud UG (AS51396)**; the **Asocks** residential-proxy botnet; and OFAC's Iranian exchange designations (Nobitex/Wallex/Bitpin/Ramzinex).

## Table of Contents

1. [The BPH Supply Chain](#1-the-bph-supply-chain)
2. [Geographic Clusters](#2-geographic-clusters)
3. [Corporate Relationship Networks](#3-corporate-relationship-networks)
4. [Upstream/Downstream Dependencies](#4-upstreamdownstream-dependencies)
5. [Financial Infrastructure Overlay](#5-financial-infrastructure-overlay)
6. [Cross-Reference with IOCTA 2026 Themes](#6-cross-reference-with-iocta-2026-themes)

---

## 1. The BPH Supply Chain

BPH infrastructure does not exist in isolation. It depends on the same physical, logical, and financial layers as legitimate hosting but deliberately introduces opacity at each tier. The supply chain runs from physical datacenter through multiple abstraction layers to the criminal end-user, with each layer creating jurisdictional and evidentiary gaps that frustrate law enforcement.

```
+=====================================================================+
|                        BPH SUPPLY CHAIN                             |
+=====================================================================+
|                                                                     |
|  PHYSICAL LAYER (Bare Metal)                                        |
|  +---------------------------------------------------------------+  |
|  | Datacenters / Colocation Facilities                           |  |
|  | - Tornado Datacenter (Langen, DE) - aurologic primary site    |  |
|  | - Chisinau bomb shelter (Moldova) - AlexHost colocation       |  |
|  | - St. Petersburg facilities - Aeza, PINSPB, Media Land        |  |
|  | - Serverion (NL) - colocation for CrazyRDP (now seized)       |  |
|  | - Proprietary deployments by criminal orgs (IOCTA 2026 trend) |  |
|  +---------------------------------------------------------------+  |
|                            |                                        |
|                            v                                        |
|  NETWORK LAYER (Routing & Addressing)                               |
|  +---------------------------------------------------------------+  |
|  | ASN Registration & IP Allocation                               |  |
|  | - RIPE NCC as primary RIR (European/CIS allocations)          |  |
|  | - LIR status grants direct control over IP resources           |  |
|  |   (aurologic, Stark pre-sanctions, others)                    |  |
|  | - ASN registration via RIPE: low barrier, shell-company ready  |  |
|  | - BGP announcement of allocated/transferred prefixes           |  |
|  | - Transit/peering agreements with upstream providers           |  |
|  |   (Tier 1 carriers often unaware of downstream abuse)         |  |
|  +---------------------------------------------------------------+  |
|                            |                                        |
|                            v                                        |
|  SERVICE LAYER (Provisioning & Management)                          |
|  +---------------------------------------------------------------+  |
|  | VPS/RDP Provisioning & Management Platforms                    |  |
|  | - VMmanager / ISPsystem (Russian-origin server mgmt panels)   |  |
|  | - WHMCS (billing & client management automation)               |  |
|  | - Custom panels (some BPH operators build proprietary tools)   |  |
|  | - Automated provisioning: credit card or crypto -> instant VPS |  |
|  | - RDP-as-a-service: pre-configured Windows instances           |  |
|  |   (CrazyRDP model before seizure)                             |  |
|  | - Shared fingerprints across operators using same platforms     |  |
|  |   (WIN-J9D866ESIJ2 hostname reuse across Stark successors)    |  |
|  +---------------------------------------------------------------+  |
|                            |                                        |
|                            v                                        |
|  CUSTOMER LAYER (Criminal End-Users)                                |
|  +---------------------------------------------------------------+  |
|  | Ransomware Affiliates                                          |  |
|  | - LockBit, BianLian, Hunters International (Zservers clients) |  |
|  | - 120+ active ransomware brands in 2025                       |  |
|  | Botnet Operators                                                |  |
|  | - C2 servers, loader distribution, exfiltration staging        |  |
|  | APT Groups                                                      |  |
|  | - Nation-state actors using BPH as cutout infrastructure       |  |
|  | - Hybrid threat actors (criminal infrastructure for state ops) |  |
|  | Infostealer Operators                                           |  |
|  | - Rhadamanthys, Lumma, RedLine distribution & C2               |  |
|  | DDoS-for-Hire / Hacktivism                                      |  |
|  | - NoName057(16) operations                                     |  |
|  | Phishing / Pig-Butchering Syndicates                            |  |
|  | - FUNNULL-hosted scam panels ($200M+ losses)                   |  |
|  +---------------------------------------------------------------+  |
|                            |                                        |
|                            v                                        |
|  FINANCIAL LAYER (Monetization & Payment)                           |
|  +---------------------------------------------------------------+  |
|  | Cryptocurrency Payment Rails                                    |  |
|  | - Bitcoin/USDT/TRON for hosting payments                       |  |
|  | - Garantex (seized) -> Grinex, Exved, A7A5, ABCeX successors  |  |
|  | - Cryptomixer.io (seized Nov 2025, EUR 1.3B mixed since 2016) |  |
|  | - Privacy coins (Monero) for premium anonymity                 |  |
|  | - Chain-hopping via blockchain bridges                          |  |
|  | - Crypto-to-cash desks for final offramp                       |  |
|  | - Designated wallets: TRON TU4tDFRvcKhAZ1jdihojmBWZqvJhQCnJ4F |  |
|  |   (Aeza OFAC-designated)                                      |  |
|  +---------------------------------------------------------------+  |
|                                                                     |
+=====================================================================+
```

### Key Supply Chain Observations

1. **Jurisdictional Layering by Design.** Each supply chain layer typically sits in a different jurisdiction. A physical server in Germany (aurologic/Tornado DC) may be leased to a UK LLP (Femo IT), which sells VPS to an anonymous customer paying via a Seychelles-registered crypto exchange. No single law enforcement agency has visibility across the full chain.

2. **LIR Status as Force Multiplier.** Entities operating as RIPE Local Internet Registries gain direct control over IP address allocation, enabling rapid prefix transfers between related entities without third-party gatekeeping. This is the mechanism behind prefix-hopping evasion (see Taxonomy, Pattern 3.4).

3. **Provisioning Platform Fingerprints.** Shared use of VMmanager/ISPsystem creates detectable fingerprints across ostensibly unrelated BPH operations. The WIN-J9D866ESIJ2 RDP hostname, observed by GreyNoise/Censys migrating from Stark Industries prefixes to THE.Hosting/WorkTitans prefixes, demonstrates that the service layer often survives corporate restructuring unchanged.

4. **Proprietary Infrastructure as Emerging Threat.** IOCTA 2026 documents a trend toward criminal organizations deploying their own hardware in colocation facilities, bypassing the hosting provider layer entirely and eliminating a critical evidence source.

---

## 2. Geographic Clusters

BPH operations concentrate in specific geographic corridors, each offering distinct advantages to operators.

### 2.1 Russia / St. Petersburg Nexus

**Role:** Epicenter of Russian-language BPH operations. St. Petersburg hosts the highest concentration of sanctioned and T1-classified hosting providers globally.

| Provider | ASN(s) | Risk Tier | Status | Key Detail |
|----------|--------|-----------|--------|------------|
| **Aeza International** | AS210644, AS216246 | T1 | Sanctioned (OFAC July 2025) | CEO Penzev arrested April 2025; TRON wallet designated; AS211522 belongs to front Hypercore Ltd |
| **Media Land LLC** | AS206728 + sister ASNs | T1 | Sanctioned (OFAC/UK/AU Nov 2025) | Underground-forum advertised BPH; multiple sister ASNs for redundancy |
| **PINSPB** | AS44050 | T1 | Active | Long-running St. Petersburg BPH provider |
| **PROSPERO / Proton66** | AS200593, AS198953 | T1 | Active | Forum-advertised BPH (confirmed by Intrinsec); aka BEARHOST |
| **ELITETEAM / 1337TEAM** | AS51381 | T1 | Active | Seychelles registration; DDoS-Guard peering; forum presence |
| **UFO Hosting LLC** | AS33993 | T2 | Evading | Russian prefix migration vehicle for Stark Industries |

**Why St. Petersburg:** Proximity to technical talent pools, established underground forum communities (XSS, Exploit), permissive jurisdictional environment for hosting, limited Western LE cooperation, and an ecosystem of crypto payment processors. The city functions as a self-reinforcing cluster where providers share datacenter facilities, transit, and even customers.

### 2.2 UK Shell Company Pattern

**Role:** Preferred jurisdiction for corporate shells due to Companies House ease-of-registration, limited LLP financial filing requirements, and perceived legitimacy of UK-registered entities for RIPE membership.

| Provider | ASN | UK Entity | Status | Key Pattern |
|----------|-----|-----------|--------|-------------|
| **Stark Industries** | (Historical) | Ltd, dissolved | Dissolved / Sanctioned | Original template for UK shell BPH |
| **GCSAS** | AS215540 | LLP OC450701 | Active (T2) | Classic LLP with no financial filings |
| **QWINS** | AS213702 | Ltd | Active (T2) | Short corporate history, immediate ASN |
| **Femo IT / Defhost** | AS214351 | Ltd | Active (T2) | aurologic downstream; 12+ malware families |
| **Hypercore** | AS215552 | Ltd | Sanctioned (Nov 2025) | Aeza front company; sanctioned 5 months after Aeza |
| **XHOST Internet Solutions** | (Multiple) | LP | Active (T1) | Zservers UK front entity |
| **Silent Connection** | AS215240 | Ltd, dissolved | Dissolved | Corporate entity dead but network persisted post-dissolution |
| **Dolphon 1337** | AS215208 | Ltd, dissolved | Dissolved | Name referencing 1337TEAM; short-lived shell |

**The UK Shell Company Playbook:**

```
Step 1: Register UK LLP or Ltd via formation agent (cost: ~GBP 12)
        -> Virtual office address (e.g., 71-75 Shelton Street, London)
        -> Nominee director (often rotated every 6 months)

Step 2: Apply for RIPE membership using UK entity as sponsoring org
        -> LLP has no financial filing requirement
        -> Ltd has minimal filing (confirmation statement only)

Step 3: Register ASN and request IP allocation from RIPE
        -> Announce prefixes via upstream (often aurologic AS30823)

Step 4: Operate BPH services
        -> If entity is flagged or dissolved, transfer resources
        -> Create new shell and repeat

Typical lifecycle: 6-18 months per entity
```

**Why the UK:** Companies House allows online formation in hours for minimal cost. LLPs have no requirement to file financial statements. Confirmation statements require only director name and registered address. Nominee director services are widely available and legal. RIPE NCC accepts UK LLP/Ltd as sponsoring organizations without deep due diligence. The perceived legitimacy of a UK-registered entity provides cover that offshore jurisdictions do not.

### 2.3 Netherlands Infrastructure Hub

**Role:** Preferred jurisdiction for BPH operations requiring legitimate-looking infrastructure, dense peering, and high-bandwidth connectivity.

| Provider | ASN | Location | Risk Tier | Key Detail |
|----------|-----|----------|-----------|------------|
| **MIRhosting B.V.** | AS52000 | Netherlands | T1 | Andrey Nesterenko; Stark infrastructure pillar |
| **WorkTitans / THE.Hosting** | AS209847 | Netherlands | T1 (sanctions evasion) | Youssef Zinad / Fezzy BV; Stark successor |
| **aurologic GmbH** | AS30823 | Langen, DE (NL peering) | T2 (Upstream Enabler) | Central upstream for ~10 downstream BPH ops |

**Why the Netherlands:** The Amsterdam Internet Exchange (AMS-IX) and surrounding facilities provide some of the densest peering in Europe. Netherlands hosting culture has historically been permissive, with strong privacy protections. Dutch B.V. (besloten vennootschap) entities are relatively simple to establish. The proximity to DE-CIX (Frankfurt) and LINX (London) provides excellent connectivity. For BPH operators, the Netherlands offers the appearance of Western European legitimacy combined with high-performance infrastructure.

### 2.4 Moldova Corridor

**Role:** Jurisdiction with limited law enforcement cooperation capacity, functioning as operational base for BPH providers requiring physical infrastructure outside EU/NATO reach.

| Provider | ASN | Location | Risk Tier | Key Detail |
|----------|-----|----------|-----------|------------|
| **AlexHost** | AS200019 | Chisinau | T4 | Colocation in literal bomb shelter; Voxility DDoS mitigation |
| **PQ Hosting Plus S.R.L.** | AS44477 (post-transfer) | Moldova | T1 (sanctions evasion) | Neculiti brothers; AS44477 transferred from Stark pre-sanctions |

**Why Moldova:** Moldova sits outside the EU (though an EU candidate), has limited cybercrime enforcement capacity, and offers geographic proximity to both Russia and Romania. The Neculiti brothers' PQ Hosting operation demonstrates how Moldovan entities serve as waypoints in sanctions evasion chains: AS44477 was transferred from Stark Industries to PQ Hosting Plus S.R.L. before sanctions hit, preserving operational continuity. AlexHost's colocation in a repurposed bomb shelter in Chisinau illustrates the unconventional physical infrastructure available in the jurisdiction.

### 2.5 Asia-Pacific / Triad Nexus

**Role:** Infrastructure laundering, pig-butchering hosting, and CDN-based abuse at scale, often tied to organized crime networks (Triads) operating across Southeast Asia.

| Provider | ASN | Location | Risk Tier | Key Detail |
|----------|-----|----------|-----------|------------|
| **FUNNULL Technology** | (CDN, no single ASN) | China (ops), global (infra) | T1 / Sanctioned | Liu Lizhi; $200M+ pig-butchering; infrastructure laundering |
| **CTG Server Limited** | AS152194 | Hong Kong | T1 | FUNNULL backbone ASN |
| **Kaopu Cloud HK** | AS138915 | Hong Kong | T3 | Associated with APAC BPH cluster |
| **Shinjiru** | AS45839 | Malaysia | T4 | Long-running permissive hoster; "offshore" marketed |
| **StarCloud Global** | (Front brand) | Variable | T5 | FUNNULL front brand |

**The FUNNULL Infrastructure Laundering Model:**

```
FUNNULL CDN Core
      |
      v
CTG Server Limited (AS152194) <-- Backbone routing
      |
      +--> 175+ rotating CNAMEs pointing to:
      |       |
      |       +--> Compromised AWS accounts
      |       +--> Compromised Cloudflare accounts
      |       +--> Compromised Google Cloud accounts
      |       +--> Compromised Microsoft Azure accounts
      |
      +--> US-IP Geofencing
              |
              +--> Returns HTTP 451 to US investigator IPs
              +--> Serves scam content to APAC victim IPs
```

**Why APAC:** Proximity to Triad-operated scam compounds (Myanmar, Cambodia, Laos). Hong Kong's business registration ease. Malaysia's historically permissive hosting regulation. The ability to leverage compromised accounts at global cloud providers (AWS, Cloudflare, Google, Microsoft) means FUNNULL's actual infrastructure footprint is diffuse and parasitic on legitimate platforms, making traditional ASN-based blocking ineffective.

---

## 3. Corporate Relationship Networks

The following diagrams map the specific corporate structures, succession chains, and dependency relationships observed in the BPH ecosystem.

### 3.1 The Stark Industries Sanctions Evasion Chain

Stark Industries Solutions Ltd represents the most thoroughly documented BPH sanctions evasion case, demonstrating how a sanctioned entity can achieve seamless operational continuity through pre-positioned successor entities.

**Timeline:**

| Date | Event |
|------|-------|
| Feb 2022 | Stark Industries Solutions Ltd incorporated (UK) |
| 2022-2024 | Rapid growth; becomes one of Europe's largest BPH operations |
| Pre-May 2025 | AS44477 transferred to PQ Hosting Plus S.R.L. (Moldova) |
| May 2025 | EU sanctions designation against Stark Industries |
| June 2025 | WorkTitans B.V. / THE.Hosting created (Netherlands) |
| Aug-Nov 2025 | Seamless migration confirmed: GreyNoise/Censys observe RDP hostname WIN-J9D866ESIJ2 reuse on WorkTitans/THE.Hosting prefixes |
| Ongoing | Infrastructure continues operating across successor entities |

**Corporate Network Diagram:**

```
        STARK INDUSTRIES SOLUTIONS LTD
        (UK, Dissolved, EU-Sanctioned May 2025)
                      |
     +----------------+----------------+------------------+
     |                |                |                  |
     v                v                v                  v
 AS44477          WorkTitans B.V.   UFO Hosting LLC   MIRhosting B.V.
 (pre-sanctions   / THE.Hosting     (Russia)          (Netherlands)
  transfer)       (Netherlands)      AS33993           AS52000
     |            AS209847                |              |
     v            Youssef Zinad /         v              v
 PQ Hosting       Fezzy BV          Russian prefix   Infrastructure
 Plus S.R.L.          |              migration        pillar;
 (Moldova,            v              vehicle          Nesterenko
  Neculiti       Confirmed by                         long-standing
  brothers)      GreyNoise/Censys:                    BPH enabler
                 RDP hostname
                 WIN-J9D866ESIJ2
                 reuse proves
                 operational
                 continuity
```

**Analytical Assessment:** The Stark evasion chain demonstrates pre-planning. The transfer of AS44477 to PQ Hosting occurred before sanctions, indicating awareness that designation was imminent. WorkTitans B.V. was created one month after sanctions, with Youssef Zinad / Fezzy BV providing a Netherlands-based corporate vehicle with no apparent connection to the sanctioned entity. The RDP hostname reuse (WIN-J9D866ESIJ2) is the forensic smoking gun: it proves that the same server images were migrated from Stark prefixes to WorkTitans prefixes without reimaging, meaning the successor inherited the exact operational infrastructure.

---

### 3.2 The aurologic GmbH Downstream Cluster

aurologic GmbH (AS30823) operates from the Tornado Datacenter in Langen, Germany, with an estimated 1-5 Tbps capacity. It functions as the single most critical upstream enabler in the European BPH ecosystem. Disrupting aurologic would cascade across 10+ downstream BPH operations.

```
                        aurologic GmbH
                         AS30823
                    Langen, Germany
                   Tornado Datacenter
                     1-5 Tbps capacity
                    CEO: [Hofmann]
                           |
        +------------------+------------------+
        |                  |                  |
   +----v----+       +-----v-----+     +------v------+
   | Femo IT |       | Railnet / |     | Tnsecurity  |
   | Defhost |       | Virtualine|     | EVILEMPIRE  |
   | AS214351|       | AS214943  |     | AS216309    |
   | (T2)    |       | (T2)      |     | (T2)        |
   +---------+       +-----------+     +-------------+
        |                  |                  |
   +----v----+       +-----v-----+     +------v------+
   |metaspinn|       | WAIcore   |     | Karina      |
   |er net   |       | AS213887  |     | Rashkovska  |
   |AS209800 |       | (T3)      |     | AS215789    |
   | (T3)    |       +-----------+     | (T2)        |
   +---------+                         +-------------+
        |
   +----v----+       +-----------+     +-------------+
   |KPROHOST |       | Altawk    |     |SWISSNETWORK |
   |AS214940 |       | (T3)      |     |02/Global-   |
   | (T3)    |       +-----------+     |Data System  |
   +---------+                         |AS34888/     |
                                       |AS42624 (T3) |
                                       +-------------+
                           |
                      +----v----+
                      |  Aeza   |
                      |AS210644 |
                      | (T1)    |
                      +---------+
```

**The Hofmann Denial:** aurologic CEO Hofmann has publicly denied a contractual relationship with Aeza. However, BGP routing data consistently shows Aeza prefixes transiting aurologic infrastructure. This discrepancy between stated business relationships and observable routing is itself a significant indicator (see Taxonomy, Pattern 3.3 — Sub-Sub-Leasing). Whether the relationship is direct or mediated through an intermediary, the routing dependency is factual and verifiable.

**Single Point of Failure Analysis:** If aurologic were depeered by its upstream carriers or had its RIPE LIR status revoked, the following downstream operations would lose connectivity simultaneously:

| Downstream | ASN | Tier | Likely Impact |
|-----------|-----|------|---------------|
| Femo IT / Defhost | AS214351 | T2 | Total loss of transit |
| Railnet / Virtualine | AS214943 | T2 | Total loss of transit |
| Tnsecurity / EVILEMPIRE | AS216309 | T2 | Total loss of transit |
| metaspinner net | AS209800 | T3 | Total loss of transit |
| WAIcore | AS213887 | T3 | Total loss of transit |
| Karina Rashkovska | AS215789 | T2 | Total loss of transit |
| KPROHOST | AS214940 | T3 | Total loss of transit |
| Altawk | — | T3 | Total loss of transit |
| SWISSNETWORK02 / Global-Data System | AS34888/AS42624 | T3 | Partial loss (may have alt transit) |
| Aeza | AS210644 | T1 | Partial loss (multi-homed, but aurologic is primary) |

This makes aurologic the highest-leverage intervention point in the European BPH ecosystem.

---

### 3.3 The Aeza Group Front Company Structure

Aeza International Ltd was designated by OFAC in July 2025. The group operated through a web of Russian and international entities, with a UK front (Hypercore LTD) sanctioned separately in November 2025.

```
             AEZA INTERNATIONAL LTD
             (Russia, OFAC-Sanctioned July 2025)
             AS210644 / AS216246  (AS211522 -> Hypercore front)
             TRON: TU4tDFRvcKhAZ1jdihojmBWZqvJhQCnJ4F
                          |
         +----------------+----------------+
         |                |                |
         v                v                v
   Aeza Group LLC   Aeza Logistic   Cloud Solutions
   (Russia)         LLC (Russia)    LLC (Russia)
         |                                 |
         v                                 v
     Datavice                        Hypercore LTD
     (Operational                    (UK, Sanctioned
      brand)                          Nov 2025)
                                     AS215552

   PERSONNEL:
   +------------------------------------------+
   | CEO:  Penzev (arrested April 2025)       |
   | GD:   Bozoyan                            |
   | CTO:  Gast                               |
   | 33% Owner: Knyazev                       |
   +------------------------------------------+
```

**Analytical Assessment:** The five-month gap between Aeza's OFAC designation (July 2025) and Hypercore's designation (November 2025) represents a window during which Hypercore operated as an undesignated successor, presumably continuing to service Aeza's customer base. This delay pattern is common and exploitable: sanctioned entities can pre-position successors that operate in a gray zone until authorities catch up. The arrest of CEO Penzev in April 2025 (before the OFAC designation) suggests that criminal investigation and sanctions tracks were running in parallel. **ASN correction (2026-06):** AS211522 -- previously logged as an Aeza secondary ASN -- is in fact registered to the front company **Hypercore Ltd** (RIPE as-name HYPERCORELTD, created 2025-07-10; Companies House No. 16558658). Aeza migrated 2,100+ IPs from AS210644 to AS211522 beginning 2025-07-20, and OFAC/OFSI designated Hypercore on 2025-11-19.

---

### 3.4 The FUNNULL / Triad Nexus CDN Laundering Network

FUNNULL represents a distinct model from traditional BPH: rather than operating dedicated infrastructure, it parasitically leverages compromised accounts at legitimate cloud providers to create a distributed, resilient, and difficult-to-attribute hosting network.

```
    FUNNULL TECHNOLOGY INC.
    (Sanctioned; Liu Lizhi)
              |
              v
    CTG SERVER LIMITED (AS152194)
    [Backbone / Core Routing]
              |
              +--> 175+ Rotating CNAMEs
              |         |
              |    +----+----+----+----+
              |    |    |    |    |    |
              |    v    v    v    v    v
              |   AWS  CF  GCP  MSFT  Other
              |   (compromised accounts at each)
              |
              +--> StarCloud Global (front brand)
              |
              +--> US-IP Geofencing Layer
              |    Returns HTTP 451 to US IPs
              |    Serves scam content to APAC victims
              |
              +--> $200M+ pig-butchering losses attributed
              |
              +--> Infrastructure laundering cycle:
                   1. Compromise/fraudulently register cloud account
                   2. Deploy scam infrastructure
                   3. CNAME rotation every 24-72 hours
                   4. Account burned -> acquire new account
                   5. Repeat at scale across providers
```

**Why This Model Is Dangerous:** Traditional BPH can be disrupted by depeering an ASN or blocking a CIDR range. FUNNULL's model distributes malicious infrastructure across the IP space of the world's most trusted cloud providers, making IP-based blocking impractical without causing massive collateral damage to legitimate services. The geofencing layer adds an additional evasion mechanism: investigators in the US see a 451 compliance page, while victims in APAC see the scam content, complicating evidence collection across jurisdictions.

---

### 3.5 The Zservers Post-Sanctions Prefix-Hopping

Zservers and its UK front entity XHOST Internet Solutions LP were subject to trilateral sanctions (US, UK, AU) in February 2025 following Chainalysis tracing of payments from LockBit, BianLian, and Hunters International ransomware operations, as well as links to the 2022 Medibank breach in Australia.

```
    ZSERVERS (Historical: AS216071)
    + XHOST INTERNET SOLUTIONS LP (UK front)
    [Trilateral Sanctions: Feb 2025 — US/UK/AU]
              |
              | Post-sanctions prefix migration:
              |
              +---> AS213194 (first hop)
              |
              +---> AS61336  (second hop)
              |
              +---> AS213010 (third hop)
              |
              +---> [additional hops expected]

    CONFIRMED CRIMINAL CLIENTS (Chainalysis):
    +------------------------------------------+
    | LockBit (ransomware)                     |
    | BianLian (ransomware)                    |
    | Hunters International (ransomware)       |
    | 2022 Medibank breach infrastructure      |
    +------------------------------------------+
```

**Prefix-Hopping Mechanics:** After the February 2025 sanctions, Zservers' original AS216071 became unusable for BGP announcement (upstream carriers depeered it). The operators responded by moving prefixes to AS213194, then to AS61336, then to AS213010 — each time using a different organizational wrapper for RIPE registration. This pattern exploits the latency in blocklist propagation: by the time the security community updates blocklists for one ASN, the infrastructure has already migrated to the next.

**Tracking Methodology:** Prefix-hopping can be tracked by monitoring: (a) BGP announcements for prefixes previously associated with sanctioned entities, (b) shared technical fingerprints (TLS certificates, server banners, scan behavior) across ASNs, and (c) GreyNoise/Shodan temporal analysis showing infrastructure "teleporting" between networks.

---

## 4. Upstream/Downstream Dependencies

### Critical Chokepoints

The BPH ecosystem contains several single points of failure where intervention would produce outsized disruption.

| Chokepoint | Type | Downstream Impact | Intervention Leverage |
|-----------|------|-------------------|----------------------|
| **aurologic GmbH (AS30823)** | Upstream Enabler | ~10 downstream BPH operations lose transit (see Section 3.2) | RIPE LIR revocation or upstream depeering would cascade across T1-T3 entities |
| **DDoS-Guard (AS49612)** | DDoS Mitigation / Peering | ELITETEAM (AS51381) and broader Russian BPH ecosystem lose DDoS protection | Challenging — DDoS-Guard also serves Russian government sites, complicating targeted action |
| **Voxility** | DDoS Mitigation | AlexHost (AS200019) loses DDoS protection layer | Voxility has legitimate customer base; targeted policy enforcement more appropriate than blanket action |
| **Serverion (NL)** | Colocation | CrazyRDP infrastructure (now seized) was physically hosted here | Already actioned — LE seizure demonstrates colocation as viable intervention point |
| **RIPE NCC** | Resource Registry | All European BPH operations depend on RIPE for ASN/IP resources | Policy-level intervention (stricter LIR vetting, faster deregistration of shell-company members) |

### Dependency Matrix

```
                    UPSTREAM PROVIDERS
                    ==================
                    aurologic (AS30823)
                    DDoS-Guard (AS49612)
                    Tier 1 Transit (various)
                    Voxility (DDoS mitigation)
                          |
          +---------------+---------------+
          |               |               |
    +-----------+   +-----------+   +-----------+
    | T1 BPH    |   | T2 BPH    |   | T3/T4     |
    | Providers |   | Providers |   | Providers |
    +-----------+   +-----------+   +-----------+
    | Aeza      |   | Femo IT   |   | metaspinner|
    | Media Land|   | GCSAS     |   | KPROHOST  |
    | PROSPERO  |   | QWINS     |   | Altawk    |
    | ELITETEAM |   | Tnsecurity|   | WAIcore   |
    | Zservers  |   | Railnet   |   | HostSlick |
    | FUNNULL   |   | K.Rashkov.|   | NECHAEVDS |
    | Stark*    |   |           |   |           |
    +-----------+   +-----------+   +-----------+
          |               |               |
          +---------------+---------------+
                          |
                    END-USER CRIMINALS
                    ==================
                    Ransomware affiliates
                    Botnet operators
                    APT groups
                    Phishing operators
                    DDoS-for-hire
```

### Peering Relationships of Note

| Provider A | Relationship | Provider B | Significance |
|-----------|-------------|-----------|--------------|
| ELITETEAM (AS51381) | Peering | DDoS-Guard (AS49612) | DDoS-Guard provides resilience for ELITETEAM operations |
| aurologic (AS30823) | Transit | Aeza (AS210644) | Primary transit for sanctioned entity (disputed by Hofmann) |
| aurologic (AS30823) | Transit | Femo IT (AS214351) | Direct downstream relationship |
| aurologic (AS30823) | Transit | Tnsecurity (AS216309) | Direct downstream relationship |
| Voxility | DDoS mitigation | AlexHost (AS200019) | DDoS protection layer for Moldova-based hoster |
| MIRhosting (AS52000) | Infrastructure | Stark successors | Nesterenko as long-standing infrastructure pillar |

---

## 5. Financial Infrastructure Overlay

The BPH ecosystem depends on a parallel financial infrastructure optimized for anonymity, sanctions evasion, and high-volume cryptocurrency processing.

### 5.1 The Garantex Succession

Garantex, designated by OFAC in April 2022 and seized by LE in March 2025, was the central financial node for Russian-language cybercrime. Its seizure triggered fragmentation into multiple successor platforms.

```
              GARANTEX
    (OFAC April 2022 / Seized March 2025)
                  |
    +-------------+-------------+
    |      |      |      |      |
    v      v      v      v      v
 Grinex  Exved  InDeFi  A7A5  ABCeX
              Bank
    |      |      |      |      |
    v      v      v      v      v
 Rapira  Exmo  Aifory  Bitpapa MKAN
              Pro              Coin
```

| Successor | Status | Notes |
|-----------|--------|-------|
| **Grinex** | Active | Primary successor; same operator base suspected |
| **Exved** | Active | Secondary successor platform |
| **InDeFi Bank** | Active | DeFi-native successor |
| **A7A5** | Active | Lower-profile exchange |
| **ABCeX** | Active | Lower-profile exchange |
| **Rapira** | Active | Russian-language exchange |
| **Exmo** | Active | Pre-existing exchange absorbing Garantex users |
| **Aifory Pro** | Active | Newer entrant |
| **Bitpapa** | Active | P2P exchange model |
| **MKAN Coin** | Active | Newer entrant |

### 5.2 Cryptocurrency Mixing and Laundering

| Service | Status | Volume | Relevance |
|---------|--------|--------|-----------|
| **Cryptomixer.io** | Seized (Nov 2025) | EUR 1.3B mixed since 2016 | Primary mixer for BPH payment laundering; seizure disrupted but did not eliminate mixing |
| **Blockchain bridges** | Active (various) | Unknown | Chain-hopping: BTC -> bridge -> altchain -> bridge -> USDT on TRON |
| **Privacy coins (Monero)** | Active | Unknown | XMR used for premium-tier BPH payments where traceability must be minimized |
| **Crypto-to-cash desks** | Active (CIS region) | Unknown | Physical cash conversion; final offramp from crypto to fiat |

### 5.3 Designated Wallets and On-Chain Indicators

| Entity | Wallet | Chain | Designation |
|--------|--------|-------|-------------|
| **Aeza International** | TU4tDFRvcKhAZ1jdihojmBWZqvJhQCnJ4F | TRON | OFAC SDN (July 2025) |
| **Zservers** | (Multiple, Chainalysis-identified) | BTC/TRON | Trilateral sanctions (Feb 2025) |

### 5.4 Financial Flow Diagram

```
    CRIMINAL END-USER
    (ransomware affiliate, botnet operator, etc.)
              |
              | Pays in BTC/USDT/XMR
              v
    +-------------------+
    | BPH PROVIDER      |
    | (Aeza, Zservers,  |
    | Media Land, etc.) |
    +-------------------+
              |
              | Revenue in crypto
              v
    +-------------------+        +-------------------+
    | MIXER / TUMBLER   |------->| BLOCKCHAIN BRIDGE |
    | (Cryptomixer.io   |        | (BTC->ETH->TRON)  |
    | successors)       |        +-------------------+
    +-------------------+                |
              |                          v
              v                  +-------------------+
    +-------------------+        | PRIVACY COIN      |
    | EXCHANGE          |        | CONVERSION        |
    | (Grinex, Exved,   |        | (BTC->XMR->BTC)   |
    | A7A5, etc.)       |        +-------------------+
    +-------------------+                |
              |                          v
              +------------+-------------+
                           |
                           v
                  +-------------------+
                  | FIAT OFFRAMP      |
                  | - Crypto-to-cash  |
                  |   desks (CIS)     |
                  | - P2P exchanges   |
                  | - Nested accounts |
                  +-------------------+
```

---

## 6. Cross-Reference with IOCTA 2026 Themes

Europol's Internet Organised Crime Threat Assessment (IOCTA) 2026 identifies several strategic themes that directly intersect with the BPH ecosystem mapped above.

### 6.1 Ransomware-as-a-Service (RaaS)

**IOCTA 2026 Finding:** 120+ active ransomware brands operated in 2025, representing continued growth and fragmentation of the RaaS ecosystem.

**BPH Nexus:** Every RaaS operation requires hosting infrastructure for: (a) affiliate panels, (b) negotiation/payment portals, (c) data leak sites, (d) C2 servers, and (e) payload staging. BPH providers are the infrastructure backbone:

| RaaS Operation | Known BPH Provider | Evidence Source |
|---------------|-------------------|-----------------|
| LockBit | Zservers | Chainalysis payment tracing |
| BianLian | Zservers | Chainalysis payment tracing |
| Hunters International | Zservers | Chainalysis payment tracing |
| Multiple (unnamed) | Aeza, PROSPERO, Media Land | Recorded Future TAE reports; multiple CTI vendors |

### 6.2 Infostealer Distribution

**IOCTA 2026 Finding:** Infostealers represent a growing initial access vector, with credential markets fueling downstream attacks.

**BPH Nexus:** Infostealer distribution and C2 infrastructure concentrates on BPH networks:

| Infostealer | BPH Association | Infrastructure Role |
|------------|----------------|---------------------|
| Rhadamanthys | Multiple T1-T2 providers | C2 servers, payload distribution |
| Lumma | Multiple T1-T2 providers | C2 servers, exfiltration staging |
| RedLine | Multiple T1-T2 providers | C2 servers, credential panel hosting |

Femo IT/Defhost (AS214351) alone has been associated with 12+ distinct malware families, illustrating how a single BPH provider can host infrastructure for multiple concurrent infostealer campaigns.

### 6.3 DDoS-for-Hire and Hacktivism

**IOCTA 2026 Finding:** DDoS-for-hire services continue to proliferate, with hacktivist groups leveraging cybercriminal infrastructure.

**BPH Nexus:** NoName057(16) and similar pro-Russian hacktivist groups use BPH infrastructure for DDoS amplification and C2. ELITETEAM (AS51381) with DDoS-Guard peering provides a resilient platform for DDoS operations — the irony of DDoS mitigation infrastructure protecting DDoS-for-hire operations is not lost on the analytical community.

### 6.4 Hybrid Threat Actors

**IOCTA 2026 Finding:** The boundary between state-sponsored and criminal cyber operations continues to blur, with state actors using cybercriminal infrastructure as proxy.

**BPH Nexus:** BPH infrastructure provides deniability for state-aligned operations. A nation-state actor purchasing VPS from a BPH provider like PROSPERO or Media Land through anonymous cryptocurrency payment creates an attribution gap that is functionally identical to the one enjoyed by criminal users. This dual-use nature makes BPH infrastructure a strategic enabler for hybrid warfare.

### 6.5 DNS Abuse

**IOCTA 2026 Finding:** DNS infrastructure abuse for C2 communication, phishing delivery, and fast-flux continues to be a primary threat vector.

**BPH Nexus:** BPH providers typically do not enforce DNS abuse policies. Malicious domains hosted on BPH networks can serve as: phishing landing pages, C2 communication channels via DNS tunneling, fast-flux domain infrastructure with rapidly rotating A records across BPH IP space, and DGA (Domain Generation Algorithm) resolution targets.

### 6.6 Residential Proxy Ecosystem

**IOCTA 2026 Finding:** The residential proxy market, both legitimate and malicious, creates anonymization layers that complicate attribution and enforcement.

**BPH Nexus:** While residential proxies are distinct from datacenter-based BPH, the two ecosystems are complementary. Criminal operators use BPH for persistent infrastructure (C2 servers, panels, staging) and residential proxies for transient operations (credential stuffing, account takeover, initial access). Some BPH providers offer proxy services directly or host the management infrastructure for residential proxy botnets. The convergence of these two infrastructure types represents an evolution in criminal operational security.

---

## Appendix A: Entity Quick Reference

| Entity | ASN(s) | Tier | Status | Geographic Cluster | Primary Role |
|--------|--------|------|--------|--------------------|--------------|
| Aeza International | AS210644, AS216246 | T1 | Sanctioned | Russia / St. Petersburg | Pure BPH |
| AlexHost | AS200019 | T4 | Active | Moldova | BPH-Adjacent |
| Altawk | — | T3 | Active | UK Shell | BPH downstream |
| aurologic GmbH | AS30823 | T2 | Active | Germany/Netherlands | Upstream Enabler |
| CTG Server Limited | AS152194 | T1 | Active | Hong Kong | FUNNULL backbone |
| DDoS-Guard | AS49612 | T5 | Active | Russia | Dual-use / Peering |
| Dolphon 1337 | AS215208 | — | Dissolved | UK Shell | Corporate Shell |
| ELITETEAM / 1337TEAM | AS51381 | T1 | Active | Russia (Seychelles reg.) | Pure BPH |
| Femo IT / Defhost | AS214351 | T2 | Active | UK Shell | BPH downstream |
| FUNNULL Technology | CDN | T1 | Sanctioned | APAC / Triad Nexus | Infrastructure Laundering |
| GCSAS | AS215540 | T2 | Active | UK Shell | Corporate Shell / BPH |
| Hypercore LTD | AS215552, AS211522 | T1 | Sanctioned | UK Shell | Sanctions Evasion (Aeza) |
| Kaopu Cloud HK | AS138915 | T3 | Active | Hong Kong | APAC BPH cluster |
| Karina Rashkovska | AS215789 | T2 | Active | UK Shell / aurologic | BPH downstream |
| KPROHOST | AS214940 | T3 | Active | aurologic downstream | BPH downstream |
| Media Land LLC | AS206728 + sisters | T1 | Sanctioned | Russia / St. Petersburg | Pure BPH |
| metaspinner net | AS209800 | T3 | Active | aurologic downstream | BPH downstream |
| MIRhosting B.V. | AS52000 | T1 | Active | Netherlands | Infrastructure Pillar |
| PINSPB | AS44050 | T1 | Active | Russia / St. Petersburg | Pure BPH |
| PQ Hosting Plus S.R.L. | AS44477 | T1 | Sanctioned | Moldova | Sanctions Evasion (Stark) |
| PROSPERO / Proton66 | AS200593, AS198953 | T1 | Active | Russia | Pure BPH |
| QWINS LTD | AS213702 | T2 | Active | UK Shell | BPH |
| Railnet / Virtualine | AS214943 | T2 | Active | aurologic downstream | BPH downstream |
| Shinjiru | AS45839 | T4 | Active | Malaysia | BPH-Adjacent |
| Silent Connection | AS215240 | — | Dissolved | UK Shell | Corporate Shell |
| StarCloud Global | — | T5 | Active | APAC | FUNNULL front brand |
| Stark Industries | (Historical) | T1 | Dissolved/Sanctioned | UK Shell / Moldova | Pure BPH (historical) |
| SWISSNETWORK02 / Global-Data | AS34888, AS42624 | T3 | Active | aurologic downstream | BPH downstream |
| Tnsecurity / EVILEMPIRE | AS216309 | T2 | Active | aurologic downstream | BPH downstream |
| UFO Hosting LLC | AS33993 | T2 | Evading | Russia | Sanctions Evasion (Stark) |
| WAIcore | AS213887 | T3 | Active | aurologic downstream | BPH downstream |
| WorkTitans / THE.Hosting | AS209847 | T1 | Evading | Netherlands | Sanctions Evasion (Stark) |
| XHOST Internet Solutions LP | Multiple | T1 | Active | UK Shell | Zservers front entity |
| Zservers | AS216071 (historical) | T1 | Sanctioned | Russia | Pure BPH |

## Appendix B: ASN Cross-Reference Index

| ASN | Entity | Tier | Notes |
|-----|--------|------|-------|
| AS30823 | aurologic GmbH | T2 | Critical upstream; LIR |
| AS33993 | UFO Hosting LLC | T2 | Stark Russian prefix vehicle |
| AS34888 | SWISSNETWORK02 | T3 | aurologic downstream |
| AS42624 | Global-Data System | T3 | aurologic downstream |
| AS44050 | PINSPB | T1 | St. Petersburg BPH |
| AS44477 | PQ Hosting Plus S.R.L. | T1 | Transferred from Stark pre-sanctions |
| AS45839 | Shinjiru | T4 | Malaysia permissive hoster |
| AS49612 | DDoS-Guard | T5 | Dual-use; ELITETEAM peer |
| AS51381 | ELITETEAM / 1337TEAM | T1 | Seychelles; forum-advertised |
| AS52000 | MIRhosting B.V. | T1 | Nesterenko; Stark infra pillar |
| AS61336 | Zservers (hop 2) | T1 | Post-sanctions prefix hop |
| AS138915 | Kaopu Cloud HK | T3 | APAC BPH cluster |
| AS152194 | CTG Server Limited | T1 | FUNNULL backbone |
| AS198953 | Proton66 | T1 | PROSPERO sister ASN |
| AS200019 | AlexHost | T4 | Chisinau bomb shelter |
| AS200593 | PROSPERO | T1 | Forum-advertised BPH |
| AS206728 | Media Land LLC | T1 | St. Petersburg; sister ASNs |
| AS209800 | metaspinner net | T3 | aurologic downstream |
| AS209847 | WorkTitans / THE.Hosting | T1 | Stark successor; Zinad/Fezzy BV |
| AS210644 | Aeza International | T1 | OFAC-sanctioned; primary ASN |
| AS211522 | Hypercore LTD | T1 | Aeza front; RIPE HYPERCORELTD (created 2025-07-10) |
| AS213010 | Zservers (hop 3) | T1 | Post-sanctions prefix hop |
| AS213194 | Zservers (hop 1) | T1 | Post-sanctions prefix hop |
| AS213702 | QWINS LTD | T2 | UK shell BPH |
| AS213887 | WAIcore | T3 | aurologic downstream |
| AS214351 | Femo IT / Defhost | T2 | aurologic downstream; 12+ malware families |
| AS214940 | KPROHOST | T3 | aurologic downstream |
| AS214943 | Railnet / Virtualine | T2 | aurologic downstream |
| AS215208 | Dolphon 1337 | — | Dissolved UK shell |
| AS215240 | Silent Connection | — | Dissolved UK shell |
| AS215540 | GCSAS | T2 | UK LLP shell |
| AS215552 | Hypercore LTD | T1 | Aeza front; sanctioned Nov 2025 |
| AS215789 | Karina Rashkovska | T2 | aurologic downstream |
| AS216071 | Zservers (historical) | T1 | Original ASN; depeered post-sanctions |
| AS216246 | Aeza International | T1 | Tertiary ASN |
| AS216309 | Tnsecurity / EVILEMPIRE | T2 | aurologic downstream; abuse.ch listed |

---

*This ecosystem map is a living analytical product. Update as new corporate relationships are identified, sanctions are issued, or infrastructure migrations are observed. Cross-reference all provider assessments against the risk tier definitions in [`taxonomy/BPH_TAXONOMY.md`](../taxonomy/BPH_TAXONOMY.md).*
