from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .anthropic_messages import AnthropicAdapterConfig, AnthropicMessagesAdapter
from .base import AgentAdapter
from .deterministic_stub import DeterministicStubAdapter
from .openai_responses import OpenAIAdapterConfig, OpenAIResponsesAdapter

PROVIDERS = ("deterministic_stub", "openai", "anthropic")

# Run classes. Scientific sets are always `pilot_real_model`; `smoke_technical` exists
# for plumbing checks and is the only class in which refusal fallbacks may be enabled.
RUN_CLASS_INFRA = "infrastructure"
RUN_CLASS_SCIENTIFIC = "pilot_real_model"
RUN_CLASS_SMOKE = "smoke_technical"


@dataclass(frozen=True)
class ProviderBinding:
    """Everything the runner needs from the model layer, and nothing else.

    The model layer is orthogonal to gate, topology, root mode and probe. Two runs
    that differ only in this binding differ in exactly one factor on the ledger.
    """

    adapter_name: str
    factory: Callable[[], AgentAdapter]
    metadata: dict[str, Any]
    run_class: str
    live: bool


def build_provider(
    provider: str,
    model: str | None = None,
    reasoning_effort: str | None = None,
    probe: bool = True,
    timeout_seconds: float = 60.0,
    stub_mode: str = "naive",
    smoke: bool = False,
    fallbacks: bool = False,
) -> ProviderBinding:
    if fallbacks and not smoke:
        raise ValueError(
            "refusal fallbacks are a technical-only option: they require a smoke-test run "
            "(smoke=True / --smoke) and are never permitted in a scientific set"
        )
    if provider == "deterministic_stub":
        if fallbacks:
            raise ValueError("fallbacks have no meaning for the deterministic stub")
        return ProviderBinding(
            adapter_name=f"deterministic_stub:{stub_mode}",
            factory=lambda: DeterministicStubAdapter(stub_mode),
            metadata={"provider": "local", "requested_model": None, "stub_mode": stub_mode,
                      "probe": probe, "fallbacks": False},
            run_class=RUN_CLASS_INFRA,
            live=False,
        )
    run_class = RUN_CLASS_SMOKE if smoke else RUN_CLASS_SCIENTIFIC
    if provider == "openai":
        if fallbacks:
            raise ValueError("refusal fallbacks are implemented for the anthropic provider only")
        config = OpenAIAdapterConfig.from_environment(
            model=model, reasoning_effort=reasoning_effort, timeout_seconds=timeout_seconds, probe=probe
        )
        metadata = {**config.metadata(), "fallbacks": False}
        return ProviderBinding(
            adapter_name="openai",
            factory=lambda: OpenAIResponsesAdapter(config),
            metadata=metadata,
            run_class=run_class,
            live=True,
        )
    if provider == "anthropic":
        config = AnthropicAdapterConfig.from_environment(
            model=model, effort=reasoning_effort, timeout_seconds=timeout_seconds,
            probe=probe, fallbacks=fallbacks,
        )
        return ProviderBinding(
            adapter_name="anthropic",
            factory=lambda: AnthropicMessagesAdapter(config),
            metadata=config.metadata(),
            run_class=run_class,
            live=True,
        )
    raise ValueError(f"unknown provider: {provider}; known: {', '.join(PROVIDERS)}")
