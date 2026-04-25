from __future__ import annotations

import queue
import tempfile
import threading
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import sounddevice as sd
import soundfile as sf
from PySide6.QtCore import QObject, Signal

from taryam_speech_to_text.audio.devices import resolve_device_index


@dataclass
class CaptureConfig:
    rate: int = 16000
    channels: int = 1
    max_record_seconds: int = 300
    mic_device: str = ""


class AudioCapture(QObject):
    level_changed = Signal(int)
    error = Signal(str)

    def __init__(self, cfg: CaptureConfig):
        super().__init__()
        self.cfg = cfg
        self._queue: queue.Queue = queue.Queue()
        self._stream = None
        self._writer: threading.Thread | None = None
        self._recording = False
        self._start_time = 0.0
        self.output_file = str(Path(tempfile.gettempdir()) / "dictation_temp.wav")

    @property
    def recording(self) -> bool:
        return self._recording

    def _audio_callback(self, indata, frames, _t, status):
        if status:
            self.error.emit(str(status))
        rms = float(np.sqrt(np.mean(np.square(indata)))) if len(indata) else 0.0
        self.level_changed.emit(min(int(rms * 2500), 100))
        self._queue.put(indata.copy())

    def _writer_loop(self):
        with sf.SoundFile(
            self.output_file, mode="w", samplerate=self.cfg.rate, channels=self.cfg.channels, subtype="PCM_16"
        ) as file:
            while self._recording or not self._queue.empty():
                try:
                    data = self._queue.get(timeout=0.1)
                    file.write(data)
                except queue.Empty:
                    continue

    def start(self) -> None:
        if self._recording:
            return
        self._recording = True
        self._start_time = time.time()
        while not self._queue.empty():
            self._queue.get()
        device_idx = resolve_device_index(self.cfg.mic_device)
        try:
            self._stream = sd.InputStream(
                samplerate=self.cfg.rate,
                channels=self.cfg.channels,
                callback=self._audio_callback,
                device=device_idx,
            )
            self._stream.start()
        except Exception as exc:
            self._recording = False
            self.error.emit(str(exc))
            return
        self._writer = threading.Thread(target=self._writer_loop, daemon=True)
        self._writer.start()

    def stop(self) -> str:
        self._recording = False
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        if self._writer is not None:
            self._writer.join()
            self._writer = None
        self.level_changed.emit(0)
        return self.output_file

    def elapsed_seconds(self) -> int:
        if not self._recording:
            return 0
        return int(time.time() - self._start_time)
