from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WakeWordEvent:
    detected: bool
    keyword: str = ""


class WakeWordEngine:
    def __init__(self, keyword: str = "assistant"):
        self.keyword = keyword

    def detect(self, pcm16_bytes: bytes) -> WakeWordEvent:
        # Placeholder. Integrate Porcupine, Snowboy, or an OEM wake word engine.
        return WakeWordEvent(detected=False, keyword=self.keyword)
