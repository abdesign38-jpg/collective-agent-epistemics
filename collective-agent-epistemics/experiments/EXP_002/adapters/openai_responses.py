from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..models import AgentMessage, AgentObservation, AgentResponse
from ..prompting import render_agent_input

DEFAULT_MODEL = "gpt-6-astra"


class ModelAgentResponse(BaseModel):
    model_config = ConfigDict(strict=True)

    answer: Literal["A", "B"]
    confidence: float = Field(ge=0.0, le=1.0)
    message: str = Field(min_length=1)

    @field_validator("message")
    @classmethod
    def message_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("message must not be blank")
        return value


@dataclass(frozen=True)
class OpenAIAdapterConfig:
    model: str = DEFAULT_MODEL
    reasoning_effort: str | None = None
    timeout_seconds: float = 60.0

    @classmethod
    def from_environment(
        cls,
        model: str | None = None,
        reasoning_effort: str | None = None,
        timeout_seconds: float = 60.0,
    ) -> "OpenAIAdapterConfig":
        return cls(
            model=model or os.getenv("EXP002_MODEL") or DEFAULT_MODEL,
            reasoning_effort=reasoning_effort,
            timeout_seconds=timeout_seconds,
        )

    def metadata(self) -> dict[str, Any]:
        return {
            "provider": "openai",
            "requested_model": self.model,
            "reasoning_effort": self.reasoning_effort,
            "timeout_seconds": self.timeout_seconds,
            "sdk_version": _sdk_version(),
        }


class OpenAIAdapterError(RuntimeError):
    pass


class OpenAIResponsesAdapter:
    def __init__(self, config: OpenAIAdapterConfig, client: Any | None = None) -> None:
        self.config = config
        self.last_call_metadata: dict[str, Any] = {}
        if client is not None:
            self.client = client
            return
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise OpenAIAdapterError("OPENAI_API_KEY is required for the OpenAI adapter")
        from openai import OpenAI

        self.client = OpenAI(
            api_key=api_key,
            timeout=config.timeout_seconds,
            max_retries=0,
        )

    def respond(
        self,
        agent_id: str,
        observation: AgentObservation,
        received_message: AgentMessage | None,
        condition: str,
    ) -> AgentResponse:
        del condition
        prompt = render_agent_input(agent_id, observation, received_message)
        request: dict[str, Any] = {
            "model": self.config.model,
            "input": prompt,
            "text_format": ModelAgentResponse,
            "timeout": self.config.timeout_seconds,
            "store": False,
        }
        if self.config.reasoning_effort is not None:
            request["reasoning"] = {"effort": self.config.reasoning_effort}

        started = time.perf_counter()
        try:
            response = self.client.responses.parse(**request)
        except Exception as exc:
            self.last_call_metadata = {
                "provider": "openai",
                "requested_model": self.config.model,
                "attempt_count": 1,
                "latency_ms": round((time.perf_counter() - started) * 1000, 3),
                "error": type(exc).__name__,
            }
            raise OpenAIAdapterError("OpenAI Responses request failed") from exc

        self.last_call_metadata = _response_metadata(
            response,
            self.config.model,
            round((time.perf_counter() - started) * 1000, 3),
        )
        if getattr(response, "status", "completed") != "completed":
            raise OpenAIAdapterError(f"OpenAI response incomplete: {response.status}")
        if getattr(response, "incomplete_details", None) is not None:
            raise OpenAIAdapterError("OpenAI response contains incomplete details")
        parsed = getattr(response, "output_parsed", None)
        if parsed is None:
            raise OpenAIAdapterError("OpenAI response did not contain parsed output")
        if not isinstance(parsed, ModelAgentResponse):
            try:
                parsed = ModelAgentResponse.model_validate(parsed, strict=True)
            except Exception as exc:
                raise OpenAIAdapterError("OpenAI response failed schema validation") from exc
        return AgentResponse(
            answer=parsed.answer,
            confidence=parsed.confidence,
            message=parsed.message,
        )


def _response_metadata(response: Any, requested_model: str, latency_ms: float) -> dict[str, Any]:
    usage = getattr(response, "usage", None)
    return {
        "provider": "openai",
        "requested_model": requested_model,
        "returned_model": getattr(response, "model", None),
        "response_id": getattr(response, "id", None),
        "usage": {
            "input_tokens": getattr(usage, "input_tokens", None),
            "output_tokens": getattr(usage, "output_tokens", None),
            "total_tokens": getattr(usage, "total_tokens", None),
        },
        "latency_ms": latency_ms,
        "attempt_count": 1,
    }


def _sdk_version() -> str:
    try:
        import openai

        return openai.__version__
    except ImportError:
        return "unavailable"
