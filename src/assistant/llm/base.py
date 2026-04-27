from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LLMResponse:
    text: str
    latency_ms: int | None = None
    provider: str | None = None


class LLMClient:
    def generate(self, prompt: str, system: str | None = None) -> LLMResponse:
        raise NotImplementedError
