# Monitoring (Roadmap Phase 2)

> **Since:** 2026-10-30 | **Tool:** [`tools/monitor.py`](../tools/monitor.py) | **Schedule:** [`.github/workflows/monitor.yml`](../.github/workflows/monitor.yml), Mondays 05:17 UTC
>
> The monitor checks the outside world against what this repository records and reports every difference as a finding. It never edits the data: an analyst decides what each finding means.

---

## How it works

The **baseline is the repository itself**. Each check fetches live state from public sources and compares it with the recorded value in the data files. A finding stays open until one of two things happens:

1. **The data is updated** to match. For example, record the new routing state in `data/asns.csv`, or name the new origin ASN in `known_prefixes`. Then run `tools/generate_docs.py`. The next run finds no difference.
2. **The finding is acknowledged** in [`monitor/acknowledged.csv`](../monitor/acknowledged.csv), with a reason. Use this for differences that are real but not worth recording, such as one-off IP-lease churn.

There is no hidden state between runs, so the issue always shows exactly what the data has not caught up with. Raw observations are kept as a workflow artifact for 90 days (`snapshot-<date>.json`).

## Checks

| Check | Compares | Against | Severity |
|-------|----------|---------|----------|
| `asn` | Holder, routing state (live / dark / unregistered / reassigned), IPv4 prefix count, ASN-DROP listing | `data/asns.csv` | high: deregistration, re-registration, dark→live, newly on ASN-DROP · medium: live→dark, holder change, delisting · low: prefix count change of ≥25% (min. 3); any change on a `do-not-block` ASN |
| `drop` | Spamhaus DROP prefixes announced by ASNs recommended `hunt`, `monitor` or `do-not-block` (upstream carriers excluded) | `data/asns.csv` | medium |
| `prefix` | Origin and announcement of every prefix in `known_prefixes`. ASNs named in that text count as recorded. Prefixes after a "Historical …:" lead-in, or marked historical in their own note, are skipped. While the entity's own ASNs still announce a prefix or part of it, other origins inside it count as sub-lets | `BPH_Master.csv` | medium: new origin; re-announced although noted "not announced" · low: no longer announced |
| `withdrawn` | Prefixes a tracked operator ASN (T1–T3, not historical, not a carrier) stopped announcing in the lookback window (default 90 days, max. 40 per ASN), grouped by the ASN that now originates them | announced-prefix history | medium: moved to another tracked entity, or ≥3 prefixes to one new origin · low: otherwise |
| `asndrop` | ASN-DROP entries whose Spamhaus `domain` is one a tracked operator uses, but whose ASN the repo does not track | `data/asns.csv`, `data/domains.csv` | high |
| `ripe` | aut-num and route/route6 objects created or changed in the lookback window that are maintained by (`mnt-by`) or registered to (`org`) a tracked RIPE handle, and point at an untracked ASN; route objects grouped per origin | `data/registry_handles.csv` | medium |
| `domain` | Registration (RDAP 404 / re-registration), registrar (IANA ID), RDAP status, nameservers (seizure banners flagged), A-record ASN (skipped for CDN-fronted domains) | `data/domains.csv` | high: seized, dropped, re-registered, hold status · medium: registrar change · low: other status, nameserver and hosting changes; a lookup that now answers |
| `company` | Company status and filings dated after the recorded latest filing | `data/companies.csv` | high: status change · medium: new filing · low: accounts |

Every finding has a stable **key**, `check:subject:aspect`, for example `asn:AS209946:state`, `prefix:AS6461:origin:railnet-llc-virtualine-technologies`, `company:14459750:filing:2026-10-14:CS01`. The issue embeds the keys of the previous run, so each run marks its **new** findings and posts them as a comment.

## Acknowledging a finding

`monitor/acknowledged.csv` columns: `key`, `observed`, `reason`, `date`.

- **`observed` set** (recommended): copy it from `findings.json`. The finding stays suppressed only while the live value is unchanged. If more prefixes move or the status changes again, it re-opens.
- **`observed` empty**: suppresses the key whatever the value. The validator warns after 180 days.

The validator rejects acknowledgements without a reason, with a non-ISO date, or with a key that does not start with a check name.

## Watchlists

| File | Holds | Selection rules |
|------|-------|-----------------|
| [`data/companies.csv`](../data/companies.csv) | UK companies the repo cites: number, registered name, entities, `link` (`registered-entity` or `name-match`), recorded status slug, latest filing accounted for | Every Companies House number in the CSV, plus exact-name matches for UK-registered rows (VPSVAULT.HOST LTD). Status slugs follow Companies House (`active`, `active-proposal-to-strike-off`, `dissolved`, …). |
| [`data/registry_handles.csv`](../data/registry_handles.csv) | RIPE maintainers and organisations behind tracked networks | The `mnt-by` and `org` of every aut-num in `data/asns.csv` for T1–T3 entities, excluding `do-not-block` ASNs, upstream carriers, `RIPE-NCC-END-MNT`, a maintainer named after a private individual, and six LIR-service maintainers that also maintain many unrelated customers (`LocalNCC-mnt`, `SBMT`, `NETWORK-SUPPORT-MNT`, `ru-avm-1-mnt`, `MNT-PIN`, `MNT-PINSUPPORT`). Two maintainers named after operators were added by hand (`GHOSTYNETWORKS-MNT`, `VIRTUALINE-MNT`). |

## Running it

```bash
python tools/monitor.py                       # all checks, writes monitor-out/
python tools/monitor.py --checks asn,prefix   # a subset
python tools/monitor.py --previous old.md     # mark findings not in an earlier report as new
python -m unittest discover -s tests          # offline tests (also run in CI)
```

Outputs:
- `report.md`: the issue body. IPv4 addresses are defanged.
- `new.md`: new findings only.
- `findings.json`: open and acknowledged findings, plus fetch errors.
- `snapshot-<date>.json`: raw observations.

A full run takes about 10 minutes. Fetch errors never become findings. They are listed in a collapsed section of the report, and `--strict` turns them into exit code 2.

**Workflow.** The weekly run opens a single issue titled "Monitor findings" (label `monitor`), or updates it if one is already open, and comments with the new findings. A manual run with a subset of checks only uploads the artifact.

**Companies House key.** Without one, the monitor reads the public Companies House website at one request per second. If the `COMPANIES_HOUSE_API_KEY` repository secret is set (a free key from the Companies House developer hub), it uses the REST API instead.

**Scheduled runs pause.** GitHub pauses scheduled workflows in public repositories after 60 days without repository activity.

## Privacy and politeness

- **No private individuals are named.**
  - Registry holder and AS names are shown only when they look like an organisation; otherwise "[name withheld]".
  - Holders the register already redacts are never compared.
  - Officer and person-with-significant-control filings appear as generic labels ("Officer details changed").
  - Honorific-plus-name patterns are redacted from all other filing descriptions.
- **Honest, identifying User-Agent.** Requests use `BPH_Research-monitor/1.0`. RIPEstat calls carry `sourceapp=bph-research-monitor`, and at most 5 run in parallel.
- **Per-host spacing.** RIPE DB requests are spaced 0.3 s apart and Companies House requests 1 s apart.
- **No bot-check workarounds.** A source that refuses (HTTP 403/429) is retried later as a fetch error.

## Validation: the October 2026 replay

Roadmap Phase 2 was "done when" the changes the October 2026 audit found by hand would each have produced a finding.

- **Live replay.** A copy of the data was rolled back to its 2026-09-25 state, and the monitor was run against live sources on 2026-10-30.
- **Offline replay.** The same cases are encoded in the offline tests, `tests/test_monitor.py`, class `OctoberReplay`.

| October 2026 change | Finding produced (live replay) |
|---------------------|--------------------------------|
| Altawk AS209946 went dark | `asn:AS209946:state` - recorded live, now dark |
| MIRhosting AS52000 and AS206932 went dark | `asn:AS52000:state`, `asn:AS206932:state` |
| WorkTitans withdrew its ranges | `asn:AS209847:prefix-count` - recorded 14, now 2 |
| GCSAS added to ASN-DROP | `asn:AS215540:asndrop` - now listed (globconnex.com) |
| RetryHost block 94.26.38.0/24 re-originated by AS51130 | `prefix:AS51130:origin:…` |
| Strike-off notices of 2026-10-13 (Femo IT, First Server, WAICORE LTD, Tiger Network) | a status and a `GAZ1` filing finding for each of the four companies |

## First run (2026-10-30)

Before tuning, the first runs on 2026-10-30 raised 332 findings. Most came from two sources:
- **Per-prefix withdrawn rows (89).** These are now grouped by new origin.
- **RIPE objects (216).** Most were maintained by six LIR-service maintainers, which are now excluded.

After tuning and the data updates below, 30 findings remained.

Changes recorded in the data (all registry facts, no tier changes):

| Finding | Recorded as |
|---------|-------------|
| AS203319 (GIR-AS-1) on ASN-DROP under `gir.network`, untracked | Added to GIR as an additional ASN (dark; `block`, pre-emptive) |
| Former AS202412 prefixes originated by AS6461 (Zayo Bandwidth) from 2026-10-27 16:00 UTC, the hour AS202412 went dark after the seizure | Railnet / Virtualine `known_prefixes` and notes. The reason is not public. |
| FIRST-SERVER-MNT route objects for AS197703 "FIRST-SERVER-AE" (IP MARKET - FZCO, UAE) | Added to First Server as an additional ASN (`block-prefixes`) |
| PINSPB organisation holds AS45054 "Metrobit-AS" | Added to PINSPB (dark; `monitor`) |
| Prefixes of dark or shrinking operator ASNs now originated elsewhere: MIRhosting → AS48729 (ServerKing, 9 prefixes); Altawk → AS218688 (WULDI LLC, registered 2026-09-11, all 5 prefixes); WorkTitans → AS51722 (PIXOOF, under route objects WorkTitans' own maintainer created); Kaopu → AS63139 (BEDGE, 6); PINSPB and First Server → IHOR HOSTING LTD (AS209641, AS207569) | Each source entity's `known_prefixes` and notes. These are successor candidates and are not attributed. |
| Route objects created by Tiger's, Chang Way's and AnonRDP's maintainers for other ASNs | Entity notes |
| Shinjiru: 37 announced IPv4 prefixes with 20 Spamhaus DROP entries inside them (16 and 5 at the September audit) | Shinjiru notes. **T4 tier review recommended.** |
| FIRST SERVER LIMITED filed a confirmation statement on 2026-10-14, the day after its Gazette notice | First Server notes; `data/companies.csv` baseline |
| VPSVAULT.HOST LTD (SC832751): strike-off notices 2025-12-23 (discontinued) and 2026-08-25 | VPSVault notes; added to the company watchlist |
| The 8 rate-limited RDAP lookups of the registrar pilot answered; `garantex.org` delegates to US Secret Service seizure nameservers | `data/domains.csv`, `analysis/REGISTRAR_PILOT.md` |

Of the 30 that remained, a rule change resolved one: other ASNs' /48s inside HostZealot's IPv6 /32 no longer count while HostZealot's own ASNs still announce part of it (sub-letting). The other 29 are acknowledged in `monitor/acknowledged.csv` with reasons:
- single-prefix IP-lease churn;
- moves into ASNs of other tracked entities, such as four entities' prefixes moving to Aeza's AS203273;
- a MIRhosting LIR customer;
- the route-object groups recorded in notes.

## Limits

- **RIPE region only.** Handles are watched in the RIPE database only. ARIN and APNIC operators (AnonRDP's AS403005, FUNNULL, Kaopu) are covered through routing and ASN-DROP, not through registry objects.
- **No RDAP for 17 domains.** These are ccTLD domains without an RDAP service (including .ru and .su), so only their nameservers and hosting are checked.
- **Routing view.** Routing data comes from RIPE RIS. Announced-prefix history ignores prefixes seen by fewer than 10 RIS peers, so very low-visibility announcements can be missed.
- **No listing dates.** ASN-DROP and DROP carry no dates, so a listing is reported when the monitor first sees it, not when Spamhaus added it.
- **Detection, not judgement.** A finding is not attribution. Prefixes moving to a new origin are often ordinary IP-lease churn, and only an analyst can decide that a new ASN is a successor.
