# BPH Research Repository

> **Bullet-Proof Hosting, Threat Activity Enablers & Cybercrime Infrastructure Intelligence**
>
> Maintained by CrimsonVector Research | Last Updated: 2026-07-17

---

## Overview

This repository is a comprehensive intelligence resource for tracking bullet-proof hosting (BPH) providers, threat activity enablers (TAEs), and the infrastructure that underpins modern cybercrime. It combines a structured provider database with analytical documents, an investigative playbook, and an organized source library.

**Current scope:** 63 providers/entities tracked across the BPH ecosystem, including sanctioned operators, upstream enablers, financial facilitators, corporate shells, sanctions-evasion vehicles, SEA guarantee-marketplace laundering facilitators, and residential-proxy/anonymization TAE networks.

---

## Repository Structure

```
BPH_Research/
|
|-- README.md                    <-- You are here
|-- BPH_Master.csv               <-- Master provider database (flat CSV, 25 columns)
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
|
|-- playbook/
|   |-- ANALYST_PLAYBOOK.md      <-- Investigation guide: identification indicators, OSINT
|                                     pivoting, tools/sources, workflows, templates
|
|-- sources/
|   |-- SOURCE_INDEX.md           <-- Catalog of all sources with metadata and grade
|
|-- tools/
|   |-- build_dashboard_data.py  <-- Generates the public dashboard_data/ from the CSV +
|   |                                 the private findings file, with denylist/defang gates
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
1. Add an entry to **`sources/SOURCE_INDEX.md`** with full metadata and source grade
2. Use the assessment template in **`playbook/ANALYST_PLAYBOOK.md`** Section 5 to evaluate new providers
3. Add the provider to **`BPH_Master.csv`** with all applicable columns populated
4. Update relevant analytical documents as needed

---

## Master Database Schema

The CSV uses 25 columns. Key fields:

| Column | Description |
|--------|-------------|
| `provider_name` | Primary name |
| `status` | active / flagged / suspected / sanctioned / evading / seized / dissolved / exposed |
| `risk_tier` | T1-Confirmed BPH through T5-Watch List (see taxonomy) |
| `primary_asn` | Primary Autonomous System Number |
| `sanctions_designations` | OFAC / EU / UK / AU designations with dates |
| `associated_threat_actors` | APT groups, ransomware brands hosted |
| `associated_malware` | Specific malware families observed |
| `rf_threat_density_score` | Recorded Future Threat Density Score (if available) |
| `sources` | Source IDs referencing SOURCE_INDEX.md |

Full schema documented in the CSV header row.

---

## Key Intelligence Highlights

### Sanctioned Entities (as of July 2026)
- **Aeza International Ltd** — OFAC July 2025 (with UK NCA) + UK Sept 2025 + OFAC expansion Nov 2025 (Hypercore, Datavice)
- **Stark Industries Solutions** — EU May 2025 (**Hybrid Threats Regulation (EU) 2024/2642**, not the 17th Russia package)
- **Zservers / XHOST** — US/UK/AU trilateral Feb 2025
- **Media Land LLC** — OFAC/UK/AU trilateral Nov 2025 + **EU July 2026** (Impl. Reg. (EU) 2026/1714) + **DOJ indictment July 2026**
- **FUNNULL Technology** — OFAC May 29 2025
- **Garantex** — OFAC April 2022 + **EU 16th package Feb 24 2025** (first EU crypto-exchange listing); evading via Grinex/Exved
- **WorkTitans B.V. / THE.Hosting** — successor to EU-sanctioned Stark; Dutch FIOD raid May 2026 (network survived)
- **PQ Hosting Plus S.R.L.** — EU via Stark/Neculiti designation
- **Hypercore LTD** — OFAC Nov 2025 (Aeza front); AS215552 + AS211522. *UK: caught via ownership/control, not a standalone listing*
- **Datavice MCHJ** — OFAC Nov 2025 (Aeza expansion entity, Uzbekistan). *OFAC-only — not UK-designated*
- **Grinex / A7A5 (Old Vector)** — OFAC Aug 2025 (Garantex successors); EU 19th-package A7A5 ban Oct 2025. *Grinex suspended operations April 2026; A7A5 volume collapsed ~96%*
- **Nobitex / Wallex / Bitpin / Ramzinex** — OFAC June 2026 ("Economic Fury" — Iranian exchanges)
- **First VPN Service (1VPNS)** — OFAC July 2026 (criminal VPN/anonymization enabler; with UK FCDO)
- **Prince Group / Huione ecosystem** — OFAC (35 targets) + FBI infra seizure + FinCEN H-Pay successor rule, June 2026

> **Note on legal basis vs. lifecycle status:** OFAC/EU/UK *designation* is a `sanctioned` status regardless of tier; being sanctioned on non-cyber grounds (e.g. the Iranian exchanges, designated for terror finance) does not auto-escalate an entity to tier T1. See `taxonomy/BPH_TAXONOMY.md`.

### Critical Infrastructure Node
- **aurologic GmbH (AS30823)** — Central upstream for the European BPH cluster. `BPH_Master.csv` lists **11 downstream entities** routing through it: Aeza, Femo IT, Railnet/Virtualine, Tnsecurity, Karina Rashkovska, metaspinner, KPROHOST, Altawk, SWISSNETWORK02/Global-Data, WAIcore, and BtHoster. Disrupting aurologic would cascade across all of them.

### Recent Enforcement
- **CrazyRDP seized** Nov 2025 (Operation Endgame, Dutch police, 250 servers)
- **Cryptomixer.io seized** Nov 2025 (EUR 1.3B Bitcoin mixed since 2016)
- **Operation Endgame** targeting infostealers Nov 2025 (1025 servers worldwide)
- **Grinex suspends operations** April 2026 (claimed $13.7M cyberattack; Elliptic/Chainalysis suspect a false-flag exit)
- **Dutch FIOD raid on THE.Hosting/WorkTitans** May 2026 (800+ servers, 2 arrests) — *network survived at near pre-raid levels (ELLIO/Dark Reading)*
- **Asocks residential-proxy botnet** dismantled May 2026 (NCSC-NL/Politie — 17M devices, 200 servers)
- **Operation Endgame** June 2026 — SocGholish/Amadey/StealC (326 servers, 142 domains, EUR 41M frozen)
- **FBI/Google seize NetNut proxy + Popa botnet** July 2026 (Alarum Technologies; 2M+ devices; 316 actor clusters)
- **Operation Riptide — Media Land/ML.Cloud** July 2026 (EU sanctions + DOJ indictment, $10M RFJ reward)

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
| C | Community/Independent (Krebs, abuse.ch, Spamhaus) |
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
2. **New source:** Add to `sources/SOURCE_INDEX.md` with metadata and grade (update the Source Statistics counts), cross-reference the Source ID in the CSV `sources` column
3. **Status change:** Update CSV status/tier, add a `TIMELINE.md` entry, update the ecosystem map if relationships changed
4. **Sanctions update:** Add to timeline, update the CSV `sanctions_designations` field, check for evasion vehicles
5. **After any CSV change:** regenerate `BPH_Master.xlsx` (single-sheet mirror) and re-run `tools/build_dashboard_data.py` so the workbook and `dashboard_data/` stay in sync. Appendices A/B of `ECOSYSTEM_MAP.md` are also CSV-derived — keep them consistent.

---

*This repository is maintained for authorized cybercrime research and defensive security purposes.*
