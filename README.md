# BPH Research Repository

> **Bullet-Proof Hosting, Threat Activity Enablers & Cybercrime Infrastructure Intelligence**
>
> Maintained by CrimsonVector Research | Last Updated: 2026-05-16

---

## Overview

This repository is a comprehensive intelligence resource for tracking bullet-proof hosting (BPH) providers, threat activity enablers (TAEs), and the infrastructure that underpins modern cybercrime. It combines a structured provider database with analytical documents, an investigative playbook, and an organized source library.

**Current scope:** 50+ providers/entities tracked across the BPH ecosystem, including sanctioned operators, upstream enablers, financial facilitators, corporate shells, and sanctions-evasion vehicles.

---

## Repository Structure

```
BPH_Research/
|
|-- README.md                    <-- You are here
|-- BPH_Master.csv               <-- Master provider database (flat CSV, 25+ columns)
|-- BPH_Master.xlsx              <-- Formatted multi-sheet Excel workbook
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
    |-- SOURCE_INDEX.md           <-- Catalog of all sources with metadata and grade
    |-- IOCTA-2026.md             <-- Europol IOCTA 2026 (markdown)
    |-- IOCTA-2026.pdf            <-- Europol IOCTA 2026 (original PDF)
    |-- Bulletproof_Defense_*.pdf  <-- CISA/NSA BPH Mitigation Guidance (Nov 2025)
    |-- screencapture-*.pdf       <-- Recorded Future TAE article (May 2026)
```

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
1. Save source material to **`sources/`** and add an entry to **`sources/SOURCE_INDEX.md`**
2. Use the assessment template in **`playbook/ANALYST_PLAYBOOK.md`** Section 5 to evaluate new providers
3. Add the provider to **`BPH_Master.csv`** with all applicable columns populated
4. Update relevant analytical documents as needed

---

## Master Database Schema

The CSV uses 25 columns. Key fields:

| Column | Description |
|--------|-------------|
| `provider_name` | Primary name |
| `status` | active / flagged / suspected / sanctioned / evading / dissolved / seized |
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

### Sanctioned Entities (as of May 2026)
- **Aeza International Ltd** — OFAC/UK July 2025 + expanded Nov 2025
- **Stark Industries Solutions** — EU May 2025 (17th Russia package)
- **Zservers / XHOST** — US/UK/AU trilateral Feb 2025
- **Media Land LLC** — OFAC/UK/AU trilateral Nov 2025
- **FUNNULL Technology** — OFAC May 2025
- **Garantex** — OFAC April 2022 + EU Feb 2026 (evading via Grinex/Exved)
- **WorkTitans B.V. / THE.Hosting** — EU via Stark/Neculiti designation
- **PQ Hosting Plus S.R.L.** — EU via Stark/Neculiti designation
- **Hypercore LTD** — OFAC/UK Nov 2025 (Aeza front)

### Critical Infrastructure Node
- **aurologic GmbH (AS30823)** — Central upstream for 10+ BPH downstream operations in Europe. Disrupting aurologic would cascade across Femo IT, Railnet/Virtualine, metaspinner, Tnsecurity, WAIcore, Altawk, Karina Rashkovska, KPROHOST, SWISSNETWORK02, and potentially Aeza transit.

### Recent Enforcement
- **CrazyRDP seized** Nov 2025 (Operation Endgame, Dutch police, 250 servers)
- **Cryptomixer.io seized** Nov 2025 (EUR 1.3B Bitcoin mixed since 2016)
- **Operation Endgame** targeting infostealers Nov 2025 (1025 servers worldwide)

---

## Classification System

Providers are classified using a 5-tier risk system and 6 provider types. See `taxonomy/BPH_TAXONOMY.md` for full definitions.

**Risk Tiers:** T1 (Confirmed BPH) > T2 (High Risk) > T3 (Suspected) > T4 (Gray Zone) > T5 (Watch List)

**Provider Types:** Pure BPH | BPH-Adjacent | Upstream Enabler | Financial Enabler | Corporate Shell | Sanctions-Evasion Vehicle

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

## Contributing

To add new intelligence to this repository:

1. **New provider:** Use the assessment template in the playbook, add to CSV, document sources
2. **New source:** Save to `/sources/`, add to SOURCE_INDEX.md, cross-reference in CSV
3. **Status change:** Update CSV status/tier, add timeline entry, update ecosystem map if relationships changed
4. **Sanctions update:** Add to timeline, update CSV sanctions_designations field, check for evasion vehicles

---

*This repository is maintained for authorized cybercrime research and defensive security purposes.*
