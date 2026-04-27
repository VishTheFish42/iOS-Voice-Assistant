from __future__ import annotations

import time

from .base import LLMClient, LLMResponse


class OllamaClient(LLMClient):
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model

    def generate(self, prompt: str, system: str | None = None) -> LLMResponse:
        # TODO: integrate Ollama generate/streaming endpoint.
        start = time.time()
        text = ""
        latency = int((time.time() - start) * 1000)
        return LLMResponse(text=text, latency_ms=latency, provider="ollama")
