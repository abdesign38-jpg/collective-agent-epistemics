import unittest
import json
from pathlib import Path

from experiments.EXP_002.models import AgentResponse
from experiments.EXP_002.run import run_experiment, write_results


class CountingAdapter:
    total_calls = 0

    def __init__(self):
        self.last_call_metadata = {}

    def respond(self, agent_id, observation, received_message, condition):
        type(self).total_calls += 1
        call_id = f"resp_{type(self).total_calls}"
        self.last_call_metadata = {"response_id": call_id, "usage": {"total_tokens": 10}}
        answer = "A" if type(self).total_calls % 2 else "B"
        return AgentResponse(answer, 0.7, f"State {answer} is favored.")


class ExecutionPolicyTests(unittest.TestCase):
    def setUp(self):
        CountingAdapter.total_calls = 0

    def test_paired_shares_seed_reuses_macro_and_counts_seven_calls(self):
        experiment = run_experiment(
            trials=1,
            rounds=1,
            seed=42,
            adapter_factory=CountingAdapter,
            adapter_name="fake",
            execution_policy="paired",
        )
        runs = {run.condition: run for run in experiment.condition_runs}
        seed_events = [runs[name].events[0] for name in ("free", "lineage", "macro")]
        self.assertEqual(
            {(event.model_output.answer, event.model_output.confidence, event.model_output.message) for event in seed_events},
            {(seed_events[0].model_output.answer, seed_events[0].model_output.confidence, seed_events[0].model_output.message)},
        )
        self.assertEqual(
            {event.provider_metadata["response_id"] for event in seed_events},
            {seed_events[0].provider_metadata["response_id"]},
        )
        self.assertEqual(experiment.execution_metadata["actual_model_call_count"], 7)
        self.assertEqual(experiment.execution_metadata["reused_response_count"], 4)
        self.assertTrue(all(event.response_reused for event in runs["macro"].events))
        self.assertTrue(all(event.source_condition in ("seed", "lineage") for event in runs["macro"].events))
        self.assertEqual(
            [event.model_output.answer for event in runs["macro"].events],
            [event.model_output.answer for event in runs["lineage"].events[:4]],
        )

    def test_paired_visible_ids_are_condition_neutral(self):
        experiment = run_experiment(
            trials=1,
            rounds=1,
            seed=42,
            adapter_factory=CountingAdapter,
            adapter_name="fake",
            execution_policy="paired",
        )
        for condition_run in experiment.condition_runs:
            for event in condition_run.events:
                self.assertEqual(event.visible_message_id, f"M{event.message_id.split('_M')[-1]}")
                self.assertNotIn(condition_run.condition, event.visible_message_id.lower())
                if event.actual_lineage.derived_from:
                    self.assertTrue(event.actual_lineage.derived_from.startswith("M"))

    def test_independent_keeps_condition_calls_separate(self):
        experiment = run_experiment(
            trials=1,
            rounds=1,
            seed=42,
            adapter_factory=CountingAdapter,
            adapter_name="fake",
            execution_policy="independent",
        )
        self.assertEqual(experiment.execution_policy, "independent")
        self.assertEqual(experiment.execution_metadata["actual_model_call_count"], 12)
        self.assertEqual(experiment.execution_metadata["reused_response_count"], 0)
        seed_ids = {
            run.events[0].provider_metadata["response_id"]
            for run in experiment.condition_runs
        }
        self.assertEqual(len(seed_ids), 3)
        self.assertTrue(all(not event.response_reused for run in experiment.condition_runs for event in run.events))

    def test_execution_policy_is_recorded_and_fingerprinted(self):
        paired = run_experiment(trials=1, rounds=1, seed=42, execution_policy="paired")
        write_results(paired)
        metadata_path = Path(__file__).parents[1] / "experiments" / "EXP_002" / "results" / "run_metadata.json"
        paired_metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        independent = run_experiment(trials=1, rounds=1, seed=42, execution_policy="independent")
        write_results(independent)
        independent_metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        self.assertEqual(paired_metadata["execution_policy"], "paired")
        self.assertEqual(independent_metadata["execution_policy"], "independent")
        self.assertNotEqual(
            paired_metadata["config_fingerprint"], independent_metadata["config_fingerprint"]
        )


if __name__ == "__main__":
    unittest.main()
