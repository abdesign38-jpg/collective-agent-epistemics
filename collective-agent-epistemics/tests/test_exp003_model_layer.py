import json
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from experiments.EXP_003.adapters.anthropic_messages import (
    AnthropicAdapterConfig,
    AnthropicAdapterError,
    AnthropicMessagesAdapter,
)
from experiments.EXP_003.adapters.openai_responses import ModelAgentResponse, ModelAgentResponseNoProbe
from experiments.EXP_003.adapters.registry import PROVIDERS, RUN_CLASS_SMOKE, build_provider
from experiments.EXP_003.factors import FACTORS, diff_factors, factors_for, factors_from_metadata, ledger
from experiments.EXP_003.models import AgentObservation
from experiments.EXP_003.run import build_metadata, run_experiment, write_results

REPO = Path(__file__).parents[1]
EXP002_RUN = (REPO / "experiments" / "EXP_002" / "results" / "archive" / "gate_2b" / "stress_set_001"
              / "G2B_STRESS001_seed_1211074116" / "attempt_001")


class FakeMessages:
    def __init__(self, parsed=None, stop_reason="end_turn", category=None, served_model="claude-opus-5",
                 fallback=False):
        self.parsed = parsed
        self.stop_reason = stop_reason
        self.category = category
        self.served_model = served_model
        self.fallback = fallback
        self.calls = []

    def parse(self, **kwargs):
        self.calls.append(kwargs)
        content = []
        iterations = []
        if self.fallback:
            content.append(SimpleNamespace(type="fallback", from_=SimpleNamespace(model="claude-opus-5"),
                                           to=SimpleNamespace(model=self.served_model)))
            iterations.append(SimpleNamespace(type="fallback_message"))
        return SimpleNamespace(
            id="msg_test",
            model=self.served_model,
            stop_reason=self.stop_reason,
            stop_details=SimpleNamespace(category=self.category, explanation="x") if self.stop_reason == "refusal" else None,
            parsed_output=self.parsed,
            content=content,
            usage=SimpleNamespace(input_tokens=11, output_tokens=7, iterations=iterations),
        )


class FakeAnthropicClient:
    def __init__(self, parsed=None, stop_reason="end_turn", category=None, served_model="claude-opus-5",
                 fallback=False):
        self.messages = FakeMessages(parsed, stop_reason, category, served_model, fallback)
        self.beta = SimpleNamespace(messages=FakeMessages(parsed, stop_reason, category, served_model, fallback))


class AnthropicAdapterTests(unittest.TestCase):
    def setUp(self):
        self.observation = AgentObservation(agent_id="D", evidence=())
        self.config = AnthropicAdapterConfig(model="claude-opus-5", effort="medium", timeout_seconds=12)

    def test_structured_output_is_converted(self):
        client = FakeAnthropicClient(ModelAgentResponse(answer="A", confidence=0.7, distinct_source_count=1, message="A favored."))
        adapter = AnthropicMessagesAdapter(self.config, client=client)
        response = adapter.respond("D", self.observation, (), "free")
        self.assertEqual((response.answer, response.confidence, response.distinct_source_count), ("A", 0.7, 1))
        self.assertEqual(adapter.last_call_metadata["response_id"], "msg_test")
        self.assertEqual(adapter.last_call_metadata["usage"]["total_tokens"], 18)

    def test_request_shape_has_no_tools_fallbacks_or_sampling(self):
        client = FakeAnthropicClient(ModelAgentResponse(answer="A", confidence=0.7, distinct_source_count=1, message="A"))
        AnthropicMessagesAdapter(self.config, client=client).respond("D", self.observation, (), "free")
        request = client.messages.calls[0]
        self.assertEqual(request["model"], "claude-opus-5")
        self.assertEqual(request["output_config"], {"effort": "medium"})
        self.assertEqual(request["thinking"], {"type": "adaptive"})
        self.assertIs(request["output_format"], ModelAgentResponse)
        self.assertEqual(request["timeout"], 12)
        for forbidden in ("tools", "fallbacks", "betas", "temperature", "top_p", "system"):
            self.assertNotIn(forbidden, request)
        self.assertEqual(request["messages"][0]["role"], "user")

    def test_probe_off_uses_exp002_shaped_schema(self):
        config = AnthropicAdapterConfig(model="m", effort="low", probe=False)
        client = FakeAnthropicClient(ModelAgentResponseNoProbe(answer="B", confidence=0.6, message="B"))
        response = AnthropicMessagesAdapter(config, client=client).respond("D", self.observation, (), "free")
        self.assertIsNone(response.distinct_source_count)
        self.assertIs(client.messages.calls[0]["output_format"], ModelAgentResponseNoProbe)

    def test_refusal_is_a_technical_failure_not_a_swap(self):
        client = FakeAnthropicClient(None, stop_reason="refusal", category="cyber")
        adapter = AnthropicMessagesAdapter(self.config, client=client)
        with self.assertRaises(AnthropicAdapterError):
            adapter.respond("D", self.observation, (), "free")
        self.assertEqual(adapter.last_call_metadata["refusal_category"], "cyber")

    def test_truncation_and_missing_output_fail_visibly(self):
        with self.assertRaises(AnthropicAdapterError):
            AnthropicMessagesAdapter(self.config, client=FakeAnthropicClient(None, stop_reason="max_tokens")).respond("D", self.observation, (), "free")
        with self.assertRaises(AnthropicAdapterError):
            AnthropicMessagesAdapter(self.config, client=FakeAnthropicClient(None)).respond("D", self.observation, (), "free")

    def test_client_is_created_with_zero_retries_and_explicit_timeout(self):
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=False):
            with patch("anthropic.Anthropic") as anthropic_client:
                AnthropicMessagesAdapter(AnthropicAdapterConfig(model="m", effort="high", timeout_seconds=17))
        anthropic_client.assert_called_once_with(timeout=17, max_retries=0)

    def test_model_and_effort_must_be_explicit(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                AnthropicAdapterConfig.from_environment(effort="medium")
        with self.assertRaises(ValueError):
            AnthropicAdapterConfig.from_environment(model="m")
        with self.assertRaises(ValueError):
            AnthropicAdapterConfig(model="m", effort="none")

    def test_metadata_declares_no_fallbacks_by_default(self):
        self.assertFalse(self.config.metadata()["fallbacks"])
        self.assertEqual(self.config.metadata()["provider"], "anthropic")

    def test_default_request_uses_stable_endpoint_and_records_served_model(self):
        client = FakeAnthropicClient(ModelAgentResponse(answer="A", confidence=0.7, distinct_source_count=1, message="A"))
        adapter = AnthropicMessagesAdapter(self.config, client=client)
        adapter.respond("D", self.observation, (), "free")
        self.assertEqual(len(client.messages.calls), 1)
        self.assertEqual(len(client.beta.messages.calls), 0)
        self.assertFalse(adapter.last_call_metadata["fallback_ran"])
        self.assertEqual(adapter.last_call_metadata["served_model"], "claude-opus-5")
        self.assertTrue(adapter.last_call_metadata["model_matches_request"])

    def test_fallbacks_on_uses_beta_endpoint_with_exact_header_and_default_form(self):
        config = AnthropicAdapterConfig(model="claude-opus-5", effort="low", fallbacks=True)
        client = FakeAnthropicClient(ModelAgentResponse(answer="A", confidence=0.7, distinct_source_count=1, message="A"),
                                     served_model="claude-opus-4-8", fallback=True)
        adapter = AnthropicMessagesAdapter(config, client=client)
        adapter.respond("D", self.observation, (), "free")
        self.assertEqual(len(client.messages.calls), 0)
        request = client.beta.messages.calls[0]
        self.assertEqual(request["betas"], ["server-side-fallback-2026-07-01"])
        self.assertEqual(request["fallbacks"], "default")
        meta = adapter.last_call_metadata
        self.assertTrue(meta["fallback_ran"])
        self.assertEqual(meta["served_model"], "claude-opus-4-8")
        self.assertFalse(meta["model_matches_request"])
        self.assertEqual(meta["fallback_switches"], [{"from_model": "claude-opus-5", "to_model": "claude-opus-4-8"}])
        self.assertTrue(config.metadata()["fallbacks"])
        self.assertEqual(config.metadata()["fallback_mode"], "default")


class RegistryTests(unittest.TestCase):
    def test_providers_listed(self):
        self.assertEqual(PROVIDERS, ("deterministic_stub", "openai", "anthropic"))

    def test_stub_binding_is_not_live(self):
        binding = build_provider("deterministic_stub", stub_mode="dedup")
        self.assertFalse(binding.live)
        self.assertEqual(binding.adapter_name, "deterministic_stub:dedup")

    def test_real_bindings_are_live_and_share_schema_version(self):
        openai = build_provider("openai", model="m", reasoning_effort="medium")
        anthropic = build_provider("anthropic", model="m", reasoning_effort="medium")
        self.assertTrue(openai.live and anthropic.live)
        self.assertEqual(openai.metadata["schema_version"], anthropic.metadata["schema_version"])
        self.assertEqual(openai.metadata["prompt_version"], anthropic.metadata["prompt_version"])

    def test_unknown_provider_rejected(self):
        with self.assertRaises(ValueError):
            build_provider("gemini")

    def test_fallbacks_require_smoke_and_anthropic(self):
        with self.assertRaises(ValueError):
            build_provider("anthropic", model="m", reasoning_effort="low", fallbacks=True)
        with self.assertRaises(ValueError):
            build_provider("openai", model="m", reasoning_effort="low", smoke=True, fallbacks=True)
        with self.assertRaises(ValueError):
            build_provider("deterministic_stub", smoke=True, fallbacks=True)
        binding = build_provider("anthropic", model="m", reasoning_effort="low", smoke=True, fallbacks=True)
        self.assertEqual(binding.run_class, RUN_CLASS_SMOKE)
        self.assertTrue(binding.metadata["fallbacks"])

    def test_smoke_without_fallbacks_is_still_smoke_class(self):
        binding = build_provider("openai", model="m", reasoning_effort="low", smoke=True)
        self.assertEqual(binding.run_class, RUN_CLASS_SMOKE)
        self.assertFalse(binding.metadata["fallbacks"])
        scientific = build_provider("openai", model="m", reasoning_effort="low")
        self.assertEqual(scientific.run_class, "pilot_real_model")


class FallbackServedAdapter:
    """Stub that reports a fallback-served response, to test the runner's refusal."""

    def __init__(self):
        self.last_call_metadata = {}

    def respond(self, agent_id, observation, received_messages, condition):
        from experiments.EXP_003.models import AgentResponse

        self.last_call_metadata = {"response_id": f"r_{agent_id}_{len(received_messages)}",
                                   "fallback_ran": True, "served_model": "substitute"}
        return AgentResponse("A", 0.7, "State A is favored with confidence 0.7000 based on 1 source(s).", 1)


class FallbackContainmentTests(unittest.TestCase):
    def test_scientific_run_refuses_fallback_served_events(self):
        with self.assertRaises(RuntimeError):
            run_experiment(trials=1, rounds=1, seed=1, adapter_factory=FallbackServedAdapter,
                           adapter_name="anthropic", run_class="pilot_real_model")

    def test_smoke_run_accepts_and_counts_fallback_events(self):
        experiment = run_experiment(trials=1, rounds=1, seed=1, adapter_factory=FallbackServedAdapter,
                                    adapter_name="anthropic", adapter_metadata={"provider": "anthropic", "fallbacks": True},
                                    run_class=RUN_CLASS_SMOKE)
        self.assertGreater(experiment.execution_metadata["fallback_events"], 0)
        self.assertEqual(experiment.execution_metadata["served_models"], ["substitute"])
        metadata = build_metadata(experiment)
        self.assertTrue(metadata["fallbacks"])
        self.assertEqual(metadata["run_class"], RUN_CLASS_SMOKE)
        self.assertIn("Never scientific evidence", metadata["note"])

    def test_fallbacks_and_run_class_are_ledger_factors(self):
        smoke = build_metadata(run_experiment(trials=1, rounds=1, seed=1, adapter_factory=FallbackServedAdapter,
                                              adapter_metadata={"provider": "anthropic", "fallbacks": True},
                                              run_class=RUN_CLASS_SMOKE))
        plain = build_metadata(run_experiment(trials=1, rounds=1, seed=1,
                                              adapter_metadata={"provider": "anthropic", "fallbacks": False},
                                              run_class="pilot_real_model"))
        changed = diff_factors(factors_from_metadata(smoke), factors_from_metadata(plain))
        self.assertEqual(set(changed), {"run_class", "fallbacks"})


class FactorLedgerTests(unittest.TestCase):
    def _exp003_metadata(self, **overrides):
        experiment = run_experiment(trials=1, rounds=4, seed=42, topology="diamond", **overrides)
        return build_metadata(experiment)

    def test_exp002_archive_maps_onto_factors(self):
        row = factors_for(EXP002_RUN)
        self.assertEqual(row["experiment"], "EXP-002")
        self.assertEqual(row["topology"], "ring")
        self.assertTrue(row["regrounding"])
        self.assertEqual(row["root_mode"], "single")
        self.assertFalse(row["probe"])
        self.assertEqual(row["provider"], "openai")
        self.assertEqual(row["model"], "gpt-5.6-sol")
        self.assertEqual(row["gate"], "2B")
        self.assertEqual(row["set"], "stress_set_001")

    def test_diff_between_exp002_and_exp003_names_only_changed_factors(self):
        a = factors_for(EXP002_RUN)
        b = factors_from_metadata(self._exp003_metadata(), None, source="stub")
        changed = diff_factors(a, b)
        for expected in ("experiment", "topology", "probe", "provider", "prompt_version", "schema_version"):
            self.assertIn(expected, changed)
        for same in ("regrounding", "root_mode", "rounds", "execution_policy", "conditions", "sensor_reliability"):
            self.assertNotIn(same, changed)

    def test_model_layer_is_exactly_one_factor(self):
        base = self._exp003_metadata(adapter_metadata={"provider": "openai", "requested_model": "gpt-x", "reasoning_effort": "medium"})
        other = self._exp003_metadata(adapter_metadata={"provider": "anthropic", "requested_model": "claude-y", "reasoning_effort": "medium"})
        changed = diff_factors(factors_from_metadata(base), factors_from_metadata(other))
        self.assertEqual(set(changed), {"provider", "model"})

    def test_gate_changes_are_named(self):
        a = factors_from_metadata(self._exp003_metadata())
        b = factors_from_metadata(build_metadata(run_experiment(trials=1, rounds=4, seed=42, topology="diamond_detached")))
        self.assertEqual(set(diff_factors(a, b)), {"topology", "regrounding"})
        c = factors_from_metadata(build_metadata(run_experiment(trials=1, rounds=4, seed=42, topology="diamond", root_mode="dual")))
        self.assertEqual(set(diff_factors(a, c)), {"root_mode"})
        d = factors_from_metadata(build_metadata(run_experiment(trials=1, rounds=4, seed=42, topology="diamond", probe=False)))
        self.assertEqual(set(diff_factors(a, d)), {"probe"})

    def test_ledger_reads_written_results_and_exp002_archive(self):
        experiment = run_experiment(trials=1, rounds=1, seed=42, topology="hives_bridged", root_mode="shared")
        with tempfile.TemporaryDirectory() as tmp:
            out = write_results(experiment, Path(tmp) / "run")
            rows = ledger([out, EXP002_RUN])
        self.assertEqual(len(rows), 2)
        self.assertEqual({r["experiment"] for r in rows}, {"EXP-003", "EXP-002"})
        self.assertTrue(all(f in rows[0] for f in FACTORS))

    def test_fingerprint_changes_with_reliability(self):
        a = build_metadata(run_experiment(trials=1, rounds=1, seed=1, sensor_reliability=0.70))
        b = build_metadata(run_experiment(trials=1, rounds=1, seed=1, sensor_reliability=0.80))
        self.assertNotEqual(a["config_fingerprint"], b["config_fingerprint"])
        self.assertEqual(a["sensor_reliability"], 0.70)


if __name__ == "__main__":
    unittest.main()
