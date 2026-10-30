#!/usr/bin/env python3
"""
generate_docs.py — rebuild the derived tables and counts from the repository data.

BPH_Master.csv, data/asns.csv and sources/sources.csv are the sources of truth.
This script regenerates everything that restates them, so those copies never need
hand edits:

  - analysis/ECOSYSTEM_MAP.md  Appendix A (entity quick reference), Appendix B (ASN
                               cross-reference with block recommendations) and Appendix C
                               (Mermaid relationship diagrams from data/relationships.csv),
                               between <!-- generated:appendix-a/b/c:start/end --> markers
  - taxonomy/BPH_TAXONOMY.md   the "— N rows" count in each "Current Tn entities" line
  - README.md                  the "Current scope: N providers/entities" count
  - sources/SOURCE_INDEX.md    every catalogue table (one <!-- generated:sources-<section> -->
                               block per section, rows from sources/sources.csv by their
                               `section`) and the Source Statistics table
  - docs/DATA_HEALTH.md        sources without a URL, grades that differ from the
                               publisher default (sources/publishers.csv) without a note,
                               the oldest verification dates and, from data/claims.csv,
                               open claims and tiers whose claims miss the taxonomy section 6
                               evidence minimum. Nothing here depends on
                               today's date, so --check stays stable; the weekly monitor
                               reports what is older than 90 days.

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


def load_sources(root: str) -> list[dict]:
    return load_csv(os.path.join(root, "sources", "sources.csv"))


def source_tables(index_text: str, sources: list[dict]) -> str:
    """Fill every <!-- generated:sources-<section> --> block from sources.csv."""
    by_section = collections.defaultdict(list)
    for s in sources:
        by_section[s["section"]].append(s)
    markers = re.findall(r"<!-- generated:(sources-[a-z0-9-]+):start -->", index_text)
    missing = set(by_section) - {m[len("sources-"):] for m in markers}
    if missing:
        raise SystemExit(f"[ABORT] sources.csv sections without a block in SOURCE_INDEX.md: {sorted(missing)}")
    for name in markers:
        rows = by_section.get(name[len("sources-"):], [])
        out = ["| ID | Grade | Title | Author(s) | Publisher | Date | Link | Local File | Key Entities |",
               "|----|-------|-------|-----------|-----------|------|------|------------|--------------|"]
        for s in rows:
            link = f"[link]({s['url']})" if s["url"] else "—"
            if s["archive_url"]:
                link += f" · [archive]({s['archive_url']})"
            out.append("| " + " | ".join([
                s["id"], s["grade"], cell(s["title"]), cell(s["authors"]) or "—", cell(s["publisher"]), cell(s["date"]) or "—",
                link, f"`{s['local_file']}`" if s["local_file"] else "—", cell(s["key_entities"]) or "—",
            ]) + " |")
        index_text = replace_block(index_text, name, "\n".join(out))
    return index_text


def publisher_defaults(root: str) -> dict[str, dict]:
    path = os.path.join(root, "sources", "publishers.csv")
    out = {}
    for p in (load_csv(path) if os.path.exists(path) else []):
        for name in [p["publisher"]] + [a.strip() for a in p["aliases"].split(";") if a.strip()]:
            out[name] = p
    return out


def grade_deviations(sources: list[dict], defaults: dict[str, dict]) -> list[tuple[dict, str]]:
    """Sources graded differently from their publisher's default without a grade_note."""
    return [(s, defaults[s["publisher"]]["default_grade"]) for s in sources
            if s["publisher"] in defaults and s["grade"] != defaults[s["publisher"]]["default_grade"] and not s["grade_note"].strip()]


def data_health(root: str, rows: list[dict], asns: list[dict], sources: list[dict], claims=(), rels=()) -> str:
    defaults = publisher_defaults(root)
    no_url = [s for s in sources if not s["url"]]
    out = [f"> Generated by `tools/generate_docs.py` from the data files - do not edit by hand. {len(sources)} sources, "
           f"{len(rows)} entities, {len(asns)} ASN register rows.", ""]
    out += ["### Sources without a URL", ""]
    if no_url:
        by_grade = collections.Counter(s["grade"] for s in no_url)
        out.append(f"{len(no_url)} of {len(sources)} (" + ", ".join(f"{g}: {by_grade[g]}" for g in "ABCDE" if by_grade[g]) + "). "
                   "First-party findings and bucket sources have no single URL by design.")
        out += ["", "| ID | Grade | Publisher | Title | Note |", "|----|-------|-----------|-------|------|"]
        out += [f"| {s['id']} | {s['grade']} | {cell(s['publisher'])} | {cell(s['title'])[:100]} | {cell(s.get('url_note', ''))[:140]} |"
                for s in sorted(no_url, key=lambda s: (s['grade'], s['id']))]
    blocked = [s for s in sources if s["url"] and not s["retrieved"]]
    if blocked:
        out += ["", f"{len(blocked)} more have a URL that could not be fetched from the collection environment (bot checks or blocks): "
                + ", ".join(s["id"] for s in sorted(blocked, key=lambda s: s["id"])) + "."]
    else:
        out.append("None.")
    dev = grade_deviations(sources, defaults)
    out += ["", "### Grades that differ from the publisher default", "",
            "A grade that differs from `sources/publishers.csv` needs a `grade_note` in `sources/sources.csv`; until then it is listed here for review."]
    if dev:
        out += ["", "| ID | Grade | Publisher | Default | Title |", "|----|-------|-----------|---------|-------|"]
        out += [f"| {s['id']} | {s['grade']} | {cell(s['publisher'])} | {d} | {cell(s['title'])[:100]} |" for s, d in dev]
    else:
        out += ["", "None."]
    oldest = sorted(rows, key=lambda r: (r["last_verified"], r["provider_name"].lower()))[:10]
    out += ["", "### Oldest entity verifications", "",
            "The ten rows whose `last_verified` is oldest. The weekly monitor reports any older than 90 days.", "",
            "| Entity | Tier | last_verified |", "|--------|------|---------------|"]
    out += [f"| {cell(r['provider_name'])} | {r['risk_tier'][:2]} | {r['last_verified']} |" for r in oldest]
    if claims:
        status = collections.Counter(c["status"] for c in claims)
        out += ["", "### Claims", "", f"{len(claims)} claims ({', '.join(f'{k} {status[k]}' for k in ('verified', 'unverified', 'disputed', 'superseded') if status[k])}); "
                f"{len(rels)} relationships. Open claims (unverified or disputed), oldest first:", "",
                "| Claim | Entity | Status | Since | Claim text |", "|-------|--------|--------|-------|------------|"]
        open_ = sorted((c for c in claims if c["status"] in ("unverified", "disputed")), key=lambda c: (c["verified_date"], c["claim_id"]))
        out += [f"| {c['claim_id']} | {cell(c['entity'])} | {c['status']} | {c['verified_date']} | {cell(c['claim'])[:140]} |" for c in open_]
        weak = tier_evidence(rows, claims, sources)
        out += ["", "### Tier evidence check", "",
                "Entities whose verified, tier-relevant claims do not reach the minimum in taxonomy section 6 for their tier "
                "(T1: a Grade A source or 3+ independent B/C; T2: 2+ B/C; T3: 1 B or 2 C; T4: any B/C/E; T5: any). "
                "Publishers stand in for independence. Each is a prompt to add the missing claim or source, or to review the tier."]
        if weak:
            out += ["", "| Entity | Tier | Evidence in claims |", "|--------|------|--------------------|"]
            out += [f"| {cell(r['provider_name'])} | {r['risk_tier'][:2]} | {why} |" for r, why in weak]
        else:
            out += ["", "None."]
    checked = collections.Counter(a["last_checked"] for a in asns)
    out += ["", "### ASN register check dates", "", "| last_checked | Rows |", "|--------------|------|"]
    out += [f"| {d} | {n} |" for d, n in sorted(checked.items())]
    return "\n".join(out)


REL_TYPES = ("operator-of", "front-of", "successor-of", "upstream-of", "ip-supplier-of", "payment-rail-of", "sister-of", "associated-with")
TIER_STYLE = {"T1": "fill:#991b1b,color:#fff,stroke:#450a0a", "T2": "fill:#c2410c,color:#fff,stroke:#7c2d12",
              "T3": "fill:#b45309,color:#fff,stroke:#78350f", "T4": "fill:#475569,color:#fff,stroke:#1e293b",
              "T5": "fill:#94a3b8,color:#000,stroke:#475569", "ext": "fill:#fff,color:#000,stroke:#64748b,stroke-dasharray:4 3"}


def load_optional(root: str, *parts: str) -> list[dict]:
    path = os.path.join(root, *parts)
    return load_csv(path) if os.path.exists(path) else []


def relationship_diagrams(rows: list[dict], rels: list[dict]) -> str:
    """One Mermaid flowchart per connected cluster of relationships; tracked entities coloured by tier."""
    tiers = {r["provider_name"]: r["risk_tier"][:2] for r in rows}
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for e in rels:
        parent[find(e["from"])] = find(e["to"])
    clusters = collections.defaultdict(list)
    for e in rels:
        clusters[find(e["from"])].append(e)
    ordered = sorted(clusters.values(), key=lambda es: (-len(es), min(x["from"].lower() for x in es)))
    big = [es for es in ordered if len(es) >= 2]
    small = [e for es in ordered if len(es) < 2 for e in es]
    if small:
        big.append(small)
    legend = ("> Generated from `data/relationships.csv` by `tools/generate_docs.py` - do not edit by hand. Arrows read "
              "*from → to* with the relationship type as label; solid = verified, dashed = unverified or disputed, "
              "\"former\" = superseded. Fill shows the tracked entity's tier (T1 dark red → T5 grey); white dashed boxes are "
              f"external parties. {len(rels)} relationships, {len(set(e['from'] for e in rels) | set(e['to'] for e in rels))} parties.")
    out = [legend]
    for n, es in enumerate(big, 1):
        title = "Other single links" if es is small else f"Cluster {n}: " + ", ".join(
            sorted({x for e in es for x in (e["from"], e["to"]) if x in tiers}, key=lambda x: (tiers[x], x.lower()))[:4])
        ids, lines = {}, ["```mermaid", "flowchart LR"]
        for e in sorted(es, key=lambda e: (e["from"].lower(), e["type"], e["to"].lower())):
            for name in (e["from"], e["to"]):
                if name not in ids:
                    ids[name] = f"n{len(ids) + 1}"
                    label = name.replace('"', "#quot;")
                    lines.append(f'  {ids[name]}["{label}"]:::{tiers.get(name, "ext").lower()}')
            label = ("former " if e["status"] == "superseded" else "") + e["type"] + (" ?" if e["status"] in ("unverified", "disputed") else "")
            arrow = "-->" if e["status"] == "verified" else "-.->"
            lines.append(f"  {ids[e['from']]} {arrow}|{label}| {ids[e['to']]}")
        used = {tiers.get(x, "ext") for x in ids}
        lines += [f"  classDef {k.lower()} {v}" for k, v in TIER_STYLE.items() if k in used]
        lines.append("```")
        out += ["", f"#### {title}", ""] + lines
    return "\n".join(out)


def tier_evidence(rows: list[dict], claims: list[dict], sources: list[dict]) -> list[tuple[dict, str]]:
    """Entities whose verified, tier-relevant claims do not meet the taxonomy section 6 minimum for their tier.
    Independence is approximated by distinct publishers."""
    by_id = {s["id"]: s for s in sources}
    ev = collections.defaultdict(lambda: collections.defaultdict(set))
    for c in claims:
        if c["status"] != "verified" or c["tier_relevant"] != "yes":
            continue
        for sid in (x.strip() for x in c["source_ids"].split(";") if x.strip()):
            s = by_id.get(sid)
            if s:
                ev[c["entity"]][s["grade"]].add(s["publisher"])
    out = []
    for r in rows:
        tier, g = r["risk_tier"][:2], ev[r["provider_name"]]
        a, b, c, e = len(g["A"]), len(g["B"]), len(g["C"]), len(g["E"])
        ok = {"T1": a >= 1 or b + c >= 3, "T2": a >= 1 or b + c >= 2, "T3": a + b >= 1 or c >= 2,
              "T4": a + b + c + e >= 1, "T5": sum(len(v) for v in g.values()) >= 1}[tier]
        if not ok:
            out.append((r, f"A {a} · B {b} · C {c} · D {len(g['D'])} · E {e} (distinct publishers)"))
    return out


def source_stats(sources: list[dict]) -> str:
    counts = collections.Counter(s["grade"] for s in sources if s["grade"])
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
    for need in (p("BPH_Master.csv"), p("data", "asns.csv"), p("sources", "sources.csv")):
        if not os.path.exists(need):
            sys.stderr.write(f"[ABORT] missing {need}\n")
            sys.exit(4)
    rows = load_csv(p("BPH_Master.csv"))
    asns = load_csv(p("data", "asns.csv"))
    files = {}
    eco = read(p("analysis", "ECOSYSTEM_MAP.md"))
    new = replace_block(eco, "appendix-a", appendix_a(rows))
    new = replace_block(new, "appendix-b", appendix_b(rows, asns))
    rels = load_optional(root, "data", "relationships.csv")
    claims = load_optional(root, "data", "claims.csv")
    if "<!-- generated:appendix-c:start -->" in new:
        new = replace_block(new, "appendix-c", relationship_diagrams(rows, rels))
    files[p("analysis", "ECOSYSTEM_MAP.md")] = (eco, new)
    tax = read(p("taxonomy", "BPH_TAXONOMY.md"))
    files[p("taxonomy", "BPH_TAXONOMY.md")] = (tax, tier_counts(tax, rows))
    readme = read(p("README.md"))
    files[p("README.md")] = (readme, scope_count(readme, rows))
    sources = load_sources(root)
    idx = read(p("sources", "SOURCE_INDEX.md"))
    files[p("sources", "SOURCE_INDEX.md")] = (idx, replace_block(source_tables(idx, sources), "source-stats", source_stats(sources)))
    health = read(p("docs", "DATA_HEALTH.md"))
    files[p("docs", "DATA_HEALTH.md")] = (health, replace_block(health, "data-health", data_health(root, rows, asns, sources, claims, rels)))
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
