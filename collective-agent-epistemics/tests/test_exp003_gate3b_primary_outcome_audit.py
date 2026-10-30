import json
import tempfile
import unittest
from pathlib import Path

from experiments.EXP_003.adapters.registry import build_provider
from experiments.EXP_003.gate_orchestrator import load_plan, plan_arms, run_campaign
from experiments.EXP_003.manifest import build_manifest
from experiments.EXP_003.tools import corpus_audit
from experiments.EXP_003.tools.gate3b_primary_outcome_audit import audit_stage, direction, render_markdown
from tests.test_exp003_orchestrator import ANCHOR

CELLS = ["A/A/A", "A/A/B", "A/B/A", "A/B/B", "B/A/A", "B/A/B", "B/B/A", "B/B/B"]


def write_gate3b_test_plan(tmp: Path, worlds: int = 2) -> Path:
    gen = build_manifest(ANCHOR, "G3B_GEN001", "diamond", "single", worlds, None, None, {42})
    dual = build_manifest(ANCHOR, "G3B_DUAL001", "diamond", "dual", 0, 1, CELLS, {42})          # 8 worlds, one per cell
    solo = build_manifest(ANCHOR, "G3B_SOLO003", "solo", "single", 0, None, None, {42}, seeds_from=gen)
    off = build_manifest(ANCHOR, "G3B_PROBEOFF001", "diamond", "single", 0, None, None, {42}, seeds_from=gen, inherit_first=1)
    for name, m in (("gen", gen), ("dual", dual), ("solo", solo), ("off", off)):
        (tmp / f"{name}.json").write_text(json.dumps(m))
    arms = [
        {"stage": "set_001", "set_id": "diamond_set_001", "topology": "diamond", "root_mode": "single", "rounds": 4, "probe": True,
         "worlds": worlds, "manifest": "gen.json", "optional": False},
        {"stage": "set_001", "set_id": "dual_root_set_001", "topology": "diamond", "root_mode": "dual", "rounds": 4, "probe": True,
         "worlds": 8, "manifest": "dual.json", "optional": False},
        {"stage": "set_001", "set_id": "solo_control_set_003", "topology": "solo", "root_mode": "single", "rounds": 12, "probe": True,
         "worlds": worlds, "manifest": "solo.json", "optional": False},
        {"stage": "set_001", "set_id": "probe_off_set_001", "topology": "diamond", "root_mode": "single", "rounds": 4, "probe": False,
         "worlds": 1, "manifest": "off.json", "optional": False},
    ]
    plan = {"plan_version": "TEST3B", "gate": "3B", "status": "DRAFT",
            "anchors": {"frozen_runtime": None, "protocol_tag": "exp-003-protocol-v0.1", "plan_freeze_commit": None,
                        "gate3a_closure_checkpoint": None, "derivation_anchor": None},
            "controlled_configuration": {"provider": "openai", "model": "gpt-5.6-sol", "reasoning_effort": "medium",
                                         "execution_policy": "paired", "sensor_reliability": 0.7},
            "arms": arms}
    path = tmp / "plan.json"
    path.write_text(json.dumps(plan))
    return path


def run_stage(tmp: Path, stub_mode: str):
    plan_path = write_gate3b_test_plan(tmp)
    plan = load_plan(plan_path)
    root = tmp / "archive"
    run_campaign(plan, plan_path, plan_arms(plan, plan_path), build_provider("deterministic_stub", stub_mode=stub_mode),
                 archive_root=root, live=False, authorize_retry=False, max_worlds=None, include_optional=False)
    corpus = corpus_audit.audit_stage(plan_path, "set_001", root, preflight=True)
    out = tmp / "audits"
    out.mkdir()
    corpus_file = out / "EXP_003_GATE_3B_SET_001_CORPUS_AUDIT_v0.1.json"
    corpus_file.write_text(json.dumps(corpus, default=str))
    return plan_path, root, corpus_file


class DirectionTests(unittest.TestCase):
    def test_single_root_and_agreeing_two_root_use_favored_state_excess(self):
        self.assertEqual(direction(0.8, 0.7, "A")["kind"], "inflation")
        self.assertEqual(direction(0.2, 0.3, "B")["kind"], "inflation")
        self.assertEqual(direction(0.6, 0.7, "A")["kind"], "discount")
        two_root = 0.844828
        d = direction(0.93, two_root, "A")
        self.assertEqual(d["favored"], "A")
        self.assertAlmostEqual(d["certainty_excess"], 0.93 - two_root, places=5)
        self.assertEqual(direction(1 - two_root, 1 - two_root, "B")["kind"], "at_reference")

    def test_even_reference_has_no_direction_label(self):
        d = direction(0.62, 0.5, "A")
        self.assertEqual(d["kind"], "departure_from_even")
        self.assertIsNone(d["certainty_excess"])
        self.assertAlmostEqual(d["departure_toward_e1"], 0.12)
        self.assertAlmostEqual(direction(0.62, 0.5, "B")["departure_toward_e1"], -0.12)


class StageAuditTests(unittest.TestCase):
    def test_naive_stub_shows_fan_in_inflation_at_D_with_fis_and_clean_positive_control(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            plan_path, root, corpus_file = run_stage(tmp, "naive")
            report = audit_stage(plan_path, "set_001", root, corpus_file)
            self.assertEqual(report["status"], "COMPLETE", report["problems"])
            self.assertEqual(sorted(report["sets"]), ["diamond_set_001", "dual_root_set_001", "probe_off_set_001", "solo_control_set_003"])
            self.assertEqual(report["sets"]["dual_root_set_001"]["strata"], {"agreeing": 4, "conflicting": 4})
            d_free = report["arm_aggregates"]["diamond_set_001"]["conditions"]["free"]["None"]["D"]
            self.assertEqual(d_free["events"], 8)            # 4 D firings x 2 worlds
            self.assertGreater(d_free["inflation"], 0)       # the naive stub double counts at the fan-in
            self.assertGreater(d_free["fis_positive_events"], 0)
            e = report["expectations"]
            self.assertEqual(e["E1"]["verdict"], "consistent")
            self.assertIn(e["E3"]["verdict"], ("consistent", "contradicted"))
            self.assertIn("E7", e)
            self.assertEqual(len(report["probe_reactivity"]), 2)   # one shared world x two conditions
            self.assertEqual(len(report["matrix_by_world"]), 10)   # 2 diamond + 8 dual worlds
            for row in report["matrix_by_world"]:
                if row["stratum"] == "conflicting":
                    self.assertIsNone(row["lineage"]["mean_certainty_excess"])
                    self.assertIsNotNone(row["lineage"]["mean_departure_toward_e1"])
            secondary = report["secondary_inbound_naming"]
            self.assertNotIn("solo_control_set_003", secondary)
            self.assertEqual(sorted(secondary["dual_root_set_001"]["free"]), ["agreeing", "conflicting"])   # strata never pooled
            for stratum in ("agreeing", "conflicting"):
                d_tab = secondary["dual_root_set_001"]["free"][stratum]["D_by_inbound_naming_sensor"]
                self.assertEqual(sum(c["events"] for c in d_tab.values()), 16)   # 4 worlds x 4 D firings
            self.assertEqual(sorted(secondary["diamond_set_001"]["lineage"]), ["None"])
            md = render_markdown(report)
            self.assertIn("## Secondary: inbound messages naming the sensor", md)
            self.assertIn("| `dual_root_set_001` | free | conflicting | D |", md)
            self.assertNotIn(str(tmp), json.dumps({k: v for k, v in report.items() if k not in ("archive_root", "corpus_audit")}, default=str))

    def test_dedup_stub_stays_at_reference_under_lineage_and_e6_reads_the_probe_gap(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            plan_path, root, corpus_file = run_stage(tmp, "dedup")
            report = audit_stage(plan_path, "set_001", root, corpus_file)
            d_lin = report["arm_aggregates"]["diamond_set_001"]["conditions"]["lineage"]["None"]["D"]
            self.assertEqual(d_lin["inflation"] + d_lin["discount"], 0)
            self.assertEqual(report["expectations"]["E6"]["comparisons"], 2)
            agreeing = report["expectations"]["E5"]
            self.assertIn(agreeing["verdict"], ("consistent", "contradicted"))
            self.assertEqual(agreeing["agreeing_worlds"], 4)

    def test_refuses_without_passing_corpus_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            plan_path, root, corpus_file = run_stage(tmp, "dedup")
            failing = json.loads(corpus_file.read_text())
            failing["status"] = "FAIL"
            corpus_file.write_text(json.dumps(failing))
            with self.assertRaises(SystemExit):
                audit_stage(plan_path, "set_001", root, corpus_file)


if __name__ == "__main__":
    unittest.main()
