import json
import tempfile
import unittest
from pathlib import Path

from experiments.EXP_003.adapters.registry import RUN_CLASS_SCIENTIFIC, build_provider
from experiments.EXP_003.gate_orchestrator import (
    GateIntegrityError,
    expected_actual_calls,
    load_plan,
    plan_arms,
    run_campaign,
    set_directory_name,
    verify_plan_and_manifest,
)
from experiments.EXP_003.manifest import build_manifest

HERE = Path(__file__).resolve().parent
EXP003 = HERE.parent / "experiments" / "EXP_003"
ANCHOR = "test-anchor|exp-003-protocol-v0.1|GATE_3A_PLAN_v0.1"


def write_test_plan(tmp: Path, worlds: int = 2, optional_arm: bool = True) -> Path:
    bounce = build_manifest(ANCHOR, "G3A_BOUNCE001", "bounce", "single", worlds, None, None, {42})
    solo = build_manifest(ANCHOR, "G3A_SOLO001", "solo", "single", 0, None, None, {42}, seeds_from=bounce)
    (tmp / "bounce.json").write_text(json.dumps(bounce))
    (tmp / "solo.json").write_text(json.dumps(solo))
    arms = [
        {"set_id": "bounce_set_001", "topology": "bounce", "root_mode": "single", "rounds": 3, "probe": False,
         "worlds": worlds, "manifest": "bounce.json", "optional": False},
        {"set_id": "solo_control_set_001", "topology": "solo", "root_mode": "single", "rounds": 12, "probe": False,
         "worlds": worlds, "manifest": "solo.json", "optional": optional_arm},
    ]
    plan = {
        "plan_version": "TEST", "gate": "3A", "status": "DRAFT",
        "anchors": {"frozen_runtime": None, "protocol_tag": "exp-003-protocol-v0.1", "plan_freeze_commit": None},
        "controlled_configuration": {"provider": "openai", "model": "gpt-5.6-sol", "reasoning_effort": "medium",
                                     "execution_policy": "paired", "sensor_reliability": 0.7},
        "arms": arms,
    }
    path = tmp / "plan.json"
    path.write_text(json.dumps(plan))
    return path


class FailingAfterTwoCalls:
    """Adapter that works for the first world's calls, then fails."""

    calls = 0

    def __init__(self):
        self.last_call_metadata = {}

    def respond(self, agent_id, observation, received_messages, condition):
        from experiments.EXP_003.adapters.deterministic_stub import DeterministicStubAdapter

        FailingAfterTwoCalls.calls += 1
        if FailingAfterTwoCalls.calls > 30:
            raise RuntimeError("synthetic provider failure")
        return DeterministicStubAdapter("dedup").respond(agent_id, observation, received_messages, condition)


class PlanTests(unittest.TestCase):
    def test_committed_plans_load_and_match_markdown_accounting(self):
        expected = {
            "GATE_3A_PLAN_v0.1.json": {"set_001": 1200, "set_002": 1200},
            "GATE_3B_PLAN_v0.1.json": {"set_001": 1356, "set_002": 924},
            "GATE_3C_PLAN_v0.1.json": {"set_001": 1596},
            "GATE_3D_PLAN_v0.1.json": {"set_001": 3168},
        }
        for name, totals in expected.items():
            plan = load_plan(EXP003 / name)
            arms = plan_arms(plan, EXP003 / name)
            self.assertEqual(plan["status"], "DRAFT", name)
            self.assertTrue(all(not a.optional for a in arms), f"{name}: no optional arms remain")
            for arm, raw in zip(arms, plan["arms"]):
                self.assertEqual(expected_actual_calls(arm), raw["calls_per_world"], f"{name}:{arm.set_id}")
            for stage, total in totals.items():
                self.assertEqual(sum(expected_actual_calls(a) * a.worlds for a in arms if a.stage == stage), total, f"{name}:{stage}")

    def test_gate_3a_set_001_is_four_matched_topologies_on_inherited_seeds(self):
        plan = load_plan(EXP003 / "GATE_3A_PLAN_v0.1.json")
        set_001 = [a for a in plan["arms"] if a["stage"] == "set_001"]
        self.assertEqual([a["topology"] for a in set_001], ["ring", "solo", "dyad", "bounce"])
        self.assertEqual([a["seeds_from"] for a in set_001], [None] + ["ring_control_set_001"] * 3)
        self.assertTrue(all(a["probe"] is False for a in set_001))

    def test_expected_calls_per_topology(self):
        plan = load_plan(EXP003 / "GATE_3A_PLAN_v0.1.json")
        arms = {a.set_id: a for a in plan_arms(plan, EXP003 / "GATE_3A_PLAN_v0.1.json")}
        for set_id in ("ring_control_set_001", "solo_control_set_001", "dyad_set_001", "bounce_set_001"):
            self.assertEqual(expected_actual_calls(arms[set_id]), 25, set_id)
        plan_d = load_plan(EXP003 / "GATE_3D_PLAN_v0.1.json")
        arms_d = {a.set_id: a for a in plan_arms(plan_d, EXP003 / "GATE_3D_PLAN_v0.1.json")}
        self.assertEqual(expected_actual_calls(arms_d["isolated_shared_root_set_001"]), 66)

    def test_plan_manifest_disagreement_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_test_plan(Path(tmp))
            plan = load_plan(path)
            arm = plan_arms(plan, path)[0]
            manifest = json.loads(arm.manifest.read_text())
            manifest["topology"] = "ring"
            with self.assertRaises(GateIntegrityError):
                verify_plan_and_manifest(plan, arm, manifest)
            manifest["topology"] = "bounce"
            manifest["model_calls_made"] = 3
            with self.assertRaises(GateIntegrityError):
                verify_plan_and_manifest(plan, arm, manifest)

    def test_inherited_manifest_shares_seeds_and_order(self):
        bounce = build_manifest(ANCHOR, "G3A_BOUNCE001", "bounce", "single", 3, None, None, set())
        solo = build_manifest(ANCHOR, "G3A_SOLO001", "solo", "single", 0, None, None, set(), seeds_from=bounce)
        self.assertEqual([w["seed"] for w in solo["worlds"]], [w["seed"] for w in bounce["worlds"]])
        self.assertEqual([w["execution_order"] for w in solo["worlds"]], [1, 2, 3])
        self.assertEqual(solo["selection"]["scheme"], "inherited")
        self.assertTrue(all(w["canonical_id"].startswith("E3_G3A_SOLO001_seed_") for w in solo["worlds"]))
        self.assertEqual([w["truth"] for w in solo["worlds"]], [w["truth"] for w in bounce["worlds"]])


class CampaignTests(unittest.TestCase):
    def _binding(self, mode="dedup"):
        return build_provider("deterministic_stub", stub_mode=mode)

    def test_preflight_campaign_archives_with_hashes_and_resumes(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            path = write_test_plan(tmp, worlds=2, optional_arm=False)
            plan = load_plan(path)
            arms = plan_arms(plan, path)
            root = tmp / "archive"
            dests = run_campaign(plan, path, arms, self._binding(), archive_root=root, live=False,
                                 authorize_retry=False, max_worlds=None, include_optional=False)
            self.assertEqual(len(dests), 4)
            for dest in dests:
                self.assertTrue((dest / "archive_metadata.json").exists())
                meta = json.loads((dest / "archive_metadata.json").read_text())
                self.assertEqual(meta["technical_integrity_status"], "pass")
                self.assertEqual(meta["fallback_events"], 0)
                self.assertIn("factors", meta)
                self.assertEqual(meta["factors"]["topology"], meta["topology"])
                for name in ("events.jsonl", "summary.csv", "run_metadata.json"):
                    self.assertTrue((dest / name).exists())
            self.assertTrue((root / "gate_3a" / "bounce_set_001").exists())
            self.assertTrue((root / "gate_3a" / "solo_control_set_001").exists())
            # Second invocation re-executes nothing, even with a zero cap on new executions.
            again = run_campaign(plan, path, arms, self._binding(), archive_root=root, live=False,
                                 authorize_retry=False, max_worlds=0, include_optional=False)
            self.assertEqual(len(again), 4)
            status = json.loads((root / "gate_3a" / "campaign_status.json").read_text())
            self.assertTrue(status["all_required_sets_complete"])
            self.assertTrue(all(s["closable"] for s in status["sets"].values()))
            self.assertEqual(json.loads((dests[0] / "archive_metadata.json").read_text())["run_class"], "gate_3a_preflight")

    def test_optional_arm_is_skipped_unless_included(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            path = write_test_plan(tmp, worlds=1, optional_arm=True)
            plan = load_plan(path)
            arms = plan_arms(plan, path)
            dests = run_campaign(plan, path, arms, self._binding(), archive_root=tmp / "a", live=False,
                                 authorize_retry=False, max_worlds=None, include_optional=False)
            self.assertEqual(len(dests), 1)
            dests = run_campaign(plan, path, arms, self._binding(), archive_root=tmp / "b", live=False,
                                 authorize_retry=False, max_worlds=None, include_optional=True)
            self.assertEqual(len(dests), 2)

    def test_max_worlds_caps_new_executions(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            path = write_test_plan(tmp, worlds=3, optional_arm=False)
            plan = load_plan(path)
            arms = plan_arms(plan, path)
            dests = run_campaign(plan, path, arms, self._binding(), archive_root=tmp / "a", live=False,
                                 authorize_retry=False, max_worlds=2, include_optional=False)
            self.assertEqual(len(dests), 2)

    def test_failure_is_preserved_and_stops_campaign_until_retry_authorized(self):
        FailingAfterTwoCalls.calls = 0
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            path = write_test_plan(tmp, worlds=2, optional_arm=False)
            plan = load_plan(path)
            arms = plan_arms(plan, path)[:1]
            binding = build_provider("deterministic_stub")
            failing = type(binding)(adapter_name="deterministic_stub:failing", factory=FailingAfterTwoCalls,
                                    metadata=binding.metadata, run_class=binding.run_class, live=False)
            root = tmp / "archive"
            with self.assertRaises(GateIntegrityError):
                run_campaign(plan, path, arms, failing, archive_root=root, live=False,
                             authorize_retry=False, max_worlds=None, include_optional=False)
            manifest = json.loads((tmp / "bounce.json").read_text())
            ordered = sorted(manifest["worlds"], key=lambda w: w["execution_order"])
            world_dirs = [root / "gate_3a" / "bounce_set_001" / w["canonical_id"] for w in ordered]
            self.assertEqual(len(world_dirs), 2)
            first_ok = (world_dirs[0] / "attempt_001" / "archive_metadata.json").exists()
            second_failed = (world_dirs[1] / "attempt_001" / "failure_metadata.json").exists()
            self.assertTrue(first_ok and second_failed)
            record = json.loads((world_dirs[1] / "attempt_001" / "failure_metadata.json").read_text())
            self.assertEqual(record["status"], "technical_failure")
            status = json.loads((root / "gate_3a" / "campaign_status.json").read_text())
            self.assertFalse(status["all_required_sets_complete"])
            self.assertEqual(status["sets"]["bounce_set_001"]["failed"], 1)
            # Without authorization the failed world blocks; with it, attempt_002 is created.
            with self.assertRaises(GateIntegrityError):
                run_campaign(plan, path, arms, self._binding(), archive_root=root, live=False,
                             authorize_retry=False, max_worlds=None, include_optional=False)
            dests = run_campaign(plan, path, arms, self._binding(), archive_root=root, live=False,
                                 authorize_retry=True, max_worlds=None, include_optional=False)
            self.assertTrue(str(dests[1]).endswith("attempt_002"))
            self.assertTrue((world_dirs[1] / "attempt_001" / "failure_metadata.json").exists())

    def test_live_requires_frozen_anchors(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            path = write_test_plan(tmp, worlds=1, optional_arm=False)
            plan = load_plan(path)
            arms = plan_arms(plan, path)
            with self.assertRaises(GateIntegrityError):
                run_campaign(plan, path, arms, self._binding(), archive_root=tmp / "a", live=True,
                             authorize_retry=False, max_worlds=None, include_optional=False)

    def test_model_layer_set_gets_provider_suffix(self):
        plan = load_plan(EXP003 / "GATE_3A_PLAN_v0.1.json")
        arm = plan_arms(plan, EXP003 / "GATE_3A_PLAN_v0.1.json")[0]
        openai = build_provider("openai", model="m", reasoning_effort="medium")
        anthropic = build_provider("anthropic", model="m", reasoning_effort="medium")
        stub = build_provider("deterministic_stub")
        self.assertEqual(set_directory_name(arm, plan, openai), "ring_control_set_001")
        self.assertEqual(set_directory_name(arm, plan, anthropic), "ring_control_set_001_anthropic")
        self.assertEqual(set_directory_name(arm, plan, stub), "ring_control_set_001")

    def test_committed_unchanged_check_accepts_relative_and_absolute_paths(self):
        """Regression: a relative plan path must not be re-rooted under its own directory."""
        import os
        import subprocess
        from experiments.EXP_003.gate_orchestrator import verify_committed_unchanged
        repo_file = Path(__file__).resolve().parents[1] / "experiments" / "EXP_002" / "protocol.md"
        self.assertTrue(repo_file.exists())
        inside_git = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=repo_file.parent,
                                    capture_output=True, text=True).stdout.strip() == "true"
        if not inside_git:
            self.skipTest("requires a git checkout; this tree is an export")
        verify_committed_unchanged(repo_file, "absolute")  # must not raise
        cwd = os.getcwd()
        try:
            os.chdir(repo_file.parents[2])  # collective-agent-epistemics/
            verify_committed_unchanged(Path("experiments/EXP_002/protocol.md"), "relative")  # must not raise
        finally:
            os.chdir(cwd)
        with self.assertRaises(GateIntegrityError):
            verify_committed_unchanged(Path(tempfile.gettempdir()) / "definitely-not-tracked.json", "untracked")

    def test_gate_specific_run_classes(self):
        from experiments.EXP_003.gate_orchestrator import run_class_for
        self.assertEqual(run_class_for("3A", True), "gate_3a_real_model")
        self.assertEqual(run_class_for("3B", False), "gate_3b_preflight")
        self.assertEqual(RUN_CLASS_SCIENTIFIC, "pilot_real_model")

    def test_max_worlds_pause_does_not_count_completed_worlds(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            path = write_test_plan(tmp, worlds=3, optional_arm=False)
            plan = load_plan(path)
            arms = plan_arms(plan, path)[:1]
            root = tmp / "a"
            first = run_campaign(plan, path, arms, self._binding(), archive_root=root, live=False,
                                 authorize_retry=False, max_worlds=2, include_optional=False)
            self.assertEqual(len(first), 2)
            second = run_campaign(plan, path, arms, self._binding(), archive_root=root, live=False,
                                  authorize_retry=False, max_worlds=1, include_optional=False)
            self.assertEqual(len(second), 3)
            status = json.loads((root / "gate_3a" / "campaign_status.json").read_text())
            self.assertTrue(status["sets"]["bounce_set_001"]["closable"])


if __name__ == "__main__":
    unittest.main()
