from __future__ import annotations

from .base import ASREngine, Transcript


class CloudASR(ASREngine):
    def __init__(self, provider: str = "openai"):
        self.provider = provider

    def transcribe(self, pcm16_bytes: bytes, sample_rate: int) -> Transcript:
        # TODO: integrate streaming ASR provider.
        # For now, return empty transcript.
        return Transcript(text="", is_final=True)
