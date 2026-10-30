#!/usr/bin/env python3
"""
generate_docs.py — rebuild the derived tables and counts from the repository data.

BPH_Master.csv, data/asns.csv and sources/SOURCE_INDEX.md are the sources of truth.
This script regenerates everything that restates them, so those copies never need
hand edits:

  - analysis/ECOSYSTEM_MAP.md  Appendix A (entity quick reference) and Appendix B
                               (ASN cross-reference with block recommendations),
                               between <!-- generated:appendix-a/b:start/end --> markers
  - taxonomy/BPH_TAXONOMY.md   the "— N rows" count in each "Current Tn entities" line
  - README.md                  the "Current scope: N providers/entities" count
  - sources/SOURCE_INDEX.md    the Source Statistics table, between
                               <!-- generated:source-stats:start/end --> markers

Usage:
  python tools/generate_docs.py           # rewrite stale blocks in place
  python tools/generate_docs.py --check   # exit 1 if any block is stale (CI)
Exit codes: 0 ok · 1 stale (with --check) · 4 input/setup error
"""
from __future__ import annotations

import argparse
import collections
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

IPV4 = re.compile(r"\b(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\b")
GRADES = [
    ("A", "Government/Official", "Sanctions notices, LE press releases, court filings, company registers, government advisories"),
    ("B", "Established CTI Vendor", "Published research from recognized threat intelligence firms"),
    ("C", "Community/Independent", "Independent researchers, community blocklists and registry mirrors, investigative journalism"),
    ("D", "Single Source / Unverified", "Reputation/review platforms, single-analyst datasets, leaked chats, and first-party findings"),
    ("E", "Self-Reported / Marketing", "Forum advertising presence and provider marketing"),
]


def read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def defang(text: str) -> str:
    """Defang IPv4 addresses, matching the convention used in the analysis documents."""
    return IPV4.sub(lambda m: "[.]".join(m.groups()), text)


def cell(text: str) -> str:
    return defang(text.replace("|", "/").strip())


def load_csv(path: str) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def replace_block(text: str, name: str, body: str) -> str:
    start, end = f"<!-- generated:{name}:start -->", f"<!-- generated:{name}:end -->"
    i, j = text.find(start), text.find(end)
    if i < 0 or j < 0 or j < i:
        raise SystemExit(f"[ABORT] markers for '{name}' not found")
    return text[: i + len(start)] + "\n" + body + "\n" + text[j:]


def appendix_a(rows: list[dict]) -> str:
    out = [
        f"> Generated from `BPH_Master.csv` ({len(rows)} rows) by `tools/generate_docs.py` - do not edit by hand. "
        "The CSV is authoritative.",
        "",
        "| Entity | ASN(s) | Tier | Status | Geographic Cluster | Primary Role |",
        "|--------|--------|------|--------|--------------------|--------------|",
    ]
    for r in sorted(rows, key=lambda r: r["provider_name"].lower()):
        asns = "; ".join(p for p in (r["primary_asn"], r["additional_asns"]) if p.strip()) or "—"
        out.append("| " + " | ".join([
            cell(r["provider_name"]), cell(asns), r["risk_tier"][:2], r["status"].capitalize(),
            cell(r["geo_cluster"]), cell(r["primary_role"]),
        ]) + " |")
    return "\n".join(out)


def appendix_b(rows: list[dict], asns: list[dict]) -> str:
    by_name = {r["provider_name"]: r for r in rows}
    checked = max((a["last_checked"] for a in asns if a["last_checked"]), default="")
    out = [
        "> Every ASN attributed to a tracked entity, generated from `data/asns.csv` by `tools/generate_docs.py` - do not "
        "edit by hand. **Block** gives the structured recommendation (`block`, `block-prefixes`, `hunt`, `monitor`, "
        "`do-not-block`); ASNs marked `do-not-block` now belong to unrelated organisations or are deregistered - never "
        f"block them as the listed entity. Routing and Spamhaus state last checked {checked}.",
        "",
        "| ASN | Entity | Tier | Block | Notes |",
        "|-----|--------|------|-------|-------|",
    ]
    for a in sorted(asns, key=lambda a: (int(a["asn"][2:]), a["provider_name"].lower())):
        r = by_name[a["provider_name"]]
        note = a["qualifier"] or "; ".join(x for x in (r["primary_role"], r["geo_cluster"]) if x)
        out.append("| " + " | ".join([
            a["asn"], cell(a["provider_name"]), r["risk_tier"][:2], a["block_recommendation"], cell(note),
        ]) + " |")
    return "\n".join(out)


def source_stats(index_text: str) -> str:
    sys.path.insert(0, HERE)
    from validate_repo import parse_source_index  # shared parser; imported lazily to avoid a cycle
    grades, _, _ = parse_source_index(index_text)
    counts = collections.Counter(g for g in grades.values() if g)
    out = ["| Grade | Count | Description |", "|-------|-------|-------------|"]
    for g, label, desc in GRADES:
        out.append(f"| {g} — {label} | {counts.get(g, 0)} | {desc} |")
    out.append(f"| **Total** | **{sum(counts.values())}** | |")
    return "\n".join(out)


def tier_counts(text: str, rows: list[dict]) -> str:
    tiers = collections.Counter(r["risk_tier"][:2] for r in rows)
    return re.sub(
        r"(\*\*Current (T[1-5]) entities[^*]*?— )(\d+)( rows\))",
        lambda m: f"{m.group(1)}{tiers.get(m.group(2), 0)}{m.group(4)}",
        text,
    )


def scope_count(text: str, rows: list[dict]) -> str:
    return re.sub(r"(\*\*Current scope:\*\* )\d+( providers/entities)", rf"\g<1>{len(rows)}\2", text)


def build(root: str) -> dict[str, tuple[str, str]]:
    """Return {path: (current_text, regenerated_text)} for every generated file."""
    p = lambda *x: os.path.join(root, *x)
    for need in (p("BPH_Master.csv"), p("data", "asns.csv")):
        if not os.path.exists(need):
            sys.stderr.write(f"[ABORT] missing {need}\n")
            sys.exit(4)
    rows = load_csv(p("BPH_Master.csv"))
    asns = load_csv(p("data", "asns.csv"))
    files = {}
    eco = read(p("analysis", "ECOSYSTEM_MAP.md"))
    new = replace_block(eco, "appendix-a", appendix_a(rows))
    new = replace_block(new, "appendix-b", appendix_b(rows, asns))
    files[p("analysis", "ECOSYSTEM_MAP.md")] = (eco, new)
    tax = read(p("taxonomy", "BPH_TAXONOMY.md"))
    files[p("taxonomy", "BPH_TAXONOMY.md")] = (tax, tier_counts(tax, rows))
    readme = read(p("README.md"))
    files[p("README.md")] = (readme, scope_count(readme, rows))
    idx = read(p("sources", "SOURCE_INDEX.md"))
    files[p("sources", "SOURCE_INDEX.md")] = (idx, replace_block(idx, "source-stats", source_stats(idx)))
    return files


def stale_files(root: str) -> list[str]:
    return [os.path.relpath(path, root) for path, (cur, new) in build(root).items() if cur != new]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=DEFAULT_ROOT)
    ap.add_argument("--check", action="store_true", help="report stale files and exit 1 instead of writing")
    args = ap.parse_args()
    root = os.path.abspath(args.repo_root)
    files = build(root)
    stale = [path for path, (cur, new) in files.items() if cur != new]
    if args.check:
        for path in stale:
            print(f"[stale] {os.path.relpath(path, root)} - run tools/generate_docs.py")
        print(f"[{'FAIL' if stale else 'ok'}] {len(files)} generated file(s), {len(stale)} stale")
        return 1 if stale else 0
    for path in stale:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(files[path][1])
        print(f"[write] {os.path.relpath(path, root)}")
    print(f"[ok] {len(files)} generated file(s), {len(stale)} rewritten")
    return 0


if __name__ == "__main__":
    sys.exit(main())
