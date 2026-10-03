import copy
import json
import tempfile
import unittest
from pathlib import Path

from experiments.EXP_003.tools.gate_synthesis import render_markdown, synthesize
from experiments.EXP_003.tools.primary_outcome_audit import audit_stage, output_paths
from tests.test_exp003_primary_outcome_audit import run_preflight_stage


class OutputNamingTests(unittest.TestCase):
    def test_version_suffix_survives_output_naming(self):
        json_path, md_path = output_paths(Path("/x/EXP_003_GATE_3A_SET_001_PRIMARY_OUTCOME_AUDIT_v0.1"))
        self.assertEqual(json_path.name, "EXP_003_GATE_3A_SET_001_PRIMARY_OUTCOME_AUDIT_v0.1.json")
        self.assertEqual(md_path.name, "EXP_003_GATE_3A_SET_001_PRIMARY_OUTCOME_AUDIT_v0.1.md")


class SynthesisTests(unittest.TestCase):
    def _stub_report(self, mode: str) -> tuple[dict, dict]:
        with tempfile.TemporaryDirectory() as tmp:
            plan_path, root, corpus_file = run_preflight_stage(Path(tmp), mode)
            return audit_stage(plan_path, "set_001", root, corpus_file), json.loads(corpus_file.read_text())

    def test_same_ordering_is_consistent_and_stages_stay_separate(self):
        a, corpus_a = self._stub_report("dedup")
        b, corpus_b = copy.deepcopy(a), copy.deepcopy(corpus_a)
        report = synthesize({"set_001": a, "set_002": b}, None, {"set_001": {"path": "a", "sha256": "0"}, "set_002": {"path": "b", "sha256": "1"}},
                            corpus={"set_001": corpus_a, "set_002": corpus_b})
        self.assertEqual(report["expectations"]["E6"]["verdict"], "consistent")
        # Closure lines are computed from the records, not asserted.
        rule = report["closure_rule"]
        self.assertIn("16/16 complete, 0 technical failure record(s)", rule["every world in all eight arms has a valid archived execution or a documented technical failure"])
        self.assertTrue(rule["both stages' manifests prospectively frozen"].startswith("NO"))  # the test plan is DRAFT
        self.assertTrue(rule["historical comparison recorded as a secondary observation"].startswith("NO"))
        without_corpus = synthesize({"set_001": a, "set_002": b}, None)
        self.assertTrue(without_corpus["closure_rule"]["raw outputs immutable"].startswith("NO"))
        for key in ("E1", "E2", "E3", "E4", "E5"):
            self.assertTrue(report["expectations"][key]["agree"])
            self.assertEqual(set(report["expectations"][key]["verdicts"]), {"set_001", "set_002"})
        self.assertEqual({p["stage"] for p in report["positions"]}, {"set_001", "set_002"})
        self.assertNotIn("pooled", json.dumps(report).lower())
        md = render_markdown(report)
        self.assertIn("| E6 |", md)
        self.assertIn("## Closure rule", md)

    def test_different_ordering_contradicts_e6(self):
        a, _ = self._stub_report("dedup")
        b = copy.deepcopy(a)
        rows = b["expectations"]["E6"]["ordering_of_arms_by_LINEAGE_discount_rate_this_stage"]
        rows[0], rows[-1] = rows[-1], rows[0]
        report = synthesize({"set_001": a, "set_002": b}, None)
        self.assertEqual(report["expectations"]["E6"]["verdict"], "contradicted")
        self.assertNotEqual(report["expectations"]["E6"]["orderings"]["set_001"], report["expectations"]["E6"]["orderings"]["set_002"])


if __name__ == "__main__":
    unittest.main()
