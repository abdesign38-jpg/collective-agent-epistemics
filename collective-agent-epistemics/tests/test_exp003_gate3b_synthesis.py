import copy
import json
import tempfile
import unittest
from pathlib import Path

from experiments.EXP_003.tools import primary_outcome_audit
from experiments.EXP_003.tools.gate3b_primary_outcome_audit import audit_stage
from experiments.EXP_003.tools.gate3b_synthesis import E7_CELLS, cell_mean, render_markdown, sign, synthesize
from tests.test_exp003_gate3b_primary_outcome_audit import run_stage
from tests.test_exp003_primary_outcome_audit import run_preflight_stage


def stub_report(mode: str) -> tuple[dict, dict]:
    with tempfile.TemporaryDirectory() as tmp:
        plan_path, root, corpus_file = run_stage(Path(tmp), mode)
        return audit_stage(plan_path, "set_001", root, corpus_file), json.loads(corpus_file.read_text())


def gate3a_stub_report(mode: str) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        plan_path, root, corpus_file = run_preflight_stage(Path(tmp), mode)
        return primary_outcome_audit.audit_stage(plan_path, "set_001", root, corpus_file)


class SignTests(unittest.TestCase):
    def test_flat_band_and_signs(self):
        self.assertEqual(sign(None), "n/a")
        self.assertEqual(sign(0.004), "flat")
        self.assertEqual(sign(-0.005), "flat")
        self.assertEqual(sign(0.0051), "positive")
        self.assertEqual(sign(-0.02), "negative")


class SynthesisTests(unittest.TestCase):
    def test_identical_stages_are_consistent_and_everything_stays_separate(self):
        a, corpus_a = stub_report("naive")
        b, corpus_b = copy.deepcopy(a), copy.deepcopy(corpus_a)
        report = synthesize({"set_001": a, "set_002": b}, {"set_001": {"path": "a", "sha256": "0"}, "set_002": {"path": "b", "sha256": "1"}},
                            corpus={"set_001": corpus_a, "set_002": corpus_b})
        e7 = report["expectations"]["E7"]
        self.assertEqual(e7["verdict"], "consistent")
        self.assertEqual([c["cell"] for c in e7["cells"]], [c[0] for c in E7_CELLS])
        self.assertEqual(e7["reversed_cells"], [])
        # The conflicting cells carry the departure quantity, the others the certainty excess.
        for c in e7["cells"]:
            self.assertEqual(c["quantity"], "mean_departure_toward_e1" if "conflicting" in c["cell"] else "mean_certainty_excess")
            self.assertIsNotNone(c["means"]["set_001"])
        for key in ("E1", "E2", "E3", "E4", "E5", "E6"):
            self.assertTrue(report["expectations"][key]["agree"])
            self.assertEqual(set(report["expectations"][key]["verdicts"]), {"set_001", "set_002"})
        self.assertEqual({r["stage"] for r in report["arm_aggregates"]}, {"set_001", "set_002"})
        self.assertEqual({r["stratum"] for r in report["arm_aggregates"] if r["root_mode"] == "dual"}, {"agreeing", "conflicting"})
        rule = report["closure_rule"]
        self.assertIn("26/26 complete, 0 technical failure record(s)", rule["every world in all six arms has a valid archived execution or a documented technical failure"])
        self.assertTrue(rule["both stages' manifests prospectively frozen"].startswith("NO"))   # the test plan is DRAFT
        self.assertTrue(rule["Gate 3A comparison recorded as a secondary placement"].startswith("NO"))
        self.assertEqual([r for r in report["gate3a_bridge"] if r["gate"] == "3A"], [])   # 3B side only, no 3A rows
        self.assertNotIn("pooled", json.dumps(report).lower())
        md = render_markdown(report)
        self.assertIn("| E7 |", md)
        self.assertIn("## Closure rule", md)
        self.assertIn("Arm 2 conflicting LINEAGE", md)

    def test_a_reversed_cell_contradicts_e7_and_names_it(self):
        a, _ = stub_report("naive")
        b = copy.deepcopy(a)
        arm1 = next(s for s, v in b["sets"].items() if v["topology"] == "diamond" and v["root_mode"] == "single" and v["probe"])
        d = b["arm_aggregates"][arm1]["conditions"]["free"]["None"]["D"]
        self.assertGreater(d["mean_certainty_excess"], 0)
        d["mean_certainty_excess"] = -d["mean_certainty_excess"]
        report = synthesize({"set_001": a, "set_002": b})
        self.assertEqual(report["expectations"]["E7"]["verdict"], "contradicted")
        self.assertEqual(report["expectations"]["E7"]["reversed_cells"], ["arm1_free"])
        self.assertEqual(cell_mean(b, "arm1", "free", "None", "mean_certainty_excess"), d["mean_certainty_excess"])

    def test_flat_against_positive_is_not_a_reversal(self):
        a, _ = stub_report("naive")
        b = copy.deepcopy(a)
        arm1 = next(s for s, v in b["sets"].items() if v["topology"] == "diamond" and v["root_mode"] == "single" and v["probe"])
        b["arm_aggregates"][arm1]["conditions"]["lineage"]["None"]["D"]["mean_certainty_excess"] = 0.001
        report = synthesize({"set_001": a, "set_002": b})
        self.assertEqual(report["expectations"]["E7"]["verdict"], "consistent")
        cell = next(c for c in report["expectations"]["E7"]["cells"] if c["cell"] == "arm1_lineage")
        self.assertEqual(cell["signs"], {"set_001": "positive", "set_002": "flat"})

    def test_gate3a_bridge_copies_bounce_and_ring_origin_counts(self):
        a, corpus_a = stub_report("dedup")
        g3a = gate3a_stub_report("dedup")
        report = synthesize({"set_001": a, "set_002": copy.deepcopy(a)}, corpus={"set_001": corpus_a, "set_002": corpus_a},
                            gate3a={"set_001": g3a})
        bridge = report["gate3a_bridge"]
        self.assertEqual({(r["gate"], r["topology"]) for r in bridge}, {("3A", "bounce"), ("3A", "ring"), ("3B", "diamond")})
        self.assertTrue(all(r["position"] == "A post-seed" for r in bridge if r["gate"] == "3A"))
        self.assertEqual({r["probe"] for r in bridge if r["gate"] == "3B"}, {True, False})
        self.assertTrue(report["closure_rule"]["Gate 3A comparison recorded as a secondary placement"].startswith("yes"))
        self.assertIn("like-for-like bridge", render_markdown(report))


if __name__ == "__main__":
    unittest.main()
