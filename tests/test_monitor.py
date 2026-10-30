"""Offline tests for tools/monitor.py: every compare function runs on fixtures, no network.

The fixtures replay the changes the October 2026 audit found by hand (roadmap Phase 2
"done when"): Altawk going dark, MIRhosting going dark, WorkTitans withdrawing ranges,
GCSAS joining ASN-DROP, the RetryHost block re-originated by AS51130, and the
2026-10-13 Companies House strike-off notices.

Run: python -m unittest discover -s tests
"""
import datetime as dt
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))
import monitor as m  # noqa: E402


def row(name, tier="T2", known_prefixes=""):
    return {"provider_name": name, "risk_tier": tier, "known_prefixes": known_prefixes}


def asn(n, name, state="live", v4="10", listed="no", rec="block", qualifier="", holder=None, basis="On Spamhaus ASN-DROP"):
    return {"asn": f"AS{n}", "provider_name": name, "relation": "primary", "qualifier": qualifier,
            "holder": holder if holder is not None else f"HOLDER-{n} Example Hosting LLC", "routing_state": state,
            "v4_prefixes": v4, "asndrop_listed": listed, "asndrop_domain": "", "block_recommendation": rec,
            "recommendation_basis": basis, "last_checked": "2026-09-25"}


def live(n, v4, holder=None):
    return {"ok": True, "holder": holder if holder is not None else f"HOLDER-{n} Example Hosting LLC", "v4_prefixes": v4}


class StateRules(unittest.TestCase):
    def test_derive_state_matches_register_rules(self):
        self.assertEqual(m.derive_state("", "X LLC", 5), "live")
        self.assertEqual(m.derive_state("", "X LLC", 0), "dark")
        self.assertEqual(m.derive_state("", "", 0), "unregistered")
        self.assertEqual(m.derive_state("historical; reassigned to Y", "Y GmbH", 9), "reassigned")
        self.assertEqual(m.derive_state("historical; deregistered", "", 0), "unregistered")


class OctoberReplay(unittest.TestCase):
    """Each October 2026 change must produce a finding against the pre-October baseline."""

    def setUp(self):
        self.rows = [row("Altawk"), row("MIRhosting", tier="T3"), row("WorkTitans"), row("GCSAS"),
                     row("Railnet", tier="T1", known_prefixes="94.26.38.0/24 (RetryHost block)")]
        self.asns = [asn(209946, "Altawk", v4="12", listed="yes"), asn(52000, "MIRhosting", v4="40", rec="hunt"),
                     asn(209847, "WorkTitans", v4="14", listed="yes"), asn(215540, "GCSAS", v4="237", rec="block-prefixes"),
                     asn(202412, "Railnet", v4="30", listed="yes")]
        self.data = m.index_data(self.rows, self.asns)
        self.obs = {209946: live(209946, 0), 52000: live(52000, 0), 209847: live(209847, 2),
                    215540: live(215540, 237), 202412: live(202412, 0)}
        self.asndrop = [{"asn": 209946, "domain": "altawk.com"}, {"asn": 209847, "domain": "stark-industries.solutions"},
                        {"asn": 215540, "domain": "globconnex.com"}, {"asn": 202412, "domain": "virtualine.org"}]

    def keys(self, findings):
        return {f["key"] for f in findings}

    def test_routing_and_asndrop_changes(self):
        keys = self.keys(m.compare_asns(self.data, self.obs, self.asndrop))
        self.assertIn("asn:AS209946:state", keys)         # Altawk went dark
        self.assertIn("asn:AS52000:state", keys)          # MIRhosting went dark
        self.assertIn("asn:AS209847:prefix-count", keys)  # WorkTitans withdrew ranges (14 -> 2)
        self.assertIn("asn:AS215540:asndrop", keys)       # GCSAS joined ASN-DROP
        self.assertIn("asn:AS202412:state", keys)         # Railnet dark after the seizure

    def test_retryhost_reorigination(self):
        kp = m.known_prefixes(self.data["rows"])
        found = m.compare_prefixes(self.data, kp, {"94.26.38.0/24": {"origins": [51130]}})
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["subject"], "AS51130")
        self.assertIn("94.26.38.0/24", found[0]["change"])
        # once the record names the new origin, the finding resolves
        self.rows[4]["known_prefixes"] = "94.26.38.0/24 (RetryHost block; re-originated by AS51130 since 2026-10-28)"
        data = m.index_data(self.rows, self.asns)
        self.assertEqual(m.compare_prefixes(data, m.known_prefixes(data["rows"]), {"94.26.38.0/24": {"origins": [51130]}}), [])

    def test_strike_off_notices(self):
        companies = [{"company_number": n, "company_name": name, "entities": ent, "link": "name-match",
                      "recorded_status": "active", "last_filing_date": "2026-05-01", "last_filing_type": "AA", "checked": "2026-09-25"}
                     for n, name, ent in [("15885164", "FEMO IT SOLUTIONS LIMITED", "Femo"), ("14459750", "FIRST SERVER LIMITED", "First Server"),
                                          ("15668439", "WAICORE LTD", "WAIcore"), ("11161830", "TIGER NETWORK LIMITED", "Tiger")]]
        data = m.index_data([], [], companies=companies)
        obs = {c["company_number"]: {"status": "active-proposal-to-strike-off",
                                     "filings": [{"date": "2026-10-13", "type": "GAZ1", "description": "First Gazette notice for compulsory strike-off"}]}
               for c in companies}
        keys = self.keys(m.compare_companies(data, obs))
        for n in ("15885164", "14459750", "15668439", "11161830"):
            self.assertIn(f"company:{n}:status", keys)
            self.assertIn(f"company:{n}:filing:2026-10-13:GAZ1", keys)

    def test_no_findings_when_record_is_current(self):
        for a, n in zip(self.asns, (209946, 52000, 209847, 215540, 202412)):
            a["routing_state"] = m.derive_state("", self.obs[n]["holder"], self.obs[n]["v4_prefixes"])
            a["v4_prefixes"] = str(self.obs[n]["v4_prefixes"])
            a["asndrop_listed"] = "yes" if any(d["asn"] == n for d in self.asndrop) else "no"
        self.assertEqual(m.compare_asns(m.index_data(self.rows, self.asns), self.obs, self.asndrop), [])


class AsnRules(unittest.TestCase):
    def test_redacted_holder_never_compared_or_printed(self):
        data = m.index_data([row("X")], [asn(1, "X", holder="[individual registrant]")])
        self.assertEqual(m.compare_asns(data, {1: live(1, 10, holder="Jane Doe")}, None), [])

    def test_holder_change_withholds_personal_names(self):
        data = m.index_data([row("X")], [asn(1, "X")])
        f = m.compare_asns(data, {1: live(1, 10, holder="John Smith")}, None)
        self.assertEqual(len(f), 1)
        self.assertNotIn("John Smith", f[0]["change"])

    def test_historical_asn_changes_are_low(self):
        data = m.index_data([row("X")], [asn(1, "X", state="reassigned", rec="do-not-block", qualifier="historical; reassigned to Y")])
        f = m.compare_asns(data, {1: live(1, 0, holder="")}, None)
        self.assertEqual([(x["key"], x["severity"]) for x in f], [("asn:AS1:state", "low")])

    def test_failed_fetch_is_not_a_finding(self):
        data = m.index_data([row("X")], [asn(1, "X")])
        self.assertEqual(m.compare_asns(data, {1: {"ok": False}}, None), [])

    def test_shared_asn_merges_entities(self):
        data = m.index_data([row("A"), row("B")], [asn(1, "A"), asn(1, "B")])
        f = m.compare_asns(data, {1: live(1, 0)}, None)
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0]["entities"], "A; B")

    def test_untracked_asndrop_successor(self):
        data = m.index_data([row("GIR")], [dict(asn(207713, "GIR"), asndrop_domain="gir.network", asndrop_listed="yes")])
        f = m.compare_asndrop(data, [{"asn": 207713, "domain": "gir.network"}, {"asn": 203319, "domain": "gir.network", "asname": "GIR-AS-1"},
                                     {"asn": 999, "domain": "unrelated.example"}])
        self.assertEqual([x["key"] for x in f], ["asndrop:AS203319"])

    def test_drop_overlap_only_for_unblocked_asns(self):
        data = m.index_data([row("T4", tier="T4"), row("T1", tier="T1")],
                            [asn(1, "T4", rec="monitor", basis="T4"), asn(2, "T1", rec="block")])
        obs = {1: {"prefixes": ["10.0.0.0/24", "10.9.0.0/24"]}, 2: {"prefixes": ["10.0.1.0/24"]}}
        f = m.compare_drop(data, obs, [{"cidr": "10.0.0.0/23"}])
        self.assertEqual([x["key"] for x in f], ["drop:AS1"])
        self.assertEqual(f[0]["observed"], "10.0.0.0/24")


class PrefixRules(unittest.TestCase):
    TEXT = ("3.3.3.0/24 (historical; unrouted); 1.1.1.0/24; 4.4.4.0/24 (not announced since 2026-09-09); 1.1.2.0/24 (AS100) - "
            "announced. Historical blocks now elsewhere (do not attribute): 2.2.2.0/24 (AS62300); 2.2.3.0/24")

    def test_known_prefix_parsing(self):
        kp = {k["prefix"]: k for k in m.known_prefixes({"P": row("P", known_prefixes=self.TEXT)})}
        self.assertFalse(kp["1.1.2.0/24"]["historical"])
        self.assertTrue(kp["2.2.2.0/24"]["historical"])
        self.assertTrue(kp["2.2.3.0/24"]["historical"])
        self.assertTrue(kp["3.3.3.0/24"]["historical"])
        self.assertFalse(kp["1.1.1.0/24"]["historical"])   # a parenthetical 'historical' applies to its own prefix only
        self.assertFalse(kp["4.4.4.0/24"]["expect_announced"])
        self.assertEqual(kp["1.1.1.0/24"]["mentioned"], {100, 62300})

    def test_reannounced_and_withdrawn(self):
        data = m.index_data([row("P", known_prefixes=self.TEXT)], [asn(100, "P")])
        kp = m.known_prefixes(data["rows"])
        obs = {"1.1.1.0/24": {"origins": []}, "1.1.2.0/24": {"origins": [100]}, "4.4.4.0/24": {"origins": [555]}}
        aspects = sorted(f["key"].split(":")[2] for f in m.compare_prefixes(data, kp, obs))
        self.assertEqual(aspects, ["reannounced", "withdrawn"])

    def test_sublets_ignored_while_entity_announces_part(self):
        data = m.index_data([row("H", known_prefixes="2a01:8640::/32")], [asn(59711, "H")])
        kp = m.known_prefixes(data["rows"])
        self.assertEqual(m.compare_prefixes(data, kp, {"2a01:8640::/32": {"origins": [59711, 57814], "exact": [59711]}}), [])
        self.assertEqual(m.compare_prefixes(data, kp, {"2a01:8640::/32": {"origins": [59711, 57814], "exact": []}}), [])
        f = m.compare_prefixes(data, kp, {"2a01:8640::/32": {"origins": [57814], "exact": []}})
        self.assertEqual(f[0]["subject"], "AS57814")

    def test_withdrawn_grouped_by_new_origin(self):
        data = m.index_data([row("MIR", tier="T3"), row("Aeza", tier="T1")], [asn(52000, "MIR", rec="hunt"), asn(203273, "Aeza")])
        asn_obs = {52000: {"withdrawn": [{"prefix": f"10.0.{i}.0/24", "last_seen": "2026-10-01"} for i in range(3)]
                           + [{"prefix": "10.1.0.0/24", "last_seen": "2026-09-01"}]}}
        cand = m.withdrawn_candidates(data, asn_obs, [])
        obs = {f"10.0.{i}.0/24": {"origins": [48729]} for i in range(3)}
        obs["10.1.0.0/24"] = {"origins": [203273]}
        f = {x["subject"]: x for x in m.compare_withdrawn(data, cand, obs)}
        self.assertEqual(f["AS48729"]["severity"], "medium")      # three prefixes to one new origin
        self.assertEqual(f["AS48729"]["observed"].count("/24"), 3)
        self.assertIn("tracked: Aeza", f["AS203273"]["change"])   # moved to another tracked entity


class RipeRules(unittest.TestCase):
    def test_recent_untracked_objects_only(self):
        data = m.index_data([row("W")], [asn(209847, "W")], handles=[{"handle": "THE-HOSTING-MNT", "kind": "mntner", "entities": "W"}])
        objs = {"THE-HOSTING-MNT": [
            {"type": "route", "key": "10.0.0.0/24", "origin": "as51722", "as_name": "", "created": "2026-09-07", "modified": "2026-09-07"},
            {"type": "route", "key": "10.0.1.0/24", "origin": "AS51722", "as_name": "", "created": "2026-09-07", "modified": "2026-09-07"},
            {"type": "route", "key": "10.0.2.0/24", "origin": "AS209847", "as_name": "", "created": "2026-09-07", "modified": "2026-09-07"},
            {"type": "route", "key": "10.0.3.0/24", "origin": "AS777", "as_name": "", "created": "2020-01-01", "modified": "2021-01-01"},
            {"type": "aut-num", "key": "AS218688", "origin": "", "as_name": "Some-Person", "created": "2026-09-11", "modified": "2026-09-11"},
        ]}
        f = {x["key"]: x for x in m.compare_ripe(data, objs, dt.date(2026, 8, 1))}
        self.assertEqual(set(f), {"ripe:AS51722:routes", "ripe:AS218688:aut-num"})
        self.assertEqual(f["ripe:AS51722:routes"]["observed"], "10.0.0.0/24 10.0.1.0/24")
        self.assertNotIn("Some-Person", f["ripe:AS218688:aut-num"]["change"])


class DomainRules(unittest.TestCase):
    def dom(self, **kw):
        d = {"domain": "example.net", "role": "operator-site", "entities": "X", "registrar": "Reg Inc", "iana_registrar_id": "100",
             "rdap_status": "client transfer prohibited", "nameservers": "a.ns.cloudflare.com b.ns.cloudflare.com",
             "a_record_asn": "AS13335", "rdap_server": "rdap.verisign.com"}
        d.update(kw)
        return d

    def test_seizure_and_registrar_change(self):
        data = m.index_data([], [], domains=[self.dom()])
        obs = {"example.net": {"rdap": "ok", "registrar": "Other", "iana_id": "200", "status": ["client transfer prohibited"],
                               "nameservers": ["ns1.fbi.seized.gov", "ns2.fbi.seized.gov"], "a_asn": "AS13335"}}
        f = {x["key"]: x for x in m.compare_domains(data, obs)}
        self.assertEqual(f["domain:example.net:seized"]["severity"], "high")
        self.assertIn("domain:example.net:registrar", f)

    def test_dropped_hold_and_pending(self):
        data = m.index_data([], [], domains=[self.dom(), self.dom(domain="pending.org", registrar="", iana_registrar_id="",
                                                                   rdap_server="rdap.example HTTP 403 (retry pending)")])
        obs = {"example.net": {"rdap": "ok", "registrar": "Reg Inc", "iana_id": "100", "status": ["server hold"],
                               "nameservers": ["a.ns.cloudflare.com", "b.ns.cloudflare.com"], "a_asn": "AS13335"},
               "pending.org": {"rdap": "ok", "registrar": "NameSilo", "iana_id": "1479", "status": [], "nameservers": []}}
        f = {x["key"]: x for x in m.compare_domains(data, obs)}
        self.assertEqual(f["domain:example.net:status"]["severity"], "high")
        self.assertIn("domain:pending.org:resolved", f)
        data = m.index_data([], [], domains=[self.dom()])
        f = m.compare_domains(data, {"example.net": {"rdap": "not-registered", "dns_ns": []}})
        self.assertEqual([x["key"] for x in f], ["domain:example.net:registration"])


class CompanyRules(unittest.TestCase):
    def test_parse_public_site(self):
        ov = '<dd class="text data" id="company-status"> Active <span id="company-status-detail">&mdash; Active proposal to strike off</span> </dd>'
        fh = ('<table id="fhTable"><tr><th>Date</th></tr><tr><td class="nowrap">\n13 Oct 2026 </td><td>\nGAZ1 </td>'
              '<td><strong>First Gazette</strong> notice for compulsory strike-off</td><td>PDF</td></tr></table>')
        p = m.parse_ch_html(ov, fh)
        self.assertEqual(p["status"], "active-proposal-to-strike-off")
        self.assertEqual(p["filings"], [{"date": "2026-10-13", "type": "GAZ1", "description": "First Gazette notice for compulsory strike-off"}])

    def test_officer_filings_never_name_people(self):
        self.assertEqual(m.filing_label("CH01", "Director's details changed for Mr John Smith on 6 October 2026"), "Officer details changed")
        self.assertEqual(m.filing_label("LLPSC04", "Change of details for Jane Roe as a person with significant control"),
                         "Person with significant control details changed")
        self.assertNotIn("Smith", m.filing_label("XX01", "Something about Mr John Smith"))


class RegistrarRules(unittest.TestCase):
    PAGE = ('<h3>2026 Notices</h3><h4>Termination</h4><div id="2026-Termination"><div class="compliance-notice" data-id="28-08-2026" '
            'id="notice-1369">28 August 2026&#58;&nbsp;<a href="/uploads/compliance_notice/attachment/1369/x.pdf">ICANN Sends Notice of '
            'Termination to Registrar</a>&nbsp;(Example Names Ltd (IANA #3765))&nbsp;<span class="action"><p>&nbsp;</p></span></div>'
            '<h4>Breach</h4><div class="compliance-notice" data-id="01-05-2014" id="notice-9">1 May 2014&#58;&nbsp;<a href="/y.pdf">'
            'ICANN Sends Notice of Breach to Registrar</a>&nbsp;(Old Registrar, Inc.)</div>')

    def test_parse_notices(self):
        n = m.parse_icann_notices(self.PAGE)
        self.assertEqual(n, [{"id": "1369", "iana_id": "3765", "registrar": "Example Names Ltd", "date": "2026-08-28",
                              "kind": "termination", "url": "https://www.icann.org/uploads/compliance_notice/attachment/1369/x.pdf"}])

    def test_new_notice_and_accreditation_change(self):
        dom = {"domain": "a.example", "entities": "X", "registrar": "Example Names Ltd", "iana_registrar_id": "3765"}
        reg = {"iana_id": "1362", "registrar": "Regtime", "accreditation": "Accredited", "icann_notices": "2025-01-02 breach"}
        data = m.index_data([], [], domains=[dom], registrars=[reg])
        obs = {"iana": {"3765": {"status": "Accredited"}, "1362": {"status": "Terminated"}},
               "notices": [{"iana_id": "3765", "date": "2026-08-28", "kind": "termination", "url": "u"},
                           {"iana_id": "3765", "date": "2020-01-01", "kind": "breach", "url": "u"},   # before the window
                           {"iana_id": "1362", "date": "2025-01-02", "kind": "breach", "url": "u"}]}  # already recorded
        f = {x["key"]: x for x in m.compare_registrars(data, obs, dt.date(2026, 8, 1))}
        self.assertEqual(set(f), {"registrar:3765:notice:2026-08-28:termination", "registrar:1362:accreditation"})
        self.assertEqual(f["registrar:3765:notice:2026-08-28:termination"]["severity"], "high")


class ReportRules(unittest.TestCase):
    def test_acks_keys_and_defang(self):
        f1 = m.finding("prefix", "medium", "AS1", "now 10.1.2.0/24", ["X"], "10.1.2.0/24", aspect="origin:x")
        f2 = m.finding("domain", "low", "xn--d1a-test.com", "nameservers changed", ["Y"], "ns1", aspect="nameservers")
        active, acked = m.apply_acks([f1, f2], [{"key": f1["key"], "observed": "10.1.2.0/24"}, {"key": f2["key"], "observed": "other"}])
        self.assertEqual(([x["key"] for x in active], [x["key"] for x in acked]), ([f2["key"]], [f1["key"]]))
        meta = {"date": "2026-10-30", "commit": "abc", "lookback": 90}
        text = m.render([f1, f2], [], [], meta, {f2["key"]}, m.CHECKS)
        self.assertIn("10[.]1[.]2[.]0/24", text)
        self.assertNotIn("10.1.2.0/24", text)
        self.assertEqual(m.previous_keys(text), {f1["key"], f2["key"]})
        self.assertEqual(text.count("-->"), 1)


if __name__ == "__main__":
    unittest.main()
