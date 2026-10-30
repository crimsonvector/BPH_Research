#!/usr/bin/env python3
"""
validate_repo.py — consistency checks across the BPH Research corpus.

BPH_Master.csv is authoritative; several documents restate parts of it by hand and
drift. This script catches that drift before it is committed.

Errors (exit 1):
  - CSV shape: 29 named columns (schema v2), every row the same width, unique provider_name
  - tier_basis starts with the row's tier; last_verified is an ISO date
  - data/asns.csv lists exactly the (ASN, entity) pairs cited in the CSV, uses a known
    block_recommendation, gives each ASN one recommendation, and never recommends
    anything but do-not-block for a historical / reassigned / recycled ASN
  - data/domains.csv names only entities that exist in the CSV, once per domain
  - data/registrars.csv (rated registrar / DNS enablers, taxonomy 2.8): unique IANA IDs, known
    subtype, tier and accreditation values, tier_basis starting with the tier, ISO-dated ICANN
    notices, existing linked entities and catalogued Source IDs
  - data/companies.csv and data/registry_handles.csv (monitor watchlists) are well formed,
    unique and name only existing entities; monitor/acknowledged.csv entries have a
    known check prefix, a reason and an ISO date
  - generated blocks (tools/generate_docs.py) are up to date
  - status is one of the taxonomy's lifecycle/auxiliary states
  - risk_tier starts with T1..T5
  - every Source ID cited in the CSV `sources` column is catalogued in
    sources/sources.csv, once, with a grade, title, publisher, section and well-formed
    URL / retrieved fields (SOURCE_INDEX.md tables and statistics are generated from it)
Warnings: a grade that differs from the publisher default in sources/publishers.csv
  without a grade_note
  - BPH_Master.xlsx mirrors the CSV cell-for-cell (skipped if openpyxl is missing)
  - ECOSYSTEM_MAP Appendix A has one row per CSV entity; Appendix B lists exactly
    the ASNs cited in the CSV
  - TAXONOMY per-tier "— N rows" counts and the README entity count match the CSV

Warnings (exit 0):
  - dashboard_data/providers.json provider count differs from the CSV (the owner's
    daily build refreshes it)
  - CSV rows with an empty `sources` column
  - rows whose last_verified is more than 90 days old

Usage:
  python tools/validate_repo.py [--repo-root DIR]
Exit codes: 0 ok (warnings allowed) · 1 consistency errors · 4 input/setup error
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime as _dt
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

EXPECTED_COLUMNS = [
    "provider_name", "status", "risk_tier", "primary_asn", "additional_asns",
    "known_prefixes", "country_registration", "country_operations",
    "corporate_entity", "aliases", "parent_entity", "upstream_providers",
    "downstream_of", "sanctions_designations", "key_personnel",
    "associated_threat_actors", "associated_malware", "operational_patterns",
    "identification_signals", "first_observed", "last_updated",
    "rf_threat_density_score", "sources", "notes", "description",
    # schema v2 (2026-10-30)
    "geo_cluster", "primary_role", "tier_basis", "last_verified",
]
BLOCK_RECS = {"block", "block-prefixes", "hunt", "monitor", "do-not-block"}
STALE_DAYS = 90
STATUSES = {"active", "flagged", "suspected", "sanctioned", "evading",
            "dissolved", "seized", "exposed", "dormant"}
ID_RE = re.compile(r"^[A-Z0-9][A-Z0-9-]+$")
ASN_RE = re.compile(r"AS(\d+)")


def read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def table_cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def load_source_catalogue(root: str):
    """Return (rows, {source_id: grade}, duplicate_ids) from sources/sources.csv."""
    with open(os.path.join(root, "sources", "sources.csv"), encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    ids = collections.Counter(r["id"] for r in rows)
    return rows, {r["id"]: r["grade"] for r in rows}, [i for i, n in ids.items() if n > 1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=DEFAULT_ROOT)
    root = os.path.abspath(ap.parse_args().repo_root)
    errors: list[str] = []
    warnings: list[str] = []

    csv_path = os.path.join(root, "BPH_Master.csv")
    if not os.path.exists(csv_path):
        sys.stderr.write(f"[ABORT] missing {csv_path}\n")
        return 4
    with open(csv_path, encoding="utf-8", newline="") as f:
        raw = list(csv.reader(f))
    header, body = raw[0], raw[1:]

    # ---- CSV shape and values ----
    if header != EXPECTED_COLUMNS:
        errors.append(f"CSV header differs from the {len(EXPECTED_COLUMNS)}-column schema: {header}")
    for n, r in enumerate(body, start=2):
        if len(r) != len(header):
            errors.append(f"CSV line {n}: {len(r)} fields, expected {len(header)}")
    rows = [dict(zip(header, r)) for r in body]
    names = collections.Counter(r["provider_name"] for r in rows)
    errors += [f"duplicate provider_name: {n}" for n, c in names.items() if c > 1]
    for r in rows:
        if r["status"] not in STATUSES:
            errors.append(f"{r['provider_name']}: unknown status {r['status']!r}")
        if not re.match(r"T[1-5]\b", r["risk_tier"]):
            errors.append(f"{r['provider_name']}: risk_tier {r['risk_tier']!r} is not T1-T5")
        if not r["sources"].strip():
            warnings.append(f"{r['provider_name']}: no sources cited")
        if not r.get("tier_basis", "").startswith(r["risk_tier"][:2]):
            errors.append(f"{r['provider_name']}: tier_basis must start with its tier {r['risk_tier'][:2]}")
        try:
            verified = _dt.date.fromisoformat(r.get("last_verified", ""))
        except ValueError:
            errors.append(f"{r['provider_name']}: last_verified {r.get('last_verified')!r} is not an ISO date")
        else:
            if (_dt.date.today() - verified).days > STALE_DAYS:
                warnings.append(f"{r['provider_name']}: last verified {verified} (> {STALE_DAYS} days)")
    tiers = collections.Counter(r["risk_tier"][:2] for r in rows)

    # ---- source catalogue (sources/sources.csv; SOURCE_INDEX.md tables are generated from it) ----
    catalogue, grades, dupes = load_source_catalogue(root)
    errors += [f"sources.csv: Source ID catalogued twice: {d}" for d in dupes]
    for s in catalogue:
        if not ID_RE.match(s["id"]):
            errors.append(f"sources.csv: malformed Source ID {s['id']!r}")
        if not s["title"].strip() or not s["publisher"].strip() or not s["section"].strip():
            errors.append(f"sources.csv: {s['id']} needs a title, publisher and section")
        for col in ("url", "archive_url"):
            if s[col] and not re.match(r"https?://\S+$", s[col]):
                errors.append(f"sources.csv: {s['id']} {col} {s[col]!r} is not an http(s) URL")
        if s["retrieved"]:
            try:
                _dt.date.fromisoformat(s["retrieved"])
            except ValueError:
                errors.append(f"sources.csv: {s['id']} retrieved {s['retrieved']!r} is not an ISO date")
    for r in rows:
        for sid in (s.strip() for s in r["sources"].split(";")):
            if sid and sid not in grades:
                errors.append(f"{r['provider_name']}: source {sid} is not in sources/sources.csv")
    errors += [f"sources.csv: no valid grade for {s}" for s, g in grades.items() if g not in tuple("ABCDE")]
    try:
        sys.path.insert(0, HERE)
        from generate_docs import grade_deviations, publisher_defaults
        warnings += [f"sources.csv: {s['id']} graded {s['grade']} but {s['publisher']} defaults to {d}; add a grade_note or regrade"
                     for s, d in grade_deviations(catalogue, publisher_defaults(root))]
    except SystemExit as e:
        errors.append(f"publisher defaults could not be read: {e}")

    # ---- xlsx mirror ----
    try:
        import openpyxl  # noqa: F401
    except ImportError:
        warnings.append("openpyxl not installed; BPH_Master.xlsx mirror not checked")
    else:
        import openpyxl
        ws = openpyxl.load_workbook(os.path.join(root, "BPH_Master.xlsx"), read_only=True).active
        xl = [["" if v is None else str(v) for v in row] for row in ws.iter_rows(values_only=True)]
        if xl != raw:
            errors.append(f"BPH_Master.xlsx does not mirror the CSV ({len(xl) - 1} vs "
                          f"{len(body)} data rows) — run tools/build_xlsx.py")

    # ---- ecosystem map appendices ----
    eco = read(os.path.join(root, "analysis", "ECOSYSTEM_MAP.md"))
    app_a = eco.split("## Appendix A", 1)[-1].split("## Appendix B", 1)[0]
    a_rows = [l for l in app_a.splitlines()
              if l.startswith("| ") and not l.startswith("| Entity") and "---" not in l]
    if len(a_rows) != len(rows):
        errors.append(f"ECOSYSTEM_MAP Appendix A has {len(a_rows)} rows, CSV has {len(rows)}")
    app_b = eco.split("## Appendix B", 1)[-1]
    b_asns = {m for l in app_b.splitlines() if l.startswith("| AS")
              for m in ASN_RE.findall(table_cells(l)[0])}
    csv_asns = {m for r in rows for m in ASN_RE.findall(r["primary_asn"] + " " + r["additional_asns"])}
    if b_asns != csv_asns:
        errors.append("ECOSYSTEM_MAP Appendix B ASNs differ from CSV: missing "
                      f"{sorted(csv_asns - b_asns, key=int)}, extra {sorted(b_asns - csv_asns, key=int)}")

    # ---- ASN register ----
    asn_path = os.path.join(root, "data", "asns.csv")
    if not os.path.exists(asn_path):
        errors.append("data/asns.csv is missing")
    else:
        with open(asn_path, encoding="utf-8", newline="") as f:
            reg = list(csv.DictReader(f))
        csv_pairs = {(f"AS{m}", r["provider_name"]) for r in rows
                     for m in ASN_RE.findall(r["primary_asn"] + " " + r["additional_asns"])}
        reg_pairs = {(a["asn"], a["provider_name"]) for a in reg}
        for asn, name in sorted(csv_pairs - reg_pairs):
            errors.append(f"data/asns.csv: missing {asn} for {name}")
        for asn, name in sorted(reg_pairs - csv_pairs):
            errors.append(f"data/asns.csv: {asn} for {name} is not in the CSV")
        recs = collections.defaultdict(set)
        for a in reg:
            rec = a["block_recommendation"]
            recs[a["asn"]].add(rec)
            if rec not in BLOCK_RECS:
                errors.append(f"data/asns.csv: {a['asn']} has unknown block_recommendation {rec!r}")
            q = a["qualifier"].lower()
            if any(k in q for k in ("historical", "reassigned", "re-registered", "recycled")) and rec != "do-not-block":
                errors.append(f"data/asns.csv: {a['asn']} ({a['provider_name']}) is historical/reassigned but "
                              f"recommended {rec!r} - must be do-not-block")
        for asn, rs in recs.items():
            if len(rs) > 1:
                errors.append(f"data/asns.csv: {asn} has conflicting recommendations {sorted(rs)}")

    # ---- domain register (registrar pilot) ----
    dom_path = os.path.join(root, "data", "domains.csv")
    if os.path.exists(dom_path):
        names = {r["provider_name"] for r in rows}
        with open(dom_path, encoding="utf-8", newline="") as f:
            doms = list(csv.DictReader(f))
        seen = collections.Counter(d["domain"] for d in doms)
        errors += [f"data/domains.csv: {d} listed {n} times" for d, n in seen.items() if n > 1]
        for d in doms:
            for ent in (re.sub(r"\s*\(lead:[^)]*\)$", "", e).strip() for e in d["entities"].split(";")):
                if ent and ent not in names:
                    errors.append(f"data/domains.csv: {d['domain']} names unknown entity {ent!r}")

    # ---- monitor watchlists (Phase 2) ----
    names = {r["provider_name"] for r in rows}

    def load_opt(*parts):
        path = os.path.join(root, *parts)
        if not os.path.exists(path):
            return None
        with open(path, encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))

    def iso(value):
        try:
            return _dt.date.fromisoformat(value)
        except ValueError:
            return None

    cos = load_opt("data", "companies.csv")
    if cos is not None:
        seen = collections.Counter(c["company_number"] for c in cos)
        errors += [f"data/companies.csv: {n} listed {k} times" for n, k in seen.items() if k > 1]
        for c in cos:
            n = c["company_number"]
            if not re.fullmatch(r"\d{8}|[A-Z]{2}\d{6}", n):
                errors.append(f"data/companies.csv: {n!r} is not a Companies House number")
            if c["link"] not in ("registered-entity", "name-match"):
                errors.append(f"data/companies.csv: {n} link {c['link']!r} (expected registered-entity / name-match)")
            if not re.fullmatch(r"[a-z]+(-[a-z]+)*", c["recorded_status"]):
                errors.append(f"data/companies.csv: {n} recorded_status {c['recorded_status']!r} is not a Companies House status slug")
            if not iso(c["last_filing_date"]) or not iso(c["checked"]):
                errors.append(f"data/companies.csv: {n} has a non-ISO date")
            errors += [f"data/companies.csv: {n} names unknown entity {e!r}" for e in (x.strip() for x in c["entities"].split(";")) if e not in names]

    hs = load_opt("data", "registry_handles.csv")
    if hs is not None:
        seen = collections.Counter(h["handle"].upper() for h in hs)
        errors += [f"data/registry_handles.csv: {h} listed {k} times" for h, k in seen.items() if k > 1]
        for h in hs:
            if h["kind"] not in ("mntner", "organisation") or h["registry"] != "RIPE":
                errors.append(f"data/registry_handles.csv: {h['handle']} has kind/registry {h['kind']}/{h['registry']} (expected mntner|organisation / RIPE)")
            errors += [f"data/registry_handles.csv: {h['handle']} names unknown entity {e!r}" for e in (x.strip() for x in h["entities"].split(";")) if e not in names]

    regs = load_opt("data", "registrars.csv")
    if regs is not None:
        seen = collections.Counter(g["iana_id"] for g in regs)
        errors += [f"data/registrars.csv: IANA {i} listed {k} times" for i, k in seen.items() if k > 1]
        for g in regs:
            who = f"data/registrars.csv: {g['registrar']} ({g['iana_id']})"
            if g["subtype"] not in ("registrar", "reseller", "privacy-proxy", "cctld", "dns-fronting"):
                errors.append(f"{who}: unknown subtype {g['subtype']!r}")
            if g["subtype"] == "registrar" and not g["iana_id"].isdigit():
                errors.append(f"{who}: an accredited registrar needs a numeric IANA ID")
            if g["accreditation"] not in ("Accredited", "Terminated", "Reserved", "n/a"):
                errors.append(f"{who}: accreditation {g['accreditation']!r} (expected IANA status or n/a)")
            if not re.fullmatch(r"T[1-5]", g["tier"]) or not g["tier_basis"].startswith(g["tier"]):
                errors.append(f"{who}: tier {g['tier']!r} missing or tier_basis does not start with it")
            for n in (x.strip() for x in g["icann_notices"].split(";") if x.strip()):
                d, _, kind = n.partition(" ")
                if not iso(d) or kind not in ("breach", "suspension", "termination", "non-renewal"):
                    errors.append(f"{who}: ICANN notice {n!r} is not 'YYYY-MM-DD kind'")
            errors += [f"{who}: linked entity {e!r} is not in the CSV" for e in (x.strip() for x in g["linked_entities"].split(";")) if e and e not in names]
            errors += [f"{who}: source {s} is not in sources/sources.csv" for s in (x.strip() for x in g["sources"].split(";")) if s and s not in grades]
            if not iso(g["last_verified"]):
                errors.append(f"{who}: last_verified is not an ISO date")

    acks = load_opt("monitor", "acknowledged.csv")
    if acks is not None:
        checks = ("asn", "drop", "prefix", "withdrawn", "asndrop", "ripe", "domain", "company")
        seen = collections.Counter((a["key"], a["observed"]) for a in acks)
        errors += [f"monitor/acknowledged.csv: {k} acknowledged {n} times" for (k, _), n in seen.items() if n > 1]
        for a in acks:
            if a["key"].split(":", 1)[0] not in checks:
                errors.append(f"monitor/acknowledged.csv: {a['key']!r} does not start with a monitor check name")
            if not a["reason"].strip():
                errors.append(f"monitor/acknowledged.csv: {a['key']} has no reason")
            when = iso(a["date"])
            if not when:
                errors.append(f"monitor/acknowledged.csv: {a['key']} date {a['date']!r} is not ISO")
            elif not a["observed"] and (_dt.date.today() - when).days > 2 * STALE_DAYS:
                warnings.append(f"monitor/acknowledged.csv: {a['key']} acknowledged without an observed value on {when}; re-review")

    # ---- generated blocks ----
    try:
        sys.path.insert(0, HERE)
        from generate_docs import stale_files
        errors += [f"{path} is stale - run tools/generate_docs.py" for path in stale_files(root)]
    except SystemExit as e:  # missing markers or inputs
        errors.append(f"generate_docs could not run: {e}")

    # ---- taxonomy + README counts ----
    tax = read(os.path.join(root, "taxonomy", "BPH_TAXONOMY.md"))
    for t, n in re.findall(r"\*\*Current (T[1-5]) entities[^*]*?— (\d+) rows\)", tax):
        if int(n) != tiers.get(t, 0):
            errors.append(f"TAXONOMY says {n} {t} rows, CSV has {tiers.get(t, 0)}")
    readme = read(os.path.join(root, "README.md"))
    m = re.search(r"\*\*Current scope:\*\* (\d+) providers/entities", readme)
    if m and int(m.group(1)) != len(rows):
        errors.append(f"README scope says {m.group(1)} entities, CSV has {len(rows)}")

    # ---- public dashboard (owner's daily build refreshes it) ----
    prov = os.path.join(root, "dashboard_data", "providers.json")
    if os.path.exists(prov):
        with open(prov, encoding="utf-8") as f:
            n = len(json.load(f))
        if n != len(rows):
            warnings.append(f"dashboard_data/providers.json has {n} providers, CSV has "
                            f"{len(rows)} — re-run tools/build_dashboard_data.py")

    for w in warnings:
        print(f"[warn] {w}")
    for e in errors:
        print(f"[error] {e}")
    print(f"[{'FAIL' if errors else 'ok'}] {len(rows)} entities, {len(grades)} sources, "
          f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
