#!/usr/bin/env python3
"""
monitor.py — find where the outside world has moved on from what the repository records.

The baseline is the repository itself: every check fetches live state and reports a
finding wherever it differs from the recorded data. A finding stays open until the data
is updated (then re-run tools/generate_docs.py) or it is acknowledged in
monitor/acknowledged.csv. Nothing here edits the data - detection is automated,
judgement stays with an analyst.

Checks (--checks, default all):
  asn        holder, routing state, IPv4 prefix count and ASN-DROP listing of every ASN
             in data/asns.csv
  drop       Spamhaus DROP prefixes announced by tracked ASNs that the repo does not
             recommend blocking
  prefix     origin and announcement of every prefix in BPH_Master.csv known_prefixes
  withdrawn  prefixes a tracked operator ASN stopped announcing in the lookback window
             that another ASN now originates
  asndrop    ASN-DROP entries under a tracked operator's Spamhaus domain that the repo
             does not track
  ripe       recent aut-num and route objects maintained by or registered to the RIPE
             handles in data/registry_handles.csv, for ASNs the repo does not track
  domain     registration, registrar, status, nameservers (incl. seizure banners) and
             hosting ASN of every domain in data/domains.csv
  company    status and new filings at Companies House for data/companies.csv
             (uses the API when COMPANIES_HOUSE_API_KEY is set, else the public site)

Usage:
  python tools/monitor.py [--checks asn,prefix,...] [--out DIR] [--previous REPORT.md]
                          [--lookback DAYS] [--today YYYY-MM-DD]
Writes to --out (default monitor-out/): report.md (issue body), new.md (findings not in
--previous; empty if none), findings.json and snapshot-<date>.json (raw observations).
Exit codes: 0 ok (with or without findings) · 2 --strict and a check had errors ·
4 input/setup error
"""
from __future__ import annotations

import argparse
import base64
import collections
import concurrent.futures as cf
import datetime as dt
import html
import ipaddress
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from generate_docs import defang, load_csv  # noqa: E402

USER_AGENT = "BPH_Research-monitor/1.0 (+https://github.com/crimsonvector/BPH_Research)"
CHECKS = ["asn", "drop", "prefix", "withdrawn", "asndrop", "ripe", "domain", "company"]
SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}
CHECK_TITLES = {
    "asn": "ASN register (`data/asns.csv`)",
    "drop": "Spamhaus DROP space on ASNs not marked for blocking",
    "prefix": "Known prefixes (`BPH_Master.csv` known_prefixes)",
    "withdrawn": "Withdrawn operator prefixes now originated elsewhere",
    "asndrop": "Untracked ASN-DROP entries under tracked operator domains",
    "ripe": "RIPE objects of tracked handles (`data/registry_handles.csv`)",
    "domain": "Domains (`data/domains.csv`)",
    "company": "Companies House (`data/companies.csv`)",
}
WITHDRAWN_CAP = 40  # withdrawn prefixes checked per ASN per run
KEYS_MARK = "monitor-keys:"

PREFIX_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}\b|\b[0-9a-f]{1,4}(?::[0-9a-f]{0,4}){1,7}/\d{1,3}\b", re.I)
ASN_RE = re.compile(r"\bAS(\d{1,10})\b")
NOT_ANNOUNCED_RE = re.compile(r"not announced|unrouted|not routed|withdrawn|no routes", re.I)
ORG_TOKEN_RE = re.compile(
    r"\b(llc|ltd|limited|gmbh|b\.?v|inc|corp|co|ooo|srl|s\.?a|sas|llp|uab|ou|oü|ab|sia|s\.?r\.?o|sdn|bhd|pte|plc|"
    r"jsc|pjsc|ao|zao|kft|spa|sp|z\.?o\.?o|mchj|ug|ag|nv|company|group|network|networks|net|hosting|host|telecom|"
    r"cloud|data|datacenter|internet|technologies|technology|tech|solutions|services|systems|isp|communications|"
    r"media|server|servers|digital|online|it|holding|enterprises|trading|university|bank|bandwidth|transit|broadband|"
    r"fiber|fibre|telecommunications|connect|connectivity|carrier|exchange|global|international|web|wireless|"
    r"mobile|cable|energy|labs|corporation|association|foundation|anonim|sirketi|ltda|lda|sarl|oy|kk)\b", re.I)
HONORIFIC_RE = re.compile(r"\b(Mr|Mrs|Ms|Miss|Mx|Dr)\.? [A-Z][\w'-]*(?: [A-Z][\w'-]*)*")
SEIZURE_NS = re.compile(r"seiz(ed|ure)", re.I)  # e.g. ns1.fbi.seized.gov, ns1.usssdomainseizure.com
HOLD_STATUS = re.compile(r"\bhold\b", re.I)
CDN_NS = re.compile(r"cloudflare|bunny\.net|ddos-guard|akamai|awsdns|fastly|cdn77", re.I)


# --------------------------------------------------------------------------- helpers

def today_utc() -> dt.date:
    return dt.datetime.now(dt.timezone.utc).date()


def split_top(text: str, sep: str = ";") -> list[str]:
    """Split on sep outside parentheses."""
    out, depth, cur = [], 0, []
    for ch in text:
        depth += ch == "("
        depth -= ch == ")" and depth > 0
        if ch == sep and depth == 0:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    out.append("".join(cur))
    return [s.strip() for s in out if s.strip()]


def norm_holder(h: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (h or "").casefold())


def safe_name(name: str) -> str:
    """Show a registry name only if it looks like an organisation; private individuals are never named."""
    name = (name or "").strip()
    if not name:
        return ""
    return name if ORG_TOKEN_RE.search(name) else "[name withheld - may be an individual; see the registry]"


def safe_asname(name: str) -> str:
    """AS names are shown when they look like network handles (upper case with -AS or digits), else withheld."""
    name = (name or "").strip()
    if re.fullmatch(r"[A-Z0-9][A-Z0-9-]*", name) and re.search(r"(^|-)AS(-|$)|\d|NET|HOST|CLOUD|TELECOM|TRANSIT", name):
        return name
    return safe_name(name)


def redact_people(text: str) -> str:
    return HONORIFIC_RE.sub("[individual]", text)


def big_count_change(old: int, new: int) -> bool:
    return abs(new - old) >= max(3, round(0.25 * old))


def asn_int(s: str) -> int:
    return int(str(s).upper().removeprefix("AS"))


def finding(check, severity, subject, change, entities=(), observed="", source="", aspect=""):
    key = f"{check}:{subject}" + (f":{aspect}" if aspect else "")
    return {"key": key, "check": check, "severity": severity, "subject": subject,
            "entities": "; ".join(sorted(set(e for e in entities if e))), "change": change,
            "observed": observed, "source": source}


# --------------------------------------------------------------------------- HTTP

class Http:
    """Small polite HTTP client: retries, per-host spacing, honest User-Agent."""

    def __init__(self, min_interval: dict[str, float] | None = None):
        self.min_interval = min_interval or {}
        self.last: dict[str, float] = {}
        self.lock = threading.Lock()

    def _wait(self, host: str):
        gap = self.min_interval.get(host, 0)
        if not gap:
            return
        with self.lock:
            now = time.monotonic()
            nxt = max(now, self.last.get(host, 0) + gap)
            self.last[host] = nxt
        time.sleep(max(0.0, nxt - now))

    def get(self, url: str, accept: str = "application/json", auth: str | None = None,
            retries: int = 3, timeout: int = 60) -> tuple[int, bytes | None]:
        host = urllib.parse.urlsplit(url).hostname or ""
        headers = {"User-Agent": USER_AGENT, "Accept": accept}
        if auth:
            headers["Authorization"] = "Basic " + base64.b64encode(f"{auth}:".encode()).decode()
        code = 0
        for attempt in range(retries):
            self._wait(host)
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout) as r:
                    return r.status, r.read()
            except urllib.error.HTTPError as e:
                code = e.code
                if code in (400, 401, 403, 404, 410, 501):
                    return code, e.read() if code == 404 else None
            except Exception:  # timeouts, resets
                code = 0
            time.sleep(2 * (attempt + 1))
        return code, None

    def json(self, url: str, **kw) -> tuple[int, dict | None]:
        code, body = self.get(url, **kw)
        if body is None:
            return code, None
        try:
            return code, json.loads(body)
        except ValueError:
            return code, None


class Ctx:
    def __init__(self, root: str, today: dt.date, lookback: int, http: Http, workers: int = 4):
        self.root, self.today, self.lookback, self.http, self.workers = root, today, lookback, http, workers
        self.since = today - dt.timedelta(days=lookback)
        self.errors: list[dict] = []
        self.snapshot: dict[str, object] = {}
        self._cache: dict[str, object] = {}
        self._lock = threading.Lock()

    def error(self, check: str, target: str, msg: str):
        with self._lock:
            self.errors.append({"check": check, "target": target, "error": msg})

    def memo(self, key: str, fn):
        with self._lock:
            if key in self._cache:
                return self._cache[key]
        val = fn()
        with self._lock:
            self._cache[key] = val
        return val

    def pmap(self, fn, items):
        with cf.ThreadPoolExecutor(self.workers) as ex:
            return list(ex.map(fn, items))

    # -- RIPEstat
    def stat(self, call: str, resource: str, check: str, **params) -> dict | None:
        q = urllib.parse.urlencode({"resource": resource, "sourceapp": "bph-research-monitor", **params})
        url = f"https://stat.ripe.net/data/{call}/data.json?{q}"

        def fetch():
            code, j = self.http.json(url)
            if not j or "data" not in j:
                self.error(check, f"{call} {resource}", f"RIPEstat HTTP {code}")
                return None
            return j["data"]
        return self.memo(url, fetch)

    def holder(self, asn: int, check: str) -> str:
        d = self.stat("as-overview", f"AS{asn}", check) or {}
        return d.get("holder") or ""

    def spamhaus(self, name: str) -> list[dict]:
        def fetch():
            code, body = self.http.get(f"https://www.spamhaus.org/drop/{name}.json")
            if body is None:
                self.error("spamhaus", name, f"HTTP {code}")
                return None
            return [json.loads(l) for l in body.decode().splitlines() if l.strip() and '"type":"metadata"' not in l]
        return self.memo(f"spamhaus:{name}", fetch)


# --------------------------------------------------------------------------- repo data

def load_repo(root: str) -> dict:
    p = lambda *x: os.path.join(root, *x)
    need = ["BPH_Master.csv", "data/asns.csv", "data/domains.csv", "data/companies.csv", "data/registry_handles.csv"]
    for n in need:
        if not os.path.exists(p(n)):
            sys.stderr.write(f"[ABORT] missing {n}\n")
            sys.exit(4)
    rows = load_csv(p("BPH_Master.csv"))
    asns = load_csv(p("data", "asns.csv"))
    ack_path = p("monitor", "acknowledged.csv")
    return index_data(rows, asns, load_csv(p("data", "domains.csv")), load_csv(p("data", "companies.csv")),
                      load_csv(p("data", "registry_handles.csv")), load_csv(ack_path) if os.path.exists(ack_path) else [])


def index_data(rows: list[dict], asns: list[dict], domains=(), companies=(), handles=(), acks=()) -> dict:
    data = {"rows": {r["provider_name"]: r for r in rows}, "asns": list(asns), "domains": list(domains),
            "companies": list(companies), "handles": list(handles), "acks": list(acks)}
    data["tracked_asns"] = {asn_int(a["asn"]) for a in asns}
    data["entity_asns"] = collections.defaultdict(set)
    data["asn_entities"] = collections.defaultdict(set)
    for a in asns:
        data["entity_asns"][a["provider_name"]].add(asn_int(a["asn"]))
        data["asn_entities"][asn_int(a["asn"])].add(a["provider_name"])
    return data


def is_carrier(a: dict) -> bool:
    return bool(re.search(r"upstream carrier|dual-use", a["recommendation_basis"], re.I))


def watched(a: dict, rows: dict) -> bool:
    """Operator ASNs whose movements matter: T1-T3, not historical, not an upstream carrier."""
    return (a["block_recommendation"] != "do-not-block" and not is_carrier(a)
            and rows[a["provider_name"]]["risk_tier"][:2] in ("T1", "T2", "T3"))


def derive_state(qualifier: str, holder: str, v4: int) -> str:
    """Same rule that built data/asns.csv routing_state."""
    q = qualifier.lower()
    if "reassigned" in q or "re-registered" in q or "recycled" in q or (
            "historical" in q and ("transferred" in q or "received" in q)):
        return "reassigned" if holder else "unregistered"
    if not holder:
        return "unregistered"
    return "live" if v4 else "dark"


def known_prefixes(rows: dict) -> list[dict]:
    """Prefixes listed in known_prefixes, with the context needed to judge them."""
    out, seen = [], set()
    for name, r in rows.items():
        field = r["known_prefixes"]
        mentioned = mentioned_asns(r)
        later_historical = False  # set once a 'Historical ...:' lead-in appears; applies to the rest of the field
        for seg in split_top(field):
            for m in PREFIX_RE.finditer(seg):
                before = seg[: m.start()].lower()
                note = re.match(r"\s*\(([^)]*)\)", seg[m.end():])  # the prefix's own parenthetical, if any
                note = note.group(1) if note else ""
                historical = later_historical or "historical" in before or "historical" in note.lower()
                if (m.group(0), name) not in seen:
                    seen.add((m.group(0), name))
                    out.append({"prefix": m.group(0), "entity": name, "mentioned": mentioned,
                                "historical": historical, "expect_announced": not NOT_ANNOUNCED_RE.search(note)})
            if "historical" in re.sub(r"\([^)]*\)", "", seg).lower():
                later_historical = True
    return out


# --------------------------------------------------------------------------- check: asn / drop / asndrop

def observe_asns(ctx: Ctx, data: dict) -> dict:
    asns = sorted(data["tracked_asns"])
    current = {a["asn"] for a in data["asns"] if watched(a, data["rows"]) or a["routing_state"] == "live"}

    def one(n):
        ov = ctx.stat("as-overview", f"AS{n}", "asn")
        rs = ctx.stat("routing-status", f"AS{n}", "asn")
        if ov is None or rs is None:
            return n, {"ok": False}
        obs = {"ok": True, "holder": ov.get("holder") or "",
               "v4_prefixes": ((rs.get("announced_space") or {}).get("v4") or {}).get("prefixes") or 0,
               "ris_peers_seeing": ((rs.get("visibility") or {}).get("v4") or {}).get("ris_peers_seeing")}
        if f"AS{n}" in current:
            ap = ctx.stat("announced-prefixes", f"AS{n}", "asn", starttime=ctx.since.isoformat()) or {}
            latest = ap.get("latest_time") or ap.get("query_endtime") or ""
            cur, gone = [], []
            for p in ap.get("prefixes") or []:
                end = max((t["endtime"] for t in p.get("timelines") or []), default="")
                if latest and end >= _shift(latest, hours=-24):
                    cur.append(p["prefix"])
                elif end:
                    gone.append({"prefix": p["prefix"], "last_seen": end[:10]})
            obs["prefixes"], obs["withdrawn"] = sorted(cur), sorted(gone, key=lambda g: g["last_seen"], reverse=True)
        return n, obs
    return dict(ctx.pmap(one, asns))


def _shift(iso: str, **delta) -> str:
    return (dt.datetime.fromisoformat(iso[:19]) + dt.timedelta(**delta)).isoformat()


def compare_asns(data: dict, obs: dict, asndrop: list[dict] | None) -> list[dict]:
    listed = {d["asn"]: d.get("domain", "") for d in asndrop} if asndrop is not None else None
    out = []
    add = out.append
    for a in data["asns"]:
        n, o, ent = asn_int(a["asn"]), obs.get(asn_int(a["asn"])), a["provider_name"]
        if not o or not o.get("ok"):
            continue  # fetch failed; recorded in errors
        hist = a["block_recommendation"] == "do-not-block"
        src = f"https://stat.ripe.net/AS{n}"
        state = derive_state(a["qualifier"], o["holder"], o["v4_prefixes"] or 0)
        if state != a["routing_state"]:
            sev = "high" if "unregistered" in (state, a["routing_state"]) or (a["routing_state"] == "dark" and state == "live") else "medium"
            add(finding("asn", "low" if hist else sev, a["asn"], f"routing state: recorded {a['routing_state']}, now {state}"
                        + (f" ({o['v4_prefixes']} IPv4 prefixes)" if state == "live" else ""), [ent], state, src, "state"))
        redacted = "[individual registrant]" in a["holder"]
        if o["holder"] and a["holder"] and not redacted and norm_holder(o["holder"]) != norm_holder(a["holder"]):
            add(finding("asn", "low" if hist else "medium", a["asn"],
                        f"holder: recorded '{a['holder']}', now '{safe_name(o['holder'])}'", [ent], norm_holder(o["holder"]), src, "holder"))
        rec_v4 = int(a["v4_prefixes"] or 0)
        if not hist and state == "live" and a["routing_state"] == "live" and big_count_change(rec_v4, o["v4_prefixes"] or 0):
            add(finding("asn", "low", a["asn"], f"IPv4 prefixes: recorded {rec_v4}, now {o['v4_prefixes']}", [ent],
                        str(o["v4_prefixes"]), src, "prefix-count"))
        if listed is not None:
            now = n in listed
            if now != (a["asndrop_listed"] == "yes"):
                change = f"ASN-DROP: now listed (domain {listed[n] or 'none'})" if now else "ASN-DROP: no longer listed"
                add(finding("asn", "high" if now and not hist else "medium", a["asn"], change, [ent],
                            "listed" if now else "delisted", src, "asndrop"))
    return merge(out)


def merge(findings: list[dict]) -> list[dict]:
    """One finding per key; entities of duplicates (shared ASNs, prefixes listed twice) are combined."""
    out: dict[str, dict] = {}
    for f in findings:
        if f["key"] in out:
            ents = set(out[f["key"]]["entities"].split("; ")) | set(f["entities"].split("; "))
            out[f["key"]]["entities"] = "; ".join(sorted(e for e in ents if e))
        else:
            out[f["key"]] = dict(f)
    return list(out.values())


def drop_index(drop: list[dict]):
    nets = []
    for d in drop:
        try:
            nets.append(ipaddress.ip_network(d["cidr"], strict=False))
        except (KeyError, ValueError):
            pass
    by_octet = collections.defaultdict(list)
    for n in nets:
        if n.version == 4:
            first = int(n.network_address) >> 24
            last = int(n.broadcast_address) >> 24
            for o in range(first, last + 1):
                by_octet[o].append(n)
    return by_octet


def drop_overlaps(prefixes: list[str], index) -> list[str]:
    hits = []
    for p in prefixes:
        try:
            net = ipaddress.ip_network(p, strict=False)
        except ValueError:
            continue
        if net.version != 4:
            continue
        o = int(net.network_address) >> 24
        if any(net.overlaps(d) for d in index.get(o, ())):
            hits.append(p)
    return hits


def compare_drop(data: dict, obs: dict, drop: list[dict]) -> list[dict]:
    index = drop_index(drop)
    out = []
    by_asn = collections.defaultdict(list)
    for a in data["asns"]:
        by_asn[asn_int(a["asn"])].append(a)
    for n, rows in sorted(by_asn.items()):
        recs = {a["block_recommendation"] for a in rows}
        if recs & {"block", "block-prefixes"} or any(is_carrier(a) for a in rows):
            continue
        hits = drop_overlaps((obs.get(n) or {}).get("prefixes") or [], index)
        if hits:
            out.append(finding("drop", "medium", f"AS{n}",
                               f"{len(hits)} announced prefix(es) on Spamhaus DROP while recommended '{'/'.join(sorted(recs))}': "
                               + ", ".join(hits[:8]) + (" ..." if len(hits) > 8 else ""),
                               [a["provider_name"] for a in rows], " ".join(sorted(hits)), f"https://stat.ripe.net/AS{n}"))
    return out


def compare_asndrop(data: dict, asndrop: list[dict]) -> list[dict]:
    domains = {a["asndrop_domain"].lower() for a in data["asns"] if a["asndrop_domain"]}
    domains |= {d["domain"].lower() for d in data["domains"] if d["role"] == "spamhaus-attribution"}
    dom_entities = collections.defaultdict(set)
    for a in data["asns"]:
        if a["asndrop_domain"]:
            dom_entities[a["asndrop_domain"].lower()].add(a["provider_name"])
    for d in data["domains"]:
        if d["role"] == "spamhaus-attribution":
            dom_entities[d["domain"].lower()].update(re.sub(r"\s*\(lead:[^)]*\)$", "", e).strip() for e in d["entities"].split(";"))
    out = []
    for d in asndrop:
        dom = (d.get("domain") or "").lower()
        if dom in domains and d["asn"] not in data["tracked_asns"]:
            out.append(finding("asndrop", "high", f"AS{d['asn']}",
                               f"on ASN-DROP under tracked domain {dom} ({d.get('asname', '')}, {d.get('cc', '')}) but not in data/asns.csv",
                               dom_entities[dom], dom, f"https://stat.ripe.net/AS{d['asn']}"))
    return out


# --------------------------------------------------------------------------- check: prefix / withdrawn

def origins_of(rs: dict) -> set[int]:
    o = {int(x["origin"]) for x in rs.get("origins") or [] if str(x.get("origin", "")).isdigit()}
    o |= {int(x["origin"]) for x in rs.get("more_specifics") or [] if str(x.get("origin", "")).isdigit()}
    return o


def observe_prefixes(ctx: Ctx, prefixes: list[str], check: str) -> dict:
    def one(p):
        rs = ctx.stat("routing-status", p, check)
        if rs is None:
            return p, None
        exact = sorted({int(x["origin"]) for x in rs.get("origins") or [] if str(x.get("origin", "")).isdigit()})
        return p, {"origins": sorted(origins_of(rs)), "exact": exact, "more_specifics": len(rs.get("more_specifics") or [])}
    return dict(ctx.pmap(one, sorted(set(prefixes))))


def describe_origins(ctx: Ctx | None, data: dict, origins) -> str:
    parts = []
    for o in sorted(origins):
        ents = data["asn_entities"].get(o)
        if ents:
            parts.append(f"AS{o} (tracked: {'; '.join(sorted(ents))})")
        else:
            h = safe_name(ctx.holder(o, "prefix")) if ctx else ""
            parts.append(f"AS{o}" + (f" ({h})" if h else ""))
    return ", ".join(parts)


def compare_prefixes(data: dict, kp: list[dict], obs: dict, ctx: Ctx | None = None) -> list[dict]:
    """Known prefixes whose routing no longer matches the record, grouped per entity and new origin."""
    groups: dict[tuple, list[str]] = collections.defaultdict(list)
    for k in kp:
        o = obs.get(k["prefix"])
        if o is None or k["historical"]:
            continue
        expected = data["entity_asns"].get(k["entity"], set()) | k["mentioned"]
        origins = set(o["origins"])
        if origins & expected:  # the entity still announces the prefix or part of it; other origins inside are sub-lets
            origins &= expected
        if origins and not k["expect_announced"]:
            groups[("reannounced", k["entity"], tuple(sorted(origins)))].append(k["prefix"])
        elif origins - expected:
            groups[("origin", k["entity"], tuple(sorted(origins - expected)))].append(k["prefix"])
        elif not origins and k["expect_announced"]:
            groups[("withdrawn", k["entity"], ())].append(k["prefix"])
    out = []
    for (aspect, entity, origins), prefixes in sorted(groups.items()):
        listed = ", ".join(prefixes)
        if aspect == "withdrawn":
            change = f"{len(prefixes)} known prefix(es) no longer announced and not noted as such: {listed}"
        elif aspect == "reannounced":
            change = f"{len(prefixes)} prefix(es) recorded as not announced are announced again by {describe_origins(ctx, data, origins)}: {listed}"
        else:
            change = f"{len(prefixes)} known prefix(es) now originated by {describe_origins(ctx, data, origins)}, not linked to this entity: {listed}"
        subject = "+".join(f"AS{o}" for o in origins) or "unannounced"
        out.append(finding("prefix", "low" if aspect == "withdrawn" else "medium", subject, change, [entity],
                           " ".join(sorted(prefixes)), aspect=f"{aspect}:{slug(entity)}"))
    return out


def mentioned_asns(row: dict) -> set[int]:
    """ASNs named in an entity's known_prefixes text count as recorded for its prefixes."""
    return {int(x) for x in ASN_RE.findall(row["known_prefixes"])}


def withdrawn_candidates(data: dict, asn_obs: dict, kp: list[dict]) -> dict[str, dict]:
    listed = {k["prefix"] for k in kp}
    cand = {}
    for a in data["asns"]:
        if not watched(a, data["rows"]):
            continue
        n = asn_int(a["asn"])
        for g in ((asn_obs.get(n) or {}).get("withdrawn") or [])[:WITHDRAWN_CAP]:
            if g["prefix"] in listed:
                continue
            c = cand.setdefault(g["prefix"], {"from": set(), "entities": set(), "last_seen": g["last_seen"]})
            c["from"].add(n)
            c["entities"].add(a["provider_name"])
    return cand


def compare_withdrawn(data: dict, cand: dict, obs: dict, ctx: Ctx | None = None) -> list[dict]:
    """Prefixes that left a tracked operator ASN and now sit elsewhere, grouped by (old ASNs, new origin).
    Several prefixes moving to one new origin, or a move to another tracked entity, is a successor signal."""
    groups: dict[tuple, dict] = {}
    for p, c in sorted(cand.items()):
        o = obs.get(p)
        if not o:
            continue
        family = set().union(*(data["entity_asns"][e] | mentioned_asns(data["rows"][e]) for e in c["entities"]))
        for new in sorted(set(o["origins"]) - family):
            g = groups.setdefault((tuple(sorted(c["from"])), new), {"prefixes": [], "entities": set(), "last": ""})
            g["prefixes"].append(p)
            g["entities"] |= c["entities"]
            g["last"] = max(g["last"], c["last_seen"])
    out = []
    for (old, new), g in sorted(groups.items()):
        tracked = new in data["tracked_asns"]
        sev = "medium" if tracked or len(g["prefixes"]) >= 3 else "low"
        ps = g["prefixes"]
        out.append(finding("withdrawn", sev, f"AS{new}",
                           f"{len(ps)} prefix(es) left {', '.join(f'AS{x}' for x in old)} (last seen {g['last']}) and are now originated by "
                           f"{describe_origins(ctx, data, [new])}: {', '.join(ps[:10])}" + (" ..." if len(ps) > 10 else ""),
                           g["entities"], " ".join(sorted(ps)), f"https://stat.ripe.net/AS{new}",
                           aspect="from:" + "+".join(f"AS{x}" for x in old)))
    return out


# --------------------------------------------------------------------------- check: ripe

def ripe_search(ctx: Ctx, query: str, attr: str, otype: str) -> list[dict] | None:
    q = urllib.parse.urlencode({"query-string": query, "inverse-attribute": attr, "type-filter": otype, "flags": ["r", "B"]}, doseq=True)
    code, j = ctx.http.json(f"https://rest.db.ripe.net/search.json?{q}")
    if code == 404:
        return []
    if not j:
        ctx.error("ripe", f"{attr} {query} {otype}", f"RIPE DB HTTP {code}")
        return None
    out = []
    for o in (j.get("objects") or {}).get("object") or []:
        attrs = collections.defaultdict(list)
        for x in o["attributes"]["attribute"]:
            attrs[x["name"]].append(x["value"])
        out.append({"type": o["type"], "key": o["primary-key"]["attribute"][0]["value"],
                    "origin": (attrs.get("origin") or [""])[0], "as_name": (attrs.get("as-name") or [""])[0],
                    "created": (attrs.get("created") or [""])[0][:10], "modified": (attrs.get("last-modified") or [""])[0][:10]})
    return out


def observe_ripe(ctx: Ctx, data: dict) -> dict:
    jobs = []
    for h in data["handles"]:
        if h["kind"] == "mntner":
            jobs += [(h["handle"], "mnt-by", t) for t in ("aut-num", "route", "route6")]
        else:
            jobs.append((h["handle"], "org", "aut-num"))

    def one(job):
        return job, ripe_search(ctx, *job)
    res = ctx.pmap(one, jobs)
    obs = collections.defaultdict(list)
    for (handle, _, _), objs in res:
        obs[handle].extend(objs or [])
    return dict(obs)


def compare_ripe(data: dict, obs: dict, since: dt.date) -> list[dict]:
    """Recently created or modified aut-num/route objects of tracked handles that point at untracked ASNs."""
    hits: dict[tuple, dict] = {}
    handle_entities = {h["handle"]: [e.strip() for e in h["entities"].split(";")] for h in data["handles"]}
    for handle, objs in obs.items():
        for o in objs:
            if max(o["created"], o["modified"]) < since.isoformat():
                continue
            asn = (o["key"] if o["type"] == "aut-num" else o["origin"]).upper()
            if not asn or asn_int(asn) in data["tracked_asns"]:
                continue
            # aut-nums are reported one by one; route objects are grouped per origin ASN
            k = ("aut-num", asn) if o["type"] == "aut-num" else ("route", asn)
            h = hits.setdefault(k, {"objs": {}, "handles": set(), "entities": set()})
            h["objs"][o["key"]] = o
            h["handles"].add(handle)
            h["entities"].update(handle_entities.get(handle, []))
    out = []
    for (kind, asn), h in sorted(hits.items()):
        via = ", ".join(sorted(h["handles"]))
        if kind == "aut-num":
            o = next(iter(h["objs"].values()))
            out.append(finding("ripe", "medium", asn, f"aut-num {asn} ({safe_asname(o['as_name'])}) created {o['created']}, "
                               f"modified {o['modified']}, via {via}; not in data/asns.csv", h["entities"], o["modified"],
                               f"https://stat.ripe.net/{asn}", "aut-num"))
        else:
            objs = sorted(h["objs"].values(), key=lambda o: o["key"])
            first = min(min(o["created"], o["modified"]) for o in objs)
            last = max(o["modified"] for o in objs)
            keys = [o["key"] for o in objs]
            out.append(finding("ripe", "medium", asn, f"{len(objs)} route object(s) for untracked origin {asn} created or changed "
                               f"{first}..{last} by {via}: {', '.join(keys[:10])}" + (" ..." if len(keys) > 10 else ""),
                               h["entities"], " ".join(keys), f"https://stat.ripe.net/{asn}", "routes"))
    return out


# --------------------------------------------------------------------------- check: domain

def rdap_bootstrap(ctx: Ctx) -> dict[str, str]:
    def fetch():
        code, j = ctx.http.json("https://data.iana.org/rdap/dns.json")
        if not j:
            ctx.error("domain", "IANA RDAP bootstrap", f"HTTP {code}")
            return {}
        return {tld: urls[0].rstrip("/") + "/" for tlds, urls in j["services"] for tld in tlds}
    return ctx.memo("rdap-bootstrap", fetch)


def observe_domains(ctx: Ctx, data: dict) -> dict:
    boot = rdap_bootstrap(ctx)

    def dns(name, rtype):
        code, j = ctx.http.json(f"https://dns.google/resolve?name={urllib.parse.quote(name)}&type={rtype}")
        if j is None:
            ctx.error("domain", f"DNS {rtype} {name}", f"HTTP {code}")
            return None
        want = {"NS": 2, "A": 1}[rtype]
        return sorted(a["data"].rstrip(".").lower() for a in j.get("Answer") or [] if a.get("type") == want)

    def one(d):
        name, tld = d["domain"], d["domain"].rsplit(".", 1)[-1]
        o = {"rdap": None}
        base = boot.get(tld)
        if base:
            code, j = ctx.http.json(base + "domain/" + name, accept="application/rdap+json, application/json")
            if code == 404:
                o["rdap"] = "not-registered"
            elif j:
                reg, iana = "", ""
                stack = list(j.get("entities") or [])
                while stack:
                    e = stack.pop(0)
                    if "registrar" in (e.get("roles") or []) and not reg:
                        v = (e.get("vcardArray") or [None, []])[1]
                        reg = next((x[3] for x in v if x[0] == "fn"), e.get("handle", ""))
                        iana = next((p.get("identifier", "") for p in e.get("publicIds") or [] if "IANA" in p.get("type", "")), "")
                    stack.extend(e.get("entities") or [])
                ev = {e.get("eventAction"): (e.get("eventDate") or "")[:10] for e in j.get("events") or []}
                o.update(rdap="ok", server=urllib.parse.urlsplit(base).hostname, registrar=reg, iana_id=iana,
                         created=ev.get("registration", ""), expires=ev.get("expiration", ""), status=sorted(j.get("status") or []),
                         nameservers=sorted(n.get("ldhName", "").lower() for n in j.get("nameservers") or []))
            else:
                ctx.error("domain", f"RDAP {name}", f"HTTP {code}")
        o["dns_ns"] = dns(name, "NS")
        a = dns(name, "A")
        if a:
            info = ctx.stat("network-info", a[0], "domain") or {}
            o["a_asn"] = f"AS{info['asns'][0]}" if info.get("asns") else ""
        else:
            o["a_asn"] = "" if a is not None else None
        return name, o
    return dict(ctx.pmap(one, data["domains"]))


def compare_domains(data: dict, obs: dict) -> list[dict]:
    out = []
    for d in data["domains"]:
        o = obs.get(d["domain"])
        if not o:
            continue
        name, ents = d["domain"], [re.sub(r"\s*\(lead:[^)]*\)$", "", e).strip() for e in d["entities"].split(";")]
        src = f"https://client.rdap.org/?type=domain&object={name}"
        was_unreg = d["rdap_status"].startswith("not registered")
        pending = "HTTP 403" in d["rdap_server"] or "HTTP 429" in d["rdap_server"] or "retry" in d["rdap_server"].lower()
        if o["rdap"] == "not-registered" and not was_unreg:
            out.append(finding("domain", "high", name, "no longer registered (RDAP 404)", ents, "not-registered", src, "registration"))
        elif o["rdap"] == "ok":
            if was_unreg:
                out.append(finding("domain", "high", name, f"re-registered at {o['registrar'] or 'unknown registrar'}",
                                   ents, o["registrar"], src, "registration"))
            elif pending or not d["registrar"]:
                out.append(finding("domain", "low", name, f"RDAP now answers: registrar {o['registrar']} (IANA {o['iana_id'] or '-'}), "
                                   f"status {'; '.join(o['status']) or '-'} - fill in data/domains.csv", ents, o["registrar"], src, "resolved"))
            else:
                rec_id, rec_name = d["iana_registrar_id"], d["registrar"]
                if (rec_id and o["iana_id"] and rec_id != o["iana_id"]) or (not rec_id and norm_holder(rec_name) != norm_holder(o["registrar"])):
                    out.append(finding("domain", "medium", name, f"registrar: recorded {rec_name} ({rec_id or '-'}), now {o['registrar']} ({o['iana_id'] or '-'})",
                                       ents, o["iana_id"] or o["registrar"], src, "registrar"))
                rec_status = sorted(s.strip() for s in d["rdap_status"].split(";") if s.strip())
                if rec_status != o["status"]:
                    added = sorted(set(o["status"]) - set(rec_status))
                    sev = "high" if any(HOLD_STATUS.search(s) for s in added) else "low"
                    out.append(finding("domain", sev, name, f"RDAP status: recorded {'; '.join(rec_status) or '-'}, now {'; '.join(o['status']) or '-'}",
                                       ents, ";".join(o["status"]), src, "status"))
        ns_now = o.get("nameservers") or o.get("dns_ns") or []
        rec_ns = sorted(d["nameservers"].split())
        if ns_now and rec_ns and ns_now != rec_ns:
            seized = any(SEIZURE_NS.search(n) for n in ns_now) and not any(SEIZURE_NS.search(n) for n in rec_ns)
            out.append(finding("domain", "high" if seized else "low", name,
                               ("SEIZED - nameservers now " if seized else "nameservers: now ") + " ".join(ns_now) + f" (recorded {' '.join(rec_ns)})",
                               ents, " ".join(ns_now), src, "seized" if seized else "nameservers"))
        elif ns_now and not rec_ns and any(SEIZURE_NS.search(n) for n in ns_now):
            out.append(finding("domain", "high", name, "SEIZED - nameservers now " + " ".join(ns_now), ents, " ".join(ns_now), src, "seized"))
        cdn = CDN_NS.search(d["nameservers"]) or CDN_NS.search(" ".join(ns_now))  # CDN-fronted A records move between PoPs
        if o.get("a_asn") and d["a_record_asn"] and o["a_asn"] != d["a_record_asn"] and not cdn:
            out.append(finding("domain", "low", name, f"A record now in {o['a_asn']} (recorded {d['a_record_asn']})",
                               ents, o["a_asn"], src, "hosting"))
    return out


# --------------------------------------------------------------------------- check: company

def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.strip().lower()).strip("-")


FILING_LABELS = [
    (r"^(LL)?AP\d", "Officer appointed"),
    (r"^(LL)?TM\d", "Officer appointment terminated"),
    (r"^(LL)?CH\d", "Officer details changed"),
    (r"^(LL)?PSC0?1|^(LL)?PSC0?2|^(LL)?PSC0?3", "Person with significant control notified"),
    (r"^(LL)?PSC0?[456]", "Person with significant control details changed"),
    (r"^(LL)?PSC0?7", "Person with significant control ceased"),
    (r"^(LL)?PSC0?[89]", "PSC statement filed"),
    (r"^RP09", "Officer address changed to the Companies House default address"),
    (r"^RP10", "PSC address changed to the Companies House default address"),
]


def filing_label(ftype: str, desc: str) -> str:
    """Generic label for filings that would otherwise name people; redact names elsewhere."""
    for pat, label in FILING_LABELS:
        if re.match(pat, ftype or ""):
            return label
    return redact_people(desc)[:140]


def parse_ch_html(overview: str, history: str) -> dict:
    def txt(s):
        return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()
    m = re.search(r'id="company-status">(.*?)</dd>', overview, re.S)
    status = ""
    if m:
        parts = [p.strip() for p in txt(m.group(1)).split("—")]
        status = slug(parts[1] if len(parts) > 1 and parts[1] else parts[0])
    filings = []
    if 'id="fhTable"' in history:
        table = history.split('id="fhTable"', 1)[1].split("</table>", 1)[0]
        for tr in re.findall(r"<tr>(.*?)</tr>", table, re.S):
            tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
            if len(tds) >= 3:
                try:
                    date = dt.datetime.strptime(txt(tds[0]), "%d %b %Y").date().isoformat()
                except ValueError:
                    continue
                filings.append({"date": date, "type": txt(tds[1]), "description": txt(tds[2])})
    return {"status": status, "filings": filings}


def observe_companies(ctx: Ctx, data: dict) -> dict:
    key = os.environ.get("COMPANIES_HOUSE_API_KEY", "").strip()

    def one(c):
        n = c["company_number"]
        if key:
            api = f"https://api.company-information.service.gov.uk/company/{n}"
            c1, prof = ctx.http.json(api, auth=key)
            c2, hist = ctx.http.json(api + "/filing-history?items_per_page=25", auth=key)
            if not prof or hist is None:
                ctx.error("company", n, f"Companies House API HTTP {c1}/{c2}")
                return n, None
            status = prof.get("company_status_detail") or prof.get("company_status") or ""
            filings = [{"date": i.get("date", ""), "type": i.get("type", ""),
                        "description": (i.get("description") or "").replace("-", " ")} for i in hist.get("items") or []]
            return n, {"status": slug(status), "filings": filings}
        site = f"https://find-and-update.company-information.service.gov.uk/company/{n}"
        c1, ov = ctx.http.get(site, accept="text/html")
        c2, fh = ctx.http.get(site + "/filing-history", accept="text/html")
        if ov is None or fh is None:
            ctx.error("company", n, f"Companies House HTTP {c1}/{c2}")
            return n, None
        return n, parse_ch_html(ov.decode("utf-8", "replace"), fh.decode("utf-8", "replace"))
    return dict(ctx.pmap(one, data["companies"]))


def compare_companies(data: dict, obs: dict) -> list[dict]:
    out = []
    for c in data["companies"]:
        n, o = c["company_number"], obs.get(c["company_number"])
        if not o:
            continue
        ents = [e.strip() for e in c["entities"].split(";")]
        src = f"https://find-and-update.company-information.service.gov.uk/company/{n}/filing-history"
        label = f"{c['company_name']} ({n}, {c['link']})"
        if o["status"] and o["status"] != c["recorded_status"]:
            out.append(finding("company", "high", n, f"{label}: status recorded {c['recorded_status']}, now {o['status']}",
                               ents, o["status"], src, "status"))
        for f in sorted(o["filings"], key=lambda f: f["date"]):
            if f["date"] > c["last_filing_date"]:
                sev = "low" if re.match(r"^(LL)?AA", f["type"]) else "medium"
                out.append(finding("company", sev, n, f"{label}: new filing {f['date']} {f['type']} - {filing_label(f['type'], f['description'])}",
                                   ents, f["date"], src, f"filing:{f['date']}:{f['type']}"))
    return out


# --------------------------------------------------------------------------- acknowledgements and report

def apply_acks(findings: list[dict], acks: list[dict]) -> tuple[list[dict], list[dict]]:
    active, acked = [], []
    for f in findings:
        hit = next((a for a in acks if a["key"] == f["key"] and (not a.get("observed") or a["observed"] == f["observed"])), None)
        (acked if hit else active).append(f)
    return active, acked


def previous_keys(text: str) -> set[str] | None:
    m = re.search(r"<!-- " + KEYS_MARK + r"(.*?)-->", text or "", re.S)
    if not m:
        return None
    try:
        return set(json.loads(m.group(1)))
    except ValueError:
        return None


def render(findings: list[dict], acked: list[dict], errors: list[dict], meta: dict, new_keys: set[str],
           checks: list[str], limit: int = 60000) -> str:
    def body(max_sev: int) -> str:
        sev = collections.Counter(f["severity"] for f in findings)
        lines = [
            "# Monitor findings",
            "",
            f"> Generated by `tools/monitor.py` on {meta['date']} against repository data at `{meta['commit']}`. "
            f"Lookback {meta['lookback']} days. Checks: {', '.join(checks)}.",
            ">",
            "> A finding means the live state differs from what the repository records. Resolve it by updating the data "
            "(then run `tools/generate_docs.py`) or acknowledge it in `monitor/acknowledged.csv`. See `docs/MONITORING.md`.",
            "",
            f"**{len(findings)} open** ({sev['high']} high, {sev['medium']} medium, {sev['low']} low) · "
            f"**{len(new_keys)} new** since the last run · {len(acked)} acknowledged · {len(errors)} fetch error(s)",
            "",
        ]
        for check in CHECKS:
            fs = sorted((f for f in findings if f["check"] == check),
                        key=lambda f: (SEVERITY_ORDER[f["severity"]], f["entities"], f["subject"]))
            if check not in checks:
                continue
            lines += [f"## {CHECK_TITLES[check]}", ""]
            if not fs:
                lines += ["No open findings.", ""]
                continue
            shown = [f for f in fs if SEVERITY_ORDER[f["severity"]] <= max_sev]
            lines += ["| | Severity | Subject | Entity | Change |", "|---|---|---|---|---|"]
            for f in shown:
                subj = f"[{f['subject']}]({f['source']})" if f["source"] and not re.search(r"\d+\.\d+\.\d+\.\d+", f["source"]) else f["subject"]
                lines.append("| " + " | ".join([
                    "**new**" if f["key"] in new_keys else "", f["severity"], defang(subj).replace("|", "/"),
                    f["entities"].replace("|", "/"), defang(f["change"]).replace("|", "/"),
                ]) + " |")
            if len(shown) < len(fs):
                lines.append(f"\n_{len(fs) - len(shown)} lower-severity finding(s) omitted to fit the issue; see the workflow artifact._")
            lines.append("")
        if errors:
            lines += ["<details><summary>Fetch errors (" + str(len(errors)) + ") - these targets were not checked this run</summary>", ""]
            lines += [f"- {e['check']}: {defang(e['target'])} - {e['error']}" for e in errors[:200]]
            lines += ["", "</details>", ""]
        keys = json.dumps(sorted(f["key"] for f in findings)).replace("--", "-\\u002d")
        lines.append(f"<!-- {KEYS_MARK}{keys}-->")
        return "\n".join(lines) + "\n"
    for max_sev in (2, 1, 0):
        text = body(max_sev)
        if len(text) <= limit:
            return text
    return text[:limit - 200] + "\n\n_Report truncated; see the workflow artifact._\n"


# --------------------------------------------------------------------------- main

def run(data: dict, checks: list[str], ctx: Ctx) -> list[dict]:
    findings: list[dict] = []
    need_asns = {"asn", "drop", "withdrawn"} & set(checks)
    asndrop = ctx.spamhaus("asndrop") if {"asn", "asndrop"} & set(checks) else None
    asn_obs = observe_asns(ctx, data) if need_asns else {}
    ctx.snapshot["asns"] = {f"AS{k}": v for k, v in asn_obs.items()}
    if "asn" in checks:
        findings += compare_asns(data, asn_obs, asndrop)
    if "drop" in checks:
        drop = ctx.spamhaus("drop_v4")
        if drop is not None:
            findings += compare_drop(data, asn_obs, drop)
    if "asndrop" in checks and asndrop is not None:
        findings += compare_asndrop(data, asndrop)
    kp = known_prefixes(data["rows"])
    if "prefix" in checks:
        pobs = observe_prefixes(ctx, [k["prefix"] for k in kp if not k["historical"]], "prefix")
        ctx.snapshot["prefixes"] = pobs
        findings += compare_prefixes(data, kp, pobs, ctx)
    if "withdrawn" in checks:
        cand = withdrawn_candidates(data, asn_obs, kp)
        wobs = observe_prefixes(ctx, list(cand), "withdrawn")
        ctx.snapshot["withdrawn"] = {p: {**(wobs.get(p) or {}), "from": sorted(c["from"]), "last_seen": c["last_seen"]} for p, c in cand.items()}
        findings += compare_withdrawn(data, cand, wobs, ctx)
    if "ripe" in checks:
        robs = observe_ripe(ctx, data)
        ctx.snapshot["ripe"] = robs
        findings += compare_ripe(data, robs, ctx.since)
    if "domain" in checks:
        dobs = observe_domains(ctx, data)
        ctx.snapshot["domains"] = dobs
        findings += compare_domains(data, dobs)
    if "company" in checks:
        cobs = observe_companies(ctx, data)
        ctx.snapshot["companies"] = cobs
        findings += compare_companies(data, cobs)
    return merge(findings)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--repo-root", default=DEFAULT_ROOT)
    ap.add_argument("--checks", default=",".join(CHECKS), help="comma-separated subset of: " + ", ".join(CHECKS))
    ap.add_argument("--out", default="monitor-out")
    ap.add_argument("--previous", help="previous report.md (or issue body) to mark new findings")
    ap.add_argument("--lookback", type=int, default=90, help="days of history for withdrawn prefixes and new RIPE objects")
    ap.add_argument("--today", help="override today's date (YYYY-MM-DD)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--strict", action="store_true", help="exit 2 if any fetch failed")
    args = ap.parse_args()
    checks = [c.strip() for c in args.checks.split(",") if c.strip()]
    bad = [c for c in checks if c not in CHECKS]
    if bad:
        sys.stderr.write(f"[ABORT] unknown check(s): {', '.join(bad)}\n")
        return 4
    root = os.path.abspath(args.repo_root)
    today = dt.date.fromisoformat(args.today) if args.today else today_utc()
    http = Http({"rest.db.ripe.net": 0.3, "find-and-update.company-information.service.gov.uk": 1.0,
                 "api.company-information.service.gov.uk": 0.6, "dns.google": 0.05})
    ctx = Ctx(root, today, args.lookback, http, args.workers)
    data = load_repo(root)
    findings = run(data, checks, ctx)
    active, acked = apply_acks(findings, data["acks"])
    prev = None
    if args.previous and os.path.exists(args.previous):
        with open(args.previous, encoding="utf-8") as f:
            prev = previous_keys(f.read())
    new_keys = {f["key"] for f in active} - (prev or set()) if prev is not None else set()
    commit = os.environ.get("GITHUB_SHA", "")[:12] or "working tree"
    meta = {"date": today.isoformat(), "commit": commit, "lookback": args.lookback}
    os.makedirs(args.out, exist_ok=True)
    report = render(active, acked, ctx.errors, meta, new_keys, checks)
    new_only = [f for f in active if f["key"] in new_keys]
    with open(os.path.join(args.out, "report.md"), "w", encoding="utf-8") as f:
        f.write(report)
    with open(os.path.join(args.out, "new.md"), "w", encoding="utf-8") as f:
        if new_only:
            f.write(f"**{len(new_only)} new finding(s)** in this run:\n\n")
            f.writelines(f"- {x['severity']} · {defang(x['subject'])} · {x['entities']} · {defang(x['change'])}\n"
                         for x in sorted(new_only, key=lambda x: (SEVERITY_ORDER[x["severity"]], x["key"])))
    with open(os.path.join(args.out, "findings.json"), "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "open": active, "acknowledged": acked, "errors": ctx.errors}, f, indent=1, default=sorted)
    with open(os.path.join(args.out, f"snapshot-{today.isoformat()}.json"), "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "observations": ctx.snapshot}, f, indent=1, default=sorted)
    sev = collections.Counter(f["severity"] for f in active)
    print(f"[ok] {len(active)} open finding(s) ({sev['high']} high, {sev['medium']} medium, {sev['low']} low), "
          f"{len(new_keys)} new, {len(acked)} acknowledged, {len(ctx.errors)} fetch error(s) -> {args.out}/report.md")
    return 2 if args.strict and ctx.errors else 0


if __name__ == "__main__":
    sys.exit(main())
