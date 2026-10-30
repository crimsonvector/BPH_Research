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
  - data/companies.csv and data/registry_handles.csv (monitor watchlists) are well formed,
    unique and name only existing entities; monitor/acknowledged.csv entries have a
    known check prefix, a reason and an ISO date
  - generated blocks (tools/generate_docs.py) are up to date
  - status is one of the taxonomy's lifecycle/auxiliary states
  - risk_tier starts with T1..T5
  - every Source ID cited in the CSV `sources` column is catalogued in
    sources/SOURCE_INDEX.md, and no Source ID is catalogued twice
  - the SOURCE_INDEX "Source Statistics" grade counts match the catalogue
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


def parse_source_index(text: str):
    """Return ({source_id: grade}, duplicate_ids, {grade: stated_count})."""
    grades, dupes = {}, []
    section_grade = None
    for line in text.splitlines():
        m = re.match(r"^#{2,4} (.*)", line)
        if m:
            g = re.search(r"\(Grade ([A-E])\)", m.group(1))
            section_grade = g.group(1) if g else None
            continue
        if not line.startswith("|"):
            continue
        cells = table_cells(line)
        if not cells or not ID_RE.match(cells[0]) or cells[0] in ("ID",):
            continue
        grade = cells[1] if len(cells) > 1 and re.fullmatch(r"[A-E]", cells[1]) else section_grade
        if cells[0] in grades:
            dupes.append(cells[0])
        grades[cells[0]] = grade
    # grades stated in prose, e.g. **Grades (...):** `X`, `Y` = B; `Z` = C.
    for line in text.splitlines():
        if line.startswith("**Grades"):
            for ids_blob, g in re.findall(r"((?:`[A-Z0-9-]+`[,\s]*)+)=\s*([A-E])", line):
                for sid in re.findall(r"`([A-Z0-9-]+)`", ids_blob):
                    grades[sid] = g
    stated = {}
    stats = text.split("## Source Statistics", 1)
    if len(stats) == 2:
        for line in stats[1].splitlines():
            m = re.match(r"^\|\s*([A-E]) — [^|]*\|\s*(\d+)\s*\|", line)
            if m:
                stated[m.group(1)] = int(m.group(2))
    return grades, dupes, stated


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

    # ---- source index ----
    idx_text = read(os.path.join(root, "sources", "SOURCE_INDEX.md"))
    grades, dupes, stated = parse_source_index(idx_text)
    errors += [f"SOURCE_INDEX: Source ID catalogued twice: {d}" for d in dupes]
    for r in rows:
        for sid in (s.strip() for s in r["sources"].split(";")):
            if sid and sid not in grades:
                errors.append(f"{r['provider_name']}: source {sid} is not in SOURCE_INDEX.md")
    ungraded = [s for s, g in grades.items() if not g]
    errors += [f"SOURCE_INDEX: no grade for {s}" for s in ungraded]
    actual = collections.Counter(g for g in grades.values() if g)
    for g in "ABCDE":
        if stated.get(g) != actual.get(g, 0):
            errors.append(f"SOURCE_INDEX statistics: grade {g} stated {stated.get(g)}, "
                          f"catalogue has {actual.get(g, 0)}")

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
