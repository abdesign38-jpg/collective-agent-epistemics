import json
import tempfile
import unittest
from pathlib import Path

from experiments.EXP_003.adapters.registry import build_provider
from experiments.EXP_003.gate_orchestrator import load_plan, plan_arms, run_campaign
from experiments.EXP_003.run import run_experiment, write_results
from experiments.EXP_003.tools.corpus_audit import audit_stage, expected_counts, render_markdown
from tests.test_exp003_orchestrator import write_test_plan


class ExpectedCountTests(unittest.TestCase):
    def test_counts_match_macro_stop_semantics(self):
        # (calls, events). Events = seed + macro events + one per call; macro events = 1 cycle x firings
        # per cycle (ring 4, bounce 5, dyad 3, solo 2, diamond 3; dual root mode runs 2 cycles).
        self.assertEqual(expected_counts("ring", 4, "single"), (25, 30))
        self.assertEqual(expected_counts("bounce", 3, "single"), (25, 31))
        self.assertEqual(expected_counts("dyad", 6, "single"), (25, 29))
        self.assertEqual(expected_counts("solo", 12, "single"), (25, 28))
        self.assertEqual(expected_counts("diamond", 4, "single"), (33, 39))
        self.assertEqual(expected_counts("diamond", 4, "shared"), (33, 39))
        # Diamond dual: E2 is held by C, which first fires in cycle 1, so MACRO stops after cycle 2.
        self.assertEqual(expected_counts("diamond", 4, "dual"), (33, 43))
        # Hives dual: E2 is held by A2, a seed-cycle sender, so MACRO stops after cycle 1.
        self.assertEqual(expected_counts("hives_bridged", 4, "shared"), (66, 78))
        self.assertEqual(expected_counts("hives_bridged", 4, "dual"), (66, 78))
        self.assertEqual(expected_counts("hives_isolated", 4, "dual"), (66, 78))

    def test_counts_match_the_runtime_for_every_planned_shape(self):
        # The formula must agree with what run.py actually archives, for every topology and
        # root mode a gate plan can request. Stub runs only; no outcome is inspected.
        binding = build_provider("deterministic_stub", stub_mode="dedup")
        shapes = [("ring", 4, "single"), ("bounce", 3, "single"), ("dyad", 6, "single"), ("solo", 12, "single"),
                  ("diamond", 4, "single"), ("diamond", 4, "shared"), ("diamond", 4, "dual"),
                  ("diamond_detached", 4, "single"), ("hives_bridged", 4, "shared"), ("hives_bridged", 4, "dual"),
                  ("hives_isolated", 4, "shared"), ("hives_isolated", 4, "dual")]
        for topology, rounds, root_mode in shapes:
            with self.subTest(topology=topology, root_mode=root_mode):
                experiment = run_experiment(1, rounds, 7, topology=topology, root_mode=root_mode,
                                            adapter_factory=binding.factory, adapter_name=binding.adapter_name,
                                            adapter_metadata=binding.metadata, run_class=binding.run_class,
                                            execution_policy="paired", probe=True, sensor_reliability=0.7)
                with tempfile.TemporaryDirectory() as tmp:
                    write_results(experiment, Path(tmp))
                    events = [line for line in (Path(tmp) / "events.jsonl").read_text().splitlines() if line.strip()]
                self.assertEqual(expected_counts(topology, rounds, root_mode)[1], len(events))


class CorpusAuditTests(unittest.TestCase):
    def test_audit_passes_on_a_complete_preflight_stage_and_reads_no_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            plan_path = write_test_plan(tmp, worlds=2, optional_arm=False)
            plan = load_plan(plan_path)
            arms = plan_arms(plan, plan_path)
            root = tmp / "archive"
            run_campaign(plan, plan_path, arms, build_provider("deterministic_stub", stub_mode="dedup"),
                         archive_root=root, live=False, authorize_retry=False, max_worlds=None, include_optional=False)
            report = audit_stage(plan_path, "set_001", root, preflight=True)
            self.assertEqual(report["status"], "PASS", report["problems"])
            self.assertEqual(report["totals"]["complete_worlds"], 4)
            self.assertEqual(report["totals"]["failure_records"], 0)
            # The boundary statement names the quantities it did NOT read; strip that fixed sentence
            # and check that nothing else in the report or markdown mentions an outcome.
            boundary = report["scientific_boundary"]
            scrubbed = {k: v for k, v in report.items() if k != "scientific_boundary"}
            text = (json.dumps(scrubbed) + render_markdown(report).replace(boundary, "")).lower()
            for forbidden in ("p_a", "confidence", "brier", "answer", "excess", "false_independent", "model_output", "agent_reported"):
                self.assertNotIn(forbidden, text.replace("plan_freeze", ""), forbidden)

    def test_audit_fails_on_tampered_raw_file_and_missing_world(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            plan_path = write_test_plan(tmp, worlds=2, optional_arm=False)
            plan = load_plan(plan_path)
            arms = plan_arms(plan, plan_path)[:1]
            root = tmp / "archive"
            run_campaign(plan, plan_path, arms, build_provider("deterministic_stub", stub_mode="dedup"),
                         archive_root=root, live=False, authorize_retry=False, max_worlds=None, include_optional=False)
            world_dirs = sorted((root / "gate_3a" / "bounce_set_001").iterdir())
            events = world_dirs[0] / "attempt_001" / "events.jsonl"
            events.write_text(events.read_text() + "\n")
            report = audit_stage(plan_path, "set_001", root, preflight=True)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any("hash mismatch" in p for p in report["problems"]))
            # The solo arm was never run: its worlds are missing.
            self.assertTrue(any("solo_control_set_001" in p and "do not match the manifest" in p for p in report["problems"]))

    def test_report_records_no_checkout_specific_path(self):
        # Audit records from different checkouts must compare equal apart from the timestamp,
        # so the archive root is recorded relative to the project root when it lies inside it.
        from experiments.EXP_003.gate_orchestrator import DEFAULT_ARCHIVE_ROOT, PROJECT_ROOT
        from experiments.EXP_003.tools.corpus_audit import portable_path
        self.assertEqual(portable_path(DEFAULT_ARCHIVE_ROOT), "experiments/EXP_003/results/archive")
        self.assertEqual(portable_path(PROJECT_ROOT / "experiments" / ".." / "experiments" / "EXP_003"), "experiments/EXP_003")
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            plan_path = write_test_plan(tmp, worlds=1, optional_arm=False)
            plan = load_plan(plan_path)
            arms = plan_arms(plan, plan_path)
            root = tmp / "archive"
            run_campaign(plan, plan_path, arms, build_provider("deterministic_stub"), archive_root=root, live=False,
                         authorize_retry=False, max_worlds=None, include_optional=False)
            report = audit_stage(plan_path, "set_001", root, preflight=True)
            # Outside the project root the path is kept, resolved, so the record is still truthful.
            self.assertEqual(report["archive_root"], root.resolve().as_posix())
            self.assertNotIn(str(PROJECT_ROOT), json.dumps({k: v for k, v in report.items() if k != "archive_root"}))

    def test_markdown_states_the_boundary_and_the_replication_rule(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            plan_path = write_test_plan(tmp, worlds=1, optional_arm=False)
            plan = load_plan(plan_path)
            arms = plan_arms(plan, plan_path)
            root = tmp / "archive"
            run_campaign(plan, plan_path, arms, build_provider("deterministic_stub"), archive_root=root, live=False,
                         authorize_retry=False, max_worlds=None, include_optional=False)
            md = render_markdown(audit_stage(plan_path, "set_001", root, preflight=True))
            self.assertIn("Scientific interpretation was **not performed**", md)
            self.assertIn("Replication start condition", md)
            self.assertIn("before any primary-outcome audit of Set 001", md)


if __name__ == "__main__":
    unittest.main()
