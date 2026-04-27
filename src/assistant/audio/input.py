from __future__ import annotations

import queue
import threading
from dataclasses import dataclass

try:
    import sounddevice as sd
except Exception:  # pragma: no cover - optional
    sd = None


@dataclass
class AudioChunk:
    data: bytes
    sample_rate: int
    channels: int


class MicrophoneStream:
    def __init__(self, sample_rate: int = 16000, channels: int = 1, chunk_ms: int = 20):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_ms = chunk_ms
        self._queue: queue.Queue[bytes] = queue.Queue(maxsize=50)
        self._running = False
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if sd is None:
            raise RuntimeError("sounddevice not installed; cannot access microphone")
        if self._running:
            return
        self._running = True
        frames_per_chunk = int(self.sample_rate * (self.chunk_ms / 1000.0))

        def _callback(indata, frames, time, status):  # noqa: ANN001
            if status:
                pass
            if not self._running:
                return
            try:
                self._queue.put_nowait(indata.tobytes())
            except queue.Full:
                # drop oldest
                try:
                    _ = self._queue.get_nowait()
                except queue.Empty:
                    return
                self._queue.put_nowait(indata.tobytes())

        self._stream = sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=frames_per_chunk,
            dtype="int16",
            channels=self.channels,
            callback=_callback,
        )
        self._stream.start()

    def stop(self) -> None:
        self._running = False
        if hasattr(self, "_stream"):
            self._stream.stop()
            self._stream.close()

    def read_chunks(self):
        while self._running:
            try:
                data = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue
            yield AudioChunk(data=data, sample_rate=self.sample_rate, channels=self.channels)
