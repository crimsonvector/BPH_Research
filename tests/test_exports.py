"""Safety and structure tests for tools/build_exports.py, run against the repository data.

Run: python -m unittest discover -s tests
"""
import csv
import datetime as dt
import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import build_exports as bx  # noqa: E402


class Exports(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = bx.build(ROOT)
        cls.asns = list(csv.DictReader(open(os.path.join(ROOT, "data", "asns.csv"), encoding="utf-8")))
        cls.bundle = json.loads(cls.files["stix/bph-bundle.json"])
        cls.events = [json.loads(v)["Event"] for k, v in cls.files.items() if k.startswith("misp/") and k.endswith(".json") and "manifest" not in k]

    def asns_with(self, *recs):
        return {a["asn"] for a in self.asns if a["block_recommendation"] in recs}

    def test_reproducible(self):
        self.assertEqual(bx.build(ROOT), self.files)

    def test_do_not_block_asns_never_exported(self):
        """Re-issued or historical ASNs never become an ASN object, indicator, MISP attribute or blocklist line
        (entity names and descriptions may still mention them)."""
        never = self.asns_with("do-not-block") - self.asns_with("block", "block-prefixes", "hunt", "monitor")
        self.assertTrue(never)
        stix_numbers = {f"AS{o['number']}" for o in self.bundle["objects"] if o["type"] == "autonomous-system"}
        patterns = " ".join(o["pattern"] for o in self.bundle["objects"] if o["type"] == "indicator")
        misp_values = {a["value"] for e in self.events for a in e["Attribute"]}
        lists = {l.split(",")[1] for l in self.files["blocklists/blocklist.csv"].splitlines()[1:]}
        for asn in never:
            self.assertNotIn(asn, stix_numbers)
            self.assertNotRegex(patterns, rf"= {asn[2:]}\]")
            self.assertNotIn(asn, misp_values)
            self.assertNotIn(asn, lists)

    def test_only_block_asns_are_blocking(self):
        listed = {l for l in self.files["blocklists/asn-block.txt"].splitlines() if l and not l.startswith("#")}
        self.assertEqual(listed, self.asns_with("block"))
        stix_asns = {o["pattern"].split("= ")[1].rstrip("]") for o in self.bundle["objects"]
                     if o["type"] == "indicator" and o["pattern"].startswith("[autonomous-system")}
        self.assertEqual({f"AS{n}" for n in stix_asns}, self.asns_with("block"))
        misp_ids = {a["value"] for e in self.events for a in e["Attribute"] if a["type"] == "AS" and a["to_ids"]}
        self.assertEqual(misp_ids, self.asns_with("block"))

    def test_moved_and_historical_prefixes_excluded(self):
        cidrs = set(self.files["blocklists/cidr-block.txt"].split())
        for p in ("45.135.232.0/24",   # Proton66: historical, now unrelated
                  "45.205.1.0/24",     # VPSVault: left the ASN, 're-check before blocking'
                  "109.120.130.0/24",  # WorkTitans: now originated by Aeza's AS203273
                  "193.46.56.0/24",    # WorkTitans: former prefix now on AS51722
                  "94.26.38.0/24",     # Railnet: entity has no live block ASN after the seizure
                  "62.60.131.0/24"):   # Feo Prest: not announced
            self.assertNotIn(p, cidrs, p)
        self.assertIn("31.56.19.0/24", cidrs)  # AnonRDP, live block ASN

    def test_validity_window(self):
        as_of = max(a["last_checked"] for a in self.asns)
        until = (dt.date.fromisoformat(as_of) + dt.timedelta(days=bx.VALID_DAYS)).isoformat()
        for o in self.bundle["objects"]:
            if o["type"] == "indicator":
                self.assertEqual((o["valid_from"][:10], o["valid_until"][:10]), (as_of, until))

    def test_stix_references_resolve(self):
        ids = [o["id"] for o in self.bundle["objects"]]
        self.assertEqual(len(ids), len(set(ids)))
        known = set(ids)
        for o in self.bundle["objects"]:
            for ref in [o.get("source_ref"), o.get("target_ref"), o.get("created_by_ref")] + o.get("object_marking_refs", []):
                if ref:
                    self.assertIn(ref, known, f"{o['id']} -> {ref}")
            for ext in o.get("extensions", {}):
                self.assertIn(ext, known)

    def test_misp_feed_consistent(self):
        manifest = json.loads(self.files["misp/manifest.json"])
        self.assertEqual(set(manifest), {e["uuid"] for e in self.events})
        hashes = [l for l in self.files["misp/hashes.csv"].splitlines() if l]
        self.assertEqual(len(hashes), sum(len(e["Attribute"]) for e in self.events))
        for e in self.events:
            self.assertIn({"name": "tlp:clear"}, e["Tag"])
            self.assertTrue(e["Attribute"])


if __name__ == "__main__":
    unittest.main()
