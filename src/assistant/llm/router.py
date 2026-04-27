from __future__ import annotations

from .base import LLMClient, LLMResponse


class LLMRouter(LLMClient):
    def __init__(self, cloud: LLMClient, local: LLMClient, cloud_enabled: bool = True):
        self.cloud = cloud
        self.local = local
        self.cloud_enabled = cloud_enabled

    def generate(self, prompt: str, system: str | None = None) -> LLMResponse:
        if self.cloud_enabled:
            try:
                response = self.cloud.generate(prompt, system=system)
                if response.text:
                    return response
            except Exception:
                pass
        return self.local.generate(prompt, system=system)
