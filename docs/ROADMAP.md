# BPH Research Roadmap

> **Started:** 2026-10-30 | **Owner:** CrimsonVector Research
>
> Plan for making the repository easier to keep accurate, cheaper to audit, and broader in scope. It grew out of the October 2026 audit (PR #5), which showed where the current design costs the most effort. Each phase ships as its own pull request; tick items off here as they merge.

---

## Why these changes

The October 2026 audit re-checked 79 entities, 113 ASNs and 186 sources. The work that took longest was not research - it was keeping hand-maintained copies in step and re-deriving facts the repo already knew:

| Pain point seen in the audit | Cost | Fix (phase) |
|---|---|---|
| Appendix A/B, tier counts, README count and source statistics edited by hand on every change | Every PR touched 4-5 files for one row | Generate them from the data (1) |
| No CI - the validator only runs if someone remembers to | Drift found late | Validate every push and PR (1) |
| "Do not block" warnings exist only as free text inside ASN qualifiers | A blocklist built from the CSV can hit re-issued ASNs (ZEMA, BLIK, KorGrid, NovoServe) | Structured `block_recommendation` per ASN (1) |
| Tier decisions not recorded | GCSAS, Cloudzy and others had to be re-derived | `tier_basis` and `last_verified` columns (1) |
| Routing changes found only by manual checks (Altawk, MIRhosting, WorkTitans dark; RetryHost block re-announced) | Weeks of lag | Scheduled routing monitor with successor detection (2) |
| UK shell strike-offs found only by reading Companies House pages | Four notices on one day would have been missed | Companies House monitor (2) |
| Claims and caveats buried in 2,000-character notes | 26 'unverified' caveats needed a dedicated research pass | `claims.csv` with per-claim source, grade and status (3) |
| Source entries without URLs; one whitepaper mislabelled for months | Re-finding sources; wrong publisher credited | Machine-readable `sources.csv` with URL, archive and retrieval date (3) |
| Relationships only in prose and hand-drawn diagrams | GCSAS-GIR, Aeza-Andwase, Pfcloud-Omegatech links hard to see | `relationships.csv` and generated diagrams (3) |
| No machine-readable export | Consumers re-parse the CSV | STIX 2.1 and MISP exports honouring block guidance (4) |
| Domains appear in nearly every enforcement action, but registrars and DNS enablers are out of scope | Blind spot | Registrar / DNS Enabler module (R) |

## Principles

1. **One source of truth per fact.** Derived tables are generated, never edited by hand.
2. **Every claim carries a source, a grade and a verification state.** Unverified claims are allowed but must be labelled and queryable.
3. **Never mislabel a legitimate party.** Re-issued ASNs, upstream carriers and registrars-of-record are marked so they are not blocked or accused by accident.
4. **Automate detection, keep judgement human.** Monitors open issues; analysts decide tier and status changes.
5. **Ship in small, validated PRs.** Each phase leaves the validator green.

---

## Phase 1 - Foundations

Goal: no more hand-synced tables, structured block guidance, recorded tier reasoning, CI.

- [x] **1.1 Schema v2.** Add four columns to `BPH_Master.csv` (appended, so existing column positions do not move): `geo_cluster`, `primary_role` (both moved out of Appendix A, where they were the only hand-kept fields), `tier_basis` (taxonomy criterion and key sources) and `last_verified` (date the row was last checked end to end, distinct from `last_updated`).
- [x] **1.2 Generator.** `tools/generate_docs.py` rebuilds ECOSYSTEM_MAP Appendix A and B, the taxonomy tier counts, the README entity count and the SOURCE_INDEX statistics. `--check` fails if any generated block is stale.
- [x] **1.3 ASN register.** `data/asns.csv`: one row per (ASN, entity) with `relation`, `qualifier`, `routing_state`, `asndrop_listed`, `last_checked`, `block_recommendation` (`block` / `block-prefixes` / `hunt` / `monitor` / `do-not-block`) and `recommendation_basis`. The validator checks it matches the CSV and that each ASN has one recommendation.
- [x] **1.4 CI.** `.github/workflows/validate.yml` runs the generator check and the validator on every push and pull request.
- [x] **1.5 Docs.** README schema and structure, contributing steps, this roadmap.

**Done when:** a row change needs edits only to the CSV (and `asns.csv` for ASN changes), then `python tools/generate_docs.py`; CI is green.

## Phase 2 - Monitoring

Goal: detect changes within a day instead of at the next audit.

- [x] **2.1 Routing monitor** (`tools/monitor.py`, checks `asn`, `drop`, `prefix`). For every ASN in `data/asns.csv` and every listed prefix: holder, routing state, prefix count, Spamhaus ASN-DROP and DROP. Writes a dated snapshot; the "diff" is against the recorded data rather than the previous snapshot, so findings persist until the data catches up or they are acknowledged (`monitor/acknowledged.csv`).
- [x] **2.2 Successor detection** (checks `asndrop`, `withdrawn`, `ripe`). New ASN-DROP entries under a tracked operator's Spamhaus `domain`; withdrawn tracked prefixes re-originated by another ASN, grouped by new origin; recent RIPE aut-num and route objects of the maintainers and organisations in `data/registry_handles.csv` that point at untracked ASNs.
- [x] **2.3 Companies House monitor** (check `company`, watchlist `data/companies.csv`). Status and filings after the recorded latest filing; officer and PSC filings shown as generic labels so no individual is named.
- [x] **2.4 Scheduled workflow** (`.github/workflows/monitor.yml`). Weekly run that opens or updates a single "Monitor findings" issue and comments with new findings; snapshot kept as an artifact; no automatic edits to the data. The domain check (registration, registrar, status, seizure nameservers) from the R1 pilot runs in the same job.

**Done when:** the October 2026 changes (Altawk, MIRhosting, WorkTitans, GCSAS listing, RetryHost re-announcement, the 2026-10-13 strike-off notices) would each have produced an issue entry. **Met:** a live replay against the 2026-09-25 data produced every one of them (see `docs/MONITORING.md`), and the same cases run offline in CI (`tests/test_monitor.py`).

## Phase 3 - Claims, sources and relationships

- [x] **3.1 `sources/sources.csv`.** ID, grade, title, publisher, date, URL, archive URL, retrieved date and URL note; every SOURCE_INDEX table and the statistics generated from it. Default grade per publisher in `sources/publishers.csv` (a different grade needs a `grade_note`). URLs found and checked for 204 of 221 sources (183 fetched, 21 behind bot checks); 23 titles, dates and publishers corrected against the live pages.
- [ ] **3.2 `data/claims.csv`.** Entity, claim, source ID, grade, status (`verified` / `unverified` / `disputed` / `superseded`), verified date. Migrate every caveat and tier-relevant claim; notes become summaries.
- [ ] **3.3 `data/relationships.csv`.** Typed edges (operator-of, front-of, successor-of, upstream-of, ip-supplier-of, payment-rail-of, sister-of) with source IDs; Mermaid diagrams generated into ECOSYSTEM_MAP.
- [x] **3.4 Staleness report.** Split in two so CI never fails because the calendar moved: `docs/DATA_HEALTH.md` (generated, date-independent: sources without URLs, grade deviations, oldest verifications) and the monitor's `stale` check, which lists entities, registrars, ASN rows and claims past 90 days in the weekly issue.

## Phase 4 - Exports

- [ ] **4.1 STIX 2.1 bundle** (identities, infrastructure, indicators for `block` / `block-prefixes` ASNs and prefixes, relationships) with `valid_until` from monitor freshness.
- [ ] **4.2 MISP feed** with decay-friendly attributes and do-not-block items excluded.
- [ ] **4.3 Plain blocklists** (ASN and CIDR) generated only from `block` recommendations.

## Phase R - Registrar and DNS Enabler module

Goal: cover the domain layer - registrars, resellers, privacy/proxy services, TLD registries and DNS / fast-flux providers - without mislabelling registrars that are merely the registrar of record.

- [x] **R1 Pilot (data we already hold).** Extract every domain in the repo (seized domains, C2 and phishing domains, provider and front-brand domains), look up registrar (IANA ID) and DNS provider via RDAP/DNS, and measure which registrars recur across tracked operators. Output `data/domains.csv` and `analysis/REGISTRAR_PILOT.md`.
- [x] **R2 Taxonomy.** Taxonomy section 2.8 "Registrar / DNS Enabler": five subtypes, registrar readings of T1-T5 and a seven-point evidence floor (registrar of record is never evidence; rates normalised by domains under management; sustained = 2+ periods; ICANN notices older than 24 months are history; reseller adverts describe the reseller).
- [x] **R3 Data.** `data/registrars.csv` with IANA ID, accreditation, tier, status, tier basis, ICANN notices, abuse metrics, linked BPH rows and sources. The five pilot candidates were evaluated in `analysis/REGISTRAR_EVALUATION.md`: NiceNIC T2, CNOBIN and Eranet T3, Regtime and Bizcn not rated; Trustname.com (ICANN-terminated 2026) added as the T1 reference case.
- [x] **R4 Sources and monitoring.** Interisle (phishing scores 2024-2026; malicious-registrations study 2026), Spamhaus Botnet Threat Updates, ICANN Contractual Compliance notices, sanctions lists and forum reseller adverts evaluated. NetBeacon (formerly DNS Abuse Institute) tables are published as images and were not used. The monitor's `registrar` check now tracks IANA accreditation and new ICANN notices for every cited registrar.

**Done when:** the pilot answers whether tracked BPH operators concentrate on a small set of registrars, and the taxonomy can rate a registrar without relying on registrar-of-record alone. **Met:** the pilot found no dominant registrar but operator-level clustering; section 2.8 rated four registrars on outside evidence only and left two candidates unrated.

---

## Status log

| Date | Change |
|---|---|
| 2026-10-30 | Roadmap written; Phase 1 and the R1 pilot started |
| 2026-10-30 | Phase 1 complete in PR: schema v2 (29 columns, tier_basis for all 79 rows), `tools/generate_docs.py`, `data/asns.csv` (124 rows; 50 block, 16 block-prefixes, 1 hunt, 38 monitor, 19 do-not-block), CI workflow |
| 2026-10-30 | R1 pilot complete in PR: 66 domains, registrar resolved for 39; no dominant registrar (NameCheap 28%, a base-rate effect); operator clustering at NiceNIC, CNOBIN and Regtime; Cloudflare DNS on 52%; Shinjiru is itself an accredited registrar; 17 ccTLD domains lack RDAP. See `analysis/REGISTRAR_PILOT.md` |
| 2026-10-30 | Phase 2 complete in PR: `tools/monitor.py` (8 checks), `data/companies.csv` (15), `data/registry_handles.csv` (87), weekly workflow, offline tests; October replay passes. First run: 8 retried RDAP lookups resolved; AS203319 (GIR), AS197703 (First Server) and AS45054 (PINSPB) added; post-seizure re-origination of Virtualine space by AS6461 recorded; successor origins recorded for MIRhosting, Altawk, WorkTitans, Kaopu, PINSPB and First Server |
| 2026-10-30 | Phase R (R2-R4) complete in PR: taxonomy section 2.8, `data/registrars.csv` (Trustname T1, NiceNIC T2, CNOBIN and Eranet T3), `analysis/REGISTRAR_EVALUATION.md`, monitor `registrar` check, 11 new sources |
| 2026-10-30 | Phase 3A (3.1, 3.4) complete in PR: `sources/sources.csv` with URLs for 204 of 221 sources, `sources/publishers.csv`, generated SOURCE_INDEX tables, `docs/DATA_HEALTH.md`, monitor `stale` check, Actions on Node 24 |
