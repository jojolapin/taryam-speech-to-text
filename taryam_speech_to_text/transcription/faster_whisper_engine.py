from __future__ import annotations

import torch

from taryam_speech_to_text.transcription.base import Engine


class FasterWhisperEngine(Engine):
    def __init__(self, model_name: str):
        from faster_whisper import WhisperModel

        device = "cuda" if torch.cuda.is_available() else "cpu"
        compute_type = "float16" if device == "cuda" else "int8"
        self._model = WhisperModel(model_name, device=device, compute_type=compute_type)

    def transcribe(self, wav_path: str, language: str) -> str:
        lang = None if language == "auto" else language
        segments, _ = self._model.transcribe(wav_path, language=lang)
        return " ".join(seg.text.strip() for seg in segments).strip()
