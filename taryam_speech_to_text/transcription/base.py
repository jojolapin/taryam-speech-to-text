from __future__ import annotations

from abc import ABC, abstractmethod


class Engine(ABC):
    @abstractmethod
    def transcribe(self, wav_path: str, language: str) -> str:
        raise NotImplementedError
