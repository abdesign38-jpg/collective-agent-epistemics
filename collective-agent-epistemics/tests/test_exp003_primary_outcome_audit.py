import json
import tempfile
import unittest
from pathlib import Path

from experiments.EXP_003.adapters.registry import build_provider
from experiments.EXP_003.gate_orchestrator import load_plan, plan_arms, run_campaign
from experiments.EXP_003.manifest import build_manifest
from experiments.EXP_003.run import run_experiment, write_results
from experiments.EXP_003.tools import corpus_audit
from experiments.EXP_003.tools.primary_outcome_audit import (
    EXP002_ARCHIVE,
    audit_stage,
    certainty_excess,
    classify,
    historical_runs,
    load_events,
    positions,
    render_markdown,
)
from experiments.EXP_003.world_generator import WorldGenerator, world_cell
from tests.test_exp003_orchestrator import ANCHOR

EXP002_GATE_2B_CORPUS_AUDIT = (Path(__file__).resolve().parents[1] / "experiments" / "EXP_002" / "audits" / "gate_2b"
                               / "corpus" / "EXP_002_GATE_2B_CORPUS_AUDIT_v0.1.json")


def write_four_arm_plan(tmp: Path, worlds: int = 2) -> Path:
    ring = build_manifest(ANCHOR, "G3A_RING001", "ring", "single", worlds, None, None, {42})
    arms = []
    manifests = {"ring": ring}
    for name, topology, rounds in (("solo", "solo", 12), ("dyad", "dyad", 6), ("bounce", "bounce", 3)):
        manifests[name] = build_manifest(ANCHOR, f"G3A_{name.upper()}001", topology, "single", 0, None, None, {42}, seeds_from=ring)
    for name, topology, rounds, set_id in (("ring", "ring", 4, "ring_control_set_001"), ("solo", "solo", 12, "solo_control_set_001"),
                                           ("dyad", "dyad", 6, "dyad_set_001"), ("bounce", "bounce", 3, "bounce_set_001")):
        (tmp / f"{name}.json").write_text(json.dumps(manifests[name]))
        arms.append({"set_id": set_id, "topology": topology, "root_mode": "single", "rounds": rounds, "probe": False,
                     "worlds": worlds, "manifest": f"{name}.json", "optional": False})
    plan = {"plan_version": "TEST", "gate": "3A", "status": "DRAFT",
            "anchors": {"frozen_runtime": None, "protocol_tag": "exp-003-protocol-v0.1", "plan_freeze_commit": None},
            "controlled_configuration": {"provider": "openai", "model": "gpt-5.6-sol", "reasoning_effort": "medium",
                                         "execution_policy": "paired", "sensor_reliability": 0.7},
            "arms": arms}
    path = tmp / "plan.json"
    path.write_text(json.dumps(plan))
    return path


def run_preflight_stage(tmp: Path, stub_mode: str, worlds: int = 2) -> tuple[Path, Path, Path]:
    """Stub-execute a four-arm stage, run the corpus audit on it, return (plan, archive root, corpus audit json)."""
    plan_path = write_four_arm_plan(tmp, worlds)
    plan = load_plan(plan_path)
    root = tmp / "archive"
    run_campaign(plan, plan_path, plan_arms(plan, plan_path), build_provider("deterministic_stub", stub_mode=stub_mode),
                 archive_root=root, live=False, authorize_retry=False, max_worlds=None, include_optional=False)
    corpus = corpus_audit.audit_stage(plan_path, "set_001", root, preflight=True)
    out = tmp / "audits"
    out.mkdir()
    corpus_file = out / "EXP_003_GATE_3A_SET_001_CORPUS_AUDIT_v0.1.json"
    corpus_file.write_text(json.dumps(corpus, default=str))
    return plan_path, root, corpus_file


class DirectionTests(unittest.TestCase):
    def test_certainty_excess_sign_convention(self):
        # Spec 4.1: positive = more certain than the evidence supports, in both observed states.
        self.assertAlmostEqual(certainty_excess(0.8, 0.7, "A"), 0.1)
        self.assertAlmostEqual(certainty_excess(0.2, 0.3, "B"), 0.1)   # raw excess −.10, but inflation
        self.assertAlmostEqual(certainty_excess(0.4, 0.3, "B"), -0.1)  # raw excess +.10, but discount
        self.assertAlmostEqual(certainty_excess(0.6, 0.7, "A"), -0.1)
        self.assertEqual(certainty_excess(0.7, 0.7, "A"), 0.0)
        self.assertEqual(certainty_excess(0.3, 0.3, "B"), 0.0)
        self.assertEqual(classify(0.0), "at_reference")
        self.assertEqual(classify(5e-7), "at_reference")
        self.assertEqual(classify(0.01), "inflation")
        self.assertEqual(classify(-0.01), "discount")


class PositionTests(unittest.TestCase):
    def _rows(self, topology: str, rounds: int):
        binding = build_provider("deterministic_stub", stub_mode="dedup")
        experiment = run_experiment(1, rounds, 7, topology=topology, root_mode="single", adapter_factory=binding.factory,
                                    adapter_name=binding.adapter_name, adapter_metadata=binding.metadata,
                                    run_class=binding.run_class, execution_policy="paired", probe=False, sensor_reliability=0.7)
        with tempfile.TemporaryDirectory() as tmp:
            write_results(experiment, Path(tmp))
            observed = world_cell(experiment.worlds[0]).split("/")[1]
            return load_events(Path(tmp) / "events.jsonl", observed)

    def test_hops_and_legs_match_the_specification_table(self):
        expected_hops = {"solo": (12, 1), "dyad": (6, 2), "ring": (4, 3), "bounce": (3, 4)}
        for topology, (rounds, hops) in expected_hops.items():
            with self.subTest(topology=topology):
                pos = positions(self._rows(topology, rounds)["free"], topology)
                self.assertEqual([e["hops"] for e in pos["A_post_seed"]], [hops] * rounds)
                self.assertEqual(pos["A_post_seed"][-1]["id"], "M13")
        bounce = positions(self._rows("bounce", 3)["lineage"], "bounce")
        self.assertEqual([(e["id"], e["leg"]) for e in bounce["by_agent"]["B"]],
                         [("M02", "outward"), ("M04", "return"), ("M06", "outward"), ("M08", "return"), ("M10", "outward"), ("M12", "return")])
        self.assertEqual([e["id"] for e in bounce["by_agent"]["C"]], ["M03", "M07", "M11"])
        ring = positions(self._rows("ring", 4)["lineage"], "ring")
        self.assertEqual([e["id"] for e in ring["by_agent"]["B"]], ["M02", "M05", "M08", "M11"])
        self.assertEqual([e["id"] for e in ring["by_agent"]["C"]], ["M03", "M06", "M09", "M12"])

    def test_stored_metrics_are_cross_checked_against_the_raw_model_output(self):
        # The audit recomputes p_a and the reference from the raw answer/confidence and the
        # world's root with the frozen runtime's functions. A stored metric that disagrees
        # with the raw output is flagged, never silently used.
        binding = build_provider("deterministic_stub", stub_mode="dedup")
        experiment = run_experiment(1, 4, 7, topology="ring", root_mode="single", adapter_factory=binding.factory,
                                    adapter_name=binding.adapter_name, adapter_metadata=binding.metadata,
                                    run_class=binding.run_class, execution_policy="paired", probe=False, sensor_reliability=0.7)
        with tempfile.TemporaryDirectory() as tmp:
            events_path = Path(tmp) / "events.jsonl"
            write_results(experiment, Path(tmp))
            observed = world_cell(experiment.worlds[0]).split("/")[1]
            clean = load_events(events_path, observed)
            self.assertTrue(all(not row["inconsistencies"] for rows in clean.values() for row in rows))
            records = [json.loads(line) for line in events_path.read_text().splitlines() if line.strip()]
            records[3]["metrics"]["p_a"] = 0.99  # tamper a stored metric, leave the raw output alone
            events_path.write_text("".join(json.dumps(r) + "\n" for r in records))
            tampered = load_events(events_path, observed)
            flagged = [row for rows in tampered.values() for row in rows if row["inconsistencies"]]
            self.assertEqual(len(flagged), 1)
            self.assertIn("stored p_a 0.99", flagged[0]["inconsistencies"][0])
            # The wrong observed state for the world is caught through the reference check.
            wrong = load_events(events_path, "A" if observed == "B" else "B")
            self.assertTrue(all(any("reference_p_a" in t for t in row["inconsistencies"]) for rows in wrong.values() for row in rows))

    def test_sustained_deviation_rule(self):
        def row(i, ce):
            return {"id": f"M{i:02d}", "sender": "A", "receivers": ["A"], "cycle": i, "certainty_excess": ce, "kind": classify(ce),
                    "inbound_agent_as_source": False}
        # Deviation, back to reference, deviation: never two consecutive → not sustained.
        pos = positions([row(1, 0.0), row(2, 0.1), row(3, 0.0), row(4, -0.1)], "solo")
        self.assertFalse(pos["A_sustained_deviation"])
        self.assertAlmostEqual(pos["A_restoration_rate"], 1 / 3, places=5)
        # Two consecutive deviations of the same sign → sustained, named at the second firing.
        pos = positions([row(1, 0.0), row(2, 0.1), row(3, 0.1)], "solo")
        self.assertTrue(pos["A_sustained_deviation"])
        self.assertEqual(pos["A_sustained_deviation_at"], ["M03"])
        # Two consecutive deviations of opposite sign → not sustained (direction changed).
        pos = positions([row(1, 0.0), row(2, 0.1), row(3, -0.1)], "solo")
        self.assertFalse(pos["A_sustained_deviation"])


class StageAuditTests(unittest.TestCase):
    def test_dedup_stub_stage_audits_end_to_end_and_records_no_checkout_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            plan_path, root, corpus_file = run_preflight_stage(tmp, "dedup")
            report = audit_stage(plan_path, "set_001", root, corpus_file)
            self.assertEqual(report["status"], "COMPLETE", report["problems"])
            self.assertEqual(sorted(report["sets"]), ["bounce_set_001", "dyad_set_001", "ring_control_set_001", "solo_control_set_001"])
            self.assertEqual(len(report["focal"]["paired_seeds"]), 2)
            self.assertEqual(len(report["focal"]["table_4_A_post_seed_all_arms"]), 2 * 4 * 2)
            self.assertEqual(len(report["focal"]["table_3_bounce_B_outward_vs_return"]), 2 * 2 * 3)
            self.assertEqual(len(report["family"]), 4 * 2 * 3)
            self.assertEqual(len(report["macro_boundary"]), 8)
            # The dedup stub covers each root once when envelopes are visible (LINEAGE: at the
            # reference everywhere) and behaves naively without them (FREE: the re-grounded
            # origin counts E1 twice and inflates). The audit must see exactly that.
            for set_id, agg in report["arm_aggregates"].items():
                lineage = agg["conditions"]["lineage"]
                for agent, rates in lineage["agents"].items():
                    self.assertEqual(rates["discount_events"] + rates["inflation_events"], 0, (set_id, agent))
                self.assertEqual(lineage["A_restoration_rate"], 1.0, set_id)
                self.assertEqual(lineage["worlds_with_sustained_A_deviation"], 0, set_id)
                free = agg["conditions"]["free"]
                self.assertGreater(free["agents"]["A"]["inflation_events"], 0, set_id)
                self.assertEqual(free["agents"]["A"]["discount_events"], 0, set_id)
            e = report["expectations"]
            self.assertEqual(e["E1"]["verdict"], "contradicted")  # FREE deviates; no LINEAGE discounts at B or C
            self.assertEqual(e["E2"]["verdict"], "contradicted")  # return magnitude equals outward (ties = not smaller)
            self.assertEqual(e["E3"]["verdict"], "contradicted")  # dyad B rate equals ring B rate (ties = not less)
            self.assertEqual(e["E4"]["verdict"], "contradicted")  # sustained A inflation under FREE
            self.assertEqual(e["E5"]["verdict"], "contradicted")  # solo inflates under FREE
            self.assertIn("synthesis", e["E6"]["verdict"])
            self.assertEqual(e["E1"]["ring_A_discount_events"], 0)
            self.assertEqual(e["E1"]["ring_LINEAGE_B_plus_C_discount_events"], 0)
            self.assertGreater(e["E1"]["ring_FREE_deviation_events"], 0)
            # Paths outside the project root are kept truthfully (this archive lives in a temp
            # dir); inside the project they are relative. Nothing else may carry a path.
            from experiments.EXP_003.gate_orchestrator import PROJECT_ROOT
            rest = {k: v for k, v in report.items() if k not in ("archive_root", "corpus_audit")}
            self.assertNotIn(str(tmp), json.dumps(rest, default=str))
            self.assertNotIn(str(PROJECT_ROOT), json.dumps(report, default=str) + render_markdown(report))
            self.assertEqual(report["corpus_audit"]["status"], "PASS")

    def test_naive_stub_shows_inflation_at_the_regrounded_origin(self):
        # The naive stub multiplies odds from every inbound message: A re-reading E1 while
        # receiving a descendant of E1 is counted twice (redundant root exposure 1). This is the
        # EXP-001-style measurement validation: the audit must see it as inflation at A.
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            plan_path, root, corpus_file = run_preflight_stage(tmp, "naive")
            report = audit_stage(plan_path, "set_001", root, corpus_file)
            for condition in ("free", "lineage"):
                ring = report["arm_aggregates"]["ring_control_set_001"]["conditions"][condition]
                self.assertGreater(ring["agents"]["A"]["inflation_events"], 0, condition)
                self.assertEqual(ring["A_restoration_rate"], 0.0, condition)
            self.assertEqual(report["expectations"]["E4"]["verdict"], "contradicted")
            self.assertEqual(report["expectations"]["E1"]["verdict"], "contradicted")

    def test_refuses_without_a_passing_corpus_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            plan_path, root, corpus_file = run_preflight_stage(tmp, "dedup", worlds=1)
            with self.assertRaises(SystemExit):
                audit_stage(plan_path, "set_001", root, tmp / "missing.json")
            failing = json.loads(corpus_file.read_text())
            failing["status"] = "FAIL"
            corpus_file.write_text(json.dumps(failing))
            with self.assertRaises(SystemExit):
                audit_stage(plan_path, "set_001", root, corpus_file)
            # A PASS record whose hashes no longer match the files is refused too.
            corpus_file.write_text(json.dumps({**failing, "status": "PASS"}))
            events = next((root / "gate_3a" / "ring_control_set_001").glob("*/attempt_001/events.jsonl"))
            events.write_text(events.read_text() + "\n")
            with self.assertRaises(SystemExit):
                audit_stage(plan_path, "set_001", root, corpus_file)


class HistoricalTests(unittest.TestCase):
    @unittest.skipUnless(EXP002_GATE_2B_CORPUS_AUDIT.exists(), "EXP-002 Gate 2B corpus audit not present")
    def test_generator_reproduces_gate_2b_truth_and_observed_state_from_the_seed(self):
        records = json.loads(EXP002_GATE_2B_CORPUS_AUDIT.read_text())["world_records"]
        self.assertEqual(len(records), 20)
        for w in records:
            world = WorldGenerator(int(w["seed"]), "ring", "single", 0.70).generate()
            self.assertEqual(world_cell(world), f"{w['truth']}/{w['observed_state']}", w["seed"])
        self.assertEqual(WorldGenerator(42, "ring", "single", 0.70).generate().truth, "A")

    @unittest.skipUnless(EXP002_ARCHIVE.exists(), "EXP-002 archive not present")
    def test_historical_runs_load_with_consistent_truth(self):
        runs = historical_runs(EXP002_ARCHIVE)
        self.assertEqual(len(runs), 36)
        self.assertEqual(len({r["seed"] for r in runs}), 21)
        self.assertEqual(sum(r["run_class"] == "gate_2b_real_model" for r in runs), 20)
        for r in runs:
            self.assertEqual(set(r["events"]), {"free", "lineage", "macro"})


if __name__ == "__main__":
    unittest.main()
