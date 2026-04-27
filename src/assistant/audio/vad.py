from __future__ import annotations

try:
    import webrtcvad
except Exception:  # pragma: no cover - optional
    webrtcvad = None


class VoiceActivityDetector:
    def __init__(self, sample_rate: int = 16000, mode: int = 2):
        if webrtcvad is None:
            raise RuntimeError("webrtcvad not installed; VAD unavailable")
        self._vad = webrtcvad.Vad(mode)
        self.sample_rate = sample_rate

    def is_speech(self, pcm16_bytes: bytes) -> bool:
        return self._vad.is_speech(pcm16_bytes, self.sample_rate)
