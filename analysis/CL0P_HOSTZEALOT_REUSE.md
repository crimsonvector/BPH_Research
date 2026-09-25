# Cl0p Infrastructure Reuse and HostZealot, 2020-2026

**Version:** 1.0
**Date:** 2026-09-25
**Maintainer:** CrimsonVector Research
**Related:** `BPH_Master.csv` row *HostZealot (HZ Hosting Ltd)* · [`TIMELINE.md`](TIMELINE.md) · [`taxonomy/BPH_TAXONOMY.md`](../taxonomy/BPH_TAXONOMY.md) §3.9-3.10 · [`playbook/ANALYST_PLAYBOOK.md`](../playbook/ANALYST_PLAYBOOK.md) §8
**Indicator format:** IPv4 addresses and prefixes are defanged (`[.]`), following the repository's dashboard OPSEC model. Refang them before loading into tooling.

---

> **Why this document exists.** A September 2026 LinkedIn post by threat-intelligence researcher Eli Woodward argued that "burned" IPs and domains keep defensive value, using Cl0p as the example: Cl0p has reused the Bulgarian host **HostZealot** across "almost a dozen campaigns and 6 years of data", used it "again" in June 2026, and one particular IP "has been observed 3 times". This document tests those claims against the published indicator record and turns the result into retention guidance. It also explains the HostZealot row added to the master database.

## Key judgments

1. **HostZealot (HZ Hosting Ltd) is Cl0p's most-reused hosting provider, independently confirmed.** HZ address space appears in **4 of Cl0p's 10 mass-exploitation campaigns** (Accellion FTA 2020-21, GoAnywhere 2023, MOVEit 2023, Cleo 2024). Primary IOC lists from CISA, Mandiant, Lumen Black Lotus Labs and Huntress reproduce Team Cymru's August 2026 finding ("most frequently observed provider ... four of nine"). HZ addresses make up **23% of CISA's GoAnywhere list and 14% of its MOVEit list**. *(High confidence.)*
2. **The reuse is at block and provider level, not IP level.** Only one HZ address recurs exactly (79[.]141[.]160[.]78: GoAnywhere and MOVEit). The same /22-/23 blocks recur over **18-27 months**. *(High confidence.)*
3. **"One IP observed 3 times" is not reproducible from public data.** No IP appears in three of the ten campaigns. Two Data Campus addresses in 92[.]118[.]36[.]0/24 (not HZ) reach three only if the May 2023 Truebot operation is counted as a campaign. *(Moderate confidence; Kroll's full MOVEit list was not available.)*
4. **The June 2026 HZ claim is not supported by published indicators.** None of the seven public PTC Windchill/FlexPLM IOC IPs (PTC; Ransom-ISAC) is in HZ space. Woodward's dataset shows two HZ flows for Windchill, but it has no IP-level data to check. *(Moderate confidence.)*
5. **HZ is gray-zone, not bulletproof, on current evidence.** HZ runs KYC and a 3-strike AUP. It is not on Spamhaus DROP or ASN-DROP, and its reputation density matches mainstream hosts. Every finding is about actors *using* HZ, not HZ enabling them. It is therefore tracked at **T4**, with explicit escalation triggers. *(Moderate confidence.)*
6. **Burned indicators keep value mainly when widened.** Exact IPs were reused only within about 0-12 months. /24s and providers recurred up to about 3 years later. A watchlist of providers seen in earlier published lists would have flagged:
   - 63% of MOVEit IPs
   - 50% of the Cleo callbacks
   - 60% of Oracle EBS IPs
   - 29% of Windchill IPs

---

## 1. The campaign series

Ten mass-exploitation campaigns against file-transfer and enterprise applications can be tied to the Cl0p brand or the TA505 / FIN11 / Lace Tempest cluster (also tracked as GOLD TAHOE and, by Unit 42, Hazy Scorpius) between December 2020 and June 2026.

| # | Campaign | Window | CVE(s) | Attribution strength | Published IOC IPs (A/B-grade) | HZ IPs |
|---|---|---|---|---|---|---|
| 1 | Accellion FTA | Dec 2020-Jan 2021 | CVE-2021-27101/-27102/-27103/-27104 | High (Mandiant UNC2546/UNC2582; CISA) | MAR + BLL exfil list | **2** |
| 2 | SolarWinds Serv-U | 2021 (zero-day was DEV-0322's); TA505 N-day use | CVE-2021-35211 | Medium | few (FIN11 C2s via Mandiant) | 0 |
| 3 | Fortra GoAnywhere MFT | late Jan-Feb 2023 | CVE-2023-0669 | High (Cl0p claim; CISA) | 52 (+25 inferred from the withdrawn 7-Jun list) | **10** (+3 inferred) |
| 4 | PaperCut MF/NG | from mid-Apr 2023 | CVE-2023-27350 | Medium (Microsoft: Lace Tempest) | 17 | 0 |
| 5 | Progress MOVEit Transfer | from 27 May 2023 | CVE-2023-34362 | High (Microsoft; Cl0p claim; CISA) | 76 | **9** |
| 6 | SysAid On-Prem | Nov 2023 | CVE-2023-47246 | Medium-High (Microsoft: Lace Tempest) | 4 | 0 |
| 7 | Cleo Harmony/VLTrader/LexiCom | from 3 Dec 2024 | CVE-2024-50623, CVE-2024-55956 | High (Cl0p claim) | 6 (Huntress) | **1** |
| 8 | Oracle E-Business Suite | Jul-Oct 2025 | CVE-2025-61882 | High (brand) / Medium (FIN11) (GTIG) | 5 | 0 |
| 9 | Gladinet CentreStack/Triofox | Nov-Dec 2025 | unknown at the time | Medium-Low | none published | 0 |
| 10 | PTC Windchill/FlexPLM | zero-day ~early Jun 2026; patch 17 Jun; KEV 25 Jun | CVE-2026-12569 | Medium-High (Ransom-ISAC; ReliaQuest) | 7 | 0 |

**Sources:**
- [Mandiant](https://www.fireeye.com/blog/threat-research/2021/02/accellion-fta-exploited-for-data-theft-and-extortion.html) and [CISA AA21-055A / MAR AR21-055A](https://www.cisa.gov/news-events/analysis-reports/ar21-055a)
- [CISA AA23-158A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-158a) and [AA23-131A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-131a)
- [Huntress (Cleo)](https://www.huntress.com/blog/threat-advisory-oh-no-cleo-cleo-software-actively-being-exploited-in-the-wild)
- [GTIG (Oracle EBS)](https://cloud.google.com/blog/topics/threat-intelligence/oracle-ebusiness-suite-zero-day-exploitation)
- [The Hacker News (Windchill)](https://thehackernews.com/2026/06/cisa-adds-exploited-ptc-windchill-rce.html)
- [Team Cymru](https://www.team-cymru.com/post/cl0p-ransomware-mft-attack-pattern-threat-intelligence)

The "almost a dozen campaigns over 6 years" framing fits: ten campaigns, or eleven if FIN11's January 2023 Serv-U re-exploitation is counted separately.

## 2. HostZealot in brief

- **Entity.** HZ HOSTING LTD. / ХЗ ХОСТИНГ ЕООД:
  - Plovdiv, Bulgaria; EIK 203391232.
  - A single-owner company incorporated in January 2015 (renamed from a predecessor name on 2015-02-20).
  - Its RIPE LIR organisation, ORG-FNL9-RIPE, dates from 2012.
  - Bulgarian registry aggregators disagree on the owner. Verify in the Commercial Register before recording personnel.
- **Network.** Four country-coded ASNs, all registered in Bulgaria. Together they announce **187 IPv4 prefixes (79,360 addresses)** plus 2a01:8640::/32 (September 2026):

  | ASN | AS-name | Role | Cl0p-relevant prefixes |
  |---|---|---|---|
  | AS59711 | HZ-EU-AS | access provider | 5[.]149[.]248[.]0/23, 77[.]83[.]196[.]0/23, 185[.]80[.]52[.]0/22, 185[.]104[.]194[.]0/24, 185[.]117[.]88[.]0/22 |
  | AS61046 | HZ-UK-AS | stub | 5[.]149[.]250[.]0/23, 185[.]81[.]112[.]0/23 |
  | AS201525 | HZ-CA-AS | stub | 79[.]141[.]166[.]0/23 (5[.]149[.]252[.]0/23 in the inferred list only) |
  | AS202015 | HZ-US-AS | stub | 79[.]141[.]160[.]0/22, 185[.]33[.]84[.]0/22, 193[.]42[.]38[.]0/24 |

  The Swedish AS209668 "HZ-HOSTING AB" is unrelated. Vendor IOC tables often geolocate HZ addresses to the Netherlands, the US, Canada or Estonia, while the registry country is Bulgaria.
- **Other tenants.** SideWinder APT (Kaspersky, October 2024: a "preference for HZ Hosting, BlueVPS and GhostNET"; BlackBerry, July 2024). Akira and Fog ransomware SSL-VPN logins (Arctic Wolf, October 2024). A DanaBot C2 (Black Lotus Labs). A TrickBot/Conti server (2020 leaked chats). APT28-attributed addresses in 79.141.161.x (maltrail).
- **Counter-indicators.**
  - The 2020 Conti chats show HZ demanding a passport from a Conti operator (KYC in practice).
  - HZ runs a 3-strike AUP and accepts fiat as well as crypto.
  - There is no Spamhaus DROP or ASN-DROP listing (checked 2026-09-25).
  - IP-reputation density is in line with mainstream hosts, and much of it comes from Tor relays and VPN/proxy exits.
- **Database treatment.**
  - HZ is a **T4-Gray Zone** row with status `active`.
  - Escalate to T3 on any two of the following:
    - documented ignored abuse reports;
    - forum BPH advertising by HZ or its resellers;
    - an RF Threat Density score above the hosting baseline;
    - a substantiated ownership link to flagged personnel;
    - a second independent quantification of HZ's share of Cl0p infrastructure.
  - An ASN-DROP listing would make it T2 at minimum.

## 3. HZ addresses in Cl0p indicator lists

Twenty-one distinct HZ addresses appear in A/B-grade lists, or 24 if the three from the withdrawn 7 June 2023 GoAnywhere list are included. All four HZ ASNs are involved. In two cases the ownership at the time is documented directly:
- The February 2021 MAR WHOIS gives netname HZ-NA23 for 79[.]141[.]162[.]82.
- Huntress in December 2024 gives "AS 59711 (HZ Hosting Ltd) - Netherlands" for 5[.]149[.]249[.]226.

| Campaign | HZ address | ASN (current) | Prefix | Source |
|---|---|---|---|---|
| Accellion | 79[.]141[.]160[.]170 | AS202015 | 79[.]141[.]160[.]0/22 | Lumen BLL exfil list (flows 2020-12-21/22, ~325 GB) |
| Accellion | 79[.]141[.]162[.]82 | AS202015 | 79[.]141[.]160[.]0/22 | Mandiant; CISA MAR (DEWMODE webshell C2; netname HZ-NA23); BLL |
| GoAnywhere | 77[.]83[.]197[.]66 | AS59711 | 77[.]83[.]196[.]0/23 | CISA AA23-158A |
| GoAnywhere | 185[.]80[.]52[.]230 | AS59711 | 185[.]80[.]52[.]0/22 | CISA AA23-158A |
| GoAnywhere | 185[.]104[.]194[.]134 | AS59711 | 185[.]104[.]194[.]0/24 | CISA AA23-158A |
| GoAnywhere | 185[.]117[.]88[.]2 | AS59711 | 185[.]117[.]88[.]0/22 | CISA AA23-158A |
| GoAnywhere | 79[.]141[.]160[.]78 | AS202015 | 79[.]141[.]160[.]0/22 | CISA AA23-158A (also MOVEit) |
| GoAnywhere | 185[.]33[.]86[.]225 | AS202015 | 185[.]33[.]84[.]0/22 | CISA AA23-158A |
| GoAnywhere | 185[.]33[.]87[.]126 | AS202015 | 185[.]33[.]84[.]0/22 | CISA AA23-158A |
| GoAnywhere | 193[.]42[.]38[.]196 | AS202015 | 193[.]42[.]38[.]0/24 | CISA AA23-158A |
| GoAnywhere | 79[.]141[.]166[.]119 | AS201525 | 79[.]141[.]166[.]0/23 | CISA AA23-158A |
| GoAnywhere | 185[.]81[.]113[.]156 | AS61046 | 185[.]81[.]112[.]0/23 | CISA AA23-158A |
| MOVEit | 5[.]149[.]248[.]68 | AS59711 | 5[.]149[.]248[.]0/23 | CISA AA23-158A |
| MOVEit | 185[.]104[.]194[.]24 | AS59711 | 185[.]104[.]194[.]0/24 | CISA AA23-158A |
| MOVEit | 185[.]104[.]194[.]40 | AS59711 | 185[.]104[.]194[.]0/24 | CISA AA23-158A |
| MOVEit | 185[.]104[.]194[.]156 | AS59711 | 185[.]104[.]194[.]0/24 | CISA AA23-158A |
| MOVEit | 185[.]117[.]88[.]17 | AS59711 | 185[.]117[.]88[.]0/22 | CISA AA23-158A |
| MOVEit | 5[.]149[.]250[.]74 | AS61046 | 5[.]149[.]250[.]0/23 | CISA AA23-158A |
| MOVEit | 5[.]149[.]250[.]92 | AS61046 | 5[.]149[.]250[.]0/23 | CISA AA23-158A |
| MOVEit | 79[.]141[.]160[.]83 | AS202015 | 79[.]141[.]160[.]0/22 | CISA AA23-158A |
| Cleo | 5[.]149[.]249[.]226 | AS59711 | 5[.]149[.]248[.]0/23 | Huntress |

**Inferred, D-grade (not counted above):** 5[.]149[.]252[.]51 (AS201525), 79[.]141[.]161[.]82 and 79[.]141[.]173[.]94 (AS202015). They come from the GoAnywhere list CISA withdrew on 16 June 2023, reconstructed from a Securonix copy. A further address, 5[.]149[.]250[.]90, appears only in unsourced community lists.

## 4. What recurs, and at what level

**Exact IPs.** Of about 218 campaign IOC IPs, only six recur in two campaigns:

| IP | Campaigns | Provider (current) |
|---|---|---|
| 79[.]141[.]160[.]78 | GoAnywhere, MOVEit (both CISA lists) | HZ Hosting (AS202015) |
| 92[.]118[.]36[.]123, .210, .213, .249 | GoAnywhere, MOVEit (Kroll, via Team Cymru) | Data Campus (AS215929) |
| 92[.]118[.]36[.]199 | Serv-U-linked FIN11 C2 (Mandiant), PaperCut (CISA AA23-131A) | Data Campus (AS215929) |

No IP appears in three of the ten campaigns. If the May 2023 Truebot operation (CISA AA23-187A) is counted as a campaign, two IPs reach three, and neither is in HZ space:
- **92[.]118[.]36[.]213**: GoAnywhere Truebot C2, MOVEit per Kroll, and a Truebot C2.
- **92[.]118[.]36[.]199**: FIN11 C2, PaperCut, and Truebot/FlawedGrace.

That is the most likely basis for an "observed 3 times" claim.

**/24s in two or more campaigns (A/B lists):**
- 92[.]118[.]36[.]0/24: Serv-U-linked, GoAnywhere, PaperCut, MOVEit.
- **79[.]141[.]160[.]0/24 (HZ): Accellion, GoAnywhere, MOVEit.**
- 5[.]188[.]206[.]0/24 (Krez 999, BG): Serv-U-linked, GoAnywhere, PaperCut.
- 5[.]188[.]86[.]0/24 (Global Layer): Serv-U-linked, MOVEit.
- 5[.]34[.]180[.]0/24 (Route 95): GoAnywhere, MOVEit.
- 91[.]222[.]174[.]0/24 (Trunk Networks): GoAnywhere, MOVEit.
- **185[.]104[.]194[.]0/24 and 185[.]117[.]88[.]0/24 (HZ): GoAnywhere, MOVEit.**
- 45[.]182[.]189[.]0/24 (Datahome, PA): GoAnywhere Truebot, SysAid, and Cleo (D-grade).
- 179[.]60[.]150[.]0/24 (Layer7): MOVEit, SysAid, Truebot.

**Providers in three or more campaigns (current ASN owner):**
- Data Campus (4)
- ReliableSite.Net (4, including Oracle EBS and Windchill)
- **HZ Hosting (4)**
- Datahome (3-4)
- HostPapa/ex-ColoCrossing (3)
- Gwy IT (3)
- Krez 999 EOOD (3)
- Route 95 LLC (3)
- OVH (3)

About two-thirds of ASNs appear in only one campaign. That is 48 of 71 here, and 53 of 79 in Team Cymru's count.

**Shared tenancy caveat.** 92[.]118[.]36[.]0/24 also hosted LARVA-57, a LockBit-using group (PRODAFT), and HZ's 79.141.161.x hosted APT28-attributed infrastructure. A hit on these ranges is not proof of Cl0p.

## 5. How long burned infrastructure stays useful

**Burn-to-reuse lag (examples):**

| Indicator / block | Publicly burned | Later reuse | Lag | Level |
|---|---|---|---|---|
| 92[.]118[.]36[.]210 | 2022-05-25 (#CobaltStrike tweet) | GoAnywhere (Jan-Feb 2023); MOVEit activity (May 2023) | ~8-12 months | exact IP |
| 92[.]118[.]36[.]213 | 2023-02-11 | Truebot C2 (May 2023); MOVEit activity (May 2023) | ~3 months | exact IP |
| 79[.]141[.]160[.]78 (HZ) | GoAnywhere use Jan 2023 (published June 2023) | MOVEit (May-June 2023) | ≤ ~5 months | exact IP |
| 79[.]141[.]160[.]0/22 (HZ) | Feb 2021 (Accellion IOCs) | GoAnywhere (Jan 2023), MOVEit (May 2023) | ~23-27 months | /22 |
| 185[.]104[.]194[.]0/24, 185[.]117[.]88[.]0/22 (HZ) | GoAnywhere (Jan 2023) | MOVEit (May 2023) | ~4 months | /24 |
| 5[.]149[.]248[.]0/23 (HZ) | 2023-06-07 (CISA) | Cleo callback (Dec 2024) | ~18 months | /23 |
| Datahome AS273045 | 2023-07-06 (CISA) | Oracle EBS exploitation (Jul-Aug 2025) | ~24 months | provider |
| ReliableSite AS23470 | 2023-05/06 | Oracle EBS C2 (2025); Windchill (Jun 2026) | ~26-36 months | provider |

**How often later IOCs sat at a provider already named in earlier public lists (A/B lists, current routing):**

| Campaign | IOC IPs | Exact IP seen before | Same /24 seen before | Provider seen before |
|---|---|---|---|---|
| GoAnywhere | 52 | 0 | 6 | 17 (33%) |
| PaperCut | 17 | 1 | 2 | 5 (29%) |
| MOVEit | 76 | 5 | 16 | 48 (63%) |
| SysAid | 4 | 0 | 2 | 2 (50%) |
| Cleo (Huntress) | 6 | 0 | 0 | 3 (50%: HZ, Inovare-Prim, ServerMania) |
| Oracle EBS | 5 | 0 | 0 | 3 (60%: Datahome, ReliableSite, Hetzner) |
| Windchill | 7 | 0 | 0 | 2 (29%: ReliableSite) |

Big clouds (OVH, Hetzner, Amazon, DigitalOcean) inflate these rates. The meaningful signal is concentrated in small, permissive hosts: HZ, Datahome, Inovare-Prim, ServerMania, King-Servers, ReliableSite, Data Campus/StreamHost, Krez 999 and Route 95.

**What this means for the Pyramid of Pain argument.**
- Bianco's pyramid is about the *pain of denial*: blocking a burned IP costs a capable actor little. It says nothing about *detection value*.
- Independent measurements support keeping burned indicators:
  - Feeds list indicators about 21 days after activity starts, and listed hosts often stay active for weeks.
  - Vendor feeds overlap by only 2.5-4% and lag each other by about a month.
  - Expired malicious domains are re-registered and re-weaponised.
- The Cl0p record adds the actor-specific half. Exact IPs burn within a year, but providers and blocks come back across Cl0p's long dormancy gaps (5-18 months), up to three years later.

## 6. Checking the post's claims

| Claim (Woodward, Sept 2026) | Finding | Verdict |
|---|---|---|
| Burned IPs/domains still have value; Pyramid-of-Pain nuance | Supported by measurement studies and by the Cl0p block/provider recurrence above | **Supported** |
| Cl0p has reused Hostzealot "across almost a dozen campaigns and 6 years of data" | HZ appears in 4 of 10 campaigns over Dec 2020-Dec 2024. The campaign series is ~10 campaigns over 6 years. Woodward's own dataset shows HZ in 5 of 8 campaigns (24 flows), the only provider in more than four | **Supported as "the most-reused provider", not as "every campaign"** |
| "In June we saw them use Hostzealot again" (Windchill) | Woodward's dataset shows 2 HZ flows for Windchill, but none of the 7 public PTC / Ransom-ISAC IOC IPs is in HZ space | **Not reproducible from public indicators** |
| "One particular IP ... observed 3 times" | No IP appears in 3 of the 10 campaigns. 92[.]118[.]36[.]213 and .199 (Data Campus, not HZ) reach three only if Truebot (May 2023) counts. HZ's 79[.]141[.]160[.]78 appears twice | **Not reproducible; likely a Data Campus IP with Truebot counted** |
| Sankey attribution of the HZ node to "BG" | HZ's ASNs are registered in Bulgaria, but the servers sit in NL, US, CA and EE | **Correct at registry level; misleading for geolocation** |

*Dataset notes.* Woodward's published Sankey data has three layers: 8 campaigns, 84 ASN labels and country nodes, with no IP-level data. HZ's campaign flows are Accellion 1, GoAnywhere 11, MOVEit 9, Cleo 1 and Windchill 2. 57 of the 84 ASN labels appear in only one campaign.

## 7. Defensive guidance

1. **Do not blanket-block HZ.** It is a commercial host with ordinary customers. Put the Cl0p-used blocks (§2 table) on a **watchlist** with a 24-36-month decay for risk scoring and alerting. Treat new connections from those blocks to internet-facing file-transfer or ERP systems as high-priority alerts.
2. **Retire exact IPs from blocking within about 12 months, but keep them for hunting.**
   - When Cl0p resurfaces (a new MFT zero-day, a leak-site update), re-run the full archived indicator set and its pivots. The pivots are certificates, JARM, nameservers and prefix lineage.
   - Look back at least 30-90 days of logs.
3. **Carry prefix, ASN and provider context on every retained IP.** The recurring signal is at /22-/24 and provider level. See playbook §8.2 for the tiered retention model (block / alert-enrich / hunt), which follows STIX `valid_until`, MISP decaying models and CISA's remove-on-reallocation rule.
4. **Weight small permissive hosts over big clouds.** A hit in HZ, Datahome, Data Campus, Krez 999, Route 95 or ReliableSite space means more than one in AWS or OVH space, where reassignment is fast and collateral damage is high.
5. **Watch the leak site as well as the network.** ShinyHunters' takeover of Cl0p's data-leak site (September 2026) may expose Cl0p hosting choices before the next campaign.

## 8. Gaps and caveats

- **Access limits.** Team Cymru's full text, Kroll's MOVEit list, the original 7 June GoAnywhere list and Fortra's February 2023 customer IOCs could not be retrieved.
- **Current routing is a proxy.** The mapping uses current routing, checked against ownership at the time wherever a source printed it. Only four addresses show real ownership changes, none of them HZ.
- **No rental history.** Without historical BGP or passive DNS, it is unknown whether Cl0p rented HZ space continuously or came back to it.
- **The 2025-2026 lists are small.** Oracle EBS, Gladinet and Windchill published only 0-7 IPs each, so HZ's absence from them is weak evidence of a shift away from HZ.
- **HZ-side facts are unconfirmed.** Its abuse-handling record and its relationships with resellers are undocumented. Its ownership record conflicts between registry aggregators.

## Sources

**Grade A**
- CISA AA23-158A.
- CISA AR21-055A / AA21-055A.
- CISA AA23-187A and AA23-131A.

**Grade B**
- Mandiant (Accellion, 2021).
- Lumen Black Lotus Labs (Accellion target list; DanaBot IOCs).
- Huntress (Cleo, 2024).
- GTIG (Oracle EBS, 2025).
- Kaspersky and BlackBerry (SideWinder, 2024).
- Arctic Wolf (Fog/Akira, 2024).
- Unit 42 (Cl0p torrents, 2023).
- The DFIR Report (2023).
- PRODAFT (LARVA-57).
- For §5: Griffioen et al. (ACNS 2020); Bouwman et al. (USENIX Security 2020); Lever et al. (IEEE S&P 2016); MISP decaying models.

**Grade C**
- Team Cymru, "Cl0p 'Til You Drop" (2026-08-12).
- The Hacker News (PTC Windchill IoCs, June-August 2026).
- maltrail.
- Spamhaus ASN-DROP (2026-09-25).
- ipverse / sapics registry and routing mirrors.

**Grade D**
- Eli Woodward's Cl0p campaign dataset (2026).
- The 2020 Conti/TrickBot leaked chats.

Source IDs are catalogued in [`sources/SOURCE_INDEX.md`](../sources/SOURCE_INDEX.md) (block "Added 2026-09-25").
