#!/usr/bin/env python3
"""
build_exports.py — machine-readable exports of the repository data (roadmap phase 4).

Everything is built from the committed data, so the output is reproducible and CI can
check it is current. IDs are UUIDv5 values derived from the data, and every timestamp
comes from the data's own check dates, never from the clock.

  exports/blocklists/asn-block.txt   ASNs whose recommendation is `block`
  exports/blocklists/cidr-block.txt  curated prefixes of entities with a live `block` or
                                     `block-prefixes` ASN (rules below)
  exports/blocklists/blocklist.csv   both lists with entity, tier, recommendation and basis
  exports/stix/bph-bundle.json       STIX 2.1 bundle: entities (identity), their networks
                                     (infrastructure + autonomous-system / ip SCOs), indicators
                                     for the blocklist entries, typed relationships
  exports/misp/                      MISP feed: manifest.json, hashes.csv, one event per entity

Safety rules (also enforced by tests):
  - `do-not-block` ASNs (re-issued or historical) appear in no export at all
  - `hunt` and `monitor` ASNs are context only: no indicator, MISP to_ids false
  - a prefix is exported only if its entity has a live `block` / `block-prefixes` ASN and the
    record does not mark it historical, not announced, former, moved, re-originated or
    "re-check before blocking"; the weekly monitor keeps those notes current
  - indicators are valid for VALID_DAYS after the data was last checked, so a stale
    repository yields expired indicators instead of silently aging ones

Usage:
  python tools/build_exports.py           # write exports/
  python tools/build_exports.py --check   # exit 1 if exports/ is stale (CI)
Exit codes: 0 ok · 1 stale (with --check) · 4 input/setup error
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import hashlib
import io
import json
import os
import re
import sys
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from generate_docs import load_csv  # noqa: E402
from monitor import known_prefixes  # noqa: E402

VALID_DAYS = 30
NS = uuid.uuid5(uuid.NAMESPACE_URL, "https://github.com/crimsonvector/BPH_Research")
STIX_SCO_NS = uuid.UUID("00abedb4-aa42-466c-9c01-fed23315a9b7")  # STIX 2.1 namespace for deterministic SCO IDs
TLP_CLEAR = "marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9"  # predefined TLP:WHITE (= TLP:CLEAR)
CONFIDENCE = {"T1": 85, "T2": 70, "T3": 50, "T4": 30, "T5": 15}
REL_CONFIDENCE = {"verified": 80, "unverified": 30, "disputed": 15}
MISP_THREAT = {"T1": "1", "T2": "2", "T3": "3", "T4": "4", "T5": "4"}
LEAD_IN = re.compile(r"former|historical|short-lived|broker|ioc ips|re-check", re.I)
MOVED = re.compile(r"\bnow\b|until|re-originated|re-check|moved|former|unrelated|not announced|unrouted|historical", re.I)
MOVED_AFTER = re.compile(r"now originate|re-originated|originates|moved to|now on AS", re.I)
HEADER = ("# {title}\n# Source: https://github.com/crimsonvector/BPH_Research (tools/build_exports.py) - MIT licence\n"
          "# Data as of {as_of}; treat as expired after {until}. {count} entries.\n# {rule}\n")


def sid(kind: str, key: str) -> str:
    return f"{kind}--{uuid.uuid5(NS, f'{kind}:{key}')}"


def sco_id(kind: str, props: dict) -> str:
    """Deterministic SCO ID as the STIX 2.1 spec defines it (UUIDv5 over the canonical ID-contributing properties)."""
    return f"{kind}--{uuid.uuid5(STIX_SCO_NS, json.dumps(props, sort_keys=True, separators=(',', ':')))}"


def ts(day: str) -> str:
    return f"{day}T00:00:00.000Z"


def epoch(day: str) -> str:
    return str(int(dt.datetime.fromisoformat(day).replace(tzinfo=dt.timezone.utc).timestamp()))


def load(root: str) -> dict:
    p = lambda *x: os.path.join(root, *x)
    for need in ("BPH_Master.csv", "data/asns.csv", "data/relationships.csv", "sources/sources.csv"):
        if not os.path.exists(p(need)):
            sys.stderr.write(f"[ABORT] missing {need}\n")
            sys.exit(4)
    rows = load_csv(p("BPH_Master.csv"))
    asns = load_csv(p("data", "asns.csv"))
    as_of = max(a["last_checked"] for a in asns)
    return {"rows": rows, "by_name": {r["provider_name"]: r for r in rows}, "asns": asns,
            "rels": load_csv(p("data", "relationships.csv")), "sources": {s["id"]: s for s in load_csv(p("sources", "sources.csv"))},
            "as_of": as_of, "until": (dt.date.fromisoformat(as_of) + dt.timedelta(days=VALID_DAYS)).isoformat()}


def exportable_prefixes(data: dict) -> list[dict]:
    """Curated prefixes safe to block: see the module docstring."""
    live_block = collections.defaultdict(list)
    for a in data["asns"]:
        if a["block_recommendation"] in ("block", "block-prefixes") and a["routing_state"] == "live":
            live_block[a["provider_name"]].append(a)
    out, seen = [], set()
    for k in known_prefixes(data["by_name"]):
        e = k["entity"]
        if e not in live_block or k["historical"] or not k["expect_announced"] or k["prefix"] in seen:
            continue
        field = data["by_name"][e]["known_prefixes"]
        i = field.find(k["prefix"])
        start = field.rfind(". ", 0, i)
        end = field.find(". ", i)
        before, after = field[start + 2 if start >= 0 else 0: i], field[i: end if end >= 0 else len(field)]
        note = re.match(r"\s*\(([^)]*)\)", field[i + len(k["prefix"]):])
        if LEAD_IN.search(before) or (note and MOVED.search(note.group(1))) or MOVED_AFTER.search(after):
            continue
        seen.add(k["prefix"])
        recs = {a["block_recommendation"] for a in live_block[e]}
        out.append({"prefix": k["prefix"], "entity": e, "tier": data["by_name"][e]["risk_tier"][:2],
                    "recommendation": "block" if "block" in recs else "block-prefixes",
                    "basis": "Known prefix of an entity with a live " + "/".join(sorted(recs)) + " ASN (BPH_Master.csv known_prefixes)"})
    return sorted(out, key=lambda x: (x["prefix"].count(":"), x["prefix"]))


def asn_entries(data: dict) -> list[dict]:
    """One entry per (ASN, entity) that may appear in exports; do-not-block rows never do."""
    return [a for a in data["asns"] if a["block_recommendation"] != "do-not-block"]


# --------------------------------------------------------------------------- blocklists

def blocklists(data: dict, prefixes: list[dict]) -> dict[str, str]:
    block = {}
    for a in asn_entries(data):
        if a["block_recommendation"] == "block":
            block.setdefault(a["asn"], []).append(a)
    asn_lines = sorted(block, key=lambda x: int(x[2:]))
    meta = {"as_of": data["as_of"], "until": data["until"]}
    asn_txt = HEADER.format(title="BPH Research - ASNs recommended for blocking", count=len(asn_lines),
                            rule="Only ASNs whose data/asns.csv recommendation is 'block' (most are on Spamhaus ASN-DROP).", **meta)
    cidr_txt = HEADER.format(title="BPH Research - prefixes recommended for blocking", count=len(prefixes),
                             rule="Curated prefixes of entities with a live block/block-prefixes ASN; excludes historical, moved and unconfirmed space.", **meta)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["type", "value", "entity", "tier", "recommendation", "basis", "as_of", "valid_until"])
    for asn in asn_lines:
        for a in sorted(block[asn], key=lambda a: a["provider_name"]):
            w.writerow(["asn", asn, a["provider_name"], data["by_name"][a["provider_name"]]["risk_tier"][:2], "block",
                        a["recommendation_basis"], data["as_of"], data["until"]])
    for p in prefixes:
        w.writerow(["cidr", p["prefix"], p["entity"], p["tier"], p["recommendation"], p["basis"], data["as_of"], data["until"]])
    return {"blocklists/asn-block.txt": asn_txt + "\n".join(asn_lines) + "\n",
            "blocklists/cidr-block.txt": cidr_txt + "\n".join(p["prefix"] for p in prefixes) + "\n",
            "blocklists/blocklist.csv": buf.getvalue()}


# --------------------------------------------------------------------------- STIX 2.1

def stix_bundle(data: dict, prefixes: list[dict]) -> str:
    author = sid("identity", "author")
    ext = sid("extension-definition", "bph-properties")
    common = {"spec_version": "2.1", "created_by_ref": author, "object_marking_refs": [TLP_CLEAR]}
    ext_ref = {"extensions": {ext: {"extension_type": "toplevel-property-extension"}}}
    objs = [
        {"type": "marking-definition", "spec_version": "2.1", "id": TLP_CLEAR, "created": "2017-01-20T00:00:00.000Z",
         "definition_type": "tlp", "name": "TLP:WHITE", "definition": {"tlp": "white"}},
        {"type": "identity", "spec_version": "2.1", "id": author, "created": ts("2026-05-18"), "modified": ts("2026-05-18"),
         "name": "CrimsonVector Research", "identity_class": "organization",
         "description": "Bulletproof hosting and threat activity enabler research (github.com/crimsonvector/BPH_Research)",
         "object_marking_refs": [TLP_CLEAR]},
        {"type": "extension-definition", "id": ext, "created": ts("2026-10-30"), "modified": ts("2026-10-30"), "name": "BPH Research properties",
         "description": "Top-level x_bph_* properties: risk tier, status, tier basis, primary role and geographic cluster of tracked entities, "
                        "and the verification status of relationships.",
         "schema": "https://github.com/crimsonvector/BPH_Research/blob/main/docs/EXPORTS.md", "version": "1.0.0",
         "extension_types": ["toplevel-property-extension"],
         "extension_properties": ["x_bph_risk_tier", "x_bph_status", "x_bph_tier_basis", "x_bph_primary_role", "x_bph_geo_cluster"], **common},
    ]
    as_of, until = ts(data["as_of"]), ts(data["until"])
    ident = {}

    def entity_identity(name: str) -> str:
        if name in ident:
            return ident[name]
        r = data["by_name"].get(name)
        o = {"type": "identity", "id": sid("identity", name), "name": name, "identity_class": "organization", **common}
        if r:
            day = ts(r["last_verified"])
            refs = [{"source_name": s, "url": data["sources"][s]["url"]} for s in (x.strip() for x in r["sources"].split(";"))
                    if s in data["sources"] and data["sources"][s]["url"]]
            o.update(created=day, modified=day, description=r["description"] or r["tier_basis"],
                     x_bph_risk_tier=r["risk_tier"], x_bph_status=r["status"], x_bph_tier_basis=r["tier_basis"],
                     x_bph_primary_role=r["primary_role"], x_bph_geo_cluster=r["geo_cluster"], **ext_ref)
            if refs:
                o["external_references"] = refs
        else:
            o.update(created=as_of, modified=as_of, description="External party linked to a tracked entity in data/relationships.csv")
        objs.append(o)
        ident[name] = o["id"]
        return o["id"]

    infra = {}

    def network(name: str) -> str:
        if name not in infra:
            r = data["by_name"][name]
            kind = "anonymization" if "Anonymization" in r["risk_tier"] or "proxy" in r["primary_role"].lower() else "hosting-malware"
            o = {"type": "infrastructure", "id": sid("infrastructure", name), "created": ts(r["last_verified"]), "modified": ts(r["last_verified"]),
                 "name": f"{name} network", "infrastructure_types": [kind], **common}
            objs.append(o)
            objs.append({"type": "relationship", "id": sid("relationship", f"{name}|operates"), "created": o["created"], "modified": o["created"],
                         "relationship_type": "related-to", "description": "operates", "source_ref": entity_identity(name), "target_ref": o["id"], **common})
            infra[name] = o["id"]
        return infra[name]

    def consists_of(name: str, sco: str):
        objs.append({"type": "relationship", "id": sid("relationship", f"{name}|consists-of|{sco}"), "created": as_of, "modified": as_of,
                     "relationship_type": "consists-of", "source_ref": network(name), "target_ref": sco, **common})

    def indicator(key: str, name: str, pattern: str, entity: str, desc: str):
        tier = data["by_name"][entity]["risk_tier"][:2]
        o = {"type": "indicator", "id": sid("indicator", key), "created": as_of, "modified": as_of, "name": name, "description": desc,
             "indicator_types": ["malicious-activity"], "pattern": pattern, "pattern_type": "stix", "valid_from": as_of, "valid_until": until,
             "confidence": CONFIDENCE[tier], **common}
        objs.append(o)
        objs.append({"type": "relationship", "id": sid("relationship", f"{key}|indicates"), "created": as_of, "modified": as_of,
                     "relationship_type": "indicates", "source_ref": o["id"], "target_ref": network(entity), **common})

    asn_obj = {}
    for a in asn_entries(data):
        n = int(a["asn"][2:])
        if n not in asn_obj:
            o = {"type": "autonomous-system", "spec_version": "2.1", "id": sco_id("autonomous-system", {"number": n}), "number": n}
            if a["holder"] and "[individual registrant]" not in a["holder"]:
                o["name"] = a["holder"]
            objs.append(o)
            asn_obj[n] = o["id"]
        consists_of(a["provider_name"], asn_obj[n])
        if a["block_recommendation"] == "block":
            indicator(f"{a['asn']}|{a['provider_name']}", f"{a['asn']} ({a['provider_name']})", f"[autonomous-system:number = {n}]",
                      a["provider_name"], f"Block {a['asn']}: {a['recommendation_basis']}. Recommendation from data/asns.csv, checked {data['as_of']}.")
    for p in prefixes:
        kind = "ipv6-addr" if ":" in p["prefix"] else "ipv4-addr"
        sco = sco_id(kind, {"value": p["prefix"]})
        objs.append({"type": kind, "spec_version": "2.1", "id": sco, "value": p["prefix"]})
        consists_of(p["entity"], sco)
        indicator(f"{p['prefix']}|{p['entity']}", f"{p['prefix']} ({p['entity']})", f"[{kind}:value ISSUBSET '{p['prefix']}']",
                  p["entity"], f"Block {p['prefix']} ({p['recommendation']}): {p['basis']}.")
    for r in data["rows"]:
        entity_identity(r["provider_name"])
    for e in data["rels"]:
        if e["status"] == "superseded":
            continue
        o = {"type": "relationship", "id": sid("relationship", f"{e['from']}|{e['type']}|{e['to']}"), "created": as_of, "modified": as_of,
             "relationship_type": e["type"], "source_ref": entity_identity(e["from"]), "target_ref": entity_identity(e["to"]),
             "confidence": REL_CONFIDENCE[e["status"]], "x_bph_status": e["status"], **common, **ext_ref}
        if e["notes"]:
            o["description"] = e["notes"]
        refs = [{"source_name": s, "url": data["sources"][s]["url"]} for s in (x.strip() for x in e["source_ids"].split(";"))
                if s in data["sources"] and data["sources"][s]["url"]]
        if refs:
            o["external_references"] = refs
        objs.append(o)
    uniq = {o["id"]: o for o in objs}  # SCOs shared by several entities collapse to one object
    bundle = {"type": "bundle", "id": sid("bundle", data["as_of"]), "objects": sorted(uniq.values(), key=lambda o: o["id"])}
    return json.dumps(bundle, indent=1, ensure_ascii=False, sort_keys=True) + "\n"


# --------------------------------------------------------------------------- MISP feed

def misp_feed(data: dict, prefixes: list[dict]) -> dict[str, str]:
    org = {"name": "CrimsonVector Research", "uuid": str(uuid.uuid5(NS, "misp:org"))}
    stamp = epoch(data["as_of"])
    attrs = collections.defaultdict(list)
    for a in asn_entries(data):
        rec = a["block_recommendation"]
        attrs[a["provider_name"]].append({
            "uuid": str(uuid.uuid5(NS, f"misp:attr:{a['asn']}|{a['provider_name']}")), "type": "AS", "category": "Network activity",
            "value": a["asn"], "to_ids": rec == "block", "comment": f"{rec}: {a['recommendation_basis']}", "timestamp": epoch(a["last_checked"]),
            "Tag": [{"name": f'bph-research:block-recommendation="{rec}"'}]})
    for p in prefixes:
        attrs[p["entity"]].append({
            "uuid": str(uuid.uuid5(NS, f"misp:attr:{p['prefix']}|{p['entity']}")), "type": "ip-dst", "category": "Network activity",
            "value": p["prefix"], "to_ids": True, "comment": f"{p['recommendation']}: {p['basis']}", "timestamp": stamp,
            "Tag": [{"name": f'bph-research:block-recommendation="{p["recommendation"]}"'}]})
    files, manifest, hashes = {}, {}, []
    for name in sorted(attrs):
        r = data["by_name"][name]
        tier = r["risk_tier"][:2]
        ev_uuid = str(uuid.uuid5(NS, f"misp:event:{name}"))
        tags = [{"name": "tlp:clear"}, {"name": f'bph-research:tier="{tier}"'}, {"name": f'bph-research:status="{r["status"]}"'}]
        head = {"info": f"BPH Research: {name} ({r['risk_tier']})", "date": r["last_verified"], "threat_level_id": MISP_THREAT[tier],
                "analysis": "2", "timestamp": stamp, "publish_timestamp": stamp, "published": True, "Orgc": org, "Tag": tags}
        event = {"Event": {"uuid": ev_uuid, **head, "Attribute": sorted(attrs[name], key=lambda x: x["uuid"])}}
        files[f"misp/{ev_uuid}.json"] = json.dumps(event, indent=1, ensure_ascii=False, sort_keys=True) + "\n"
        manifest[ev_uuid] = head
        hashes += [f"{hashlib.md5(x['value'].encode()).hexdigest()},{ev_uuid}" for x in event["Event"]["Attribute"]]
    files["misp/manifest.json"] = json.dumps(manifest, indent=1, ensure_ascii=False, sort_keys=True) + "\n"
    files["misp/hashes.csv"] = "\n".join(sorted(hashes)) + "\n"
    return files


# --------------------------------------------------------------------------- main

def build(root: str) -> dict[str, str]:
    data = load(root)
    prefixes = exportable_prefixes(data)
    files = blocklists(data, prefixes)
    files["stix/bph-bundle.json"] = stix_bundle(data, prefixes)
    files.update(misp_feed(data, prefixes))
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--repo-root", default=DEFAULT_ROOT)
    ap.add_argument("--check", action="store_true", help="report stale or extra files and exit 1 instead of writing")
    args = ap.parse_args()
    root = os.path.abspath(args.repo_root)
    out = os.path.join(root, "exports")
    files = build(root)
    existing = {os.path.relpath(os.path.join(d, f), out) for d, _, fs in os.walk(out) for f in fs} if os.path.isdir(out) else set()
    existing -= {"README.md"}
    stale = [f for f, body in files.items() if not os.path.exists(os.path.join(out, f)) or open(os.path.join(out, f), encoding="utf-8").read() != body]
    extra = sorted(existing - set(files))
    if args.check:
        for f in stale + extra:
            print(f"[stale] exports/{f} - run tools/build_exports.py")
        print(f"[{'FAIL' if stale or extra else 'ok'}] {len(files)} export file(s), {len(stale) + len(extra)} stale")
        return 1 if stale or extra else 0
    for f in stale:
        path = os.path.join(out, f)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(files[f])
    for f in extra:
        os.remove(os.path.join(out, f))
    print(f"[ok] {len(files)} export file(s), {len(stale)} written, {len(extra)} removed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
