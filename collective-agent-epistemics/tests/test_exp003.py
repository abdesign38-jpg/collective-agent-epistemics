import json
import tempfile
import unittest
from pathlib import Path

from experiments.EXP_003.adapters.deterministic_stub import DeterministicStubAdapter
from experiments.EXP_003.lineage import LineageGraph
from experiments.EXP_003.manifest import build_manifest, candidate_seed
from experiments.EXP_003.metrics import (
    brier_score,
    false_independent_support,
    probability_of_a,
    reference_probability_of_a,
)
from experiments.EXP_003.models import AgentMessage, AgentObservation, Evidence
from experiments.EXP_003.prompting import render_agent_input
from experiments.EXP_003.provenance import erosion, score_message
from experiments.EXP_003.run import run_condition, run_experiment, write_results
from experiments.EXP_003.topology import TOPOLOGIES, get_topology
from experiments.EXP_003.world_generator import WorldGenerator, generate_world, world_cell

E1_A = Evidence("E1", "A", "sensor_1", 0.70, ("A",))
E2_A = Evidence("E2", "A", "sensor_2", 0.70, ("C",))
E2_B = Evidence("E2", "B", "sensor_2", 0.70, ("C",))

SEED_42_DIAMOND = generate_world(42, "diamond", "single", world_id="w")


class RecordingAdapter(DeterministicStubAdapter):
    def __init__(self, mode="naive"):
        super().__init__(mode)
        self.calls = []

    def respond(self, agent_id, observation, received_messages, condition):
        self.calls.append((agent_id, observation, received_messages))
        return super().respond(agent_id, observation, received_messages, condition)


class TopologyTests(unittest.TestCase):
    def test_ring_reproduces_exp002_sequence(self):
        world = generate_world(42, "ring", "single", world_id="w")
        result = run_condition(world, "free", rounds=2)
        self.assertEqual(
            [(e.sender, e.receivers) for e in result.events],
            [("A", ("B",)), ("B", ("C",)), ("C", ("A",)), ("A", ("B",)),
             ("B", ("C",)), ("C", ("A",)), ("A", ("B",))],
        )
        self.assertEqual(max(e.actual_lineage.redundant_root_exposures for e in result.events), 1)

    def test_diamond_gives_d_two_inbound_messages(self):
        adapter = RecordingAdapter()
        run_condition(SEED_42_DIAMOND, "free", rounds=1, adapter=adapter)
        d_calls = [c for c in adapter.calls if c[0] == "D"]
        self.assertEqual(len(d_calls), 1)
        self.assertEqual([m.sender for m in d_calls[0][2]], ["B", "C"])

    def test_diamond_firing_order_and_ids(self):
        result = run_condition(SEED_42_DIAMOND, "lineage", rounds=1)
        self.assertEqual([e.sender for e in result.events], ["A", "B", "C", "D", "A"])
        self.assertEqual([e.visible_message_id for e in result.events], ["M01", "M02", "M03", "M04", "M05"])
        d_event = result.events[3]
        self.assertEqual(d_event.actual_lineage.derived_from, ("M02", "M03"))
        self.assertEqual(d_event.actual_lineage.inference_depth, 2)
        self.assertEqual(d_event.actual_lineage.actual_roots, ("E1",))
        self.assertEqual(d_event.actual_lineage.redundant_root_exposures, 1)

    def test_regrounded_a_sees_evidence_every_firing(self):
        adapter = RecordingAdapter()
        run_condition(SEED_42_DIAMOND, "free", rounds=2, adapter=adapter)
        a_calls = [c for c in adapter.calls if c[0] == "A"]
        self.assertEqual(len(a_calls), 3)
        self.assertTrue(all(len(obs.evidence) == 1 for _, obs, _ in a_calls))

    def test_detached_a_sees_evidence_once(self):
        world = generate_world(42, "diamond_detached", "single", world_id="w")
        adapter = RecordingAdapter()
        run_condition(world, "free", rounds=2, adapter=adapter)
        a_calls = [c for c in adapter.calls if c[0] == "A"]
        self.assertEqual([len(obs.evidence) for _, obs, _ in a_calls], [1, 0, 0])
        # Detachment does not change hidden lineage: E1 remains the only root.
        result = run_condition(world, "free", rounds=2)
        self.assertEqual({e.actual_lineage.actual_roots for e in result.events}, {("E1",)})

    def test_solo_control_reads_its_own_message(self):
        world = generate_world(42, "solo", "single", world_id="w")
        adapter = RecordingAdapter()
        run_condition(world, "free", rounds=2, adapter=adapter)
        self.assertEqual([c[0] for c in adapter.calls], ["A", "A", "A"])
        self.assertEqual([m.sender for m in adapter.calls[1][2]], ["A"])

    def test_bridged_hives_cross_feed_source_agents(self):
        world = generate_world(42, "hives_bridged", "shared", world_id="w")
        adapter = RecordingAdapter()
        run_condition(world, "free", rounds=1, adapter=adapter)
        a1_second = [c for c in adapter.calls if c[0] == "A1"][1]
        self.assertEqual(sorted(m.sender for m in a1_second[2]), ["D1", "D2"])
        result = run_condition(world, "lineage", rounds=1)
        a1_event = [e for e in result.events if e.sender == "A1"][1]
        # own E1 + D1{E1} + D2{E1} = three exposures of one root
        self.assertEqual(a1_event.actual_lineage.redundant_root_exposures, 2)
        self.assertEqual(a1_event.actual_lineage.actual_roots, ("E1",))

    def test_dyad_alternates_and_everyone_meets_source(self):
        world = generate_world(42, "dyad", "single", world_id="w")
        result = run_condition(world, "free", rounds=2)
        self.assertEqual([(e.sender, e.receivers) for e in result.events],
                         [("A", ("B",)), ("B", ("A",)), ("A", ("B",)), ("B", ("A",)), ("A", ("B",))])
        self.assertEqual(max(e.actual_lineage.redundant_root_exposures for e in result.events), 1)

    def test_bounce_reverses_return_path_and_isolates_c(self):
        world = generate_world(42, "bounce", "single", world_id="w")
        result = run_condition(world, "free", rounds=1)
        self.assertEqual([(e.sender, e.receivers) for e in result.events],
                         [("A", ("B",)), ("B", ("C",)), ("C", ("B",)), ("B", ("A",)), ("A", ("B",))])
        receivers_of_c = {r for e in result.events if e.sender == "C" for r in e.receivers}
        self.assertEqual(receivers_of_c, {"B"})
        # No fan-in anywhere: only A's own-evidence-plus-echo redundancy, exactly as in the ring.
        self.assertEqual(max(e.actual_lineage.redundant_root_exposures for e in result.events), 1)
        self.assertEqual([e.actual_lineage.inference_depth for e in result.events], [0, 1, 2, 3, 4])

    def test_bounce_matches_ring_in_calls_and_depth(self):
        from experiments.EXP_003.topology import ROUNDS_FOR_DEPTH_12
        for name in ("ring", "bounce", "dyad", "solo"):
            world = generate_world(42, name, "single", world_id="w")
            result = run_condition(world, "free", rounds=ROUNDS_FOR_DEPTH_12[name])
            self.assertEqual(len(result.events), 13, name)
            self.assertEqual(result.summary["max_inference_depth"], 12, name)

    def test_per_agent_summary_fields(self):
        world = generate_world(42, "bounce", "single", world_id="w")
        result = run_condition(world, "lineage", rounds=1, adapter=DeterministicStubAdapter("dedup"))
        self.assertEqual(set(result.summary["per_agent_final_p_a"]), {"A", "B", "C"})
        self.assertTrue(all(abs(v) < 1e-6 for v in result.summary["per_agent_max_excess"].values()))

    def test_isolated_hives_differ_from_bridged_only_by_the_bridge(self):
        from experiments.EXP_003.topology import HIVES_BRIDGED, HIVES_ISOLATED
        bridged = {(f.sender, r) for f in HIVES_BRIDGED.recursive_cycle for r in f.receivers}
        isolated = {(f.sender, r) for f in HIVES_ISOLATED.recursive_cycle for r in f.receivers}
        self.assertEqual(bridged - isolated, {("D1", "A2"), ("D2", "A1")})
        self.assertEqual(isolated - bridged, set())
        world = generate_world(42, "hives_isolated", "shared", world_id="w")
        result = run_condition(world, "lineage", rounds=1)
        a1_second = [e for e in result.events if e.sender == "A1"][1]
        # own E1 + D1{E1} only: one redundant exposure, versus two under the bridge
        self.assertEqual(a1_second.actual_lineage.redundant_root_exposures, 1)
        self.assertEqual(len(result.events), 10)

    def test_every_topology_runs_all_conditions(self):
        for name in TOPOLOGIES:
            topo = get_topology(name)
            root_mode = "single" if not topo.secondary_sources else "dual"
            experiment = run_experiment(trials=1, rounds=1, seed=3, topology=name, root_mode=root_mode)
            self.assertEqual(len(experiment.condition_runs), 3, name)


class LineageTests(unittest.TestCase):
    def test_multi_parent_union_and_depth(self):
        graph = LineageGraph()
        graph.record_message("a", (), {"E1"})
        graph.record_message("b", ("a",), set())
        graph.record_message("c", ("a",), {"E2"})
        env = graph.record_message("d", ("b", "c"), set())
        self.assertEqual(env.actual_roots, ("E1", "E2"))
        self.assertEqual(env.inference_depth, 2)
        # b{E1} + c{E1,E2} = 3 exposures, 2 distinct roots
        self.assertEqual(env.redundant_root_exposures, 1)
        self.assertEqual(graph.ancestry("d"), ["a", "b", "c", "d"])

    def test_recursion_never_creates_roots(self):
        result = run_condition(SEED_42_DIAMOND, "free", rounds=4)
        self.assertEqual(result.summary["new_independent_evidence_count"], 1)
        self.assertEqual(result.summary["independent_evidence_root_count"], 1)

    def test_dual_root_world_registers_second_root_when_c_fires(self):
        world = generate_world(42, "diamond", "dual", world_id="w")
        result = run_condition(world, "lineage", rounds=1)
        c_event = result.events[2]
        self.assertEqual(c_event.actual_lineage.actual_roots, ("E1", "E2"))
        self.assertEqual(c_event.metrics["new_independent_evidence"], 1)
        self.assertEqual(result.summary["independent_evidence_root_count"], 2)


class MetricTests(unittest.TestCase):
    def test_reference_single_root(self):
        self.assertEqual(reference_probability_of_a((E1_A,)), 0.7)
        self.assertEqual(reference_probability_of_a((Evidence("E1", "B", "s", 0.70, ("A",)),)), 0.3)

    def test_reference_two_agreeing_and_conflicting_roots(self):
        self.assertAlmostEqual(reference_probability_of_a((E1_A, E2_A)), 49 / 58, places=5)
        self.assertAlmostEqual(reference_probability_of_a((E1_A, E2_B)), 0.5, places=6)

    def test_false_independent_support(self):
        self.assertEqual(false_independent_support(2, 1), 1)
        self.assertEqual(false_independent_support(1, 1), 0)
        self.assertEqual(false_independent_support(0, 1), 0)
        self.assertIsNone(false_independent_support(None, 1))

    def test_p_a_and_brier(self):
        self.assertEqual(probability_of_a("B", 0.70), 0.30)
        self.assertEqual(brier_score("A", 0.70, "B"), 0.49)


class StubManipulationCheckTests(unittest.TestCase):
    """EXP-001-style checks: the harness must be able to see double counting when it happens."""

    def test_naive_stub_double_counts_at_d(self):
        result = run_condition(SEED_42_DIAMOND, "free", rounds=1, adapter=DeterministicStubAdapter("naive"))
        d_event = result.events[3]
        self.assertAlmostEqual(d_event.metrics["p_a"], 49 / 58, places=3)
        self.assertEqual(d_event.metrics["reference_p_a"], 0.7)
        self.assertGreater(d_event.metrics["p_a_excess_over_reference"], 0.14)
        self.assertEqual(d_event.metrics["reported_distinct_source_count"], 2)
        self.assertEqual(d_event.metrics["false_independent_support"], 1)

    def test_dedup_stub_with_envelope_holds_reference(self):
        result = run_condition(SEED_42_DIAMOND, "lineage", rounds=3, adapter=DeterministicStubAdapter("dedup"))
        self.assertTrue(all(abs(e.metrics["p_a_excess_over_reference"]) < 1e-6 for e in result.events))
        self.assertEqual(result.summary["max_false_independent_support"], 0)

    def test_dedup_stub_without_envelope_cannot_dedup(self):
        result = run_condition(SEED_42_DIAMOND, "free", rounds=1, adapter=DeterministicStubAdapter("dedup"))
        self.assertGreater(result.events[3].metrics["p_a_excess_over_reference"], 0.1)

    def test_dual_root_positive_control_reference(self):
        world = generate_world(42, "diamond", "dual", world_id="w")
        result = run_condition(world, "lineage", rounds=1, adapter=DeterministicStubAdapter("dedup"))
        d_event = result.events[3]
        self.assertEqual(d_event.metrics["reference_p_a"], reference_probability_of_a(world.evidence))
        self.assertAlmostEqual(d_event.metrics["p_a_excess_over_reference"], 0.0, places=3)

    def test_macro_stops_after_zero_new_root_cycle(self):
        result = run_condition(SEED_42_DIAMOND, "macro", rounds=6)
        self.assertEqual(result.summary["completed_cycles"], 1)
        self.assertTrue(result.summary["macro_stop_triggered"])
        self.assertEqual([e.sender for e in result.events], ["A", "B", "C", "D", "A"])


class ProvenanceTests(unittest.TestCase):
    def test_scores_exp002_outlier_messages(self):
        roots = (E1_A,)
        m12 = ("Select A: Agent B reports 0.70-reliable sensor evidence favoring A. "
               "Treat this as a single evidence item and do not double-count any relayed version.")
        m13 = ("Direct sensor_1 favors A at 0.70 reliability, and Agent B's separately reported "
               "0.70-reliable evidence also favors A. Count B's evidence only once despite C's relay.")
        m01 = "Sensor 1 directly observed A with reported reliability 0.70; no other evidence was provided."
        s01, s12, s13 = (score_message(m, roots) for m in (m01, m12, m13))
        self.assertTrue(s01["source_named"] and s01["reliability_named"])
        self.assertFalse(s01["indirection_marked"])
        self.assertFalse(s01["agent_as_source"])
        self.assertFalse(s12["source_named"])
        self.assertTrue(s12["agent_as_source"])
        self.assertTrue(s13["agent_as_source"])
        self.assertEqual(erosion([s01], s12)["eroded_fields"], ["source_named"])

    def test_relay_that_still_names_the_sensor_is_not_agent_as_source(self):
        text = "Agent A reports that Sensor 1 observed state A with 0.70 reliability; A is more likely."
        marks = score_message(text, (E1_A,))
        self.assertTrue(marks["agent_attribution"])
        self.assertTrue(marks["source_named"])
        self.assertFalse(marks["agent_as_source"])

    def test_pilot_discount_message_is_not_agent_attribution(self):
        text = ("Select A. The sole evidence root E1 reportedly favors A with 0.70 reliability, but "
                "confidence is reduced because the report is indirect, seven inference steps deep, "
                "and lacks independent corroboration.")
        marks = score_message(text, (E1_A,))
        self.assertTrue(marks["indirection_marked"])
        self.assertFalse(marks["agent_as_source"])

    def test_events_record_erosion_against_inbound(self):
        result = run_condition(SEED_42_DIAMOND, "free", rounds=1)
        for event in result.events:
            self.assertIn("erosion_count", event.provenance)
            self.assertIn("agent_as_source", event.provenance)


class PromptTests(unittest.TestCase):
    def test_free_prompt_is_neutral_and_unprimed(self):
        prompt = Path(__file__).parents[1].joinpath("experiments", "EXP_003", "prompts", "free.txt").read_text().lower()
        rendered = render_agent_input("D", AgentObservation("D", ()), (), probe=True).lower()
        for forbidden in ("lineage", "provenance", "independence", "independent", "evidence roots",
                          "double counting", "double-count", "epistemic", "recursive degradation"):
            self.assertNotIn(forbidden, prompt)
            self.assertNotIn(forbidden, rendered)

    def test_probe_off_single_inbound_prompt_is_byte_identical_to_exp002(self):
        """Lock the cross-experiment comparison: ring (EXP-002) vs bounce (EXP-003) must differ in topology only."""
        from experiments.EXP_002.models import AgentMessage as M2, AgentObservation as O2
        from experiments.EXP_002.models import EpistemicEnvelope as E2, Evidence as Ev2
        from experiments.EXP_002.prompting import render_agent_input as render2
        from experiments.EXP_003.models import EpistemicEnvelope as E3

        ev2 = Ev2("E1", "A", "sensor_1", 0.70, "A")
        # seed firing: evidence, no message
        self.assertEqual(render2("A", O2("A", (ev2,)), None),
                         render_agent_input("A", AgentObservation("A", (E1_A,)), (), probe=False))
        # FREE: one inbound, no envelope
        self.assertEqual(render2("B", O2("B", ()), M2("x", "A", "B", "Sensor 1 observed A.", None, "M01")),
                         render_agent_input("B", AgentObservation("B", ()),
                                            (AgentMessage("x", "A", "B", "Sensor 1 observed A.", None, "M01"),), probe=False))
        # LINEAGE: one inbound with envelope
        self.assertEqual(render2("C", O2("C", ()), M2("y", "B", "C", "msg", E2(("E1",), "M01", 1, False), "M02")),
                         render_agent_input("C", AgentObservation("C", ()),
                                            (AgentMessage("y", "B", "C", "msg", E3(("E1",), ("M01",), 1, False, 0), "M02"),), probe=False))

    def test_probe_can_be_switched_off(self):
        on = render_agent_input("D", AgentObservation("D", ()), (), probe=True)
        off = render_agent_input("D", AgentObservation("D", ()), (), probe=False)
        self.assertIn("distinct original sources", on)
        self.assertNotIn("distinct original sources", off)

    def test_two_inbound_messages_are_numbered_and_envelope_only_in_lineage(self):
        env = run_condition(SEED_42_DIAMOND, "lineage", rounds=0).events[0].actual_lineage
        b = AgentMessage("b", "B", "D", "State A is favored.", env, "M02")
        c = AgentMessage("c", "C", "D", "State A is favored.", env, "M03")
        prompt = render_agent_input("D", AgentObservation("D", ()), (b, c))
        self.assertIn("Received message 1 of 2:", prompt)
        self.assertIn("Received message 2 of 2:", prompt)
        self.assertEqual(prompt.count("Message metadata:"), 2)
        free = render_agent_input("D", AgentObservation("D", ()), (
            AgentMessage("b", "B", "D", "x", None, "M02"), AgentMessage("c", "C", "D", "y", None, "M03")))
        self.assertNotIn("Evidence roots", free)
        self.assertNotIn("Ground truth", prompt)

    def test_prompt_never_reveals_hidden_truth_or_condition(self):
        result = run_condition(SEED_42_DIAMOND, "macro", rounds=1)
        for event in result.events:
            self.assertNotIn("truth", event.model_visible_input.lower())
            self.assertNotIn("macro", event.model_visible_input.lower())


class PairedExecutionTests(unittest.TestCase):
    def test_seed_firings_are_shared_and_macro_reuses_lineage(self):
        experiment = run_experiment(trials=1, rounds=2, seed=42, topology="diamond")
        free, lineage, macro = experiment.condition_runs
        self.assertTrue(free.events[0].response_reused and lineage.events[0].response_reused)
        self.assertEqual(free.events[0].model_output, lineage.events[0].model_output)
        self.assertTrue(all(e.response_reused for e in macro.events))
        self.assertEqual(experiment.execution_metadata["actual_model_call_count"], 1 + 8 + 8)
        self.assertEqual(experiment.execution_metadata["reused_response_count"], len(macro.events))

    def test_bridged_hives_share_two_seed_firings(self):
        experiment = run_experiment(trials=1, rounds=1, seed=42, topology="hives_bridged", root_mode="dual")
        free = experiment.condition_runs[0]
        self.assertEqual([e.response_reused for e in free.events[:2]], [True, True])
        self.assertEqual(experiment.execution_metadata["actual_model_call_count"], 2 + 8 + 8)

    def test_results_are_written_with_topology_metadata(self):
        experiment = run_experiment(trials=2, rounds=1, seed=5, topology="diamond", root_mode="dual")
        with tempfile.TemporaryDirectory() as tmp:
            out = write_results(experiment, Path(tmp))
            metadata = json.loads((out / "run_metadata.json").read_text())
            self.assertEqual(metadata["experiment"], "EXP-003")
            self.assertEqual(metadata["topology_name"], "diamond")
            self.assertEqual(metadata["root_mode"], "dual")
            self.assertEqual(len(metadata["worlds"]), 2)
            self.assertEqual(len(metadata["config_fingerprint"]), 64)
            lines = (out / "events.jsonl").read_text().splitlines()
            self.assertTrue(all("provenance" in json.loads(l) for l in lines))


class WorldAndManifestTests(unittest.TestCase):
    def test_same_seed_shares_truth_and_e1_across_root_modes(self):
        single = generate_world(99, "diamond", "single")
        dual = generate_world(99, "diamond", "dual")
        self.assertEqual(single.truth, dual.truth)
        self.assertEqual(single.evidence[0].observed_state, dual.evidence[0].observed_state)
        self.assertEqual([e.evidence_id for e in dual.evidence], ["E1", "E2"])
        self.assertEqual(dual.evidence[1].assigned_to, ("C",))

    def test_shared_root_mode_assigns_one_sensor_to_both_hives(self):
        world = generate_world(1, "hives_bridged", "shared")
        self.assertEqual(len(world.evidence), 1)
        self.assertEqual(world.evidence[0].assigned_to, ("A1", "A2"))

    def test_dual_requires_secondary_sources(self):
        with self.assertRaises(ValueError):
            WorldGenerator(1, "solo", "dual")

    def test_cell_labels(self):
        self.assertRegex(world_cell(generate_world(3, "diamond", "dual")), r"^[AB]/[AB]/[AB]$")
        self.assertRegex(world_cell(generate_world(3, "diamond", "single")), r"^[AB]/[AB]$")

    def test_candidate_seed_is_deterministic_and_bounded(self):
        a = candidate_seed("anchor", "GEN", 1)
        self.assertEqual(a, candidate_seed("anchor", "GEN", 1))
        self.assertNotEqual(a, candidate_seed("anchor", "GEN", 2))
        self.assertTrue(1 <= a <= 2_147_483_646)

    def test_manifest_excludes_and_orders(self):
        anchor = "test-anchor"
        first = candidate_seed(anchor, "S", 1)
        manifest = build_manifest(anchor, "S", "diamond", "single", 3, None, None, {first})
        seeds = [w["seed"] for w in manifest["worlds"]]
        self.assertNotIn(first, seeds)
        self.assertEqual(len(set(seeds)), 3)
        keys = [w["order_key"] for w in manifest["worlds"]]
        self.assertEqual(keys, sorted(keys))
        self.assertEqual(manifest["model_calls_made"], 0)

    def test_stratified_manifest_fills_cells(self):
        manifest = build_manifest("t", "ST", "diamond", "single", 0, 1, ["A/A", "B/B", "A/B", "B/A"], set())
        self.assertEqual(sorted(w["cell"] for w in manifest["worlds"]), ["A/A", "A/B", "B/A", "B/B"])
        self.assertTrue(any(not r["accepted"] for r in manifest["selection"]["scan"]))


if __name__ == "__main__":
    unittest.main()
