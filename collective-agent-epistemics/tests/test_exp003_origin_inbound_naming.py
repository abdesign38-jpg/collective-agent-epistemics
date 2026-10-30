import tempfile
import unittest
from pathlib import Path

from experiments.EXP_003.tools.origin_inbound_naming import render, tabulate
from tests.test_exp003_primary_outcome_audit import run_preflight_stage


class OriginInboundNamingTests(unittest.TestCase):
    def test_tabulates_every_post_seed_origin_firing_of_the_arms_that_receive_messages(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, root, _ = run_preflight_stage(Path(tmp), "dedup", worlds=2)
            table = tabulate(root)
            sets = {key.split("|")[0] for key in table}
            self.assertEqual(sets, {"dyad_set_001", "ring_control_set_001", "bounce_set_001"})  # solo excluded
            # A fires after the seed 6 (dyad), 4 (ring), 3 (bounce) times per condition per world; 2 worlds.
            for set_id, per_world in (("dyad_set_001", 6), ("ring_control_set_001", 4), ("bounce_set_001", 3)):
                for condition in ("free", "lineage"):
                    total = sum(sum(v.values()) for k, v in table.items() if k.startswith(f"{set_id}|{condition}|"))
                    self.assertEqual(total, per_world * 2, (set_id, condition))
            for counts in table.values():
                self.assertTrue(set(counts) <= {"inflation", "at_reference", "discount"})
            markdown = render(table)
            self.assertIn("| Set | Condition | Inbound names the sensor |", markdown)
            self.assertEqual(markdown.count("\n"), len(table) + 1)


if __name__ == "__main__":
    unittest.main()
