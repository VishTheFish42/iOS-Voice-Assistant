from __future__ import annotations

import time

from .base import LLMClient, LLMResponse


class OpenAIClient(LLMClient):
    def __init__(self, api_key: str | None, model: str):
        self.api_key = api_key
        self.model = model

    def generate(self, prompt: str, system: str | None = None) -> LLMResponse:
        # TODO: integrate OpenAI Responses API with streaming for low latency.
        start = time.time()
        text = ""
        latency = int((time.time() - start) * 1000)
        return LLMResponse(text=text, latency_ms=latency, provider="openai")
