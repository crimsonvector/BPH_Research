# Registrar & DNS Pilot (Roadmap R1)

> **Date:** 2026-10-30 | **Maintainer:** CrimsonVector Research | **Data:** [`data/domains.csv`](../data/domains.csv)
>
> First look at the domain layer behind the entities this repository tracks: which registrars and DNS providers their domains use, and whether tracked operators concentrate on a small set of them. This pilot uses only domains the repository already holds. It **attributes nothing to any registrar**: a registrar of record is not evidence of enablement, and the candidates listed at the end are for evaluation in R2, not accusations.

---

## Method

1. **Domains.** 66 domains already tied to tracked entities in `BPH_Master.csv` or `data/asns.csv`:

   | Role | Count | Meaning |
   |------|-------|---------|
   | operator-site | 29 | The entity's own storefront or infrastructure domain |
   | spamhaus-attribution | 25 | The `domain` Spamhaus ASN-DROP uses to attribute the entity's ASNs |
   | seized | 5 | Domains taken in law-enforcement actions |
   | front-brand | 3 | Brands operated for the entity (FUNNULL / Triad Nexus) |
   | payment-rail | 2 | Cryptomus and Heleket |
   | associated / lead | 2 | lvcha.in (Asocks); genyus.sc (unattributed Virtualine lead) |

   Removed during curation: forums, CTI vendors, victim brands, mail providers, RIPE LIR identifiers, and domains the repository marks as unrelated (`swissnetwork.io`, `dolphinhost.net`). Subdomains were folded into their registered domain.
2. **Registrar.** RDAP, through IANA's bootstrap file, gave the registrar name and IANA registrar ID, creation and expiry dates and status. WHOIS over port 43 is not reachable from the collection environment.
3. **DNS and hosting.** NS and A records came from Google Public DNS, with the A record's origin ASN from RIPEstat.

## Coverage

| Outcome | Domains |
|---------|---------|
| Registrar resolved | 47 (39 at first pass; the 8 rate-limited lookups resolved on retry by the Phase 2 monitor, 2026-10-30) |
| ccTLD without an RDAP service (.ru, .su, .io, .co, .st, .hk, .lt, .ro, .de) | 17 |
| No longer registered (RDAP 404 at the registry) | 2 (altawk.com, delis.one) |

The ccTLD gap is not random. Russian-market operators use .ru and .su (Proton66, Zservers, 4VPS), and several hosts use .io, .co or .st. Without another data source, the registrar layer for exactly the most relevant operators stays dark.

## Findings

**1. No single "bulletproof registrar" dominates.** NameCheap is registrar of record for 11 of the 47 resolved domains (23%), spread across 10 different entities. That matches its size as one of the largest registrars, so it is a base-rate effect, not a signal of enablement. Repeated use of a large mainstream registrar says little on its own.

**2. Operators cluster on particular registrars.** Clustering inside a single operator is more informative than the totals:

| Operator | Registrar pattern |
|----------|-------------------|
| AnonRDP / Blatant | Infrastructure domains `blatant.host` (registered 2026-09-12) and `ghostynetworks.com` (2026-01-13) both at **NiceNIC International Group** (IANA 3765). The storefront domains `anonrdp.com` and `anonrdp.net` are at Tucows. |
| Feo Prest | Its Spamhaus attribution domain `feoprest.info` (registered 2025-05-20) is also at **NiceNIC** - a second, unrelated operator there |
| Railnet / Virtualine | Seized storefront `virtualine.net` and Spamhaus attribution domain `virtualine.org` both at **CNOBIN Information Technology** (IANA 3254) |
| CTG Server / WAIcore | `ctgserver.com`, `myctgs.com` and `waicore.com` all at Porkbun (IANA 1861) |
| BtHoster / Media Land | `bthoster.com` and Media Land's `sshvps.net` both at **Regtime** (IANA 1362) |
| Russian-market operators | Aeza at REG.RU (1606), Asocks at R01 (1426); sister fronts GCSAS (`globconnex.com`) and GIR (`gir.network`) both at RU-CENTER (463), as is Garantex |
| FUNNULL front brands | `cdn1.ai` and `yunray.ai` both at NameSilo (1479), registered the same day (2025-06-17) |
| Kaopu Cloud HK | `kaopuyun.com` at Bizcn (471), with DNSPod DNS |
| Cryptomus | `cryptomus.com` at Eranet International (1868) |

**3. The DNS and fronting layer is more concentrated than the registrar layer.** 34 of the 66 domains (52%) use Cloudflare nameservers, which also front most of the operators' web addresses. Any work on the domain layer should treat DNS/CDN fronting as its own dimension, separate from registrars.

**4. One tracked host is itself an accredited registrar.** Shinjiru Technology Sdn Bhd, a T4 row here, holds IANA registrar ID 1741 and registers its own domain. The registrar module has to handle entities that are both host and registrar.

**5. Seizures say little about the registrar.** Four of the five seized domains now delegate to seizure nameservers: `anonrdp.com`, `qtproxy.xyz` and `virtualine.net` to the FBI's, `garantex.org` to the US Secret Service's (`usssdomainseizure.com`). Their registrars of record were Tucows, NameCheap, CNOBIN and RU-CENTER. Seizures are typically carried out at the registry (Verisign for .com and .net, PIR for .org), so registrar of record is not evidence of anything.

## Implications for R2 (taxonomy)

- **Evidence floor.** A registrar can be rated only on external abuse evidence: ICANN Contractual Compliance breach notices or terminations, law-enforcement action, self-advertised "bulletproof domains", or sustained abuse share with documented non-response (Interisle, Spamhaus, DNS Abuse Institute). Registrar-of-record links from `data/domains.csv` are context, never evidence on their own.
- **Candidates to evaluate**, selected only by clustering in this pilot. None is attributed:
  - **NiceNIC** (3765): used by both AnonRDP infrastructure domains and by Feo Prest.
  - **CNOBIN** (3254): used by both Virtualine domains.
  - **Regtime** (1362): used by BtHoster and Media Land.
  - **Eranet** (1868) and **Bizcn** (471): used by Cryptomus and Kaopu.
  - NameCheap, Porkbun, Tucows and Cloudflare are large mainstream registrars. Evaluate them only if external abuse data singles them out.
- **Separate dimensions.** Rate registrars, privacy/proxy services and DNS/CDN fronting separately. One entity can be both host and registrar (Shinjiru).
- **Close the ccTLD gap** before drawing conclusions about Russian-market operators. Options include registry web WHOIS for .ru/.su, historical WHOIS or passive DNS datasets, and registrar disclosures in vendor reports.

## Data dictionary (`data/domains.csv`)

| Column | Meaning |
|--------|---------|
| `domain`, `tld` | Registered domain and its TLD |
| `role` | operator-site / spamhaus-attribution / seized / front-brand / payment-rail / associated / lead |
| `entities` | `provider_name`(s) in `BPH_Master.csv` (`;`-separated; a parenthetical marks a lead) |
| `registrar`, `iana_registrar_id` | Registrar of record from RDAP |
| `created`, `expires`, `rdap_status` | RDAP events and status |
| `nameservers`, `dns_provider` | Delegated nameservers and the provider they belong to |
| `a_record_asn`, `a_record_holder` | Origin ASN of the domain's first A record |
| `rdap_server` | RDAP server used, or why no RDAP data was obtained |
| `checked` | Collection date |

## Next steps

1. ~~Retry the eight rate-limited lookups, and add RDAP coverage to the Phase 2 monitor.~~ Done 2026-10-30: `tools/monitor.py --checks domain` re-checks every domain weekly (registration, registrar, status, nameservers including seizure banners) - see `docs/MONITORING.md`.
2. Draft the R2 taxonomy section: provider type "Registrar / DNS Enabler", its subtypes, tier criteria and evidence floor.
3. Evaluate the candidates above against external abuse data before any row is created.
