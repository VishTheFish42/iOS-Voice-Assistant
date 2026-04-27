from __future__ import annotations

from .base import ASREngine, Transcript


class OfflineASR(ASREngine):
    def __init__(self, provider: str = "vosk", model_path: str | None = None):
        self.provider = provider
        self.model_path = model_path

    def transcribe(self, pcm16_bytes: bytes, sample_rate: int) -> Transcript:
        # TODO: integrate Vosk or Whisper.cpp.
        return Transcript(text="", is_final=True)
