from __future__ import annotations

import sys

import keyboard
from PySide6.QtCore import QObject, Signal

from taryam_speech_to_text.hotkey_win32 import WHISPER_BRIDGE_HOTKEY_ID, parse_register_hotkey, register, unregister


class GlobalHotkey(QObject):
    """Global shortcut: on Windows prefers RegisterHotKey (reliable after lock/unlock); else ``keyboard`` hook."""

    pressed = Signal()
    error = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self._hotkey_ref = None
        self._current = ""
        self._win_hwnd = 0
        self._mode: str = "none"  # "none" | "winreg" | "keyboard"

    def set_native_host_hwnd(self, hwnd: int) -> None:
        """HWND of a top-level Qt window on the main thread (required for RegisterHotKey on Windows)."""
        self._win_hwnd = int(hwnd) if hwnd else 0
        if self._current and sys.platform == "win32":
            self.refresh()

    def refresh(self) -> None:
        """Re-register the current hotkey (e.g. after sleep/resume or session unlock)."""
        if self._current:
            self.set_hotkey(self._current)

    def set_hotkey(self, hotkey: str) -> None:
        hotkey = hotkey.lower().strip()
        self._clear_binding()
        self._current = hotkey
        if not hotkey:
            return

        if sys.platform == "win32" and self._win_hwnd:
            try:
                parse_register_hotkey(hotkey)
            except ValueError:
                pass
            else:
                if register(self._win_hwnd, hotkey):
                    self._mode = "winreg"
                    return

        self._mode = "keyboard"
        try:
            self._hotkey_ref = keyboard.add_hotkey(hotkey, lambda: self.pressed.emit(), suppress=False)
        except Exception as exc:
            self._hotkey_ref = None
            self.error.emit(str(exc))

    def _clear_binding(self) -> None:
        if self._mode == "winreg" and self._win_hwnd:
            unregister(self._win_hwnd)
        if self._hotkey_ref:
            try:
                keyboard.remove_hotkey(self._hotkey_ref)
            except Exception:
                pass
        self._hotkey_ref = None
        self._mode = "none"

    @staticmethod
    def win_hotkey_message_id() -> int:
        return 0x0312  # WM_HOTKEY

    @staticmethod
    def win_hotkey_id() -> int:
        return WHISPER_BRIDGE_HOTKEY_ID
