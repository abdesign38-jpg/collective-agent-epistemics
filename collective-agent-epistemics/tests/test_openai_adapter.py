import json
import os
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from pydantic import ValidationError

from experiments.EXP_002.adapters.openai_responses import (
    ModelAgentResponse,
    OpenAIAdapterConfig,
    OpenAIAdapterError,
    OpenAIResponsesAdapter,
)
from experiments.EXP_002.models import AgentMessage, AgentObservation, EpistemicEnvelope
from experiments.EXP_002.prompting import render_agent_input
from experiments.EXP_002.run import run_experiment, write_results
from experiments.EXP_002.world_generator import generate_world


class FakeResponses:
    def __init__(self, parsed=None, status="completed"):
        self.parsed = parsed
        self.status = status
        self.calls = []

    def parse(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(
            status=self.status,
            incomplete_details=None,
            output_parsed=self.parsed,
            id="resp_test",
            model="returned-model",
            usage=SimpleNamespace(input_tokens=10, output_tokens=5, total_tokens=15),
        )


class FakeClient:
    def __init__(self, parsed=None, status="completed"):
        self.responses = FakeResponses(parsed, status)


class OpenAIAdapterTests(unittest.TestCase):
    def setUp(self):
        self.observation = AgentObservation(agent_id="A", evidence=())

    def test_structured_output_is_converted_to_agent_response(self):
        client = FakeClient(ModelAgentResponse(answer="A", confidence=0.7, message="State A is favored."))
        adapter = OpenAIResponsesAdapter(OpenAIAdapterConfig(model="test-model"), client=client)
        response = adapter.respond("A", self.observation, None, "free")
        self.assertEqual(response.answer, "A")
        self.assertEqual(response.confidence, 0.7)
        self.assertEqual(response.message, "State A is favored.")
        self.assertEqual(adapter.last_call_metadata["response_id"], "resp_test")

    def test_request_is_stateless_and_has_no_tools(self):
        client = FakeClient(ModelAgentResponse(answer="A", confidence=0.7, message="A"))
        adapter = OpenAIResponsesAdapter(
            OpenAIAdapterConfig(model="test-model", reasoning_effort="low", timeout_seconds=12),
            client=client,
        )
        adapter.respond("A", self.observation, None, "free")
        request = client.responses.calls[0]
        self.assertEqual(request["model"], "test-model")
        self.assertEqual(request["reasoning"], {"effort": "low"})
        self.assertEqual(request["timeout"], 12)
        self.assertFalse(request["store"])
        self.assertNotIn("tools", request)
        self.assertNotIn("previous_response_id", request)
        self.assertNotIn("conversation", request)
        self.assertIs(request["text_format"], ModelAgentResponse)

    def test_invalid_structured_values_are_rejected(self):
        with self.assertRaises(ValidationError):
            ModelAgentResponse(answer="C", confidence=0.7, message="A")
        with self.assertRaises(ValidationError):
            ModelAgentResponse(answer="A", confidence=1.1, message="A")
        with self.assertRaises(ValidationError):
            ModelAgentResponse(answer="A", confidence=0.7, message=" ")

    def test_missing_parsed_output_fails_visibly(self):
        client = FakeClient(parsed=None)
        adapter = OpenAIResponsesAdapter(OpenAIAdapterConfig(model="test-model"), client=client)
        with self.assertRaises(OpenAIAdapterError):
            adapter.respond("A", self.observation, None, "free")

    def test_prompt_does_not_include_hidden_truth_or_condition_name(self):
        world = generate_world(seed=42, world_id="prompt-world")
        observation = AgentObservation(agent_id="A", evidence=world.evidence)
        prompt = render_agent_input("A", observation, None)
        self.assertNotIn("Ground truth", prompt)
        self.assertNotIn("prompt-world", prompt)
        self.assertNotIn("FREE", prompt)
        self.assertNotIn("LINEAGE", prompt)
        self.assertNotIn("MACRO", prompt)

    def test_lineage_and_macro_render_identically(self):
        envelope = EpistemicEnvelope(("E1",), "A_01", 1, False)
        message = AgentMessage("A_01", "A", "B", "State A is favored.", envelope)
        observation = AgentObservation("B", ())
        lineage_prompt = render_agent_input("B", observation, message)
        macro_prompt = render_agent_input("B", observation, message)
        free_message = AgentMessage("A_01", "A", "B", "State A is favored.", None)
        free_prompt = render_agent_input("B", observation, free_message)
        self.assertEqual(lineage_prompt, macro_prompt)
        self.assertNotEqual(free_prompt, lineage_prompt)
        self.assertNotIn("Evidence roots", free_prompt)
        self.assertIn("Evidence roots", lineage_prompt)

    def test_client_is_created_with_zero_retries_and_explicit_timeout(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False):
            with patch("openai.OpenAI") as openai_client:
                OpenAIResponsesAdapter(OpenAIAdapterConfig(timeout_seconds=17))
        openai_client.assert_called_once_with(
            api_key="test-key",
            timeout=17,
            max_retries=0,
        )

    def test_adapter_metadata_is_nested_and_cannot_overwrite_experiment_metadata(self):
        experiment = run_experiment(
            trials=1,
            rounds=1,
            seed=42,
            adapter_name="openai",
            adapter_metadata={"experiment": "wrong", "seed": 999, "provider": "openai"},
        )
        write_results(experiment)
        metadata_path = Path(__file__).parents[1] / "experiments" / "EXP_002" / "results" / "run_metadata.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        self.assertEqual(metadata["experiment"], "EXP-002")
        self.assertEqual(metadata["seed"], 42)
        self.assertEqual(metadata["trial_count"], 1)
        self.assertEqual(metadata["adapter_metadata"]["experiment"], "wrong")


if __name__ == "__main__":
    unittest.main()
