from __future__ import annotations

import torch

from taryam_speech_to_text.transcription.base import Engine


class LocalWhisperEngine(Engine):
    def __init__(self, model_name: str):
        import whisper

        self._device = "cuda" if torch.cuda.is_available() else "cpu"
        self._fp16 = self._device == "cuda"
        self._model = whisper.load_model(model_name, device=self._device, download_root=None)

    def transcribe(self, wav_path: str, language: str) -> str:
        lang = None if language == "auto" else language
        result = self._model.transcribe(wav_path, language=lang, fp16=self._fp16)
        return (result.get("text") or "").strip()
