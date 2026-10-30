# Exports (Roadmap Phase 4)

> **Since:** 2026-10-30 | **Built by:** [`tools/build_exports.py`](../tools/build_exports.py) | **Output:** [`exports/`](../exports/)
>
> Machine-readable versions of this repository's blocking guidance and entity data, for firewalls, SIEMs, threat-intelligence platforms and MISP.

Everything is generated from the committed data (`data/asns.csv`, `BPH_Master.csv` `known_prefixes`, `data/relationships.csv`, `sources/sources.csv`). CI fails if `exports/` is out of date, so the files always match the data in the same commit.

## Files

| File | Format | Contents |
|------|--------|----------|
| `exports/blocklists/asn-block.txt` | one ASN per line, `#` comments | ASNs recommended `block` |
| `exports/blocklists/cidr-block.txt` | one CIDR per line, `#` comments | Curated prefixes recommended for blocking |
| `exports/blocklists/blocklist.csv` | CSV | Both lists, with entity, tier, recommendation, basis, `as_of` and `valid_until` |
| `exports/stix/bph-bundle.json` | STIX 2.1 bundle | Entities, their networks, indicators for every blocklist entry, and typed relationships |
| `exports/misp/` | MISP feed | `manifest.json`, `hashes.csv`, and one event per entity |

**Raw URLs for automation:** `https://raw.githubusercontent.com/crimsonvector/BPH_Research/main/exports/...`

## What goes into a blocklist

| Recommendation (`data/asns.csv`) | ASN list | CIDR list | STIX indicator | MISP `to_ids` |
|---|---|---|---|---|
| `block` | yes | the entity's curated prefixes | yes | true |
| `block-prefixes` | no | the entity's curated prefixes | for the prefixes | true for the prefixes |
| `hunt`, `monitor` | no | no | no (context only) | false |
| `do-not-block` | **never exported** | never | never | never |

A **curated prefix** is one listed in the entity's `known_prefixes`. It is exported only if all of these hold:
- the entity has a **live** ASN recommended `block` or `block-prefixes`;
- the record does not mark the prefix historical, not announced, "former", moved or re-originated, or "re-check before blocking".

Prefixes that left an operator's network (successor candidates such as the former Altawk, MIRhosting or WorkTitans ranges) are therefore not attributed to anyone in the exports.

The weekly monitor ([`MONITORING.md`](MONITORING.md)) re-checks every listed prefix and opens a finding when one moves. That keeps these notes current.

## Freshness

Every export carries the date the data was last checked (`as_of`, the newest `last_checked` in `data/asns.csv`):
- Indicators are valid from `as_of` until **`as_of` + 30 days**: STIX `valid_until`, `valid_until` in `blocklist.csv`, and the header of each text list.
- If the repository stops being refreshed, consumers get expired indicators rather than silently ageing ones. Re-pull after each monitor-driven update.
- MISP attributes carry the timestamp of their check date, so MISP's decaying models score them by age.

## STIX 2.1 details

| Object | For |
|---|---|
| `identity` (organization) | every tracked entity and every external party in a relationship. Tracked entities carry `x_bph_risk_tier`, `x_bph_status`, `x_bph_tier_basis`, `x_bph_primary_role` and `x_bph_geo_cluster`, declared through a `toplevel-property-extension` (`extension-definition`), plus `external_references` to their sources with URLs. |
| `infrastructure` | each entity's network (`hosting-malware`, or `anonymization` for proxy enablers). It links to its identity with `related-to` ("operates") and to its `autonomous-system` and `ipv4-addr` / `ipv6-addr` objects with `consists-of`. |
| `indicator` | each blocklist entry: `[autonomous-system:number = N]` or `[ipv4-addr:value ISSUBSET 'cidr']`. Each `indicates` the entity's infrastructure, with confidence by tier (T1 85, T2 70, T3 50). |
| `relationship` | each row of `data/relationships.csv` except superseded ones. Types are the repository's vocabulary (`operator-of`, `front-of`, `successor-of`, `upstream-of`, `ip-supplier-of`, `payment-rail-of`, `sister-of`, `associated-with`). Confidence: verified 80, unverified 30, disputed 15. |

**Markings:** everything is marked TLP:CLEAR (the predefined TLP:WHITE marking) and created by the "CrimsonVector Research" identity.

CI validates the bundle with the OASIS `stix2-validator` (3.2.0). It is valid, with three expected warning classes:
- **{103} UUIDv5 IDs.** IDs are UUIDv5, derived from the data rather than random UUIDv4, so the same entity keeps the same ID across builds and consumers can deduplicate. SCO IDs follow the spec's deterministic-ID rule.
- **{202} Custom relationship types.** The relationship types are the repository's own.
- **{302} References without a hash.** External references point to web pages and carry no file hash.

## MISP feed

To subscribe in MISP:
1. Go to *Sync Actions → Feeds → Add Feed*.
2. Set the source format to *MISP Feed*.
3. Set the URL to `https://raw.githubusercontent.com/crimsonvector/BPH_Research/main/exports/misp`.

Feed contents:

| Element | Details |
|---|---|
| Events | One per entity that has exportable network data. `info` names the entity and tier; `threat_level_id` follows the tier (T1 high … T4/T5 undefined). |
| Event tags | `tlp:clear`, `bph-research:tier="Tn"`, `bph-research:status="…"` |
| Attributes | `AS` (every non-historical ASN) and `ip-dst` (curated prefixes) |
| Attribute tags | `bph-research:block-recommendation="…"` |
| `to_ids` | true only for the block items in the table above |

UUIDs are stable across builds. `hashes.csv` lists the MD5 of each attribute value with its event UUID, for MISP's feed caching.

## Rebuilding

```bash
python tools/build_exports.py          # after any change to the data
python tools/build_exports.py --check  # what CI runs
python -m unittest tests.test_exports  # safety tests
```

**What the safety tests prove:**
- no `do-not-block` ASN becomes an ASN object, indicator, MISP attribute or blocklist line;
- only `block` ASNs are blocking;
- moved, historical and unannounced prefixes stay out;
- every STIX reference resolves;
- the MISP manifest and hashes match the events;
- two builds are identical.

A mutation test (letting `do-not-block` rows through) makes them fail.

## Caveats

- **Guidance, not a verdict.** Review `blocklist.csv` before enforcing it. An ASN-level block of a `block` network also stops any legitimate customers it has.
- **Upstream carriers are never in the lists.** Carriers and dual-use providers are `monitor`, never `block`. Block the downstream networks instead.
- **Use Spamhaus DROP as well.** Spamhaus DROP / ASN-DROP should be consumed directly. Most `block` ASNs here are on ASN-DROP; the value added is the entity context, the curated prefixes and the relationships.
