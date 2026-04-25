from __future__ import annotations

import os

from taryam_speech_to_text.transcription.base import Engine


class OpenAIEngine(Engine):
    def __init__(self):
        from openai import OpenAI

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        self._client = OpenAI(api_key=api_key)

    def transcribe(self, wav_path: str, language: str) -> str:
        with open(wav_path, "rb") as audio_file:
            params = {"model": "whisper-1", "file": audio_file, "response_format": "text"}
            if language != "auto":
                params["language"] = language
            return self._client.audio.transcriptions.create(**params).strip()
