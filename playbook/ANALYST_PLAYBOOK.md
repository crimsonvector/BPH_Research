# BPH & TAE Analyst Playbook

**Version:** 1.3
**Last Updated:** 2026-09-25
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
8. [Infrastructure Reuse and Indicator Retention](#8-infrastructure-reuse-and-indicator-retention)

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
| T5 | Inclusion on the Spamhaus ASN-DROP list | Community-validated signal that the ASN exists primarily to facilitate abuse |
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
| B6 | UK LLP/Ltd or US LLC shell with overdue, dormant or minimal filings | UK LLPs and Ltds **must** file annual accounts (only small entities may skip the audit), so overdue, dormant or skeletal accounts on a company that holds an ASN are the signal. UK incorporation is still fast and cheap (GBP 100 online from 2026-02-01) but no longer anonymous: identity verification for directors, LLP members and PSCs has been mandatory since 2025-11-18 |
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
   - RIPE Stat: `https://stat.ripe.net/resource/AS[number]` (or `https://stat.ripe.net/app/launchpad/AS[number]`)
   - bgp.tools: `https://bgp.tools/as/[number]`
   - ipinfo.io: `https://ipinfo.io/AS[number]`

3. **Check ASN reputation immediately.**
   - abuse.ch ThreatFox ASN report: `https://threatfox.abuse.ch/asn/[number]/` (the form CISA cites; the Auth-Key is required for the abuse.ch APIs -- see Section 3)
   - Spamhaus ASN-DROP: `https://www.spamhaus.org/drop/asndrop.json` -- check if the ASN appears, and read its `domain` field: Spamhaus uses it to tie sibling and successor ASNs to one operator (e.g. `virtualine.org`, `pfcloud.io`, `kaopuyun.com`)
   - **Confirm the registry holder is still the entity you think it is.** ASNs are returned and re-issued: in September 2026, twelve ASNs in `BPH_Master.csv` belonged to unrelated organisations (a Polish payments company, an Indonesian ISP, a Japanese firm). Never block on a historical ASN without checking.
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
   - Wyoming and Delaware are the confirmed minimal-disclosure favourites: Wyoming articles name only the organiser and registered agent; Delaware certificates list no members or managers
   - Kentucky is *not* a no-disclosure state -- its annual reports list members or managers (useful for KPROHOST LLC and Railnet LLC)
   - There is no federal fallback: FinCEN's final rule (effective 2026-08-14) ended beneficial-ownership reporting for US-formed companies
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
   - BGPStream (Cisco Crosswork): `https://bgpstream.crosswork.cisco.com/` -- the old `bgpstream.com` has moved here
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

3. **UK Sanctions List (FCDO):**
   - URL: `https://sanctionslist.fcdo.gov.uk/docs/UK-Sanctions-List.csv` (machine-readable; carries a Report Date)
   - **Use this, not the OFSI consolidated list.** The OFSI consolidated list was deprecated 2026-01-28 and superseded by the FCDO UK Sanctions List; querying OFSI now returns a stale answer.
   - Grep it directly rather than relying on aggregators. Entity-splitting on aggregator sites means *absence* there does not prove a party is undesignated — confirm against this file.
   - **Check the `Subsidiaries` field, not just primary names.** Some entities (e.g. Hypercore Ltd) are captured by UK ownership-and-control rules as a subsidiary entry on a parent's row rather than by a designation of their own. A name-only search will miss them.

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
   - Web search: `https://urlhaus.abuse.ch/browse.php?search=[value]` (the by-ASN browse path used in earlier versions could not be verified; use the authenticated API for ASN-wide pulls)
   - Returns malware distribution URLs matching the IP, domain or other value
   - Note malware families, submission dates, and whether URLs are still active

2. **abuse.ch ThreatFox:**
   - URL: `https://threatfox.abuse.ch/asn/[number]/`
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
   - GreyNoise classifies sensor-observed IPs as benign, suspicious or malicious; "malicious" means it was seen scanning or exploiting at internet scale. Absence from GreyNoise is not evidence that an IP is benign

---

## 3. Key Data Sources & Tools

### BGP/Routing Intelligence

| Tool | URL | Use Case |
|------|-----|----------|
| RIPE Stat | `stat.ripe.net` | ASN details, routing history, prefix announcements, abuse contacts, resource transfers |
| BGP.tools | `bgp.tools` | Real-time BGP monitoring, AS path analysis, prefix tracking, upstream identification |
| Hurricane Electric BGP Toolkit | `bgp.he.net` | ASN lookup, prefix lists, peering data, IRR records |
| PeeringDB | `peeringdb.com` | Peering relationships, IX presence, facility locations, contact information |
| BGPStream | `bgpstream.crosswork.cisco.com` | Real-time BGP event monitoring, hijack detection, route leak alerting. Moved to Cisco Crosswork; `bgpstream.com` is the old address. Not to be confused with `bgpstream.caida.org`, CAIDA's measurement framework |

### Threat Intelligence Platforms

| Tool | URL | Use Case |
|------|-----|----------|
| Recorded Future | `recordedfuture.com` | Threat Density Score, Network Intelligence module, TAE tracking, dark web monitoring |
| Shodan | `shodan.io` | Internet-wide device scanning, service enumeration, banner grabbing, historical data |
| Censys | `platform.censys.io` | Certificate transparency, service discovery, infrastructure mapping, host enumeration. Legacy Search (`search.censys.io`) and its API were retired in September 2026 (already disabled for free users; the host redirects to Platform) -- use Platform (`api.platform.censys.io/v3/`) |
| GreyNoise | `greynoise.io` | Internet-wide scan classification (benign / suspicious / malicious), mass exploitation detection, benign scanner filtering; weekly-brief IOC files are a good source of persistent BPH scanners |
| ipinfo.io | `ipinfo.io` | IP/ASN geolocation, hosted domain counts, privacy/proxy detection, company data |
| ipapi.is | `ipapi.is` | Hosting detection, ASN abuse scoring, VPN/proxy/tor detection |

### Malware/C2 Intelligence

> **abuse.ch requires authentication.** Since 2025-06-30 the abuse.ch APIs — ThreatFox, URLhaus, MalwareBazaar, YARAify — require an account at `auth.abuse.ch` and an Auth-Key passed as an HTTP header (`Auth-Key: YOUR-AUTH-KEY-HERE`); scripted API pulls without it fail (some static `/downloads/` exports still answered unauthenticated in Aug 2026, which should not be relied on). The ThreatFox recent-IOC API returns at most 7 days, so archive history locally. Small independent organisations keep free access; commercial licensing is offered through Spamhaus Technology. Note that abuse.ch and Spamhaus remain separate organizations — Spamhaus Technology has been the primary licensee of abuse.ch data since 2022-08-01, which is a licensing alliance, not an acquisition.

| Tool | URL | Use Case |
|------|-----|----------|
| abuse.ch ThreatFox | `threatfox.abuse.ch` | IOC database searchable by ASN, malware family attribution, threat actor linkage |
| abuse.ch URLhaus | `urlhaus.abuse.ch` | Malware URL tracking by ASN, payload identification, takedown tracking |
| Spamhaus ASN-DROP | `spamhaus.org/drop/asndrop.json` | ASN blocklist -- networks recommended for "do not route or peer" treatment. **Use the JSON feed.** The legacy `asndrop.txt` is now an empty stub that still carries a current datestamp, so a freshness check passes while returning zero listings |
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
| APNIC WHOIS | `wq.apnic.net/static/search.html` | Asia-Pacific IP/ASN registration, resource delegation, abuse contacts |
| DomainTools | `domaintools.com` | Domain/IP WHOIS history, reverse WHOIS, Iris investigation platform, hosting history |

### Sanctions Databases

| Tool | URL | Use Case |
|------|-----|----------|
| OFAC SDN Search | `sanctionssearch.ofac.treas.gov` | US sanctions: individuals, entities, crypto wallets, vessels, aircraft |
| EU Sanctions Map | `sanctionsmap.eu` | EU consolidated sanctions list with geographic and regime filtering |
| UK Sanctions List (FCDO) | `sanctionslist.fcdo.gov.uk/docs/UK-Sanctions-List.csv` | UK designations, machine-readable. Supersedes the OFSI consolidated list (deprecated 2026-01-28) |
| UK OFSI | `gov.uk/ofsi` | Licensing, enforcement, and guidance. **Not** the authoritative designation list — use the FCDO list above |
| Chainalysis | `chainalysis.com` | Cryptocurrency transaction tracing, sanctions compliance, wallet clustering |

### Community Resources

| Resource | URL | Use Case |
|----------|-----|----------|
| Spamhaus Project | `spamhaus.org` | ASN/domain blocklists, SBL/XBL/DBL, BPH research, policy block listings |
| Team Cymru | `team-cymru.com` | IP reputation, BGP intelligence, Nimbus threat monitor, community feeds |
| COMM-ISAC | (URL unverified) | Communications sector information sharing and analysis center; named by CISA as a sharing channel for building a high-confidence BPH list |
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
| 4.2 | Assign provider type | Pure BPH, BPH-Adjacent, Upstream Enabler, Financial Enabler, Corporate Shell, Sanctions-Evasion Vehicle, Anonymization/Proxy Enabler | Type classification |
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
- **Status:** [active / flagged / suspected / sanctioned / evading / seized / dissolved / exposed / dormant]
- **Risk Tier:** [T1 / T2 / T3 / T4 / T5]
- **Provider Type:** [Pure BPH / BPH-Adjacent / Upstream Enabler / Financial Enabler / Corporate Shell / Sanctions-Evasion Vehicle / Anonymization/Proxy Enabler]

## Evidence

### Technical Indicators
- [ ] Malicious traffic ratio: ___% (source: ___)
- [ ] Spamhaus ASN-DROP listed: Y/N (date checked: ___)
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

**Interpretation benchmarks (CrimsonVector heuristics).** Recorded Future publishes rankings, not these bands; the thresholds below are this repository's working assumptions and should be tuned. RF's 2025 top ten by Threat Density was Virtualine, CrazyRDP, Stark Industries, Kaopu Cloud HK, Aeza, PrivateAlps, 4VPS, Defhost, Silent Connection and DolphinHost (relayed; verify against CTA-2026-0319).


| Score Range | Interpretation | Analyst Action |
|-------------|---------------|----------------|
| >10% | **Strong TAE indicator** -- the network exists primarily to enable threat activity. (Virtualine ranked #1 in RF's 2025 list; the often-quoted ~20% peak is unsourced.) | Immediate Phase 2 investigation. Consider preemptive blocking. |
| 5-10% | **Significant TAE indicator** -- malicious hosting is a substantial portion of the provider's business. | Priority Phase 2 investigation within 48 hours. |
| 1-5% | **Warrants investigation** -- could be a negligent provider or an emerging BPH operation. | Phase 1 triage. Schedule follow-up in 2 weeks to check trend. |
| <1% | **Within normal range** for most legitimate providers. | No action unless other red flags are present. |

**Trend analysis is critical:**
- **Increasing trend** = escalation trigger. A provider whose score rises from 3% to 7% over 60 days is likely transitioning to or being exploited as BPH.
- **Sudden drop** = possible infrastructure pivot. The provider may have moved operations to a new ASN while the old one is cleaned up or abandoned. Immediately search for related new ASNs.
- **Stable high score** = established BPH. The provider has reached equilibrium with its abuse-hosting business model.

### Three Operational Applications

These are the three ways analysts should integrate TAE intelligence into daily operations, adapted from Recorded Future's TAE framing (the RF source text was not re-verified in the 2026-09 audit):

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

This section references the November 19, 2025 joint guidance **"Bulletproof Defense: Mitigating Risks From Bulletproof Hosting Providers"** (TLP:CLEAR, version 1). It was authored by nine agencies: CISA, NSA, DC3, FBI, ASD's ACSC, the Canadian Centre for Cyber Security, **NCSC-NL**, NCSC-NZ and NCSC-UK -- Five Eyes plus the Netherlands. It was developed through the Joint Ransomware Task Force, with contributions from AWS, Silent Push and RedSense, and NSA publishes it as a Cybersecurity Information Sheet.

The guidance defines a BPH provider as "an internet infrastructure provider that knowingly and intentionally markets and leases their infrastructure to cybercriminals". It warns that blocking a whole AS "may be ineffective" -- filters cause collateral damage, BPH operators spread infrastructure across many ASes, and a BPH "can request a new ASN from an internet registry and receive it within two to five business days".

> **How to read this section.** Each numbered item states what CISA recommends. Lines marked **CrimsonVector practice** are this repository's own hardening, not CISA text -- earlier versions blurred the two (notably the two-source rule, per-entry expiry, age-based deletion and 12-month log retention).

### For Network Defenders (and ISPs)

#### 1. Curate a High-Confidence Malicious Resource List
- **CISA:** build a "high confidence" list of malicious internet resources from commercial and open-source feeds and from public/private sharing channels (CISA names COMM-ISAC). Free resources it cites include Spamhaus DROP, ThreatFox ASN reports (`https://threatfox.abuse.ch/asn/[ASN]`), ipapi.is's abusive-ASN and abusive-range lists, CIRA Canadian Shield and ASD's ACSC BPH paper.
- **CrimsonVector practice:** require at least two independent sources, or one high-confidence source, per entry; record granularity (ASN / prefix / IP), confidence and a validity window; never rely on a single feed.

#### 2. Conduct Traffic Analysis to Supplement the List
- **CISA:** analyse traffic against a baseline to find outliers, and allowlist expected CDNs, whose behaviour can resemble fast flux.
- **CrimsonVector practice:** use GreyNoise to separate opportunistic scanning from targeted activity, and feed confirmed discoveries back into the list.

#### 3. Automate Regular Reviews of the Curated List
- **CISA:** promptly add new malicious resources and **remove resources that are reallocated to legitimate infrastructure**; refresh ASN-to-IP mappings, because "IP addresses behind an ASN can change". The removal trigger is **reallocation, not age.**
- **CrimsonVector practice:** weekly review of active-threat entries, monthly for watch-list entries; track false positives; version-control the list. Entries that pass their validity window leave the *blocking* tier but are kept for alerting and hunting (Section 8) -- do not delete them.

#### 4. Share Threat Intelligence with the Community
- **CISA:** share threat intelligence through public and private channels.
- **CrimsonVector practice:** participate in sector ISACs, contribute validated indicators to abuse.ch and MISP communities, and use CISA's Automated Indicator Sharing (AIS).

#### 5. Configure Centralized Event Logging
- **CISA:** log the ASNs and IP addresses of connections, alert on matches against the list, and always use the latest list version.
- **CrimsonVector practice:** enrich SIEM events with ASN, organisation, registry holder and threat-density context; keep **at least 12 months** of logs for connections involving BPH-listed infrastructure (CISA sets no retention period). Listing lags activity by about three weeks on average, so every new listing should trigger a 30-90-day look-back.

#### 6. Implement Filters at the Network Border
- **CISA:** decide *whether* and at what granularity to filter through a risk analysis; keep an **audit log** recording when and why each filter was applied, with change control; refresh ASN-to-IP mappings regularly.
- **CrimsonVector practice (granularity matrix):**
  - ASN-level block: T1-T2 pure BPH where the entire ASN is malicious -- and only after confirming the current registry holder (Section 8.3)
  - Prefix-level block: mixed-use ASNs where specific prefixes are malicious
  - Individual IP block: targeted C2 addresses in otherwise-clean ranges
  - Deploy at several layers (firewall, web proxy, DNS RPZ/sinkhole, email gateway) and log every blocked connection

#### 7. Develop Filter Feedback Processes
- **CISA:** give internal users and external parties a way to ask about blocked resources, with standardised inquiry data and trend tracking.
- **CrimsonVector practice:** a spike in unblock requests for one range can mean a false positive -- or a BPH provider moving legitimate customers in as cover.

#### 8. Use Upstream Providers That Follow Secure by Design Principles
- **CISA (defenders and ISPs):** ask your upstreams how they handle requests about blocked resources, whether an unblock applies to one customer or all, and take a risk-informed approach to unblock requests.
- **CrimsonVector practice:** write abuse-handling SLAs and null-route rights into transit and peering contracts.

### For ISPs and Hosting Providers

#### 9. Notify Customers About the Lists and Filters You Apply
- **CISA:** tell customers which malicious-resource lists and filters the ISP applies, so they understand possible incidents or availability impacts, and consider opt-outs for customers with different risk tolerances.
- **CrimsonVector practice:** proactively notify customers whose own addresses appear on community blocklists, with remediation timelines and escalating consequences.

#### 10. Create Customer-Facing Filters
- **CISA:** offer filters that customers can choose to apply (e.g. DNS-based filtering using community blocklists).

#### 11. Form Standards and Norms for ISP Accountability
- **CISA:** agree a sector-wide code of conduct, binding in peering contracts. Consider a time-boxed block (e.g. **90 days**) of all malicious IP ranges managed under an AS, then ask the AS operator or its upstream to confirm the abusers were removed; repeat the block if nothing was done.

#### 12. Establish KYC Capabilities
- **CISA:** require authenticated proof of identity, banking details (e.g. a one-cent test payment) and a Legal Entity Identifier where applicable. Because BPH operators cycle receive-only email addresses and phone numbers, require the customer to **send** a verification code to the provider rather than receive one. Collect only what privacy law allows.

#### 13. Implement Internet Routing Security Best Practices
- **CISA:** follow NCSC-UK's "Responsible Use of the Border Gateway Protocol (BGP) for ISP Interworking" and NIST SP 800-189 Rev. 1.
- **CrimsonVector practice:** RPKI route-origin validation, BCP38/BCP84 ingress filtering, MANRS participation and hijack monitoring.

---

## 8. Infrastructure Reuse and Indicator Retention

"Burned" IPs and domains are cheap for an adversary to abandon -- that is the point of Bianco's Pyramid of Pain -- but the pyramid measures the *pain of denial*, not the *value of detection*. This section sets out why published indicators keep value and how to retain them without causing collateral damage.

### 8.1 What the evidence shows

- **Listing lags activity.** Across 24 open feeds (1.38M indicators), indicators were listed on average **21 days** after activity began. Listed hosts often stayed active for weeks: for one feed, more than half were still active 79+ days later. Only **6.2%** of entries appeared on a second feed. (Griffioen et al., ACNS 2020)
- **Vendors barely overlap.** Two leading commercial vendors shared only **2.5-4%** of indicators for the same 22 actors, with about a month's lag between them. (Bouwman et al., USENIX Security 2020)
- **Burned domains come back.** About **8.7%** of blacklisted domains were listed *after* expiring and changing owner, and expired malicious domains are re-registered and re-weaponised. (Lever et al., IEEE S&P 2016)
- **Reuse traces detect early.** Unit 42's detector for stockpiled domains, built on certificate-transparency and passive-DNS reuse features, caught malicious domains **~34 days** before VirusTotal vendors. (Unit 42, Dec 2023)
- **Actor-level reuse happens at block and provider level.** Cl0p's MFT campaigns, 2020-2026:
  - Exact IPs recurred only within about 0-12 months of exposure.
  - The same **/22-/24 blocks and providers** recurred **18-36 months** later.
  - HostZealot, Cl0p's most-reused provider, served 4 of 10 campaigns.
  - A watchlist of providers named in earlier public IOC lists would have flagged 50-63% of the IOC IPs in later campaigns (MOVEit, SysAid, Cleo, Oracle EBS).
  - See [`analysis/CL0P_HOSTZEALOT_REUSE.md`](../analysis/CL0P_HOSTZEALOT_REUSE.md).
- **Counterpoints are concentrated in identifiable classes:**
  - Cloud IPs are recycled quickly: in Pauley et al. (IEEE S&P 2022), an AWS IP released by a tenant had an 87% chance of being re-leased to the researchers during their 101-day study, which captured traffic still meant for previous tenants.
  - Shared-hosting IPs carry large collateral damage.
  - Compromised or residential hosts are victims.
  - Fast-flux IPs rotate every 3-5 minutes (CISA AA25-093A).
  - Some BPH providers expose "dummy" interfaces so only decoys get listed (CISA AA25-093A).

### 8.2 Tiered retention model (CrimsonVector practice)

| Tier | Contents | Validity | Action |
|---|---|---|---|
| **1 -- Block** | Corroborated, fresh indicators on BPH-owned or dedicated infrastructure | Short `valid_until` (30-120 days, in line with MISP's 120-day NIDS default), decaying from the last sighting | Automated blocking |
| **2 -- Alert / Enrich** | Decayed indicators not shown to be reallocated; actor-preferred provider blocks (e.g. HostZealot's Cl0p-used /22s-/24s for 24-36 months) | Scored, never auto-blocked | SIEM enrichment, priority elevation, conditional challenges |
| **3 -- Hunt / Archive** | Everything, indefinitely, with provenance: source and grade, first/last seen, sightings, and the ASN, prefix, organisation and hosting class *at time of observation* | Indefinite | Retro-hunting, clustering, pivoting |

**Rules:**
1. **Decay by hosting class, not one clock.**
   - Cloud/CDN and residential/proxy IPs decay in days. Phishing domains decay in days too (MISP's phishing default is 3 days).
   - BPH-owned prefix indicators decay slowly and stay tied to prefix and ASN lineage. A new ASN takes 2-5 days to obtain; IPv4 space is the scarce asset.
   - Compromised hosts are never promoted to blocking without corroboration.
2. **Remove from Tiers 1-2 on evidence of reallocation**, which is CISA's trigger:
   - an RIR holder change
   - a BGP origin change
   - a match against a cloud range
   - a passive-DNS ownership change

   Keep the Tier 3 record.
3. **Carry context on every record** (prefix, ASN, provider, upstream), so a quiet IP still informs about its block. Use Spamhaus ASN-DROP as an annotation and attribution anchor, not as an automatic block.
4. **Re-hunt triggers:**
   - Any new public report, designation or ASN-DROP addition: look back 30-90 days.
   - An actor or provider resurfacing after dormancy (Cl0p between campaigns; Stark -> WorkTitans): re-run the full archived set and its pivots (certificates, RDP/VM hostnames, nameservers, prefix lineage).
   - Any prefix transfer or origin-AS change for a tracked prefix.
5. **Measure the cost.**
   - Log every block with its reason and date (the CISA audit log).
   - Record true- and false-positive sightings and feed them back into decay, as MISP's sightings model does.
   - Review Tier-2 and Tier-3 hits separately from Tier 1.

Standards support this split. STIX 2.1 indicators carry `valid_from`/`valid_until`. MISP decaying models flag attributes as *decayed* rather than deleting them: the NIDS model has a 120-day lifetime and threshold 30, and `excludeDecayed` exports only live indicators.

### 8.3 ASN hygiene before any ASN-level action

- **Check the current holder first.** Confirm the RIR/ipverse holder name and the announced prefixes. Registries re-issue returned ASNs to unrelated organisations; see taxonomy §3.9.
- **Never block a historical ASN.** Treat any CSV ASN marked `historical; reassigned to X - do not block` as history only.
- **Distrust unexplained dark ASNs.** When a tracked ASN goes dark, look for a sibling ASN under the same Spamhaus ASN-DROP `domain` field, and for the old prefixes reappearing under a new origin. Virtualine's AS214943 went dark while its ranges moved to OMEGATECH AS202412.
- **Mark silent networks `dormant`, not closed.** If an entity's ASNs are still registered to it but have announced nothing, with no new reporting, for 6+ months, set its status to `dormant` and keep its tier (taxonomy §5). Keep watch rules on the ASNs, move blocks on its old prefixes to the hunt tier (§8.2), and reassess as soon as anything is re-announced or the ASN changes hands. ELITETEAM's AS51381 and AS56873 are the reference case: still registered and still on ASN-DROP, but unrouted.

---

## Appendix A: Quick Reference -- Common BPH Provider Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| **Phoenix Rebrand** | Provider is taken down or sanctioned, re-emerges under new name/ASN within days or weeks | Stark Industries --> PQ Hosting Plus / THE.Hosting --> WorkTitans B.V.; Aeza --> Hypercore / Datavice |
| **Upstream Laundering** | BPH obtains transit from a "clean" upstream to avoid guilt-by-association | Multiple BPH providers routing through aurologic AS30823 |
| **Corporate Carousel** | Rapid incorporation and dissolution of shell companies to hold ASN resources | BtHoster's UK '[Word] Network LTD' shells. Constraints: RIPE transfer policy bars re-transferring IPv4 and 16-bit ASNs for 24 months, and RIPE NCC freezes the registrations of EU-sanctioned holders, so operators often abandon ASNs and move prefixes instead |
| **Cloudflare Fronting** | Provider advises customers to place Cloudflare in front of their infrastructure to mask the hosting origin | Common advice on underground forums |
| **Jurisdiction Shopping** | Registration in Country A, servers in Country B, ownership in Country C | UK registration, Netherlands servers, Russian beneficial owners |
| **Sanctions Evasion via Transfer** | Sanctioned entity transfers ASN/prefix resources to an apparently unrelated new entity | Stark's AS44477 moved to PQ Hosting Plus four days before the EU listing. Check RIPE DB transfer logs and compare maintainers (RF ties the Stark chain to one maintainer identity) |
| **ASN Recycling** | A shell's ASN is returned and re-issued to an unrelated organisation while the operator moves on | Karina Rashkovska AS215789 --> BLIK; CrazyRDP AS394711 --> KorGrid LLC (see taxonomy §3.9) |
| **Repeat Tenancy** | Capable actors return to the same non-bulletproof host across campaigns, renting fresh VPS in the same blocks | Cl0p and HostZealot, 2020-2024 (see `analysis/CL0P_HOSTZEALOT_REUSE.md`) |

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
