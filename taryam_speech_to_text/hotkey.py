from __future__ import annotations

import keyboard
from PySide6.QtCore import QObject, Signal


class GlobalHotkey(QObject):
    pressed = Signal()
    error = Signal(str)

    def __init__(self):
        super().__init__()
        self._hotkey_ref = None
        self._current = ""

    def set_hotkey(self, hotkey: str) -> None:
        hotkey = hotkey.lower().strip()
        if self._hotkey_ref:
            try:
                keyboard.remove_hotkey(self._hotkey_ref)
            except Exception:
                pass
            self._hotkey_ref = None
        self._current = hotkey
        try:
            self._hotkey_ref = keyboard.add_hotkey(hotkey, lambda: self.pressed.emit(), suppress=False)
        except Exception as exc:
            self.error.emit(str(exc))
