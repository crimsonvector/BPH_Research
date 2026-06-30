#!/usr/bin/env python3
"""
build_dashboard_data.py — generate the public CrimsonVector BPH dashboard data.

Source of truth:
  - BPH_Master.csv            (already-public provider DB)  -> providers + aggregates
  - dashboard_src/findings.json (PRIVATE, gitignored)       -> forward-hunt feed

Outputs (dashboard_data/, public — committed and served same-origin by the site):
  - providers.json            every tracked provider (public-safe fields)
  - aggregates.json           computed stats + enforcement timeline
  - feed.json                 published forward-hunt findings (summaries)
  - finding/<id>.json         per-finding detail
  - manifest.json             build metadata

OPSEC model (the whole point):
  1. Source-split  — feed comes ONLY from the curated findings.json, never from
     the raw investigations tree.
  2. Inclusion     — a finding is emitted only if publish==true AND confidence in
     {confirmed, high}. publish=false holds a confirmed lead out of the feed.
  3. Defang        — every IOC and every free-text field is defanged.
  4. Denylist gate — the ENTIRE generated output is scanned (after un-defanging,
     so a defanged internal IP can't sneak through) for any token in
     tools/denylist.txt. Any hit  -> abort, write nothing, exit non-zero.
  5. Defang assertion — the output is re-scanned for any un-defanged URL scheme
     or bare IPv4. Any hit -> abort, write nothing, exit non-zero.

Nothing is written to disk unless BOTH gates pass. Tradecraft is never published,
regardless of the IOC policy.

Usage:
  python build_dashboard_data.py [--repo-root DIR] [--out DIR] [--quiet]
Exit codes: 0 ok · 2 denylist hit · 3 defang leak · 4 input/setup error
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import os
import re
import sys

# --------------------------------------------------------------------------- #
# paths
# --------------------------------------------------------------------------- #
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)  # repo root (tools/ is one level down)


def p(*parts: str) -> str:
    return os.path.join(*parts)


# --------------------------------------------------------------------------- #
# defang
# --------------------------------------------------------------------------- #
# TLDs that actually occur in our IOC corpus. A dotted token in prose is only
# defanged when its final label is one of these — so filenames/extensions like
# Client32.ini, stager2.exe, trojan.msil are left readable.
TLD_ALLOWLIST = {
    "com", "net", "org", "info", "io", "co", "me", "xyz", "works", "work",
    "su", "ru", "top", "online", "site", "shop", "live", "boats", "mom",
    "cc", "biz", "pro", "app", "dev", "cloud", "host", "click", "link",
}

_SCHEME_RE = re.compile(r"\bhttps://", re.I), re.compile(r"\bhttp://", re.I)
_IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_DOMAIN_RE = re.compile(
    r"\b([a-z0-9](?:[a-z0-9-]*[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)+)\b",
    re.I,
)


def _defang_dots(s: str) -> str:
    return s.replace(".", "[.]")


def defang_value(v: str) -> str:
    """Aggressively defang a known IOC value (domain / ip / url)."""
    if not v:
        return v
    v = re.sub(r"^https://", "hxxps://", v, flags=re.I)
    v = re.sub(r"^http://", "hxxp://", v, flags=re.I)
    return _defang_dots(v)


def defang_text(s: str) -> str:
    """Defang free text: URL schemes, every IPv4, and domains with a known TLD.

    Leaves filenames and non-network dotted tokens intact for readability.
    """
    if not s:
        return s
    s = re.sub(r"\bhttps://", "hxxps://", s, flags=re.I)
    s = re.sub(r"\bhttp://", "hxxp://", s, flags=re.I)
    s = _IPV4_RE.sub(lambda m: _defang_dots(m.group(0)), s)

    def _dom(m: re.Match) -> str:
        tok = m.group(1)
        if tok.rsplit(".", 1)[-1].lower() in TLD_ALLOWLIST:
            return _defang_dots(tok)
        return tok

    return _DOMAIN_RE.sub(_dom, s)


def defang_obj(o):
    """Recursively defang all string values in a JSON-able structure.

    Keys are NOT defanged. Values that look like a bare IOC (domain/ip/url with
    no spaces) get the aggressive treatment; longer prose gets defang_text.
    """
    if isinstance(o, str):
        if " " not in o and ("." in o or "://" in o):
            return defang_value(o)
        return defang_text(o)
    if isinstance(o, list):
        return [defang_obj(x) for x in o]
    if isinstance(o, dict):
        return {k: defang_obj(v) for k, v in o.items()}
    return o


# --------------------------------------------------------------------------- #
# gates
# --------------------------------------------------------------------------- #
def load_denylist(path: str) -> list[str]:
    if not os.path.exists(path):
        die(4, f"denylist not found: {path}\n"
               f"  Copy tools/denylist.example.txt -> tools/denylist.txt and fill in\n"
               f"  the real internal tokens. The build refuses to run without it.")
    toks = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                toks.append(line)
    if not toks:
        die(4, f"denylist is empty: {path}")
    return toks


def _normalize_for_scan(text: str) -> str:
    """Un-defang so a defanged internal token still trips the denylist."""
    return (text.replace("[.]", ".")
                .replace("hxxps://", "https://")
                .replace("hxxp://", "http://")
                .lower())


def denylist_gate(payload: str, denylist: list[str]) -> list[str]:
    scan = _normalize_for_scan(payload)
    return [t for t in denylist if t.lower() in scan]


_LEAK_SCHEME = re.compile(r"\bhttps?://", re.I)
_LEAK_IPV4 = re.compile(r"(?<![\d\[.])\b(?:\d{1,3}\.){3}\d{1,3}\b")


def defang_leak_gate(payload: str) -> list[str]:
    leaks = []
    for m in _LEAK_SCHEME.finditer(payload):
        leaks.append(f"un-defanged scheme: {payload[m.start():m.start()+40]!r}")
    for m in _LEAK_IPV4.finditer(payload):
        leaks.append(f"bare IPv4: {m.group(0)}")
    return leaks


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def die(code: int, msg: str):
    sys.stderr.write(f"\n[ABORT] {msg}\n")
    sys.exit(code)


def split_multi(s: str) -> list[str]:
    if not s:
        return []
    parts = re.split(r"[;,/]| and ", s)
    return [x.strip() for x in parts if x.strip()]


_MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july",
     "august", "september", "october", "november", "december"], start=1)}
_MON_RE = re.compile(
    r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+"
    r"(?:(\d{1,2})\s+)?(\d{4})", re.I)


def extract_dates(text: str):
    """Yield (iso_date, label) for each month-year(-day) mention in text."""
    for m in _MON_RE.finditer(text):
        mon = m.group(1).lower()[:3]
        mon_num = {k[:3]: v for k, v in _MONTHS.items()}.get(mon)
        if not mon_num:
            continue
        day = int(m.group(2)) if m.group(2) else 1
        year = int(m.group(3))
        try:
            iso = _dt.date(year, mon_num, min(day, 28)).isoformat() if not m.group(2) \
                else _dt.date(year, mon_num, day).isoformat()
        except ValueError:
            continue
        yield iso, m.group(0)


_AUTH_KEYWORDS = [
    ("OFAC", ["ofac", "treasury", "sdn", "fincen"]),
    ("EU", ["eu ", "european", "package"]),
    ("UK", ["uk ", "nca", "ofsi", "u.k"]),
    ("AU", ["au ", "austrac", "australia"]),
    ("Canada", ["canada", "fintrac", "canadian"]),
]


def guess_authority(text: str) -> list[str]:
    t = text.lower()
    out = [name for name, kws in _AUTH_KEYWORDS if any(k in t for k in kws)]
    return out or ["Other"]


# --------------------------------------------------------------------------- #
# build: providers
# --------------------------------------------------------------------------- #
PROVIDER_FIELDS = [
    "provider_name", "status", "risk_tier", "primary_asn", "additional_asns",
    "known_prefixes", "country_registration", "country_operations",
    "corporate_entity", "aliases", "parent_entity", "upstream_providers",
    "sanctions_designations", "key_personnel", "associated_threat_actors",
    "associated_malware", "operational_patterns", "first_observed",
    "last_updated", "rf_threat_density_score", "description",
]


def load_providers(csv_path: str) -> list[dict]:
    if not os.path.exists(csv_path):
        die(4, f"BPH_Master.csv not found: {csv_path}")
    rows = []
    with open(csv_path, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, restval=""):
            rows.append({k: (r.get(k) or "").strip() for k in PROVIDER_FIELDS})
    return rows


def tier_code(risk_tier: str) -> str:
    m = re.match(r"\s*(T\d)", risk_tier or "")
    return m.group(1) if m else "Untiered"


def is_sanctioned(s: str) -> bool:
    s = (s or "").lower()
    return bool(s) and "not directly designated" not in s and "not designated" not in s


# --------------------------------------------------------------------------- #
# build: aggregates
# --------------------------------------------------------------------------- #
def build_aggregates(providers: list[dict]) -> dict:
    def counter(values):
        c = {}
        for v in values:
            if v:
                c[v] = c.get(v, 0) + 1
        return dict(sorted(c.items(), key=lambda kv: (-kv[1], kv[0])))

    by_tier = counter(tier_code(r["risk_tier"]) for r in providers)
    by_status = counter(r["status"] for r in providers)

    countries = []
    for r in providers:
        countries += split_multi(r["country_operations"] or r["country_registration"])
    by_country = counter(countries)

    upstreams = []
    for r in providers:
        upstreams += split_multi(r["upstream_providers"])
    top_upstreams = dict(list(counter(upstreams).items())[:12])

    malware = []
    for r in providers:
        malware += split_multi(r["associated_malware"])
    top_malware = dict(list(counter(malware).items())[:12])

    # sanctions-by-authority: count distinct providers per authority
    auth_counts = {}
    timeline = []
    for r in providers:
        s = r["sanctions_designations"]
        if not is_sanctioned(s):
            continue
        for a in set(guess_authority(s)):
            auth_counts[a] = auth_counts.get(a, 0) + 1
        dates = list(extract_dates(s))
        if dates:
            for iso, label in dates:
                timeline.append({
                    "date": iso,
                    "date_label": label,
                    "provider": r["provider_name"],
                    "authorities": guess_authority(s),
                    "detail": s,
                })
        else:
            timeline.append({
                "date": None, "date_label": "", "provider": r["provider_name"],
                "authorities": guess_authority(s), "detail": s,
            })
    timeline.sort(key=lambda e: (e["date"] is None, e["date"] or ""))

    sanctioned = sum(1 for r in providers if is_sanctioned(r["sanctions_designations"]))
    seized = sum(1 for r in providers
                 if "seiz" in (r["sanctions_designations"] + r["status"]).lower())

    return {
        "totals": {
            "providers": len(providers),
            "sanctioned": sanctioned,
            "seized_or_takedown": seized,
            "active": by_status.get("active", 0),
        },
        "by_tier": by_tier,
        "by_status": by_status,
        "by_country": dict(list(by_country.items())[:12]),
        "by_authority": dict(sorted(auth_counts.items(), key=lambda kv: -kv[1])),
        "top_upstreams": top_upstreams,
        "top_malware": top_malware,
        "timeline": timeline,
    }


# --------------------------------------------------------------------------- #
# build: feed + findings
# --------------------------------------------------------------------------- #
PUBLISHABLE_CONFIDENCE = {"confirmed", "high"}
FEED_SUMMARY_FIELDS = [
    "id", "title", "date", "first_observed", "category", "family",
    "confidence", "status", "asn", "provider", "bph_link", "vt", "summary",
    "tags",
]


def load_findings(path: str) -> list[dict]:
    if not os.path.exists(path):
        sys.stderr.write(f"[warn] no findings file at {path} — feed will be empty\n")
        return []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("findings", [])


def build_feed(findings: list[dict]):
    published, feed = [], []
    for fnd in findings:
        if not fnd.get("publish"):
            continue
        if (fnd.get("confidence") or "").lower() not in PUBLISHABLE_CONFIDENCE:
            sys.stderr.write(
                f"[skip] {fnd.get('id')}: publish=true but confidence="
                f"{fnd.get('confidence')!r} not publishable\n")
            continue
        # strip private bookkeeping keys
        clean = {k: v for k, v in fnd.items()
                 if not k.startswith("_") and k != "publish"}
        published.append(clean)
        feed.append({k: clean.get(k) for k in FEED_SUMMARY_FIELDS})
    feed.sort(key=lambda e: (e.get("date") or "", e.get("id") or ""), reverse=True)
    return feed, published


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=DEFAULT_ROOT)
    ap.add_argument("--out", default=None)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    root = os.path.abspath(args.repo_root)
    out_dir = os.path.abspath(args.out) if args.out else p(root, "dashboard_data")
    log = (lambda *a: None) if args.quiet else (lambda *a: print(*a))

    denylist = load_denylist(p(root, "tools", "denylist.txt"))
    providers_raw = load_providers(p(root, "BPH_Master.csv"))
    findings_raw = load_findings(p(root, "dashboard_src", "findings.json"))

    # ---- build (in memory) ----
    providers = defang_obj([{k: r[k] for k in PROVIDER_FIELDS} for r in providers_raw])
    aggregates = defang_obj(build_aggregates(providers_raw))
    feed, published = build_feed(findings_raw)
    feed = defang_obj(feed)
    published = defang_obj(published)

    now = _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0)
    last_updated = max((r["last_updated"] for r in providers_raw if r["last_updated"]),
                       default="")
    manifest = {
        "generated_utc": now.isoformat(),
        "provider_count": len(providers),
        "published_finding_count": len(published),
        "held_finding_count": sum(1 for f in findings_raw if not f.get("publish")),
        "source_last_updated": last_updated,
        "schema": {"providers": 1, "aggregates": 1, "feed": 1, "finding": 1},
    }

    outputs = {
        "providers.json": providers,
        "aggregates.json": aggregates,
        "feed.json": feed,
        "manifest.json": manifest,
    }
    for fnd in published:
        outputs[p("finding", f"{fnd['id']}.json")] = fnd

    # ---- gates (over the FULL serialized output) ----
    blob = json.dumps(outputs, ensure_ascii=False)

    hits = denylist_gate(blob, denylist)
    if hits:
        die(2, "DENYLIST violation — internal token(s) in output, publishing "
               f"NOTHING:\n   {', '.join(sorted(set(hits)))}")

    leaks = defang_leak_gate(blob)
    if leaks:
        die(3, "DEFANG leak — un-defanged IOC in output, publishing NOTHING:\n"
               + "\n".join(f"   - {x}" for x in leaks[:20]))

    # ---- write (only reached if both gates pass) ----
    os.makedirs(p(out_dir, "finding"), exist_ok=True)
    for rel, obj in outputs.items():
        dest = p(out_dir, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8", newline="\n") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
            f.write("\n")

    log(f"[ok] gates passed — wrote {len(outputs)} file(s) to {out_dir}")
    log(f"     providers={len(providers)} published_findings={len(published)} "
        f"held={manifest['held_finding_count']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
