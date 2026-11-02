import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from experiments.EXP_003.adapters.registry import build_provider
from experiments.EXP_003.gate_orchestrator import load_plan, plan_arms, run_campaign
from experiments.EXP_003.manifest import build_manifest
from experiments.EXP_003.tools import corpus_audit
from experiments.EXP_003.tools.gate3c_primary_outcome_audit import (
    TwinRef,
    audit_stage,
    default_twins,
    prompt_skeleton,
    render_markdown,
)
from experiments.EXP_003.tools.gate3c_synthesis import render_markdown as render_synthesis
from experiments.EXP_003.tools.gate3c_synthesis import synthesize
from tests.test_exp003_gate3b_primary_outcome_audit import run_stage as run_gate3b_stage
from tests.test_exp003_orchestrator import ANCHOR
from tests.test_exp003_primary_outcome_audit import run_preflight_stage as run_gate3a_stage

DETACHED = (("ring", 4), ("solo", 12), ("dyad", 6), ("bounce", 3))
GATE3A_TWIN = {"ring": "ring_control", "solo": "solo_control", "dyad": "dyad", "bounce": "bounce"}


def build_fixture(tmp: Path, stub_mode: str) -> dict:
    """Stub Gate 3A (twins and drift gauge), stub Gate 3B (diamond twin), then a two-stage stub Gate 3C
    on the same worlds, all under one archive root. Returns paths and twin maps for both stages."""
    (tmp / "g3a").mkdir()
    (tmp / "g3b").mkdir()
    a_plan, a_root, a_corpus = run_gate3a_stage(tmp / "g3a", stub_mode, worlds=2)
    b_plan, b_root, b_corpus = run_gate3b_stage(tmp / "g3b", stub_mode)
    root = tmp / "archive"
    shutil.copytree(a_root / "gate_3a", root / "gate_3a")
    shutil.copytree(b_root / "gate_3b", root / "gate_3b")
    ring = json.loads((tmp / "g3a" / "ring.json").read_text())
    gen = json.loads((tmp / "g3b" / "gen.json").read_text())
    arms = []
    for stage in ("set_001", "set_002"):
        for base, rounds in DETACHED:
            m = build_manifest(ANCHOR, f"G3C_{base.upper()}DET{stage[-3:]}", f"{base}_detached", "single", 0, None, None, {42}, seeds_from=ring)
            (tmp / f"{base}_det_{stage}.json").write_text(json.dumps(m))
            arms.append({"stage": stage, "set_id": f"{base}_detached_{stage}", "topology": f"{base}_detached", "root_mode": "single",
                         "rounds": rounds, "probe": False, "worlds": 2, "manifest": f"{base}_det_{stage}.json", "optional": False})
        m = build_manifest(ANCHOR, f"G3C_DIAMONDDET{stage[-3:]}", "diamond_detached", "single", 0, None, None, {42}, seeds_from=gen)
        (tmp / f"diamond_det_{stage}.json").write_text(json.dumps(m))
        arms.append({"stage": stage, "set_id": f"diamond_detached_{stage}", "topology": "diamond_detached", "root_mode": "single",
                     "rounds": 4, "probe": True, "worlds": 2, "manifest": f"diamond_det_{stage}.json", "optional": False})
    for base, rounds in DETACHED:
        m = build_manifest(ANCHOR, f"G3C_{base.upper()}CTL001", base, "single", 0, None, None, {42}, seeds_from=ring)
        (tmp / f"{base}_ctl.json").write_text(json.dumps(m))
        arms.append({"stage": "set_001", "set_id": f"{base}_contemporary_set_001", "topology": base, "root_mode": "single",
                     "rounds": rounds, "probe": False, "worlds": 2, "manifest": f"{base}_ctl.json", "optional": False})
    plan = {"plan_version": "TEST3C", "gate": "3C", "status": "DRAFT",
            "anchors": {"gate3a_closure_checkpoint": None, "gate3b_closure_checkpoint": None, "frozen_runtime": None,
                        "protocol_tag": "exp-003-protocol-v0.1", "plan_freeze_commit": None, "derivation_anchor": None},
            "controlled_configuration": {"provider": "openai", "model": "gpt-5.6-sol", "reasoning_effort": "medium",
                                         "execution_policy": "paired", "sensor_reliability": 0.7},
            "arms": arms}
    plan_path = tmp / "plan.json"
    plan_path.write_text(json.dumps(plan))
    loaded = load_plan(plan_path)
    all_arms = plan_arms(loaded, plan_path)
    out = tmp / "audits"
    out.mkdir()
    corpus_files = {}
    for stage in ("set_001", "set_002"):
        run_campaign(loaded, plan_path, [a for a in all_arms if a.stage == stage], build_provider("deterministic_stub", stub_mode=stub_mode),
                     archive_root=root, live=False, authorize_retry=False, max_worlds=None, include_optional=False)
        corpus = corpus_audit.audit_stage(plan_path, stage, root, preflight=True)
        corpus_files[stage] = out / f"EXP_003_GATE_3C_{stage.upper()}_CORPUS_AUDIT_v0.1.json"
        corpus_files[stage].write_text(json.dumps(corpus, default=str))
    twins = {
        "set_001": {**{f"{b}_detached_set_001": TwinRef("gate_3c", f"{b}_contemporary_set_001", corpus_files["set_001"], "contemporary") for b, _ in DETACHED},
                    "diamond_detached_set_001": TwinRef("gate_3b", "diamond_set_001", b_corpus, "historical"),
                    "ring_contemporary_set_001": TwinRef("gate_3a", "ring_control_set_001", a_corpus, "historical")},
        "set_002": {**{f"{b}_detached_set_002": TwinRef("gate_3a", f"{GATE3A_TWIN[b]}_set_001", a_corpus, "historical") for b, _ in DETACHED},
                    "diamond_detached_set_002": TwinRef("gate_3b", "diamond_set_001", b_corpus, "historical")},
    }
    return {"plan": plan_path, "root": root, "corpus": corpus_files, "twins": twins}


class HelperTests(unittest.TestCase):
    def test_default_twins_cover_every_detached_arm_and_the_gauge(self):
        t1 = default_twins("set_001", Path("/x"))
        self.assertEqual(set(t1), {"ring_detached_set_001", "solo_detached_set_001", "dyad_detached_set_001", "bounce_detached_set_001",
                                   "diamond_detached_set_001", "ring_contemporary_set_001"})
        self.assertEqual(t1["diamond_detached_set_001"].gate_dir, "gate_3b")
        self.assertEqual(t1["ring_contemporary_set_001"].set_id, "ring_control_set_001")
        t2 = default_twins("set_002", Path("/x"))
        self.assertTrue(all(v.kind == "historical" for v in t2.values()))
        self.assertEqual(len(t2), 5)

    def test_prompt_skeleton_ignores_the_observation_block(self):
        a = "You are Agent A.\n\nTask.\n\nDirect observation:\nSource: sensor_1\nObserved state: A\nReported reliability: 0.70\n\nReceived message:\nSender: Agent C\nMessage: x"
        b = "You are Agent A.\n\nTask.\n\nDirect observation: none\n\nReceived message:\nSender: Agent C\nMessage: y"
        self.assertEqual(prompt_skeleton(a), prompt_skeleton(b))


class StageAuditTests(unittest.TestCase):
    def test_naive_stub_shows_displacement_and_a_clean_detached_origin(self):
        with tempfile.TemporaryDirectory() as tmp:
            fx = build_fixture(Path(tmp), "naive")
            report = audit_stage(fx["plan"], "set_001", fx["root"], fx["corpus"]["set_001"], fx["twins"]["set_001"])
            self.assertEqual(report["status"], "COMPLETE", report["problems"])
            self.assertEqual(len(report["arms"]), 9)
            self.assertEqual({m["status"] for m in report["manipulation_check"].values()}, {"PASS"})
            self.assertEqual(len(report["manipulation_check"]), 5)
            # Deterministic stub: the seed firing is identical in detached and twin executions.
            for sc in report["seed_comparability"].values():
                self.assertEqual(sc["distribution"]["zero"], sc["worlds"])
                self.assertTrue(all(r["message_identical"] for r in sc["rows"]))
            # Drift gauge compares the stub Gate 3A ring with the stub contemporary ring on the same seeds: identical.
            g = report["drift_gauge"]
            self.assertEqual(g["status"], "PASS")
            self.assertTrue(all(p["difference"] == 0 for p in g["positions_lineage_deviation_counts"].values()))
            # The naive re-grounded twin inflates at the origin; the detached origin has no evidence to double count.
            e6 = report["arms"]["ring_detached_set_001"]["E6"]
            self.assertEqual(e6["verdict"], "consistent")
            self.assertEqual(e6["frequency_tier"], 1)
            self.assertGreater(e6["twin_lineage"]["events"], 0)
            self.assertIsNone(report["arms"]["ring_detached_set_001"]["E6"]["detached_lineage"]["fis_positive_at_events"])  # probe off
            self.assertIsNotNone(report["arms"]["diamond_detached_set_001"]["E6"]["detached_lineage"]["fis_positive_at_events"])
            # Material paired displacement in the ring: twin trajectories inflate, detached ones do not.
            ring = report["arms"]["ring_detached_set_001"]
            self.assertEqual(ring["paired"]["lineage"]["E3a_verdict"], "consistent")
            self.assertEqual(ring["paired"]["lineage"]["worlds_paired"], 2)
            for pw in ring["paired"]["lineage"]["worlds"].values():
                self.assertEqual(pw["matched_positions"], 12)   # 4 cycles x 3 firings
            self.assertEqual(set(report["expectations"]), {"E1", "E2", "E3a", "E3b", "E4", "E5", "E6", "E7"})
            self.assertIn(report["expectations"]["E5"]["verdict"], ("consistent", "contradicted", "not assessable"))
            self.assertEqual(report["expectations"]["E5"]["required_order"], ["ring", "bounce", "dyad", "solo"])
            self.assertIn("within_agent", ring)
            traj = next(iter(ring["within_agent"].values()))["lineage"]["A"]
            self.assertEqual(len(traj), 5)                     # seed + 4 post-seed A firings
            self.assertIsNone(traj[0]["delta_within_agent"])
            md = render_markdown(report)
            self.assertIn("## Drift gauge", md)
            self.assertIn("## Origin after lineage return (E6, strict H1)", md)
            self.assertNotIn(str(tmp), json.dumps({k: v for k, v in report.items() if k not in ("archive_root", "corpus_audit", "twin_corpus_audits")}, default=str))

    def test_dedup_stub_has_no_displacement_and_passes_the_solo_null(self):
        with tempfile.TemporaryDirectory() as tmp:
            fx = build_fixture(Path(tmp), "dedup")
            report = audit_stage(fx["plan"], "set_001", fx["root"], fx["corpus"]["set_001"], fx["twins"]["set_001"])
            self.assertEqual(report["status"], "COMPLETE", report["problems"])
            ring = report["arms"]["ring_detached_set_001"]
            self.assertEqual(ring["paired"]["lineage"]["E3a_verdict"], "contradicted")   # detached == twin under dedup
            self.assertEqual(ring["paired"]["lineage"]["worlds_with_material_displacement"], 0)
            self.assertEqual(report["arms"]["solo_detached_set_001"]["E4"]["verdict"], "consistent")
            self.assertEqual(report["expectations"]["E4"]["verdict"], "consistent")
            self.assertEqual(report["arms"]["ring_detached_set_001"]["E6"]["verdict"], "consistent")

    def test_set_002_uses_historical_twins_and_the_synthesis_assesses_e7(self):
        with tempfile.TemporaryDirectory() as tmp:
            fx = build_fixture(Path(tmp), "naive")
            s1 = audit_stage(fx["plan"], "set_001", fx["root"], fx["corpus"]["set_001"], fx["twins"]["set_001"])
            s2 = audit_stage(fx["plan"], "set_002", fx["root"], fx["corpus"]["set_002"], fx["twins"]["set_002"])
            self.assertEqual(s2["status"], "COMPLETE", s2["problems"])
            self.assertIsNone(s2["drift_gauge"])
            self.assertEqual({e["twin"]["kind"] for e in s2["arms"].values()}, {"historical"})
            report = synthesize({"set_001": s1, "set_002": s2}, {"set_001": {"path": "a", "sha256": "0"}, "set_002": {"path": "b", "sha256": "1"}},
                                corpus={"set_001": json.loads(fx["corpus"]["set_001"].read_text()), "set_002": json.loads(fx["corpus"]["set_002"].read_text())})
            e7 = report["expectations"]["E7"]
            self.assertEqual(len(e7["cells"]), 10)
            self.assertEqual(e7["verdict"], "consistent")    # same stub, same seeds: identical directions
            self.assertEqual(report["expectations"]["E3a"]["standing"]["set_002"], "qualified (historical twins)")
            self.assertEqual(report["expectations"]["E2"]["standing"]["set_002"], "primary (within-detached)")
            self.assertIn("set_002", report["set_002_paired_qualified"]["verdicts"])
            self.assertTrue(report["closure_rule"]["manipulation check passed in every detached arm"].startswith("yes"))
            self.assertTrue(report["closure_rule"]["drift gauge recorded"].startswith("yes: PASS"))
            # A reversed cell contradicts E7 and is named.
            flipped = copy.deepcopy(s2)
            sid, arm = next((sid, e) for sid, e in flipped["arms"].items() if e["detached"] and e["base"] == "ring")
            v = arm["far"]["lineage"]["far_stage_mean_excess"]
            arm["far"]["lineage"]["far_stage_mean_excess"] = -0.05 if (v or 0) >= 0 else 0.05
            s1_pos = copy.deepcopy(s1)
            s1_pos["arms"]["ring_detached_set_001"]["far"]["lineage"]["far_stage_mean_excess"] = 0.05 if (v or 0) >= 0 else -0.05
            bad = synthesize({"set_001": s1_pos, "set_002": flipped})
            self.assertEqual(bad["expectations"]["E7"]["verdict"], "contradicted")
            self.assertEqual(bad["expectations"]["E7"]["reversed_cells"], ["ring_lineage"])
            self.assertIn("## Set 002 paired verdicts (historical controls, qualified)", render_synthesis(report))

    def test_refuses_without_passing_corpus_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            fx = build_fixture(Path(tmp), "dedup")
            failing = json.loads(fx["corpus"]["set_001"].read_text())
            failing["status"] = "FAIL"
            fx["corpus"]["set_001"].write_text(json.dumps(failing))
            with self.assertRaises(SystemExit):
                audit_stage(fx["plan"], "set_001", fx["root"], fx["corpus"]["set_001"], fx["twins"]["set_001"])


if __name__ == "__main__":
    unittest.main()
