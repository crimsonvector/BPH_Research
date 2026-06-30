# BPH & TAE Analyst Playbook

**Version:** 1.0
**Last Updated:** 2026-05-16
**Maintainer:** CrimsonVector Research

> *A practitioner's guide to identifying, investigating, and tracking bullet-proof hosting providers and threat activity enablers.*

---

## Table of Contents

1. [BPH Identification Indicators](#1-bph-identification-indicators)
2. [OSINT Pivoting Techniques](#2-osint-pivoting-techniques)
3. [Key Data Sources & Tools](#3-key-data-sources--tools)
4. [Investigation Workflow](#4-investigation-workflow)
5. [New Provider Assessment Template](#5-new-provider-assessment-template)
6. [Recorded Future TAE Framework Integration](#6-recorded-future-tae-framework-integration)
7. [CISA/NSA BPH Mitigation Framework](#7-cisansa-bph-mitigation-framework)

---

## 1. BPH Identification Indicators

Use the following red-flag checklists when triaging a suspected BPH provider. No single indicator is dispositive; look for clustering of signals across all three categories.

### Red Flags -- Technical

| # | Indicator | Why It Matters |
|---|-----------|----------------|
| T1 | Disproportionate malicious traffic concentration (benchmark against Recorded Future Threat Density Score) | Legitimate hosters rarely exceed 1-2% malicious IPs in their announced space; BPH providers routinely hit 10-20%+ |
| T2 | ASN registered recently (<24 months) with immediate high-volume hosting | Normal providers grow gradually; instant capacity suggests pre-staged infrastructure for abuse |
| T3 | Single upstream provider, especially aurologic (AS30823) or similar known enabler | Legitimate networks multi-home for resilience; single-homing to a known enabler signals intentional alignment |
| T4 | IP prefixes announced and withdrawn at rates inconsistent with normal business (prefix churn/hopping) | Rapid prefix rotation defeats IP-based blocklists and complicates attribution |
| T5 | Inclusion on the abuse.ch ASN-DROP list | Community-validated signal that the ASN exists primarily to facilitate abuse |
| T6 | VirusTotal community scores showing high percentage of flagged IPs within announced prefixes | Crowdsourced corroboration of malicious hosting concentration |
| T7 | VMmanager/ISPsystem default hostname reuse across the provider's fleet | Indicator from Sophos Feb 2026 research; shows rapid, templated VM deployment without customization -- hallmark of BPH scale operations |
| T8 | Identical RDP hostnames across multiple VMs (e.g., WIN-J9D866ESIJ2 pattern from Stark/WorkTitans migration) | Reveals mass-cloned VM images, often carried across provider migrations -- a fingerprint linking old and new infrastructure |

### Red Flags -- Business/Corporate

| # | Indicator | Why It Matters |
|---|-----------|----------------|
| B1 | No formal storefront or verifiable physical presence | Legitimate hosting companies need visible sales channels; BPH operators hide behind anonymity |
| B2 | Business conducted exclusively via Telegram, email, or encrypted messaging | Avoids creating auditable transaction records and frustrates law enforcement subpoenas |
| B3 | No KYC -- anonymous registration with username/password only | Deliberate choice to avoid knowing customers, ensuring plausible deniability |
| B4 | Cryptocurrency-only payment, especially Monero/privacy coins | Eliminates the financial paper trail that leads investigators to beneficial owners |
| B5 | Advertising on underground forums (XSS, Exploit, BreachForums, cracked.io) | The customer acquisition channel reveals the intended customer base |
| B6 | UK LLP or LLC incorporation with no financial filings | A favorite shell structure: UK LLPs require no audited accounts and can be formed remotely with minimal identity verification |
| B7 | Nominee directors with short tenures (6-month rotations -- see QWINS pattern) | Short-tenure nominees make it nearly impossible to identify beneficial owners and frustrate corporate subpoenas |
| B8 | Formation agent addresses shared with many other entities | Mass-incorporation agents are a key enabler; the same registered office appearing on dozens of unrelated companies is a strong shell indicator |
| B9 | Corporate entity dissolved but network infrastructure persists | The legal entity was a disposable wrapper; the infrastructure outlives the corporate fiction |

### Red Flags -- Network Behavior

| # | Indicator | Why It Matters |
|---|-----------|----------------|
| N1 | Selective abuse response (responds to some reports but not others, or only under threat of upstream disconnection) | Creates the appearance of compliance while protecting revenue-generating malicious customers |
| N2 | Self-identification as "bulletproof," "abuse-proof," or "we ignore Spamhaus" | Explicit marketing to criminal clientele; some providers say this openly on forums |
| N3 | Marketing as "DMCA-ignored," "offshore," or "uncensored" hosting | Euphemisms for the same promise: your content will not be taken down regardless of complaints |
| N4 | Conflicting geolocation (registered in one country, servers in another, beneficial ownership in a third) | Jurisdictional arbitrage: deliberately structured to fall between the cracks of any single country's law enforcement |
| N5 | Advising customers to front via Cloudflare to avoid detection | Active coaching of customers on evasion techniques transforms the provider from passive host to active co-conspirator |

**Analyst Rule of Thumb:** If you observe indicators from all three categories (Technical + Business/Corporate + Network Behavior), you are almost certainly looking at a BPH provider or a BPH-adjacent operation. Document every indicator with a source and timestamp.

---

## 2. OSINT Pivoting Techniques

### ASN-to-Provider Attribution

This is the most common starting point. You have a suspicious IP; you need to identify who is behind it.

**Step-by-step:**

1. **Identify the ASN** from the suspicious IP address.
   - Command line: `whois [IP]`
   - Web: bgp.tools, Hurricane Electric BGP Toolkit (`bgp.he.net`)
   - Programmatic: Team Cymru IP-to-ASN mapping service

2. **Map the ASN to its registered organization.**
   - RIPE Stat: `https://stat.ripe.net/app/launchpad/S2_AS[number]`
   - BGPView: `https://bgpview.io/asn/[number]`
   - ipinfo.io: `https://ipinfo.io/AS[number]`

3. **Check ASN reputation immediately.**
   - abuse.ch ThreatFox: `https://threatfox.abuse.ch/browse/as_num/[number]/`
   - Spamhaus ASN-DROP list: check if the ASN appears
   - GreyNoise: search by ASN for scanning/exploitation activity

4. **Map all announced prefixes.**
   - RIPE Stat routing status widget
   - bgp.tools prefix list for the ASN
   - Note: record both currently announced and historically announced prefixes

5. **Identify upstream transit providers.**
   - bgp.tools: AS path analysis shows who provides transit
   - PeeringDB: peering relationships and Internet Exchange presence
   - **Critical check:** Does aurologic (AS30823) appear anywhere in the upstream path? This is the single most important European BPH enabler upstream.

6. **Cross-reference upstream against the known enabler list.**
   - Maintain a running list of known upstream enablers (see BPH_Master.csv, filter by type = "Upstream Enabler")
   - A provider with a known enabler upstream warrants immediate escalation to Phase 2

7. **Document the full AS path** from the suspicious IP to the tier-1 backbone. Every hop is a potential investigation target.

### Corporate Shell Identification

Once you have the organization name from WHOIS/RIPE, trace the corporate structure.

**Step-by-step:**

1. **Get the organization name** from the RIPE/ARIN WHOIS record for the ASN.

2. **Search UK Companies House** (the most common jurisdiction for BPH shells):
   - URL: `https://find-and-update.company-information.service.gov.uk/`
   - Search by company name, officer name, or registered office address

3. **Analyze the filing for red flags:**
   - Incorporation date vs. ASN registration date (close dates suggest purpose-built shell)
   - Registered office address (is it a virtual office? does it appear for other companies?)
   - Directors: current and resigned -- look for short tenures, nominee patterns
   - Filing history: are annual accounts filed? are they overdue?
   - Dissolution status: has the company been struck off while infrastructure persists?

4. **Cross-jurisdiction search via OpenCorporates:**
   - URL: `https://opencorporates.com/`
   - Search for the same entity name, director names, or registered agent in other countries
   - BPH operators often maintain parallel shells in multiple jurisdictions

5. **For US LLCs, check state Secretary of State records:**
   - Wyoming, Kentucky, and Delaware are favorites for minimal-disclosure shell LLCs
   - Wyoming in particular requires no public disclosure of members/managers
   - Check for registered agent services that are commonly used (e.g., mass-filing agents)

6. **Build the corporate chain:**
   - Who owns the entity that registered the ASN?
   - Who owns *that* entity?
   - Follow the chain until you reach a natural person or hit a jurisdictional wall
   - Document every link with the source and date

### Historical Infrastructure Tracking

BPH providers rebrand, migrate, and re-emerge. Historical analysis is how you connect the dots.

**Step-by-step:**

1. **Passive DNS:**
   - Validin (community passive DNS, web UI) / urlscan.io: historical DNS records and resolutions for domains hosted on the provider's IPs
   - DomainTools Iris: reverse DNS, historical WHOIS, domain-to-IP mapping
   - CIRCL passive DNS: `https://www.circl.lu/services/passive-dns/`
   - **What to look for:** domains that migrated from a known BPH provider to the new one

2. **Certificate Transparency:**
   - crt.sh: `https://crt.sh/?q=[domain or organization]`
   - Search by organization name, domain, or IP
   - **What to look for:** certificates issued to the same organization across different domains/IPs; certificates that pre-date the official corporate registration

3. **Historical BGP data:**
   - RIPE Stat BGP routing history widget
   - BGPStream: `https://bgpstream.com/`
   - **What to look for:** prefix announcements that were previously made by a different (now-defunct) ASN -- this is the BGP equivalent of following someone who changed their name

4. **Wayback Machine:**
   - Archive.org: `https://web.archive.org/web/*/[domain]`
   - **What to look for:** historical website content of the hosting provider; pricing pages, terms of service, contact information that may reveal real identities

5. **RIPE DB history:**
   - Check for resource transfers (ASN transfers, IP prefix transfers)
   - **Critical for sanctions evasion:** sanctioned entities transfer resources to new shells to continue operations under a different name

6. **Shodan historical data:**
   - Compare server configurations, banners, and software versions across time periods
   - **What to look for:** identical server configurations appearing on new IPs after old ones were blocklisted -- the WIN-J9D866ESIJ2 RDP hostname pattern is a real-world example

### Sanctions Cross-Referencing

Every BPH investigation must include a sanctions check. Failure to do so exposes your organization to secondary sanctions liability.

**Step-by-step:**

1. **OFAC SDN Search (US):**
   - URL: `https://sanctionssearch.ofac.treas.gov/`
   - Search by entity name, individual name, and known aliases
   - Check the full SDN entry for associated crypto wallet addresses

2. **EU Consolidated Sanctions List:**
   - URL: `https://www.sanctionsmap.eu/`
   - Search by name, entity, or country

3. **UK OFSI (Office of Financial Sanctions Implementation):**
   - URL: `https://www.gov.uk/government/publications/financial-sanctions-consolidated-list-of-targets`
   - Downloadable and searchable

4. **Australian DFAT Consolidated List:**
   - Downloadable consolidated list of sanctions targets

5. **Designated crypto wallets:**
   - OFAC increasingly designates specific cryptocurrency addresses
   - Cross-reference any wallets found during investigation against the OFAC SDN list
   - Use Chainalysis or similar tools to trace wallet activity and identify connected addresses

6. **Secondary sanctions exposure:**
   - Transactions with sanctioned entities trigger liability even if your organization is not the primary target
   - If a BPH provider is linked to a sanctioned entity (e.g., Zservers/XHOST), anyone transacting with that provider may face sanctions exposure
   - Document and escalate immediately

### Malware Infrastructure Correlation

Map the provider's infrastructure to known malware campaigns and threat actors.

**Step-by-step:**

1. **abuse.ch URLhaus:**
   - URL: `https://urlhaus.abuse.ch/browse/asn/AS[number]/`
   - Returns all malware distribution URLs hosted on the ASN
   - Note malware families, submission dates, and whether URLs are still active

2. **abuse.ch ThreatFox:**
   - URL: `https://threatfox.abuse.ch/browse/as_num/[number]/`
   - IOC database searchable by ASN
   - Links IOCs to specific malware families and threat actors

3. **VirusTotal:**
   - Search by IP or domain; check the "Relations" tab for connected infrastructure
   - Community comments often contain analyst notes and attribution
   - The "Communicating Files" section shows malware samples that contacted the IP

4. **Shodan:**
   - Search by org name, ASN, or specific service banners
   - Look for: C2 frameworks (Cobalt Strike, Sliver, Havoc), open admin panels, default credentials

5. **Censys:**
   - Certificate-based discovery: find all IPs using certificates issued to the same entity
   - Service-based discovery: identify unusual services running on the provider's IP space

6. **GreyNoise:**
   - Differentiate targeted attacks from opportunistic scanning
   - If an IP is flagged as "malicious" by GreyNoise, it is actively scanning/exploiting at internet scale

---

## 3. Key Data Sources & Tools

### BGP/Routing Intelligence

| Tool | URL | Use Case |
|------|-----|----------|
| RIPE Stat | `stat.ripe.net` | ASN details, routing history, prefix announcements, abuse contacts, resource transfers |
| BGP.tools | `bgp.tools` | Real-time BGP monitoring, AS path analysis, prefix tracking, upstream identification |
| Hurricane Electric BGP Toolkit | `bgp.he.net` | ASN lookup, prefix lists, peering data, IRR records |
| BGPView | `bgpview.io` | ASN search, prefix mapping, upstream/downstream provider identification |
| PeeringDB | `peeringdb.com` | Peering relationships, IX presence, facility locations, contact information |
| BGPStream | `bgpstream.com` | Real-time BGP event monitoring, hijack detection, route leak alerting |

### Threat Intelligence Platforms

| Tool | URL | Use Case |
|------|-----|----------|
| Recorded Future | `recordedfuture.com` | Threat Density Score, Network Intelligence module, TAE tracking, dark web monitoring |
| Shodan | `shodan.io` | Internet-wide device scanning, service enumeration, banner grabbing, historical data |
| Censys | `search.censys.io` | Certificate transparency, service discovery, infrastructure mapping, host enumeration |
| GreyNoise | `greynoise.io` | Internet-wide scan classification, mass exploitation detection, benign scanner filtering |
| ipinfo.io | `ipinfo.io` | IP/ASN geolocation, hosted domain counts, privacy/proxy detection, company data |
| ipapi.is | `ipapi.is` | Hosting detection, ASN abuse scoring, VPN/proxy/tor detection |

### Malware/C2 Intelligence

| Tool | URL | Use Case |
|------|-----|----------|
| abuse.ch ThreatFox | `threatfox.abuse.ch` | IOC database searchable by ASN, malware family attribution, threat actor linkage |
| abuse.ch URLhaus | `urlhaus.abuse.ch` | Malware URL tracking by ASN, payload identification, takedown tracking |
| abuse.ch ASN-DROP | `spamhaus.com/drop` | ASN blocklist -- networks recommended for "do not route or peer" treatment |
| VirusTotal | `virustotal.com` | Multi-engine scanning, IP/domain reputation, file relations, community intelligence |
| ANY.RUN | `any.run` | Interactive malware sandbox, C2 extraction, network traffic capture, behavioral analysis |
| MalwareBazaar | `bazaar.abuse.ch` | Malware sample repository with hosting attribution, YARA rule matching |

### Corporate/Registration Intelligence

| Tool | URL | Use Case |
|------|-----|----------|
| UK Companies House | `find-and-update.company-information.service.gov.uk` | UK company filings, directors, registered offices, dissolution status, filing history |
| OpenCorporates | `opencorporates.com` | Cross-jurisdiction corporate search, officer search, registered agent identification |
| RIPE NCC Database | `apps.db.ripe.net` | WHOIS for European IP resources and ASN registration, maintainer objects, organization records |
| ARIN WHOIS | `whois.arin.net` | North American IP/ASN registration, organization details, POC records |
| APNIC WHOIS | `wq.apnic.net` | Asia-Pacific IP/ASN registration, resource delegation, abuse contacts |
| DomainTools | `domaintools.com` | Domain/IP WHOIS history, reverse WHOIS, Iris investigation platform, hosting history |

### Sanctions Databases

| Tool | URL | Use Case |
|------|-----|----------|
| OFAC SDN Search | `sanctionssearch.ofac.treas.gov` | US sanctions: individuals, entities, crypto wallets, vessels, aircraft |
| EU Sanctions Map | `sanctionsmap.eu` | EU consolidated sanctions list with geographic and regime filtering |
| UK OFSI | `gov.uk/ofsi` | UK financial sanctions list, licensing information |
| Chainalysis | `chainalysis.com` | Cryptocurrency transaction tracing, sanctions compliance, wallet clustering |

### Community Resources

| Resource | URL | Use Case |
|----------|-----|----------|
| Spamhaus Project | `spamhaus.org` | ASN/domain blocklists, SBL/XBL/DBL, BPH research, policy block listings |
| Team Cymru | `team-cymru.com` | IP reputation, BGP intelligence, Nimbus threat monitor, community feeds |
| COMM-ISAC | `comm-isac.org` | Communications sector information sharing and analysis center |
| Krebs on Security | `krebsonsecurity.com` | Investigative journalism on cybercrime infrastructure, BPH provider exposures |
| BleepingComputer | `bleepingcomputer.com` | Malware/ransomware news with infrastructure details, IOC reporting |

---

## 4. Investigation Workflow

### Phase 1: Triage (15-30 minutes)

**Objective:** Determine whether the target warrants a full investigation.

| Step | Action | Tool(s) | Output |
|------|--------|---------|--------|
| 1.1 | IP/ASN lookup -- identify the ASN, organization, and registered country | `whois`, bgp.tools, RIPE Stat | ASN number, org name, country |
| 1.2 | Reputation check -- query for immediate red flags | abuse.ch ThreatFox, VirusTotal, Shodan | Malicious IOC count, community flags |
| 1.3 | Cross-reference master list -- check BPH_Master.csv for known entity | Local CSV | Known/unknown status |
| 1.4 | Quick upstream check -- who provides transit? | bgp.tools AS path | Upstream ASN(s) |

**Decision Gate:**
- **2+ red flags from Section 1 identified** --> Proceed to Phase 2
- **Single red flag, ambiguous** --> Add to T5 (watch list), set 30-day review reminder
- **No red flags** --> Document the negative finding and close

### Phase 2: Infrastructure Mapping (1-2 hours)

**Objective:** Build a complete picture of the provider's network footprint and threat profile.

| Step | Action | Tool(s) | Output |
|------|--------|---------|--------|
| 2.1 | Map all announced prefixes | RIPE Stat routing status | Full prefix list with sizes |
| 2.2 | Identify all upstream/transit providers | bgp.tools AS path analysis | Transit provider list |
| 2.3 | Check for known enabler upstreams | Cross-reference against enabler list | **Escalation trigger if aurologic AS30823 or equivalent found** |
| 2.4 | Enumerate services on announced IP space | Shodan, Censys | Service inventory, C2 panel identification |
| 2.5 | Count hosted domains | ipinfo.io hosted domains | Domain count per prefix |
| 2.6 | Check malware hosting | ThreatFox, URLhaus by ASN | Malware family list, IOC count |
| 2.7 | Calculate approximate malicious ratio | Malicious IPs / total announced IPs | Percentage (compare to RF Threat Density benchmarks) |

**Key Deliverable:** Infrastructure map showing all prefixes, upstream relationships, and malicious activity concentration.

### Phase 3: Attribution (2-4 hours)

**Objective:** Identify the people and entities behind the infrastructure.

| Step | Action | Tool(s) | Output |
|------|--------|---------|--------|
| 3.1 | Corporate registration search | Companies House, OpenCorporates, state SOS | Company records, filing history |
| 3.2 | Officer/director research | Companies House, sanctions databases | Director names, tenure patterns, sanctions hits |
| 3.3 | Beneficial ownership analysis | Follow the corporate chain | Ownership diagram |
| 3.4 | Historical infrastructure analysis | Passive DNS, crt.sh, BGP history | Timeline of infrastructure changes, predecessor entities |
| 3.5 | Financial indicators | Payment methods, crypto wallet analysis | Payment method list, wallet addresses, Garantex/Grinex exposure |
| 3.6 | Forum presence research | Underground forum archives, cached pages | Advertising posts, customer testimonials, pricing |

**Key Deliverable:** Attribution report linking infrastructure to specific entities and (where possible) individuals.

### Phase 4: Classification & Reporting (1 hour)

**Objective:** Formalize findings into the standard taxonomy and update the master dataset.

| Step | Action | Reference | Output |
|------|--------|-----------|--------|
| 4.1 | Apply risk tier | `taxonomy/BPH_TAXONOMY.md` criteria (T1-T5) | Tier assignment with justification |
| 4.2 | Assign provider type | Pure BPH, BPH-Adjacent, Upstream Enabler, Financial Enabler, Corporate Shell, Sanctions-Evasion Vehicle | Type classification |
| 4.3 | Document operational patterns | Taxonomy Section 3 pattern matching | Pattern list with evidence |
| 4.4 | Score identification signals | Taxonomy Section 4 signal matrix | Signal score |
| 4.5 | Update BPH_Master.csv | Populate all 25 schema columns | New row in master dataset |
| 4.6 | Write structured assessment | Assessment template (Section 5 below) | Completed assessment document |

**Key Deliverable:** Completed provider assessment filed in the standard format.

---

## 5. New Provider Assessment Template

Copy this template for each new provider investigation. Fill in every field; mark unknown fields as `[UNKNOWN -- investigation ongoing]` rather than leaving blank.

```markdown
# Provider Assessment: [PROVIDER NAME]

## Basic Information
- **Primary ASN:** AS[number]
- **Additional ASNs:** AS[number], AS[number]
- **Known Prefixes:** [list all announced prefixes with CIDR notation]
- **Country (Registration):** [country where ASN/company is registered]
- **Country (Operations):** [country where servers are physically located]
- **Corporate Entity:** [legal entity name, jurisdiction, registration number]
- **Aliases:** [all known names, brands, domain names]
- **First Observed:** [date of first CrimsonVector observation]

## Classification
- **Status:** [active / flagged / suspected / sanctioned / evading / seized / dissolved / exposed]
- **Risk Tier:** [T1 / T2 / T3 / T4 / T5]
- **Provider Type:** [Pure BPH / BPH-Adjacent / Upstream Enabler / Financial Enabler / Corporate Shell / Sanctions-Evasion Vehicle]

## Evidence

### Technical Indicators
- [ ] Malicious traffic ratio: ___% (source: ___)
- [ ] abuse.ch ASN-DROP listed: Y/N (date checked: ___)
- [ ] Upstream providers: [list with ASN numbers]
- [ ] Known enabler upstream present: Y/N (which: ___)
- [ ] Route diversification: Y/N (number of upstreams: ___)
- [ ] Prefix churn observed: Y/N (details: ___)
- [ ] VMmanager/ISPsystem hostname pattern: Y/N
- [ ] Identical RDP hostnames: Y/N (pattern: ___)

### Business Indicators
- [ ] KYC enforcement: Y/N (evidence: ___)
- [ ] Payment methods: [list all accepted methods]
- [ ] Forum presence: [list forums with links to archived posts]
- [ ] Formal storefront: Y/N (URL: ___)
- [ ] Anonymous registration permitted: Y/N
- [ ] Marketing language: [quote relevant terms -- "offshore," "DMCA-ignored," etc.]

### Governance Indicators
- [ ] Corporate structure: [describe the entity chain]
- [ ] Director history: [names, tenure, nominee status]
- [ ] Sanctions exposure: [direct designation / linked to designated entity / no known exposure]
- [ ] Law enforcement cooperation: [known cooperation / known non-cooperation / unknown]
- [ ] Financial filings: [up to date / overdue / never filed]

## Associated Infrastructure
- **Upstream Providers:** [ASN, name, relationship]
- **Downstream Customers:** [known hosted entities]
- **Threat Actors:** [APT groups, ransomware operators, fraud networks]
- **Malware Families:** [specific families hosted, with ThreatFox/URLhaus references]
- **C2 Frameworks:** [Cobalt Strike, Sliver, Havoc, etc. -- with Shodan/Censys references]

## Analyst Assessment
[Narrative assessment -- 2-4 paragraphs. State the conclusion first, then the evidence.
Every factual claim must cite a source. Use the format: (Source: [tool/database], [date accessed]).
Address confidence level: high/moderate/low and state what additional evidence would increase confidence.]

## Sources
1. [Source 1 -- tool, URL, date accessed]
2. [Source 2 -- tool, URL, date accessed]
3. [Source 3 -- tool, URL, date accessed]

## Recommendation
- [ ] Block at ASN level (appropriate for T1-T2 Pure BPH)
- [ ] Block specific prefixes (appropriate when ASN contains mixed legitimate/malicious)
- [ ] Monitor and alert (appropriate for T3-T4, or newly identified providers under investigation)
- [ ] Passive monitoring only (appropriate for T5 watch-list entries)
- [ ] No action required (document rationale)
- [ ] Escalate to legal/compliance (sanctions exposure identified)
- [ ] Share with ISACs/law enforcement (active threat to sector)
```

---

## 6. Recorded Future TAE Framework Integration

This section operationalizes Recorded Future's Threat Activity Enabler (TAE) concept and Threat Density Score for daily analyst workflows.

### Understanding the Threat Density Score

The Threat Density Score measures **validated malicious activity as a proportion of total IP prefixes announced by an ASN.** It answers the question: "What fraction of this network's address space is being used for malicious purposes?"

**Interpretation benchmarks:**

| Score Range | Interpretation | Analyst Action |
|-------------|---------------|----------------|
| >10% | **Strong TAE indicator** -- the network exists primarily to enable threat activity. Virtualine peaked at approximately 20%. | Immediate Phase 2 investigation. Consider preemptive blocking. |
| 5-10% | **Significant TAE indicator** -- malicious hosting is a substantial portion of the provider's business. | Priority Phase 2 investigation within 48 hours. |
| 1-5% | **Warrants investigation** -- could be a negligent provider or an emerging BPH operation. | Phase 1 triage. Schedule follow-up in 2 weeks to check trend. |
| <1% | **Within normal range** for most legitimate providers. | No action unless other red flags are present. |

**Trend analysis is critical:**
- **Increasing trend** = escalation trigger. A provider whose score rises from 3% to 7% over 60 days is likely transitioning to or being exploited as BPH.
- **Sudden drop** = possible infrastructure pivot. The provider may have moved operations to a new ASN while the old one is cleaned up or abandoned. Immediately search for related new ASNs.
- **Stable high score** = established BPH. The provider has reached equilibrium with its abuse-hosting business model.

### Three Operational Applications

These are the three ways analysts should integrate TAE intelligence into daily operations, derived from Recorded Future's framework:

#### Application 1: Preventive Control Adjustments

**Purpose:** Use high-risk ASN intelligence to conditionally strengthen or restrict network and access controls *before* malicious infrastructure is used for attack delivery.

**How to operationalize:**
- Maintain a dynamic blocklist/watchlist of ASNs with Threat Density Score >5%
- Feed this list into firewall rules, web proxy policies, and email gateway configurations
- For ASNs scoring >10%, implement default-deny with exception-based allow
- For ASNs scoring 5-10%, implement enhanced logging and conditional challenges (CAPTCHAs, MFA step-up)
- Review and update the list weekly; automate where possible via API integration

#### Application 2: Elevate Detection & Prioritization

**Purpose:** Incorporate ASN risk intelligence into detection logic, alert scoring, and prioritization playbooks to accelerate response when communication with high-risk infrastructure occurs.

**How to operationalize:**
- Enrich SIEM alerts with ASN risk scores at ingestion time
- Create correlation rules: "Alert + source/destination ASN in TAE list = automatic priority elevation"
- Modify SOC triage playbooks: connections to TAE-listed networks skip Tier 1 and go directly to Tier 2 analysts
- Add ASN risk context to threat hunting queries as a weighting factor
- Track metrics: what percentage of true positive alerts involved TAE-listed infrastructure?

#### Application 3: Conduct Focused Hunting & Exposure Assessment

**Purpose:** Use ASN risk intelligence as a pivot to uncover hidden exposure, assess potential impact, and determine whether adversary infrastructure has already intersected the environment.

**How to operationalize:**
- Weekly hunting query: "Show all connections to/from ASNs with Threat Density Score >5% in the past 30 days"
- Quarterly exposure assessment: "Which of our third-party providers have any infrastructure hosted on or transiting through TAE-listed networks?"
- Supply chain audit: review CDN, DNS, email, and SaaS provider infrastructure for TAE adjacency
- Retrospective analysis after new TAE designations: "Did we have any historical connections to this newly-designated network?"

### Key Analyst Questions

Use these questions as a self-assessment checklist and as discussion prompts for security leadership briefings:

1. **How much of your network communicates with high-risk infrastructure?** Quantify: number of unique internal IPs that have connected to TAE-listed ASNs in the past 90 days.

2. **Are you prioritizing alerts involving high-risk networks?** If two alerts fire simultaneously and one involves a TAE-listed ASN, does your workflow ensure the TAE-linked alert is triaged first?

3. **Is TAE or ASN risk intelligence integrated into your detection and triage workflows?** Not as a standalone dashboard, but embedded in the SIEM correlation rules and SOC playbooks.

4. **Do any of your third-party providers rely on TAE-linked infrastructure?** This is your supply chain blind spot. A legitimate SaaS vendor hosting on or transiting through BPH infrastructure is an indirect exposure.

5. **Do you have hidden exposure to TAE networks?** Check DNS resolution chains, email routing, CDN edges, and API endpoints -- not just direct IP connections.

6. **Are your controls dynamically adjusting to infrastructure risk?** Static blocklists decay rapidly. Controls must ingest updated threat intelligence on at least a weekly cadence.

7. **Can you proactively restrict or challenge traffic to and from high-risk networks?** The goal is to shift from reactive (block after compromise) to proactive (restrict before compromise).

---

## 7. CISA/NSA BPH Mitigation Framework

This section references the November 19, 2025 joint guidance titled **"Bulletproof Defense: How to Identify and Mitigate Malicious Use of Bulletproof Hosting Services"**, issued by CISA, NSA, FBI, DC3, and Five Eyes partner agencies (ASD/ACSC, CCCS, NCSC-NZ, NCSC-UK).

The guidance provides a framework for both **network defenders** and **ISPs/hosting providers** to counter BPH threats. Below is the actionable distillation.

### For Network Defenders (Enterprises & Government)

#### 1. Curate a High-Confidence Malicious Resource List
- Aggregate indicators from commercial threat intelligence feeds (Recorded Future, CrowdStrike, Mandiant) and open-source feeds (abuse.ch, Spamhaus, Team Cymru)
- Deduplicate and validate: each entry should have at least two independent sources or one high-confidence source
- Organize by granularity: ASN-level, prefix-level, and individual IP-level entries
- Assign confidence scores and expiration dates to every entry
- **Do not rely on a single feed.** No single source has complete coverage.

#### 2. Conduct Traffic Analysis to Supplement the List
- Analyze netflow/firewall logs for communication patterns with known BPH infrastructure
- Identify outlier activity: unusual volumes, unusual ports, unusual times to/from suspicious ASNs
- Use GreyNoise to contextualize scanning activity (benign vs. malicious)
- Feed newly discovered malicious IPs back into the curated list

#### 3. Automate Regular Reviews of the Curated List
- Set a review cadence: weekly for active-threat entries, monthly for watch-list entries
- Automate staleness checks: remove entries that have not been revalidated within their expiration window
- Track false positive rates: entries that triggered blocks on legitimate traffic must be investigated and either removed or confirmed
- Version-control the list: maintain a changelog so analysts can understand why entries were added or removed

#### 4. Share Threat Intelligence with the Community
- Participate in ISACs (sector-specific Information Sharing and Analysis Centers)
- Contribute validated indicators to community platforms (abuse.ch, MISP instances)
- Share sanitized case studies: describe the TTPs without revealing proprietary detection methods
- Engage with CISA's Automated Indicator Sharing (AIS) program

#### 5. Configure Centralized Event Logging
- Ensure all network border devices (firewalls, proxies, DNS resolvers) log connections to/from the curated malicious list
- Forward these logs to the SIEM with enrichment (ASN, org name, threat density score)
- Create dashboards: "Connections to BPH Infrastructure -- Last 7 Days"
- Set retention: minimum 12 months for logs involving BPH-listed infrastructure

#### 6. Implement Filters at the Network Border
- **Granularity decision matrix:**
  - ASN-level block: appropriate for T1-T2 Pure BPH providers where the entire ASN is malicious
  - Prefix-level block: appropriate for mixed-use ASNs where specific prefixes are malicious
  - Individual IP block: appropriate for targeted C2 addresses within otherwise-clean ranges
- Deploy at multiple layers: firewall, web proxy, DNS resolver (RPZ/sinkhole), email gateway
- Log all blocked connections for retrospective analysis

#### 7. Develop Filter Feedback Processes
- Create a process for internal users and external parties to inquire about blocked resources
- Provide a mechanism for legitimate entities to request unblocking (with verification)
- Track block-related inquiries: a spike in complaints about a specific block may indicate a false positive or a BPH provider migrating legitimate customers as cover

### For ISPs and Hosting Providers

#### 8. Use Upstream Providers That Follow Secure by Design Principles
- Vet your own upstream providers for BPH adjacency
- Contractually require abuse handling SLAs in peering and transit agreements
- Reserve the right to null-route prefixes that are sources of sustained abuse

#### 9. Notify Customers About Malicious Lists
- Proactively inform customers when their IP addresses appear on community blocklists
- Provide remediation guidance and a timeline for compliance
- Enforce consequences: progressive warnings, traffic throttling, contract termination

#### 10. Create Customer-Facing Filters
- Offer customers the option to enable BPH-based filtering on their traffic
- Provide DNS-based filtering using community blocklists (Spamhaus, abuse.ch)

#### 11. Establish KYC Capabilities
- Implement identity verification for all new customers (government ID, verified payment method)
- Maintain records sufficient to respond to law enforcement requests
- Flag accounts that fail or refuse KYC for enhanced monitoring

#### 12. Implement Internet Routing Security Best Practices
- Deploy RPKI (Resource Public Key Infrastructure) for BGP route origin validation
- Implement BCP38/BCP84 (network ingress filtering) to prevent IP spoofing
- Participate in MANRS (Mutually Agreed Norms for Routing Security)
- Monitor for unauthorized route announcements (BGP hijacking)

---

## Appendix A: Quick Reference -- Common BPH Provider Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| **Phoenix Rebrand** | Provider is taken down or sanctioned, re-emerges under new name/ASN within weeks | Zservers --> XHOST --> subsequent entities |
| **Upstream Laundering** | BPH obtains transit from a "clean" upstream to avoid guilt-by-association | Multiple BPH providers routing through aurologic AS30823 |
| **Corporate Carousel** | Rapid incorporation and dissolution of shell companies to hold ASN resources | UK LLP incorporated, ASN registered, LLP dissolved, ASN transferred to new LLP |
| **Cloudflare Fronting** | Provider advises customers to place Cloudflare in front of their infrastructure to mask the hosting origin | Common advice on underground forums |
| **Jurisdiction Shopping** | Registration in Country A, servers in Country B, ownership in Country C | UK registration, Netherlands servers, Russian beneficial owners |
| **Sanctions Evasion via Transfer** | Sanctioned entity transfers ASN/prefix resources to an apparently unrelated new entity | Check RIPE DB transfer logs and compare entity details |

## Appendix B: Glossary

| Term | Definition |
|------|------------|
| **BPH** | Bullet-Proof Hosting -- hosting services that knowingly permit malicious content and resist abuse complaints and law enforcement takedowns |
| **TAE** | Threat Activity Enabler -- Recorded Future's term for network infrastructure providers that disproportionately facilitate threat activity |
| **ASN** | Autonomous System Number -- a unique identifier assigned to a network that controls a collection of IP prefixes |
| **Prefix** | A block of IP addresses announced via BGP, expressed in CIDR notation (e.g., 192.0.2.0/24) |
| **BGP** | Border Gateway Protocol -- the routing protocol that determines how traffic flows between autonomous systems on the internet |
| **RPKI** | Resource Public Key Infrastructure -- a cryptographic framework for verifying that an ASN is authorized to announce specific IP prefixes |
| **KYC** | Know Your Customer -- identity verification procedures for customer onboarding |
| **OFAC** | Office of Foreign Assets Control -- the US Treasury bureau that administers sanctions programs |
| **SDN** | Specially Designated Nationals -- OFAC's list of sanctioned individuals and entities |
| **IOC** | Indicator of Compromise -- an artifact (IP, domain, hash, URL) that indicates malicious activity |
| **C2** | Command and Control -- the infrastructure used by threat actors to communicate with compromised systems |
| **RIR** | Regional Internet Registry -- organizations that manage IP address and ASN allocation (RIPE, ARIN, APNIC, LACNIC, AFRINIC) |
| **Threat Density Score** | Recorded Future metric: validated malicious activity divided by total announced IP space for an ASN |
| **Prefix Churn** | Rapid announcement and withdrawal of IP prefixes, used to evade blocklists |
| **Nominee Director** | A person who serves as a corporate director on behalf of (and under the direction of) the actual beneficial owner |

---

*End of playbook. For questions, corrections, or additions, contact CrimsonVector Research.*
