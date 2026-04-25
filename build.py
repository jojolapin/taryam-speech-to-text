from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from taryam_speech_to_text.copyright import copyright_notice

ROOT = Path(__file__).resolve().parent
ICON = ROOT / "app.ico"


def main() -> int:
    try:
        from build_icon import generate_icon

        generate_icon(ICON)
        print(f"Icon generated: {ICON}")
    except Exception as exc:
        print(f"Icon generation skipped: {exc}")

    cmd = [sys.executable, "-m", "PyInstaller", "--noconfirm", "whisper_bridge.spec"]
    print("Running:", " ".join(cmd))
    proc = subprocess.run(cmd, cwd=ROOT)
    if proc.returncode == 0:
        print(copyright_notice())
        print(f"Build complete: {ROOT / 'dist' / 'WhisperBridge.exe'}")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
