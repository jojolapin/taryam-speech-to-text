"""Resolve bundled user documentation paths (dev and PyInstaller one-file)."""

from __future__ import annotations

import sys
from pathlib import Path


def help_markdown_path() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / "taryam_speech_to_text" / "docs" / "HELP.md"
    return Path(__file__).resolve().parent / "docs" / "HELP.md"
