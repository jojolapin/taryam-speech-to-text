"""Legal and branding text. Edit COPYRIGHT_OWNER to your full legal name or company."""

from __future__ import annotations

# Replace with your legal name or registered business entity.
COPYRIGHT_OWNER = "Taryam"
COPYRIGHT_YEARS = "2026"
PRODUCT_NAME = "Whisper Bridge"

# Used by QSettings — keep stable across releases so user preferences are preserved.
SETTINGS_ORGANIZATION = "Taryam"
SETTINGS_APPLICATION = "SpeechToText"


def copyright_notice() -> str:
    return f"Copyright (c) {COPYRIGHT_YEARS} {COPYRIGHT_OWNER}. All rights reserved."


def copyright_short() -> str:
    return f"© {COPYRIGHT_YEARS} {COPYRIGHT_OWNER}"
