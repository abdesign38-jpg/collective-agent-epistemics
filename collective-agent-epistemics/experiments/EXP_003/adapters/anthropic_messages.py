from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any, Literal

from ..models import AgentMessage, AgentObservation, AgentResponse
from ..prompting import PROMPT_VERSION, render_agent_input
from .openai_responses import SCHEMA_VERSION, ModelAgentResponse, ModelAgentResponseNoProbe

Effort = Literal["low", "medium", "high", "xhigh", "max"]
SUPPORTED_EFFORTS = ("low", "medium", "high", "xhigh", "max")
DEFAULT_MODEL = "claude-opus-5"
MAX_TOKENS = 4096
FALLBACK_BETA = "server-side-fallback-2026-07-01"


@dataclass(frozen=True)
class AnthropicAdapterConfig:
    """Second-provider configuration.

    The response schema, prompt and probe are shared with the OpenAI adapter so that
    provider is the only factor that changes between paired model sets.

    Refusal fallbacks are a technical-only option. Off (the default), a refusal is a
    technical failure and the harness retries the same seed. On, the request opts into
    Anthropic's server-side `fallbacks: "default"`, which re-runs a declined request on
    a substitute model inside the same call; every served model is recorded per event
    and the registry permits this only for smoke-test run classes, never for a
    scientific set, so the frozen design is not touched.
    """

    model: str
    effort: Effort
    timeout_seconds: float = 60.0
    probe: bool = True
    fallbacks: bool = False

    def __post_init__(self) -> None:
        if not self.model.strip():
            raise ValueError("EXP-003 Anthropic runs require an explicit model via --model or EXP003_MODEL")
        if self.effort not in SUPPORTED_EFFORTS:
            raise ValueError(
                "EXP-003 Anthropic runs require an explicit effort: " + ", ".join(SUPPORTED_EFFORTS)
            )
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")

    @classmethod
    def from_environment(
        cls,
        model: str | None = None,
        effort: str | None = None,
        timeout_seconds: float = 60.0,
        probe: bool = True,
        fallbacks: bool = False,
    ) -> "AnthropicAdapterConfig":
        selected_model = model or os.getenv("EXP003_MODEL")
        if not selected_model:
            raise ValueError("EXP-003 Anthropic runs require an explicit model via --model or EXP003_MODEL")
        if effort is None:
            raise ValueError("EXP-003 Anthropic runs require an explicit effort via --reasoning-effort")
        return cls(  # type: ignore[arg-type]
            model=selected_model, effort=effort, timeout_seconds=timeout_seconds,
            probe=probe, fallbacks=fallbacks,
        )

    def metadata(self) -> dict[str, Any]:
        return {
            "provider": "anthropic",
            "requested_model": self.model,
            "reasoning_effort": self.effort,
            "thinking": "adaptive",
            "timeout_seconds": self.timeout_seconds,
            "store": False,
            "max_retries": 0,
            "fallbacks": self.fallbacks,
            "fallback_mode": "default" if self.fallbacks else None,
            "probe": self.probe,
            "prompt_version": PROMPT_VERSION,
            "schema_version": SCHEMA_VERSION,
            "sdk_version": _sdk_version(),
        }


class AnthropicAdapterError(RuntimeError):
    pass


class AnthropicMessagesAdapter:
    def __init__(self, config: AnthropicAdapterConfig, client: Any | None = None) -> None:
        self.config = config
        self.last_call_metadata: dict[str, Any] = {}
        if client is not None:
            self.client = client
            return
        if not (os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN")):
            raise AnthropicAdapterError(
                "ANTHROPIC_API_KEY (or ANTHROPIC_AUTH_TOKEN) is required for the Anthropic adapter"
            )
        import anthropic

        self.client = anthropic.Anthropic(timeout=config.timeout_seconds, max_retries=0)

    def respond(
        self,
        agent_id: str,
        observation: AgentObservation,
        received_messages: tuple[AgentMessage, ...],
        condition: str,
    ) -> AgentResponse:
        del condition
        prompt = render_agent_input(agent_id, observation, received_messages, probe=self.config.probe)
        schema = ModelAgentResponse if self.config.probe else ModelAgentResponseNoProbe
        request: dict[str, Any] = {
            "model": self.config.model,
            "max_tokens": MAX_TOKENS,
            "messages": [{"role": "user", "content": prompt}],
            "output_format": schema,
            "thinking": {"type": "adaptive"},
            "output_config": {"effort": self.config.effort},
            "timeout": self.config.timeout_seconds,
        }
        if self.config.fallbacks:
            # Technical-only. The "default" scalar form pairs with this exact beta header.
            request["betas"] = [FALLBACK_BETA]
            request["fallbacks"] = "default"
            endpoint = self.client.beta.messages
        else:
            endpoint = self.client.messages

        started = time.perf_counter()
        try:
            response = endpoint.parse(**request)
        except Exception as exc:
            self.last_call_metadata = {
                "provider": "anthropic",
                "requested_model": self.config.model,
                "attempt_count": 1,
                "latency_ms": round((time.perf_counter() - started) * 1000, 3),
                "error": type(exc).__name__,
            }
            raise AnthropicAdapterError("Anthropic Messages request failed") from exc

        self.last_call_metadata = _response_metadata(
            response, self.config.model, round((time.perf_counter() - started) * 1000, 3)
        )
        stop_reason = getattr(response, "stop_reason", "end_turn")
        if stop_reason == "refusal":
            details = getattr(response, "stop_details", None)
            category = getattr(details, "category", None) if details is not None else None
            self.last_call_metadata["refusal_category"] = category
            raise AnthropicAdapterError(f"Anthropic response refused (category={category})")
        if stop_reason == "max_tokens":
            raise AnthropicAdapterError("Anthropic response truncated at max_tokens")
        parsed = getattr(response, "parsed_output", None)
        if parsed is None:
            raise AnthropicAdapterError("Anthropic response did not contain parsed output")
        if not isinstance(parsed, schema):
            try:
                parsed = schema.model_validate(parsed, strict=True)
            except Exception as exc:
                raise AnthropicAdapterError("Anthropic response failed schema validation") from exc
        return AgentResponse(
            answer=parsed.answer,
            confidence=parsed.confidence,
            message=parsed.message,
            distinct_source_count=getattr(parsed, "distinct_source_count", None),
        )


def _fallback_trace(response: Any) -> tuple[bool, list[dict[str, Any]]]:
    """Whether a server-side fallback served this response, and the switch points."""
    usage = getattr(response, "usage", None)
    iterations = getattr(usage, "iterations", None) or []
    ran = any(getattr(entry, "type", None) == "fallback_message" for entry in iterations)
    switches: list[dict[str, Any]] = []
    for block in getattr(response, "content", None) or []:
        if getattr(block, "type", None) == "fallback":
            from_ = getattr(block, "from_", None)
            to = getattr(block, "to", None)
            switches.append({
                "from_model": getattr(from_, "model", None),
                "to_model": getattr(to, "model", None),
            })
            ran = True
    return ran, switches


def _response_metadata(response: Any, requested_model: str, latency_ms: float) -> dict[str, Any]:
    usage = getattr(response, "usage", None)
    input_tokens = getattr(usage, "input_tokens", None)
    output_tokens = getattr(usage, "output_tokens", None)
    total = (input_tokens or 0) + (output_tokens or 0) if usage is not None else None
    served_model = getattr(response, "model", None)
    fallback_ran, switches = _fallback_trace(response)
    return {
        "provider": "anthropic",
        "requested_model": requested_model,
        "returned_model": served_model,
        "served_model": served_model,
        "fallback_ran": fallback_ran,
        "fallback_switches": switches,
        "model_matches_request": bool(served_model) and served_model.startswith(requested_model),
        "response_id": getattr(response, "id", None),
        "stop_reason": getattr(response, "stop_reason", None),
        "usage": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total,
        },
        "latency_ms": latency_ms,
        "attempt_count": 1,
    }


def _sdk_version() -> str:
    try:
        import anthropic

        return anthropic.__version__
    except ImportError:
        return "unavailable"
