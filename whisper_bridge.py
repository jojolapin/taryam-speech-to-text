"""Backward-compatible launcher.

Legal notice: ``taryam_speech_to_text.copyright`` (edit ``COPYRIGHT_OWNER`` for distribution).
"""

from taryam_speech_to_text.app import main


if __name__ == "__main__":
    raise SystemExit(main())