from __future__ import annotations

import ctypes
from typing import Optional

import pyautogui
import pyperclip
import win32con
import win32gui
import win32process
from PySide6.QtCore import QObject, QTimer, Signal


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]


class GUITHREADINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_ulong),
        ("flags", ctypes.c_ulong),
        ("hwndActive", ctypes.c_void_p),
        ("hwndFocus", ctypes.c_void_p),
        ("hwndCapture", ctypes.c_void_p),
        ("hwndMenuOwner", ctypes.c_void_p),
        ("hwndMoveSize", ctypes.c_void_p),
        ("hwndCaret", ctypes.c_void_p),
        ("rcCaret", RECT),
    ]


def get_focused_control_hwnd(hwnd_top: int) -> Optional[int]:
    """Return ``hwndFocus`` for the thread that owns the top-level ``hwnd_top``, or ``None``."""
    if not hwnd_top or not win32gui.IsWindow(hwnd_top):
        return None
    try:
        target_tid, _pid = win32process.GetWindowThreadProcessId(hwnd_top)
    except Exception:
        return None
    gti = GUITHREADINFO()
    gti.cbSize = ctypes.sizeof(GUITHREADINFO)
    if not ctypes.windll.user32.GetGUIThreadInfo(target_tid, ctypes.byref(gti)):
        return None
    fh = gti.hwndFocus
    if not fh:
        return None
    hwnd_focus = int(fh)
    if win32gui.IsWindow(hwnd_focus):
        return hwnd_focus
    return None


def _should_use_wm_paste(focus_hwnd: int) -> bool:
    try:
        cls = win32gui.GetClassName(focus_hwnd)
    except Exception:
        return False
    if cls in ("Edit", "Scintilla"):
        return True
    if cls.startswith("RichEdit"):
        return True
    if cls.startswith("TX12_"):
        return True
    return False


def restore_focus_to_window(target_hwnd: int, focused_hwnd: Optional[int]) -> bool:
    """Bring ``target_hwnd`` to foreground and focus ``focused_hwnd`` (or top-level). Returns success."""
    if not target_hwnd or not win32gui.IsWindow(target_hwnd):
        return False
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    current_tid = kernel32.GetCurrentThreadId()
    try:
        target_tid, _pid = win32process.GetWindowThreadProcessId(target_hwnd)
    except Exception:
        return False
    attached = False
    if current_tid != target_tid:
        attached = bool(user32.AttachThreadInput(current_tid, target_tid, True))
    try:
        if win32gui.IsIconic(target_hwnd):
            user32.ShowWindow(target_hwnd, win32con.SW_RESTORE)
        win32gui.BringWindowToTop(target_hwnd)
        user32.SetForegroundWindow(target_hwnd)
        fh = int(focused_hwnd) if focused_hwnd and win32gui.IsWindow(int(focused_hwnd)) else target_hwnd
        user32.SetFocus(fh)
        fg = win32gui.GetForegroundWindow()
        return fg == target_hwnd
    except Exception:
        return False
    finally:
        if attached:
            user32.AttachThreadInput(current_tid, target_tid, False)


class PasteController(QObject):
    done = Signal(bool, str)

    def __init__(self) -> None:
        super().__init__()
        self._old_clipboard: Optional[str] = None
        self._clipboard_gen = 0

    def copy_and_paste(
        self,
        text: str,
        target_hwnd: Optional[int],
        focused_hwnd: Optional[int],
        auto_paste: bool,
        preserve_clipboard: bool,
    ) -> None:
        self._clipboard_gen += 1
        gen = self._clipboard_gen
        self._old_clipboard = None
        if preserve_clipboard and auto_paste:
            try:
                self._old_clipboard = pyperclip.paste()
            except Exception:
                self._old_clipboard = None

        try:
            pyperclip.copy(text)
        except Exception:
            self.done.emit(False, "paste")
            return

        if not auto_paste:
            self.done.emit(True, "clipboard")
            return

        tw = int(target_hwnd) if target_hwnd and win32gui.IsWindow(int(target_hwnd)) else 0
        fw = int(focused_hwnd) if focused_hwnd and win32gui.IsWindow(int(focused_hwnd)) else None

        def phase_restore() -> None:
            if not tw or not win32gui.IsWindow(tw):
                self.done.emit(False, "focus_failed_clipboard")
                return
            if not restore_focus_to_window(tw, fw):
                self.done.emit(False, "focus_failed_clipboard")
                return
            QTimer.singleShot(120, phase_paste)

        def phase_paste() -> None:
            if gen != self._clipboard_gen:
                return
            try:
                fh = fw if fw and win32gui.IsWindow(fw) else tw
                if _should_use_wm_paste(fh):
                    win32gui.SendMessage(fh, win32con.WM_PASTE, 0, 0)
                else:
                    pyautogui.hotkey("ctrl", "v")
            except Exception:
                self.done.emit(False, "paste")
                return

            if preserve_clipboard and self._old_clipboard is not None:

                def restore_clipboard() -> None:
                    if gen != self._clipboard_gen:
                        return
                    try:
                        pyperclip.copy(self._old_clipboard)
                    except Exception:
                        pass
                    self._old_clipboard = None

                QTimer.singleShot(3000, restore_clipboard)

            self.done.emit(True, "pasted")

        QTimer.singleShot(0, phase_restore)
