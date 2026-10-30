"""Offline tests for the Phase 3 parts of tools/generate_docs.py.

Run: python -m unittest discover -s tests
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))
import generate_docs as g  # noqa: E402


def src(sid, grade, publisher, url="", section="s1"):
    return {"id": sid, "grade": grade, "title": f"Title {sid}", "authors": "", "publisher": publisher, "date": "2026",
            "type": "", "url": url, "archive_url": "", "retrieved": "", "local_file": "", "key_entities": "", "grade_note": "",
            "section": section}


def claim(entity, ids, status="verified", tier="yes"):
    return {"claim_id": "x-01", "entity": entity, "claim": "c", "source_ids": ids, "status": status, "tier_relevant": tier,
            "verified_date": "2026-10-30", "notes": ""}


class TierEvidence(unittest.TestCase):
    SOURCES = [src("OFAC-X", "A", "OFAC"), src("V1", "B", "Vendor One"), src("V1B", "B", "Vendor One"),
               src("V2", "B", "Vendor Two"), src("J1", "C", "Journal")]

    def check(self, tier, claims):
        rows = [{"provider_name": "E", "risk_tier": tier}]
        return g.tier_evidence(rows, claims, self.SOURCES)

    def test_t1_needs_grade_a_or_three_publishers(self):
        self.assertEqual(self.check("T1-Confirmed", [claim("E", "OFAC-X")]), [])
        self.assertEqual(self.check("T1-Confirmed", [claim("E", "V1; V2; J1")]), [])
        # two sources from one publisher count once
        self.assertEqual(len(self.check("T1-Confirmed", [claim("E", "V1; V1B; V2")])), 1)

    def test_only_verified_tier_relevant_claims_count(self):
        self.assertEqual(len(self.check("T2-High", [claim("E", "V1"), claim("E", "V2", status="unverified")])), 1)
        self.assertEqual(len(self.check("T2-High", [claim("E", "V1"), claim("E", "V2", tier="no")])), 1)
        self.assertEqual(self.check("T2-High", [claim("E", "V1"), claim("E", "V2")]), [])

    def test_t3_and_t5(self):
        self.assertEqual(self.check("T3-Suspected", [claim("E", "V1")]), [])
        self.assertEqual(len(self.check("T3-Suspected", [claim("E", "J1")])), 1)
        self.assertEqual(len(self.check("T5-Watch", [])), 1)
        self.assertEqual(self.check("T5-Watch", [claim("E", "J1", status="unverified")]), [])   # single-source watch-list claim


class Diagrams(unittest.TestCase):
    def test_mermaid_clusters_and_styles(self):
        rows = [{"provider_name": "Aeza", "risk_tier": "T1"}, {"provider_name": "Hypercore", "risk_tier": "T1"},
                {"provider_name": "Lone", "risk_tier": "T3"}]
        rels = [{"from": "Hypercore", "type": "successor-of", "to": "Aeza", "status": "verified"},
                {"from": "Upstream \"X\" (AS1)", "type": "upstream-of", "to": "Hypercore", "status": "unverified"},
                {"from": "Lone", "type": "front-of", "to": "Other Co", "status": "superseded"}]
        text = g.relationship_diagrams(rows, rels)
        self.assertEqual(text.count("```mermaid"), 2)               # one cluster plus the single-link group
        self.assertIn("-->|successor-of|", text)
        self.assertIn("-.->|upstream-of ?|", text)                  # unverified is dashed and marked
        self.assertIn("-.->|former front-of|", text)                # superseded
        self.assertIn("#quot;", text)                               # quotes escaped for Mermaid
        self.assertIn(":::ext", text)
        self.assertIn("classDef t1", text)


class SourceTables(unittest.TestCase):
    def test_blocks_filled_and_sections_required(self):
        doc = "x\n<!-- generated:sources-s1:start -->\n<!-- generated:sources-s1:end -->\n"
        out = g.source_tables(doc, [src("A1", "A", "OFAC", url="https://example.gov/a"), src("B1", "B", "Vendor")])
        self.assertIn("| A1 | A |", out)
        self.assertIn("[link](https://example.gov/a)", out)
        self.assertIn("| B1 | B |", out)
        with self.assertRaises(SystemExit):
            g.source_tables(doc, [src("C1", "C", "J", section="missing")])

    def test_grade_deviation_needs_note(self):
        defaults = {"Dark Reading": {"default_grade": "C"}}
        s = src("DR1", "B", "Dark Reading")
        self.assertEqual(len(g.grade_deviations([s], defaults)), 1)
        s["grade_note"] = "original reporting with named analysts"
        self.assertEqual(g.grade_deviations([s], defaults), [])


if __name__ == "__main__":
    unittest.main()
