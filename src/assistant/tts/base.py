from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SpeechAudio:
    pcm16_bytes: bytes
    sample_rate: int


class TTSEngine:
    def synthesize(self, text: str) -> SpeechAudio:
        raise NotImplementedError
