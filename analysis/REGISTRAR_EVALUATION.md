# Registrar Evaluation (Roadmap R2–R3)

> **Date:** 2026-10-30 | **Maintainer:** CrimsonVector Research | **Rules:** [taxonomy section 2.8](../taxonomy/BPH_TAXONOMY.md#28-registrar--dns-enabler) | **Data:** [`data/registrars.csv`](../data/registrars.csv)
>
> The registrar pilot ([`REGISTRAR_PILOT.md`](REGISTRAR_PILOT.md)) nominated five registrars because tracked operators cluster on them. This document tests each one against outside evidence, under the evidence floor in taxonomy section 2.8. Being the registrar of record for a tracked operator's domain is context and never counts. Two candidates are rated T3, one T2, and two not at all. Trustname.com is added as the reference case for T1.

---

## Outcome

| Registrar (IANA ID) | Pilot link (context only) | Tier | Status | Deciding evidence |
|---------------------|---------------------------|------|--------|-------------------|
| Fewmoretaps OU d/b/a **Trustname.com** (4318) | none | **T1** | exposed | ICANN terminated its accreditation on 2026-08-27 for failing its DNS-abuse duties; marketed as "bulletproof" |
| **NiceNIC** International Group (3765) | AnonRDP infrastructure domains; Feo Prest | **T2** | flagged | #1 by Interisle phishing rate three years running; 87.6% of its 2025 registrations blocklisted; in every Spamhaus botnet table since mid-2024 |
| **CNOBIN** Information Technology (3254) | both Virtualine domains | **T3** | suspected | Top-20 phishing rate in 2025 and 2026, rising; one Spamhaus appearance |
| **Eranet** International (1868) | Cryptomus | **T3** | suspected | Top-20 phishing rate in 2025 and 2026; 17.8% of 2025 registrations blocklisted |
| **Regtime** (1362) | BtHoster; Media Land | not rated | — | No outlier evidence. Its only appearance is one Spamhaus table in Q3 2023 (#20, 11 domains). |
| **Bizcn** (471) | Kaopu Cloud | not rated | — | No current evidence. A 2014 ICANN breach notice (cured) and 2014 vendor allegations are history (rule 6). |

None of the five candidates has an ICANN enforcement notice in 2023–2026, and none of them faces sanctions or law-enforcement action. Sanctions were checked against the OFAC SDN list (2026-10-27), the OFAC consolidated list and the UK Sanctions List (2026-10-30). The only hit was an unrelated name match. The ratings rest on normalised measurement data, which shows how much of a registrar's business is abuse. Measurement does not show intent, so no candidate reaches T1.

## Method

**1. ICANN Contractual Compliance.**
- Source: the formal notices page, https://www.icann.org/compliance/notices. The page was parsed in full, and the weekly monitor now re-checks it (`--checks registrar`).
- The DNS-abuse duty itself is RAA section 3.18.2, in force since 5 April 2024 (ICANN advisory, 2024-02-05).

**2. Normalised measurement.** Interisle Consulting Group publishes a phishing domain score for each registrar: phishing domains per 10,000 domains under management, May to April each year.
- Phishing Landscape 2024: https://interisle.net/s/PhishingLandscape2024.pdf
- Phishing Landscape 2025: https://interisle.net/s/phishinglandscape2025.pdf
- Registrar tables: https://www.cybercrimeinfocenter.org/phishing-activity-in-registrars-may-april-2025 and …-2026
- *Malicious Registrations in the Domain Name Market* (June 2026), sent to the ICANN Board: https://itp.cdn.icann.org/en/files/correspondence/rose-aaron-to-sinha-26-06-2026-en.pdf. It gives the share of each registrar's 2025 registrations that ended up on blocklists.

**3. Independent counts.** Spamhaus *Botnet Threat Update* tables of the registrars most abused for botnet C&C domains:
- July–December 2024: https://content.spamhaus.org/b1e35611-db7c-4d58-8e9a-a0cfa1e8c534.pdf
- January–June 2025: https://content.spamhaus.org/22f3805e-27c4-4bd9-a06e-37df8dab3d8c.pdf
- July–December 2025: https://content.spamhaus.org/30bc0262-14ee-42d9-93bb-31985ef89497.pdf
- January–June 2026: https://content.spamhaus.org/d32359a1-1665-4dd8-8cf4-a75d2f66fc1d.pdf

These are raw counts, not rates. They show persistence, not share.

**4. Other evidence searched.** Sanctions lists, law-enforcement filings, vendor and journalism reporting, and forum adverts. Forum reseller adverts are Grade E, and they describe the reseller, not the registrar.

Every figure in this document was read from the primary source. Two kinds of figure seen during research are left out because they could not be confirmed first-hand: earlier editions, and tables published only as images (e.g. NetBeacon's monthly high-rate tables).

## Evidence by candidate

### NiceNIC International Group (IANA 3765): T2

| Source | Period | Measure | Value | Rank |
|--------|--------|---------|-------|------|
| Interisle Phishing Landscape 2024 | May 2023–Apr 2024 | phishing domains per 10,000 under management | 4,490.9 (45,238 of 100,732) | #1 |
| Interisle Phishing Landscape 2025 | May 2024–Apr 2025 | same | 8,129.4 (114,493 of 140,839) | #1 |
| Interisle 2026 tables | May 2025–Apr 2026 | same | 11,471.1 (272,696 phishing domains against 237,724 under management) | #1 |
| Interisle, Malicious Registrations (2026) | domains created in 2025 | share blocklisted | 87.6% (157,970 of 180,404); market-wide 10% | #1 |
| Spamhaus Botnet Threat Update | Jul–Dec 2024 | botnet C&C domains | 1,636 (+757%) | #1 |
| Spamhaus Botnet Threat Update | Jan–Jun 2025 | same | 614 (−62%, "great efforts") | #3 |
| Spamhaus Botnet Threat Update | Jul–Dec 2025 | same | 738 | #4 |
| Spamhaus Botnet Threat Update | Jan–Jun 2026 | same | 1,514 (+105%) | #4 |

**Why T2.** It is a sustained outlier in two independent sources across three periods, and the normalised measure shows abuse is most of its business. That meets the second T2 condition. GoDaddy, for scale, scores about 10–11 on the same Interisle measure.

**Why not T1.** There is no ICANN notice, law-enforcement action or evidence of intent. Spamhaus also recorded a real improvement in early 2025.

**Not counted.** An advocacy project says it filed an ICANN complaint in August 2026. That cannot be verified, because ICANN complaints are not public.

### CNOBIN Information Technology (IANA 3254): T3

| Source | Period | Measure | Value | Rank |
|--------|--------|---------|-------|------|
| Interisle Phishing Landscape 2024 | May 2023–Apr 2024 | phishing domain score | not in the top 20 | — |
| Interisle Phishing Landscape 2025 | May 2024–Apr 2025 | same | 284.9 (1,543 of 54,167) | #9 |
| Interisle 2026 tables | May 2025–Apr 2026 | same | 592.3 (3,809 of 64,312) | #12 |
| Spamhaus Botnet Threat Update | Jul–Dec 2025 | botnet C&C domains | 159, new entry | #13 |
| Spamhaus Botnet Threat Update | Jan–Jun 2026 | same | left the top 20 | — |

**Why T3.** It has a top-20 normalised rate in two periods and is rising. Phishing domains are still about 6% of its domains under management, and no non-response to abuse reports is documented, so the T2 conditions are not met.

**Not counted:**
- Third-party resellers sell "BIZCN/Cnobin" registrations as bulletproof on forums: SecuredNet in 2022 and bpname.cc in 2025 (bitcointalk topics 5385828 and 5553500). Those adverts describe the resellers.
- A shared ownership with Bizcn is claimed on forums and hinted at by shared Xiamen contact numbers, but it is unverified.

### Eranet International (IANA 1868): T3

| Source | Period | Measure | Value | Rank |
|--------|--------|---------|-------|------|
| Interisle Phishing Landscape 2025 | May 2024–Apr 2025 | phishing domain score | 150.6 (3,994 of 265,145) | #16 |
| Interisle 2026 tables | May 2025–Apr 2026 | same | 569.7 (55,096 of 967,149; +1,279%) | #13 |
| Interisle, Malicious Registrations (2026) | domains created in 2025 | share blocklisted | 17.8% (145,455 of 815,751) | — |

**Why T3.** It has a top-20 normalised rate in two periods. At 17.8%, the share blocklisted is above the 10% market-wide figure but below the 25% T2 mark.

**History, not evidence:**
- Eranet's InterNIC listing gives TodayNIC's contact address. TodayNIC received an ICANN breach notice on 2014-10-10 for failing to investigate and respond to abuse reports (RAA 3.18). The breaches were cured.
- Forum reviewers list Eranet among registrars that "tend to ignore minor DMCA complaints" (Grade E).

### Regtime (IANA 1362) and Bizcn (IANA 471): not rated

**Regtime.** It appears in none of the Interisle tables from 2024 to 2026 and in none of the Spamhaus registrar tables from mid-2024. Its only appearance is Spamhaus Q3 2023, at #20 with 11 domains. It holds `bthoster.com` and Media Land's `sshvps.net`, which is registrar-of-record context only.

**Bizcn:**
- Its only ICANN notice is a breach notice of 8 May 2014, which was cured. It concerned Whois accuracy and record keeping, not abuse handling.
- In 2014, a vendor (LegitScript) alleged that Bizcn ignored reports about rogue online pharmacies.
- No measurement source from 2023–2026 names it.
- Forum resellers bundle it with CNOBIN.

Both stay unrated. The monitor will report any ICANN notice or change of accreditation for either.

## Trustname.com (IANA 4318): the T1 reference case

ICANN issued Fewmoretaps OU, d/b/a Trustname.com, four notices of breach: on 10 June, 26 June, 16 July and 26 August 2026. It then terminated the registrar's accreditation on 27 August 2026, effective 11 September.
- **The grounds** were failure to take "prompt and appropriate mitigation action(s)" against DNS abuse (RAA 3.18.2) and failure to investigate and respond to abuse reports (3.18.1). Notice: https://www.icann.org/uploads/compliance_notice/attachment/1367/hedlund-to-nestsiarovich-27aug26.pdf
- **Trade press.** Domain Name Wire (2026-08-28) and Domain Incite (2026-09-01) describe it as a registrar that claimed to offer "bulletproof" registrations.
- **Forum review.** A 2025 forum review ranked it "99.99% bulletproof".

No tracked operator domain is registered with Trustname. It is rated as the calibration case for the T1 registrar reading. If the operation reappears as a reseller of another registrar, its status becomes `evading`.

## Context: controls and the wider field

The same Interisle 2026 table shows how far the outliers sit from mainstream registrars:

| Registrar | 2026 phishing domain score |
|-----------|----------------------------|
| GoDaddy | 11.0 |
| NameSilo | 312.2 |
| Gname | 301.1 |
| Dominet (HK) | 1,311.4 |
| WebNic | 1,216.8 |

Several registrars outside this repository's scope would also rate T2–T3 under section 2.8:
- **WebNic** received ICANN's DNS-abuse breach notice of 29 July 2025, cured on 27 October 2026.
- **Dominet (HK)** holds IANA ID 3775. Unit 42 found 68% of Smishing Triad root domains registered there.

They are not rated here because none holds a tracked operator's domain. A later pass can add them if tracked operators start using them.

**NameSilo** is registrar of record for four tracked domains: two FUNNULL front brands, Asocks and NETINNOVATIONLLC. Its 2026 score (312.2) places it in the top 20 (#19), which would make it a T3 candidate under section 2.8. **Recommended next evaluation.**

## Limits

- **No raw volume.** Normalised scores depend on the registrar's domains under management in gTLDs. A registrar that mostly sells ccTLDs can look better or worse than it is.
- **Phishing-heavy.** Interisle measures phishing. Malware and botnet abuse are covered only through Spamhaus counts.
- **Measurement is not intent.** A high rate is consistent with negligent abuse handling, a reseller channel that has gone bad, or a deliberately permissive business. Only ICANN notices, law-enforcement action or self-advertising separate these.
- **The ccTLD gap remains.** The Russian-market operators' .ru and .su registrations are outside ICANN's contracts and outside these measurements.
