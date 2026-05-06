"""Windows RegisterHotKey + WM_HOTKEY — survives lock/unlock better than low-level hooks."""

from __future__ import annotations

import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32

MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
MOD_WIN = 0x0008

# Unique within our process; avoid clashing with other RegisterHotKey users in same app.
WHISPER_BRIDGE_HOTKEY_ID = 0xB8E1

_VK_SPECIAL = {
    "space": 0x20,
    "tab": 0x09,
    "enter": 0x0D,
    "return": 0x0D,
    "esc": 0x1B,
    "escape": 0x1B,
    "backspace": 0x08,
    "delete": 0x2E,
    "insert": 0x2D,
    "home": 0x24,
    "end": 0x23,
    "page up": 0x21,
    "page down": 0x22,
    "up": 0x26,
    "down": 0x28,
    "left": 0x25,
    "right": 0x27,
    "print screen": 0x2C,
    "scroll lock": 0x91,
    "pause": 0x13,
    "caps lock": 0x14,
    "num lock": 0x90,
}


def _vk_from_key_token(token: str) -> int | None:
    t = token.strip().lower()
    if not t:
        return None
    if t in _VK_SPECIAL:
        return _VK_SPECIAL[t]
    if len(t) == 1 and t.isalpha():
        return ord(t.upper())
    if len(t) == 1 and t.isdigit():
        return ord(t)
    if t.startswith("f") and len(t) > 1 and t[1:].isdigit():
        n = int(t[1:])
        if 1 <= n <= 24:
            return 0x70 + (n - 1)
    return None


def parse_register_hotkey(combo: str) -> tuple[int, int]:
    """Return (fsModifiers, vk) for RegisterHotKey, or raise ValueError if unsupported."""
    if "," in combo:
        raise ValueError("multi-step hotkeys are not supported for RegisterHotKey")
    parts = [p.strip().lower() for p in combo.split("+") if p.strip()]
    if not parts:
        raise ValueError("empty hotkey")
    mods = 0
    key_parts: list[str] = []
    for p in parts:
        if p in ("ctrl", "control"):
            mods |= MOD_CONTROL
        elif p == "shift":
            mods |= MOD_SHIFT
        elif p == "alt":
            mods |= MOD_ALT
        elif p in ("win", "windows", "left windows", "right windows"):
            mods |= MOD_WIN
        else:
            key_parts.append(p)
    if len(key_parts) != 1:
        raise ValueError("multi-key sequences are not supported for RegisterHotKey")
    vk = _vk_from_key_token(key_parts[0])
    if vk is None:
        raise ValueError(f"unknown key: {key_parts[0]!r}")
    return mods, vk


def register(hwnd: int, combo: str) -> bool:
    if not hwnd:
        return False
    user32.UnregisterHotKey(hwnd, WHISPER_BRIDGE_HOTKEY_ID)
    mods, vk = parse_register_hotkey(combo)
    return bool(user32.RegisterHotKey(wintypes.HWND(hwnd), WHISPER_BRIDGE_HOTKEY_ID, mods, vk))


def unregister(hwnd: int) -> None:
    if hwnd:
        user32.UnregisterHotKey(hwnd, WHISPER_BRIDGE_HOTKEY_ID)
