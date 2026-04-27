from __future__ import annotations

from .base import SpeechAudio, TTSEngine


class CloudTTS(TTSEngine):
    def __init__(self, provider: str = "openai"):
        self.provider = provider

    def synthesize(self, text: str) -> SpeechAudio:
        # TODO: integrate low-latency cloud TTS.
        return SpeechAudio(pcm16_bytes=b"", sample_rate=16000)
