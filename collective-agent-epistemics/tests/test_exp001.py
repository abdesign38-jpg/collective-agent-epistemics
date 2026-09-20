import unittest
import json
from pathlib import Path

from experiments.EXP_001.run import load_worlds, run_condition

class Exp001Tests(unittest.TestCase):
    def test_free_mode_can_create_false_independent_support(self):
        world = [w for w in load_worlds() if w["world_id"] == "W1_single_root"][0]
        events, summary = run_condition(world, "free", rounds=2)
        self.assertGreater(summary["final_false_independent_support"], 0)
        self.assertEqual(summary["final_independent_roots"], 1)

    def test_lineage_mode_preserves_single_root(self):
        world = [w for w in load_worlds() if w["world_id"] == "W1_single_root"][0]
        events, summary = run_condition(world, "lineage", rounds=3)
        self.assertEqual(summary["final_independent_roots"], 1)
        self.assertEqual(summary["final_false_independent_support"], 0)

    def test_macro_stops_when_cycle_adds_no_new_root(self):
        world = [w for w in load_worlds() if w["world_id"] == "W1_single_root"][0]
        events, summary = run_condition(world, "macro", rounds=8)
        self.assertEqual(summary["completed_cycles"], 1)

    def test_free_mode_can_amplify_wrong_confidence(self):
        world = [w for w in load_worlds() if w["world_id"] == "W4_misleading_single_root"][0]
        _, free_summary = run_condition(world, "free", rounds=4)
        _, lineage_summary = run_condition(world, "lineage", rounds=4)
        self.assertEqual(free_summary["accuracy"], 0)
        self.assertGreater(free_summary["final_brier_score"], lineage_summary["final_brier_score"])
        self.assertGreater(free_summary["final_confidence"], lineage_summary["final_confidence"])

if __name__ == "__main__":
    unittest.main()
