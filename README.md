# BPH Research Repository

> **Bullet-Proof Hosting, Threat Activity Enablers & Cybercrime Infrastructure Intelligence**
>
> Maintained by CrimsonVector Research | Last Updated: 2026-10-30

---

## Overview

This repository is a comprehensive intelligence resource for tracking bullet-proof hosting (BPH) providers, threat activity enablers (TAEs), and the infrastructure that underpins modern cybercrime. It combines a structured provider database with analytical documents, an investigative playbook, and an organized source library.

**Current scope:** 79 providers/entities tracked across the BPH ecosystem, including sanctioned operators, upstream enablers, financial facilitators, corporate shells, sanctions-evasion vehicles, SEA guarantee-marketplace laundering facilitators, and residential-proxy/anonymization TAE networks.

---

## Repository Structure

```
BPH_Research/
|
|-- README.md                    <-- You are here
|-- BPH_Master.csv               <-- Master provider database (flat CSV, 29 columns - schema v2)
|-- BPH_Master.xlsx              <-- Single-sheet Excel mirror of the CSV
|
|-- taxonomy/
|   |-- BPH_TAXONOMY.md          <-- Classification framework (risk tiers, provider types,
|                                     operational patterns, identification signals)
|
|-- analysis/
|   |-- ECOSYSTEM_MAP.md         <-- Relationship mapping, geographic clusters, corporate
|   |                                 networks, upstream dependencies, financial overlay
|   |-- TIMELINE.md              <-- Sanctions & enforcement chronology (reverse-chrono)
|   |-- CL0P_HOSTZEALOT_REUSE.md <-- Cl0p MFT campaigns 2020-2026: HostZealot reuse and the
|   |                                 defensive value of burned indicators
|   |-- REGISTRAR_PILOT.md       <-- Registrar & DNS pilot (roadmap R1): which registrars and DNS
|   |                                 providers tracked operators use; candidates for R2
|   |-- REGISTRAR_EVALUATION.md  <-- Candidate registrars tested against outside evidence (R2-R3)
|
|-- playbook/
|   |-- ANALYST_PLAYBOOK.md      <-- Investigation guide: identification indicators, OSINT
|                                     pivoting, tools/sources, workflows, templates
|
|-- sources/
|   |-- sources.csv              <-- Source catalogue: ID, grade, publisher, date, URL, retrieved date
|   |-- publishers.csv           <-- Default grade per publisher (deviations need a grade_note)
|   |-- SOURCE_INDEX.md           <-- Catalog of all sources (tables generated from sources.csv)
|
|-- data/
|   |-- asns.csv                 <-- ASN register: one row per (ASN, entity) with routing state,
|   |                                 Spamhaus status and a structured block_recommendation
|   |-- domains.csv              <-- Domain register (registrar pilot): registrar / IANA ID, DNS
|   |                                 provider and hosting for domains tied to tracked entities
|   |-- companies.csv            <-- UK companies the monitor watches at Companies House
|   |-- registry_handles.csv     <-- RIPE maintainers/organisations the monitor watches
|   |-- registrars.csv           <-- Rated registrar / DNS enablers (taxonomy 2.8), kept apart from
|   |                                 the CSV because they have no ASNs
|
|-- monitor/
|   |-- acknowledged.csv         <-- Monitor findings reviewed and accepted, with reasons
|
|-- docs/
|   |-- ROADMAP.md               <-- Improvement plan and status (phases 1-4, registrar module)
|   |-- MONITORING.md            <-- What the weekly monitor checks and how to act on findings
|
|-- .github/workflows/
|   |-- validate.yml             <-- CI: generated-block check, validator, monitor unit tests
|   |-- monitor.yml              <-- Weekly monitor run; keeps one "Monitor findings" issue current
|
|-- tools/
|   |-- build_dashboard_data.py  <-- Generates the public dashboard_data/ from the CSV +
|   |                                 the private findings file, with denylist/defang gates
|   |-- build_xlsx.py            <-- Regenerates BPH_Master.xlsx from the CSV
|   |-- generate_docs.py         <-- Regenerates ECOSYSTEM_MAP Appendices A/B, tier and entity
|   |                                 counts and source statistics from the data
|   |-- monitor.py               <-- Compares live routing, Spamhaus, RIPE DB, RDAP and Companies
|   |                                 House state with the data; reports differences as findings
|   |-- validate_repo.py         <-- Cross-file consistency checks (CSV schema, ASN register,
|   |                                 source index, workbook, generated blocks)
|   |-- denylist.example.txt     <-- Template for the (gitignored) publication denylist
|
|-- dashboard_data/              <-- Sanitized, public dashboard outputs (generated)
|   |-- providers.json           <-- Public-safe provider fields, one per tracked entity
|   |-- aggregates.json          <-- Computed stats + enforcement timeline
|   |-- feed.json                <-- Published forward-hunt findings (summaries)
|   |-- finding/<id>.json        <-- Per-finding detail
|   |-- manifest.json            <-- Build metadata
|
|-- LICENSE                       <-- MIT License
```

> **Note:** Source documents (PDFs, web captures) are not included in this repository. See `sources/SOURCE_INDEX.md` for a full catalog with links and metadata.
>
> **Also gitignored (private inputs, never published):** the raw `dashboard_src/findings.json` forward-hunt file and the live `tools/denylist.txt`. Only the build script and the sanitized `dashboard_data/` outputs are public. See [Dashboard Data Pipeline](#dashboard-data-pipeline).

---

## Quick Start

### For threat analysts
1. Start with **`BPH_Master.csv`** to look up a specific provider, ASN, or alias
2. Use **`taxonomy/BPH_TAXONOMY.md`** to understand risk tier definitions and classification criteria
3. Reference **`playbook/ANALYST_PLAYBOOK.md`** for investigation workflows and OSINT pivoting techniques

### For understanding the ecosystem
1. Read **`analysis/ECOSYSTEM_MAP.md`** for the big picture: who connects to whom, geographic clusters, corporate shell networks
2. Review **`analysis/TIMELINE.md`** for the chronology of sanctions, takedowns, and evasion responses

### For adding new intelligence
1. Add the source to **`sources/sources.csv`** with full metadata, URL and grade (the SOURCE_INDEX tables are generated from it)
2. Use the assessment template in **`playbook/ANALYST_PLAYBOOK.md`** Section 5 to evaluate new providers
3. Add the provider to **`BPH_Master.csv`** with all applicable columns populated
4. Update relevant analytical documents as needed

---

## Master Database Schema

The CSV uses 29 columns (schema v2, 2026-10-30: four columns appended at the end, so earlier positions are unchanged). Key fields:

| Column | Description |
|--------|-------------|
| `provider_name` | Primary name |
| `status` | active / flagged / suspected / sanctioned / evading / seized / dissolved / exposed / dormant (network still held but silent for 6+ months) |
| `risk_tier` | T1-Confirmed BPH through T5-Watch List (see taxonomy) |
| `primary_asn` | Primary Autonomous System Number. Qualifiers matter: an ASN marked `historical; reassigned to X - do not block` now belongs to an unrelated organisation |
| `sanctions_designations` | OFAC / EU / UK / AU designations with dates |
| `associated_threat_actors` | APT groups, ransomware brands hosted |
| `associated_malware` | Specific malware families observed |
| `rf_threat_density_score` | Recorded Future Threat Density Score (if available) |
| `sources` | Source IDs from `sources/sources.csv` (catalogued in SOURCE_INDEX.md) |
| `geo_cluster` / `primary_role` | Geography and role shown in ECOSYSTEM_MAP Appendix A (schema v2) |
| `tier_basis` | Taxonomy criterion and key evidence behind the tier; must start with the tier code (schema v2) |
| `last_verified` | Date the row was last checked end to end (distinct from `last_updated`); rows older than 90 days are flagged (schema v2) |

**ASN register (`data/asns.csv`).** One row per (ASN, entity) pair cited in the CSV, with `routing_state` (`live`, `dark`, `unregistered`, `reassigned`), Spamhaus ASN-DROP status and a `block_recommendation`:

| Value | Meaning |
|-------|---------|
| `block` | Block at ASN level (T1, or on Spamhaus ASN-DROP) |
| `block-prefixes` | Block the entity's malicious prefixes, not the whole ASN (T2, shared tenancy, successor hops) |
| `hunt` | Alert and block confirmed-malicious IPs only (T3) |
| `monitor` | No blocking; watch for change (T4/T5, upstream carriers, dark ASNs) |
| `do-not-block` | Historical, reassigned or recycled ASN - now belongs to someone else or nobody |

Build blocklists from `data/asns.csv`, never from the free-text qualifiers in the CSV. Registry holders that are private individuals are recorded as `[individual registrant]`.

Full schema documented in the CSV header row.

---

## Key Intelligence Highlights

### Sanctioned Entities (as of October 2026)
- **Aeza Group LLC / Aeza International Ltd (UK front)** — OFAC July 2025 (with UK NCA); UK designated Aeza Group LLC Nov 19 2025 (Russia regime); OFAC follow-on Nov 2025 (Hypercore, Smart Digital Ideas, Datavice, Makarov, Zakirov)
- **Stark Industries Solutions** — EU May 20 2025 (Impl. Reg. (EU) 2025/965 under the **hybrid-threats regime (EU) 2024/2642**, not the 17th Russia package); company dissolved Sept 2025
- **Zservers / XHOST** — Feb 11 2025, lists differ by authority (OFAC: Zservers + 2 admins; UK: + XHOST Internet Solutions LP and 6 people; AU: + 5 people); 127 servers seized by Dutch police Feb 12 2025
- **Media Land LLC** — US/UK/AU Nov 2025 (differing lists) + **EU July 13 2026** (Impl. Reg. (EU) 2026/1714) + **DOJ indictment unsealed July 14 2026** ($62M+ losses) + New Zealand (Volosovik) Aug 2026
- **FUNNULL Technology** — OFAC May 29 2025 (with administrator Liu Lizhi). *CTG Server Limited and StarCloud were not designated*
- **Garantex** — OFAC April 2022 + **EU 16th package Feb 24 2025** (first EU crypto-exchange listing); domains seized March 6 2025; successor Grinex
- **Hypercore LTD** — OFAC Nov 2025 (Aeza front; AS211522, dark since ~Feb 2026). *OFAC-only in the UK Nov 2025 notices*
- **Datavice MCHJ** — OFAC Nov 2025 (Aeza evasion vehicle, Uzbekistan). *OFAC-only*
- **Grinex / A7A5 (Old Vector; A7 LLC network)** — OFAC Aug 2025; UK Aug 2025; EU 19th-package A7A5 ban (effective Nov 25 2025). *Grinex suspended after an April 15 2026 drain*
- **Nobitex / Wallex / Bitpin / Ramzinex** — OFAC June 2026 ("Economic Fury"; Nobitex also under E.O. 13224 with four executives)
- **First VPN Service (1VPNS)** — OFAC July 2026 (criminal VPN; dismantled in Operation Saffron, May 2026)
- **A7 Network** — OFAC designated the whole network a transnational criminal organization on Oct 1 2026 (FinCEN proposed a rule against its Sub-Agents the same day); extends the A7A5/Old Vector designations
- **Cryptomus / Heleket (Xeltox Enterprises Ltd)** and **TokenSpot CJSC** (Grinex front) — UK Oct 8 2026 (Russia regime). Chainalysis names Cryptomus/Heleket as the payment rail of Zservers, Stark, First VPN and Aeza
- **Prince Group / Huione ecosystem** — OFAC/UK/DOJ/FinCEN Oct 14 2025 (146 targets; Huione Section 311 final rule) + OFAC June 2026 (35 targets) + FinCEN proposed H-Pay successor rule; Xinbi Guarantee disrupted Sept 2026
- *Not sanctioned (corrected 2026-09-25):* **PQ Hosting Plus S.R.L.** (absent from the EU annex; exposure only via the listed Neculitis) and **WorkTitans/THE.Hosting** (successor network; FIOD raid May 2026)

> **Note on legal basis vs. lifecycle status:** OFAC/EU/UK *designation* is a `sanctioned` status regardless of tier; being sanctioned on non-cyber grounds (e.g. the Iranian exchanges, designated for terror finance) does not auto-escalate an entity to tier T1. See `taxonomy/BPH_TAXONOMY.md`.

### Critical Infrastructure Node
- **aurologic GmbH (AS30823)** — Central upstream for the European BPH cluster; Recorded Future says it transits about 70% of the most prominent high-risk TAE networks. RF names Aeza, Femo IT/Defhost, Railnet/Virtualine, the metaspinner-named front and SWISSNETWORK02/Global-Data as downstreams; Qurium adds Tnsecurity, WAIcore and Altawk. By Sept 2026 several of those downstream ASNs had gone dark or been re-issued, and Virtualine had moved to OMEGATECH (AS202412) - which was itself seized in Operation Omegaline in Oct 2026.

### Cl0p and HostZealot (Sept 2026)
- **HostZealot / HZ Hosting Ltd (Bulgaria)** appears in **4 of 10 Cl0p mass-exploitation campaigns** (Accellion 2020, GoAnywhere and MOVEit 2023, Cleo 2024) - 21 HZ addresses in CISA, Mandiant, Lumen and Huntress IOC lists. Reuse is block-level: one exact IP recurs, while 79[.]141[.]160[.]0/22 and 5[.]149[.]248[.]0/23 recur over 18-27 months. No published indicator supports HZ use in the June 2026 Windchill campaign. Tracked at T4 (repeatedly abused, not shown to enable). See [`analysis/CL0P_HOSTZEALOT_REUSE.md`](analysis/CL0P_HOSTZEALOT_REUSE.md).

### Data-quality note (2026-09-25 audit)
- Every ASN in the CSV was re-checked against registry and Spamhaus ASN-DROP data. Two had never belonged to the named entity (AS216071 for Zservers, AS215552 for Hypercore) and three Media Land ASNs were unrelated; they were removed. Twelve more have been re-issued to unrelated organisations and are now marked `historical; reassigned ... - do not block`. **Never build an ASN blocklist from the CSV without reading those qualifiers.**
- Follow-up decisions (2026-09-25):
  - A new `dormant` status covers networks that are still registered to the entity but have announced nothing, with no new reporting, for 6+ months: ELITETEAM/1337TEAM, HOSTYPE and SWISSNETWORK02/Global-Data. Their tiers are unchanged.
  - CDNCloud was removed: no ASN, registry record, blocklist entry or CTI report could be found for it.
  - Kaopu Cloud HK and PrivateAlps/Private Layer were raised to T1 on Recorded Future's 2025 Threat Density top 10 (#4 and #6), with the taxonomy's three-independent-source minimum met. MIRhosting was raised to T1 because its founder was arrested in the FIOD action against WorkTitans, whose only upstream it was.

### Data-quality note (2026-10-30 audit)
- Every ASN and listed prefix in the CSV was re-checked against RIPEstat and Spamhaus. **Gone dark in October:** Altawk's AS209946, both MIRhosting ASNs, and nearly all of WorkTitans' space (now `seized`). **Newly on Spamhaus ASN-DROP:** GCSAS (AS215540); Cloudzy (AS14956) re-listed; new Spamhaus-attributed ASNs for Pfcloud (AS205329) and Chang Way (AS218974). A former Virtualine block (RetryHost, 94.26.38.0/24) was re-announced from an Iranian ASN after the seizure - a lead.
- Companies House: Aeza International Ltd and Hypercore Ltd are dissolved; QWINS' company was dissolved (row now `dissolved`, network still live); Femo IT, First Server, WAIcore and Tiger Network received strike-off notices on 2026-10-13.
- Corrections: Cloudzy's operator is Hannan (not Hassan) Nozari and the EvilProxy link is restored; the 1VPNS operation produced an interview, not an arrest; Intel 471's Media Land figures (80% of *active* domains); the AlexHost phishing wave was 2023 and impersonated AlexHost; 'Dolphon 1337' is registered as Dolphin 1337 Limited; FUNNULL's 175+ CNAME figure is Silent Push's.
- Tier changes: Cloudzy T3 -> T2 (ASN-DROP escalation rule). New rows: TokenSpot CJSC (T1) and Xeltox Enterprises / Cryptomus-Heleket (T2).
- Follow-up (same day): **GCSAS raised to T1** - Recorded Future's 2025 top-10 '4VPS' (#7) is GCSAS plus its Sevastopol sister **Global Internet Solutions (GIR, AS207713)**, now a T1 row; Intrinsec, eSentire and RF all classify the pair as BPH/TAE. New rows: BL Networks/BitLaunch (T3; top DDoSia C2 host per RF) and watch-list rows for Zomro, Evoxt and the Aeza IPv4 suppliers Andwase and Prostie Reshenia. Most older 'unverified' caveats are now sourced or removed; the Silent Push BPH whitepaper had been mislabelled as Spamhaus's.

### Recent Enforcement
- **Dutch police seize ~250 servers of a bulletproof host** Nov 12 2025 - press-attributed to **CrazyRDP**; police said the case is *not* part of Operation Endgame
- **Operation Endgame 3.0** Nov 10-13 2025 (Rhadamanthys/VenomRAT/Elysium; 1,025 servers)
- **Operation Olympia - Cryptomixer.io** Nov 24-28 2025, announced Dec 1 (EUR 1.3B Bitcoin mixed since 2016; EUR 25M seized)
- **Grinex suspends operations** April 2026 after a ~$13-15M drain it blamed on foreign services
- **Dutch FIOD raid on THE.Hosting/WorkTitans** May 18 2026 (800+ servers; WorkTitans owner and MIRhosting founder arrested) - *post-raid reports conflict on how much of the network survived*
- **Operation Saffron - First VPN (1VPNS)** May 19-20 2026 (33 servers; a suspect searched and interviewed in Ukraine - no arrest announced)
- **Residential-proxy botnet (press-attributed to Asocks)** dismantled May 28 2026 (NCSC-NL/Politie; 17M devices; a subset of 200+ NL backend servers seized)
- **Operation Endgame** June 15-19 2026 - SocGholish/Amadey/StealC (326 servers, 142 domains, EUR 41M frozen)
- **FBI seizes NetNut domains; Google disrupts the Popa botnet** July 2 2026 (Alarum Technologies; 2M+ devices; 316 actor clusters)
- **Media Land/ML.Cloud** July 2026 - EU sanctions (July 13) and the DOJ indictment under FBI Operation Riptide (July 14)
- **QScan/QTRouter (PRC "QTFY" proxy/ORB platform)** domains seized Aug 26 2026 (DOJ/FBI with Lumen)
- **Xinbi Guarantee** disrupted Sept 9 2026 (OFAC + DOJ Scam Center Strike Force; $52.8M USDT frozen)
- **Dutch police take down a proxy service** of ~178,000 infected devices Oct 8 2026 (servers offline at several hosting providers; service not named)
- **Operation Omegaline - Virtualine/Omegatech** Oct 27 2026: FBI seized virtualine[.]net (E.D. Va. warrant) with Polizei Hessen, Politie Midden-Nederland, the NCA, OverRIPE and Lumen; Dutch police seized dozens of servers in Limburg (data on 3,000+ customers). DOJ alleges CSAM hosting and money laundering; no operators named or charged. OMEGATECH AS202412 is now near-invisible in routing. RF's 2025 Threat Density #1 - the repo had already tied Omegatech to Virtualine (May 2026). Same day: anonrdp[.]com moved to FBI seizure nameservers; **AnonRDP** (self-styled bulletproof VPS/RDP and fast-flux host) moved to anonrdp[.]st and is now tracked at T1 on Blatant Technologies AS403005, whose nine /24s are all on Spamhaus DROP

---

## Classification System

Providers are classified using a 5-tier risk system and 7 provider types. See `taxonomy/BPH_TAXONOMY.md` for full definitions.

**Risk Tiers:** T1 (Confirmed BPH) > T2 (High Risk) > T3 (Suspected) > T4 (Gray Zone) > T5 (Watch List)

**Provider Types (7):** Pure BPH | BPH-Adjacent | Upstream Enabler | Financial Enabler | Corporate Shell | Sanctions-Evasion Vehicle | Anonymization/Proxy Enabler

---

## Source Grading

All sources are graded for reliability:

| Grade | Description |
|-------|-------------|
| A | Government/Official (sanctions, LE press releases) |
| B | Established CTI Vendor (Recorded Future, Mandiant, etc.) |
| C | Community/Independent (Krebs, abuse.ch, Spamhaus, Team Cymru, registry mirrors) |
| D | Single Source / Unverified |
| E | Self-Reported / Marketing |

See `sources/SOURCE_INDEX.md` for the full catalog.

---

## Dashboard Data Pipeline

`tools/build_dashboard_data.py` regenerates the public `dashboard_data/` outputs from two sources of truth:

- **`BPH_Master.csv`** (public) → `providers.json` (public-safe fields only) and `aggregates.json` (computed stats + enforcement timeline).
- **`dashboard_src/findings.json`** (private, gitignored) → `feed.json` and `finding/<id>.json`.

**OPSEC model.** A forward-hunt finding is published only if `publish == true` **and** its confidence is `confirmed` or `high`; setting `publish=false` holds a confirmed lead out of the public feed. Every IOC and free-text field is defanged. The entire generated output is then scanned against `tools/denylist.txt` (after un-defanging, so a defanged internal IP cannot slip through) and re-scanned for any un-defanged URL scheme or bare IPv4. **If either gate trips, nothing is written and the build exits non-zero.**

```
python tools/build_dashboard_data.py        # writes dashboard_data/ if both gates pass
```

Run it after any change to `BPH_Master.csv` or the private findings file, and review the diff before committing — committing `dashboard_data/` is what publishes it. Exit codes: `0` ok · `2` denylist hit · `3` defang leak · `4` input/setup error.

---

## Contributing

To add new intelligence to this repository:

1. **New provider:** Use the assessment template in the playbook, add to `BPH_Master.csv`, document sources
2. **New source:** Add a row to `sources/sources.csv` with metadata, URL and grade (the SOURCE_INDEX tables and statistics are generated), cross-reference the Source ID in the CSV `sources` column
3. **Status change:** Update CSV status/tier, add a `TIMELINE.md` entry, update the ecosystem map if relationships changed
4. **Sanctions update:** Add to timeline, update the CSV `sanctions_designations` field, check for evasion vehicles
5. **ASN changes:** add or update the matching row in `data/asns.csv` (one row per ASN and entity, with a `block_recommendation`).
6. **After any data change:** run `python tools/generate_docs.py` (rebuilds Appendices A/B, tier and entity counts and source statistics - never edit those blocks by hand), `python tools/build_xlsx.py` (workbook mirror), and `tools/build_dashboard_data.py` where you hold the private inputs.
7. **Before committing:** run `python tools/validate_repo.py`. CI runs it, plus `generate_docs.py --check` and the monitor's offline tests, on every push and pull request. It fails on schema or ASN-register errors, uncatalogued Source IDs, a stale workbook, stale generated blocks, and any historical ASN not marked `do-not-block`.
8. **Monitor findings:** the weekly [monitor](docs/MONITORING.md) keeps one open "Monitor findings" issue. Resolve each finding by updating the data (it disappears on the next run) or acknowledge it in `monitor/acknowledged.csv` with a reason.

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for the improvement plan.

---

*This repository is maintained for authorized cybercrime research and defensive security purposes.*
