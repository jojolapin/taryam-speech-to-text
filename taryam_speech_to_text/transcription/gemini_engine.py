from __future__ import annotations

import os

from google import genai

from taryam_speech_to_text.transcription.base import Engine


class GeminiEngine(Engine):
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set")
        self._client = genai.Client(api_key=api_key)

    def transcribe(self, wav_path: str, language: str) -> str:
        uploaded_file = self._client.files.upload(file=wav_path)
        prompt = "Transcribe this audio exactly as spoken. Output only the transcription, nothing else."
        if language == "en":
            prompt += " The spoken language is English."
        elif language == "fr":
            prompt += " The spoken language is French."
        response = self._client.models.generate_content(model="gemini-2.5-flash", contents=[uploaded_file, prompt])
        self._client.files.delete(name=uploaded_file.name)
        return (response.text or "").strip()
