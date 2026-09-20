import unittest

from experiments.EXP_002.adapters.deterministic_stub import DeterministicStubAdapter
from experiments.EXP_002.models import AgentMessage, AgentObservation, AgentResponse
from experiments.EXP_002.run import run_condition, run_experiment
from experiments.EXP_002.world_generator import generate_world


class RecordingAdapter(DeterministicStubAdapter):
    def __init__(self):
        self.received_envelopes = []

    def respond(self, agent_id, observation, received_message, condition):
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
        self.assertEqual(result.summary["stop_reason"], "no_new_independent_roots_after_cycle")

    def test_event_keeps_model_output_separate_from_hidden_lineage(self):
        world = generate_world(seed=42, world_id="test-world")
        result = run_condition(world, "free", rounds=1)
        event = result.events[1]
        self.assertIsInstance(event.model_output, AgentResponse)
        self.assertIsNone(event.agent_message.envelope)
        self.assertEqual(event.actual_lineage.actual_roots, ("E1",))
        self.assertEqual(event.agent_reported_information, event.model_output.message)


if __name__ == "__main__":
    unittest.main()
