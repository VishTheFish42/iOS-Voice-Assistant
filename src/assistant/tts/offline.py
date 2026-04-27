from __future__ import annotations

from .base import SpeechAudio, TTSEngine


class OfflineTTS(TTSEngine):
    def __init__(self, provider: str = "piper", model_path: str | None = None):
        self.provider = provider
        self.model_path = model_path

    def synthesize(self, text: str) -> SpeechAudio:
        # TODO: integrate Piper or other offline TTS engine.
        return SpeechAudio(pcm16_bytes=b"", sample_rate=16000)
