import unittest
from pathlib import Path

from experiments.EXP_002.adapters.deterministic_stub import DeterministicStubAdapter
from experiments.EXP_002.metrics import brier_score, event_metrics, probability_of_a
from experiments.EXP_002.models import AgentResponse
from experiments.EXP_002.run import run_condition, run_experiment
from experiments.EXP_002.world_generator import generate_world


class RecordingAdapter(DeterministicStubAdapter):
    def __init__(self):
        self.received_envelopes = []
        self.calls = []

    def respond(self, agent_id, observation, received_message, condition):
        self.calls.append((agent_id, received_message))
        self.received_envelopes.append(
            None if received_message is None else received_message.envelope
        )
        return super().respond(agent_id, observation, received_message, condition)


class Exp002Tests(unittest.TestCase):
    def test_world_identity_is_shared_across_conditions(self):
        experiment = run_experiment(trials=1, rounds=1, seed=42)
        self.assertEqual(len(experiment.worlds), 1)
        self.assertEqual(len(experiment.condition_runs), 3)
        self.assertTrue(all(run.world is experiment.worlds[0] for run in experiment.condition_runs))
        self.assertEqual({run.world.truth for run in experiment.condition_runs}, {experiment.worlds[0].truth})

    def test_recursive_communication_cannot_create_new_root(self):
        world = generate_world(seed=42, world_id="test-world")
        result = run_condition(world, "free", rounds=4)
        self.assertEqual({event.actual_lineage.actual_roots for event in result.events}, {("E1",)})
        self.assertEqual(result.summary["new_independent_evidence_count"], 1)

    def test_lineage_depth_increases_without_root_growth(self):
        world = generate_world(seed=42, world_id="test-world")
        result = run_condition(world, "lineage", rounds=1)
        self.assertEqual(
            [event.actual_lineage.inference_depth for event in result.events],
            [0, 1, 2, 3],
        )
        self.assertTrue(all(event.actual_lineage.actual_roots == ("E1",) for event in result.events))

    def test_one_cycle_has_exact_sequential_topology(self):
        world = generate_world(seed=42, world_id="test-world")
        result = run_condition(world, "free", rounds=1)
        self.assertEqual(
            [(event.sender, event.receiver) for event in result.events],
            [("A", "B"), ("B", "C"), ("C", "A"), ("A", "B")],
        )

    def test_two_cycles_have_exact_sequential_topology(self):
        world = generate_world(seed=42, world_id="test-world")
        result = run_condition(world, "free", rounds=2)
        self.assertEqual(
            [(event.sender, event.receiver) for event in result.events],
            [
                ("A", "B"),
                ("B", "C"),
                ("C", "A"),
                ("A", "B"),
                ("B", "C"),
                ("C", "A"),
                ("A", "B"),
            ],
        )

    def test_each_invocation_consumes_message_for_current_sender(self):
        world = generate_world(seed=42, world_id="test-world")
        adapter = RecordingAdapter()
        run_condition(world, "free", rounds=2, adapter=adapter)
        for agent_id, received_message in adapter.calls:
            if received_message is not None:
                self.assertEqual(received_message.receiver, agent_id)

    def test_condition_isolation_controls_visible_metadata(self):
        world = generate_world(seed=42, world_id="test-world")
        free_adapter = RecordingAdapter()
        lineage_adapter = RecordingAdapter()
        macro_adapter = RecordingAdapter()
        run_condition(world, "free", rounds=1, adapter=free_adapter)
        run_condition(world, "lineage", rounds=1, adapter=lineage_adapter)
        run_condition(world, "macro", rounds=1, adapter=macro_adapter)
        self.assertTrue(all(envelope is None for envelope in free_adapter.received_envelopes))
        self.assertTrue(any(envelope is not None for envelope in lineage_adapter.received_envelopes))
        self.assertTrue(any(envelope is not None for envelope in macro_adapter.received_envelopes))

    def test_macro_stops_after_zero_new_root_cycle(self):
        world = generate_world(seed=42, world_id="test-world")
        result = run_condition(world, "macro", rounds=8)
        self.assertEqual(result.summary["completed_cycles"], 1)
        self.assertTrue(result.summary["macro_stop_triggered"])
        self.assertEqual(result.summary["stop_reason"], "no_new_independent_roots_after_cycle")
        self.assertEqual(
            [(event.sender, event.receiver) for event in result.events],
            [("A", "B"), ("B", "C"), ("C", "A"), ("A", "B")],
        )

    def test_macro_stop_is_observable_on_final_allowed_cycle(self):
        world = generate_world(seed=42, world_id="test-world")
        result = run_condition(world, "macro", rounds=1)
        self.assertEqual(result.summary["completed_cycles"], 1)
        self.assertTrue(result.summary["macro_stop_triggered"])
        self.assertEqual(result.summary["stop_reason"], "no_new_independent_roots_after_cycle")

    def test_non_macro_cycle_exhaustion_reports_max_rounds(self):
        world = generate_world(seed=42, world_id="test-world")
        result = run_condition(world, "lineage", rounds=1)
        self.assertEqual(result.summary["completed_cycles"], 1)
        self.assertFalse(result.summary["macro_stop_triggered"])
        self.assertEqual(result.summary["stop_reason"], "max_rounds")

    def test_event_keeps_model_output_separate_from_hidden_lineage(self):
        world = generate_world(seed=42, world_id="test-world")
        result = run_condition(world, "free", rounds=1)
        event = result.events[1]
        self.assertIsInstance(event.model_output, AgentResponse)
        self.assertIsNone(event.agent_message.envelope)
        self.assertEqual(event.actual_lineage.actual_roots, ("E1",))
        self.assertEqual(event.agent_reported_information, event.model_output.message)

    def test_p_a_is_fixed_to_state_a(self):
        self.assertEqual(probability_of_a("A", 0.70), 0.70)
        self.assertEqual(probability_of_a("B", 0.70), 0.30)

    def test_p_a_delta_uses_fixed_proposition(self):
        previous = AgentResponse(answer="A", confidence=0.80, message="State A is favored.")
        current = AgentResponse(answer="B", confidence=0.75, message="State B is favored.")
        envelope = run_condition(generate_world(42), "free", rounds=0).events[0].actual_lineage
        metrics = event_metrics(current, "A", envelope, 0, previous)
        self.assertEqual(metrics["reported_confidence"], 0.75)
        self.assertEqual(metrics["p_a"], 0.25)
        self.assertEqual(metrics["p_a_delta_without_new_evidence"], -0.55)

    def test_brier_known_values(self):
        self.assertEqual(brier_score("A", 0.70, "A"), 0.09)
        self.assertEqual(brier_score("A", 0.70, "B"), 0.49)
        self.assertEqual(brier_score("A", 1.0, "B"), 1.0)

    def test_condition_summary_contains_p_a_trajectory(self):
        world = generate_world(seed=42, world_id="test-world")
        result = run_condition(world, "lineage", rounds=1)
        self.assertEqual(result.summary["p_a_trajectory"], [event.metrics["p_a"] for event in result.events])
        self.assertEqual(
            result.summary["p_a_delta_without_new_evidence"],
            [event.metrics["p_a_delta_without_new_evidence"] for event in result.events],
        )

    def test_free_prompt_is_neutral_and_unprimed(self):
        prompt = Path(__file__).parents[1].joinpath(
            "experiments", "EXP_002", "prompts", "free.txt"
        ).read_text(encoding="utf-8").lower()
        for forbidden in (
            "lineage",
            "provenance",
            "independence",
            "evidence roots",
            "double counting",
            "epistemic",
            "recursive degradation",
        ):
            self.assertNotIn(forbidden, prompt)

    def test_run_metadata_identity_is_dynamic(self):
        experiment = run_experiment(
            trials=2,
            rounds=3,
            seed=42,
            adapter_name="future_adapter",
            adapter_metadata={"provider": "test", "model": "stub-v2"},
        )
        self.assertEqual(experiment.adapter_name, "future_adapter")
        self.assertEqual(experiment.rounds, 3)
        self.assertEqual(experiment.seed, 42)
        self.assertEqual(len(experiment.worlds), 2)


if __name__ == "__main__":
    unittest.main()
