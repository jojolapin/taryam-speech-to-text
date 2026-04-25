from __future__ import annotations

from taryam_speech_to_text.settings import AppConfig
from taryam_speech_to_text.transcription.base import Engine
from taryam_speech_to_text.transcription.gemini_engine import GeminiEngine
from taryam_speech_to_text.transcription.openai_engine import OpenAIEngine

_ENGINE_CACHE: dict[tuple[str, str], Engine] = {}


def get_engine(cfg: AppConfig) -> Engine:
    if cfg.engine == "openai":
        key = ("openai", "api")
        if key not in _ENGINE_CACHE:
            _ENGINE_CACHE[key] = OpenAIEngine()
        return _ENGINE_CACHE[key]
    if cfg.engine == "gemini":
        key = ("gemini", "api")
        if key not in _ENGINE_CACHE:
            _ENGINE_CACHE[key] = GeminiEngine()
        return _ENGINE_CACHE[key]

    local_key = (cfg.local_backend, cfg.local_model)
    if local_key in _ENGINE_CACHE:
        return _ENGINE_CACHE[local_key]

    if cfg.local_backend == "openai-whisper":
        from taryam_speech_to_text.transcription.local_whisper_engine import LocalWhisperEngine

        _ENGINE_CACHE[local_key] = LocalWhisperEngine(cfg.local_model)
    else:
        from taryam_speech_to_text.transcription.faster_whisper_engine import FasterWhisperEngine

        _ENGINE_CACHE[local_key] = FasterWhisperEngine(cfg.local_model)
    return _ENGINE_CACHE[local_key]
