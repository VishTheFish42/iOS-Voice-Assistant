from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Transcript:
    text: str
    is_final: bool = True
    confidence: float | None = None


class ASREngine:
    def transcribe(self, pcm16_bytes: bytes, sample_rate: int) -> Transcript:
        raise NotImplementedError
