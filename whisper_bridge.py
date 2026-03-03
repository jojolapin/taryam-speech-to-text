import sys
import os
import queue
import tempfile
import threading
import ctypes
import time
import keyboard
import sounddevice as sd
import soundfile as sf
import pyperclip
import pyautogui
import win32gui
import win32con
import win32process
from dotenv import load_dotenv
from openai import OpenAI
from google import genai

from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout,
                               QMenu, QSystemTrayIcon)
from PySide6.QtCore import Qt, QPoint, QThread, Signal, QObject, QEvent, QTimer
from PySide6.QtGui import (QFont, QCursor, QIcon, QPixmap, QPainter, QColor,
                           QAction, QActionGroup)

# Load environment variables
load_dotenv()

# --- GLOBAL STATE ---
ACTIVE_ENGINE = "local"  # "gemini", "openai", or "local" — default: local Whisper
ACTIVE_LANGUAGE = "auto"  # "auto", "en", or "fr"
ACTIVE_WHISPER_MODEL = "base"  # for local: "base", "large-v3", "small", "medium", "large-v2"
WHISPER_MODELS_PRELOAD = ("base", "small", "medium", "large-v2", "large-v3")
HOTKEY = 'f8'
RATE = 44100
CHANNELS = 1
WAVE_OUTPUT_FILENAME = os.path.join(tempfile.gettempdir(), "dictation_temp.wav")

# Initialize Clients
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


# --- THREAD 1: THE API WORKER ---
class TranscriptionWorker(QThread):
    finished = Signal(str)
    error = Signal(str)

    def run(self):
        try:
            if ACTIVE_ENGINE == "openai":
                with open(WAVE_OUTPUT_FILENAME, "rb") as audio_file:
                    params = {"model": "whisper-1", "file": audio_file, "response_format": "text"}
                    if ACTIVE_LANGUAGE != "auto":
                        params["language"] = ACTIVE_LANGUAGE
                    text = openai_client.audio.transcriptions.create(**params).strip()

            elif ACTIVE_ENGINE == "gemini":
                uploaded_file = gemini_client.files.upload(file=WAVE_OUTPUT_FILENAME)
                prompt = "Transcribe this audio exactly as spoken. Output only the transcription, nothing else."
                if ACTIVE_LANGUAGE == "en":
                    prompt += " The spoken language is English."
                elif ACTIVE_LANGUAGE == "fr":
                    prompt += " The spoken language is French."

                response = gemini_client.models.generate_content(
                    model='gemini-2.5-flash', contents=[uploaded_file, prompt]
                )
                gemini_client.files.delete(name=uploaded_file.name)
                text = response.text.strip()

            elif ACTIVE_ENGINE == "local":
                try:
                    import whisper
                except ImportError:
                    self.error.emit("Local Whisper not installed. Run: pip install openai-whisper")
                    return
                # Uses .pt from ~/.cache/whisper/ or downloads on first use
                import torch
                device = "cuda" if torch.cuda.is_available() else "cpu"
                fp16 = device == "cuda"
                model = whisper.load_model(ACTIVE_WHISPER_MODEL, device=device, download_root=None)
                lang = None if ACTIVE_LANGUAGE == "auto" else ACTIVE_LANGUAGE
                result = model.transcribe(WAVE_OUTPUT_FILENAME, language=lang, fp16=fp16)
                text = (result.get("text") or "").strip()

            else:
                self.error.emit(f"Unknown engine: {ACTIVE_ENGINE}")
                return

            self.finished.emit(text)
        except Exception as e:
            self.error.emit(str(e))


# --- THREAD SAFE SIGNAL FOR GLOBAL HOTKEY ---
class HotkeySignal(QObject):
    # Emit with hwnd of window that had focus when F8 was pressed (0 = ignore)
    toggle = Signal(int)


# --- BACKGROUND: PRELOAD ALL LOCAL WHISPER MODELS (once) ---
def _whisper_preload_sentinel():
    return os.path.join(os.path.expanduser("~"), ".cache", "whisper", ".whisper_bridge_preload_done")


class PreloadWhisperModelsWorker(QThread):
    """Downloads all Whisper models in the background so they're ready when the user switches model."""

    def run(self):
        if os.path.isfile(_whisper_preload_sentinel()):
            return
        try:
            import whisper
        except ImportError:
            return
        cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "whisper")
        os.makedirs(cache_dir, exist_ok=True)
        for name in WHISPER_MODELS_PRELOAD:
            try:
                whisper.load_model(name, device="cpu", download_root=cache_dir)
            except Exception:
                pass
        try:
            with open(_whisper_preload_sentinel(), "w") as f:
                f.write("1")
        except Exception:
            pass


# --- THE MAIN GUI WIDGET ---
class DictationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.stream = None
        self.file_writer = None
        self.transcription_thread = None

        # Drag state
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        # Focus tracking: the window where user wants text pasted
        self.target_hwnd = None
        self._my_pid = os.getpid()

        # Poll every 250ms to remember which EXTERNAL window has focus
        # Timer STOPS during recording so we don't overwrite the target
        self._focus_timer = QTimer(self)
        self._focus_timer.timeout.connect(self._track_foreground_window)
        self._focus_timer.start(250)

        self.init_ui()
        self._apply_noactivate()  # Win32-level no-activate
        self.setup_tray()
        self.setup_hotkey()
        # Pre-download all Whisper models once in the background (does not block UI)
        self._preload_worker = PreloadWhisperModelsWorker()
        self._preload_worker.start()

    def _apply_noactivate(self):
        """Apply WS_EX_NOACTIVATE at Win32 level - the widget will NEVER steal focus."""
        hwnd = int(self.winId())
        ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        ex_style |= win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)

    def _is_own_process_window(self, hwnd):
        """Check if a window belongs to our own process (widget, etc.)."""
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            return pid == self._my_pid
        except Exception:
            return False

    @staticmethod
    def _is_console_like_window(hwnd):
        """Ignore Run/Console/Debug windows so we never paste transcription there."""
        try:
            title = (win32gui.GetWindowText(hwnd) or "").lower()
            if not title:
                return False
            for skip in ("run", "console", "debug", "terminal", "output"):
                if skip in title:
                    return True
            return False
        except Exception:
            return False

    def _track_foreground_window(self):
        """Track which EXTERNAL window has focus. Ignores our process and Run/Console/Debug."""
        try:
            hwnd = win32gui.GetForegroundWindow()
            if hwnd and not self._is_own_process_window(hwnd) and not self._is_console_like_window(hwnd):
                self.target_hwnd = hwnd
        except Exception:
            pass

    def init_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)

        self.setFixedSize(240, 96)

        layout = QHBoxLayout()
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(15)

        font_large = QFont("Segoe UI", 16)
        font_mic = QFont("Segoe UI", 22)

        self.btn_settings = QPushButton("⚙️")
        self.btn_settings.setFont(font_large)
        self.btn_settings.setObjectName("IconButton")
        self.btn_settings.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_settings.clicked.connect(self.show_settings_menu)

        self.btn_mic = QPushButton("🎙️")
        self.btn_mic.setFont(font_mic)
        self.btn_mic.setObjectName("MicButton")
        self.btn_mic.setFixedSize(60, 60)
        self.btn_mic.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_mic.clicked.connect(self.toggle_recording)

        self.btn_help = QPushButton("❓")
        self.btn_help.setFont(font_large)
        self.btn_help.setObjectName("IconButton")
        self.btn_help.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_help.clicked.connect(lambda: QApplication.quit() if keyboard.is_pressed('shift') else None)

        layout.addWidget(self.btn_settings)
        layout.addWidget(self.btn_mic)
        layout.addWidget(self.btn_help)

        self.setLayout(layout)
        self.apply_styles()
        self.setup_menus()

        # Install event filter on buttons so dragging works everywhere
        self.btn_settings.installEventFilter(self)
        self.btn_mic.installEventFilter(self)
        self.btn_help.installEventFilter(self)

    def apply_styles(self):
        self.setStyleSheet("""
            DictationWidget {
                background-color: #F8F9FA;
                border-radius: 20px;
                border: 1px solid #DCDCDC;
            }
            QPushButton#IconButton {
                background: transparent;
                border: none;
                color: #5F6368;
            }
            QPushButton#IconButton:hover {
                color: #202124;
            }
            QPushButton#MicButton {
                background-color: #FFFFFF;
                border-radius: 30px;
                border: 1px solid #DADCE0;
            }
            QPushButton#MicButton:hover {
                background-color: #F1F3F4;
            }
            QPushButton#MicButton[recording="true"] {
                background-color: #EA4335;
                border: none;
            }
            QMenu {
                background-color: #FFFFFF;
                border: 1px solid #DCDCDC;
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item {
                padding: 5px 20px 5px 20px;
            }
            QMenu::item:selected {
                background-color: #F1F3F4;
                color: #202124;
            }
        """)

    # --- NATIVE SYSTEM TRAY LOGIC ---
    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)

        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setBrush(QColor(41, 128, 185))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, 64, 64)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(16, 16, 32, 32)
        painter.end()

        self.tray_icon.setIcon(QIcon(pixmap))

        tray_menu = QMenu()
        show_action = tray_menu.addAction("Show / Hide Widget")
        show_action.triggered.connect(self.toggle_visibility)

        tray_menu.addSeparator()

        quit_action = tray_menu.addAction("Quit Application")
        quit_action.triggered.connect(QApplication.quit)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()

    # --- SETTINGS MENU LOGIC ---
    def setup_menus(self):
        self.settings_menu = QMenu(self)

        engine_menu = self.settings_menu.addMenu("Engine")
        engine_group = QActionGroup(self)

        act_gemini = QAction("Gemini API", self, checkable=True)
        act_openai = QAction("OpenAI Whisper API", self, checkable=True)
        act_local = QAction("Local Whisper", self, checkable=True)

        if ACTIVE_ENGINE == "gemini":
            act_gemini.setChecked(True)
        elif ACTIVE_ENGINE == "local":
            act_local.setChecked(True)
        else:
            act_openai.setChecked(True)

        engine_group.addAction(act_gemini)
        engine_group.addAction(act_openai)
        engine_group.addAction(act_local)
        engine_menu.addAction(act_gemini)
        engine_menu.addAction(act_openai)
        engine_menu.addAction(act_local)

        act_gemini.triggered.connect(lambda: self.update_setting("engine", "gemini"))
        act_openai.triggered.connect(lambda: self.update_setting("engine", "openai"))
        act_local.triggered.connect(lambda: self.update_setting("engine", "local"))

        # Local model choice (base, large-v3, etc.) when engine is Local Whisper
        local_model_menu = self.settings_menu.addMenu("Local model")
        local_model_group = QActionGroup(self)
        for name, key in [("Base (fast)", "base"), ("Small", "small"), ("Medium", "medium"),
                          ("Large v2", "large-v2"), ("Large v3", "large-v3")]:
            act = QAction(name, self, checkable=True)
            if ACTIVE_WHISPER_MODEL == key:
                act.setChecked(True)
            local_model_group.addAction(act)
            local_model_menu.addAction(act)
            act.triggered.connect(lambda checked, k=key: self.update_setting("local_model", k))

        lang_menu = self.settings_menu.addMenu("Language")
        lang_group = QActionGroup(self)

        act_auto = QAction("Auto-Detect", self, checkable=True)
        act_en = QAction("English", self, checkable=True)
        act_fr = QAction("French", self, checkable=True)

        if ACTIVE_LANGUAGE == "auto":
            act_auto.setChecked(True)
        elif ACTIVE_LANGUAGE == "en":
            act_en.setChecked(True)
        elif ACTIVE_LANGUAGE == "fr":
            act_fr.setChecked(True)

        lang_group.addAction(act_auto)
        lang_group.addAction(act_en)
        lang_group.addAction(act_fr)
        lang_menu.addAction(act_auto)
        lang_menu.addAction(act_en)
        lang_menu.addAction(act_fr)

        act_auto.triggered.connect(lambda: self.update_setting("lang", "auto"))
        act_en.triggered.connect(lambda: self.update_setting("lang", "en"))
        act_fr.triggered.connect(lambda: self.update_setting("lang", "fr"))

    def update_setting(self, setting_type, value):
        global ACTIVE_ENGINE, ACTIVE_LANGUAGE, ACTIVE_WHISPER_MODEL
        if setting_type == "engine":
            ACTIVE_ENGINE = value
            print(f"🔄 Engine set to: {ACTIVE_ENGINE.upper()}")
        elif setting_type == "lang":
            ACTIVE_LANGUAGE = value
            print(f"🌍 Language set to: {ACTIVE_LANGUAGE.upper()}")
        elif setting_type == "local_model":
            ACTIVE_WHISPER_MODEL = value
            print(f"📦 Local model set to: {ACTIVE_WHISPER_MODEL}")

    def show_settings_menu(self):
        self.settings_menu.exec(self.btn_settings.mapToGlobal(QPoint(0, self.btn_settings.height())))

    # --- DRAG MECHANICS ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            global_x = event.globalPosition().toPoint().x()
            global_y = event.globalPosition().toPoint().y()
            self.drag_offset_x = global_x - self.frameGeometry().x()
            self.drag_offset_y = global_y - self.frameGeometry().y()
            self.setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            new_x = event.globalPosition().toPoint().x() - self.drag_offset_x
            new_y = event.globalPosition().toPoint().y() - self.drag_offset_y
            self.move(new_x, new_y)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            event.accept()

    # --- EVENT FILTER: allows dragging even when clicking on buttons ---
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
            global_x = event.globalPosition().toPoint().x()
            global_y = event.globalPosition().toPoint().y()
            self.drag_offset_x = global_x - self.frameGeometry().x()
            self.drag_offset_y = global_y - self.frameGeometry().y()
            self.setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))
            return False  # Don't block — let buttons still receive their click
        elif event.type() == QEvent.Type.MouseMove and event.buttons() & Qt.MouseButton.LeftButton:
            new_x = event.globalPosition().toPoint().x() - self.drag_offset_x
            new_y = event.globalPosition().toPoint().y() - self.drag_offset_y
            self.move(new_x, new_y)
            return True  # Consume move to prevent button weirdness
        elif event.type() == QEvent.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton:
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            return False
        return super().eventFilter(obj, event)

    # --- RECORDING LOGIC ---
    def setup_hotkey(self):
        self.hotkey_signal = HotkeySignal()

        def on_f8():
            # Capture the window that has focus at F8 press; never use Run/Console/Debug
            try:
                hwnd = win32gui.GetForegroundWindow()
                if hwnd and not self._is_own_process_window(hwnd) and not self._is_console_like_window(hwnd):
                    self.hotkey_signal.toggle.emit(int(hwnd))
                else:
                    self.hotkey_signal.toggle.emit(0)
            except Exception:
                self.hotkey_signal.toggle.emit(0)

        self.hotkey_signal.toggle.connect(self._on_hotkey_triggered)
        keyboard.add_hotkey(HOTKEY, on_f8, suppress=True)

    def _on_hotkey_triggered(self, hwnd):
        """When F8 is pressed: set target only when starting and hwnd is not Run/Console (0 = keep current)."""
        if hwnd and not self.is_recording:
            self.target_hwnd = hwnd
        # If hwnd was 0 (e.g. console had focus), target_hwnd stays as last good window from polling
        self.toggle_recording()

    def audio_callback(self, indata, frames, time, status):
        self.audio_queue.put(indata.copy())

    def file_writer_thread(self):
        with sf.SoundFile(WAVE_OUTPUT_FILENAME, mode='w', samplerate=RATE, channels=CHANNELS, subtype='PCM_16') as file:
            while self.is_recording:
                try:
                    data = self.audio_queue.get(timeout=0.1)
                    file.write(data)
                except queue.Empty:
                    continue

    def toggle_recording(self):
        if not self.is_recording:
            # FREEZE: stop polling so the target window is locked in
            self._focus_timer.stop()

            self.is_recording = True
            self.btn_mic.setProperty("recording", True)
            self.btn_mic.style().unpolish(self.btn_mic)
            self.btn_mic.style().polish(self.btn_mic)
            self.btn_mic.setText("⏹️")

            print(f"🎯 Target window: {self._get_window_title(self.target_hwnd)}")

            while not self.audio_queue.empty():
                self.audio_queue.get()

            self.stream = sd.InputStream(samplerate=RATE, channels=CHANNELS, callback=self.audio_callback)
            self.stream.start()

            self.writer_thread = threading.Thread(target=self.file_writer_thread, daemon=True)
            self.writer_thread.start()
            print("🎙️ Recording started...")

        else:
            self.is_recording = False
            self.btn_mic.setProperty("recording", False)
            self.btn_mic.style().unpolish(self.btn_mic)
            self.btn_mic.style().polish(self.btn_mic)
            self.btn_mic.setText("⏳")
            self.btn_mic.setEnabled(False)

            if self.stream:
                self.stream.stop()
                self.stream.close()
            self.writer_thread.join()
            print("🛑 Recording stopped. Processing...")

            self.transcription_thread = TranscriptionWorker()
            self.transcription_thread.finished.connect(self.on_transcription_success)
            self.transcription_thread.error.connect(self.on_transcription_error)
            self.transcription_thread.start()

    @staticmethod
    def _get_window_title(hwnd):
        """Get window title for debug logging."""
        try:
            return win32gui.GetWindowText(hwnd) if hwnd else "(None)"
        except Exception:
            return "(Error)"

    def restore_target_window(self):
        """Bring the target window (where user had their cursor) back to the foreground."""
        if not self.target_hwnd:
            return False

        try:
            if not win32gui.IsWindow(self.target_hwnd):
                return False

            # Trick Windows into allowing SetForegroundWindow
            ctypes.windll.user32.keybd_event(win32con.VK_MENU, 0, 0, 0)
            win32gui.SetForegroundWindow(self.target_hwnd)
            ctypes.windll.user32.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
            # Give the window time to restore focus and caret position before we paste
            time.sleep(0.35)
            return True
        except Exception as e:
            print(f"⚠️ Could not restore window: {e}")
            return False

    def on_transcription_success(self, text):
        # Do NOT print the transcription — that made it look like text was "going to the console"
        pyperclip.copy(text)

        if not self.restore_target_window():
            print("⚠️ Could not restore target window. Text is in clipboard — paste manually with Ctrl+V.")
            self.reset_ui()
            return

        time.sleep(0.2)
        fg = win32gui.GetForegroundWindow()
        # If PyCharm/IDE stole focus (e.g. console got it), bring target back and retry once
        if fg != self.target_hwnd and win32gui.IsWindow(self.target_hwnd):
            ctypes.windll.user32.keybd_event(win32con.VK_MENU, 0, 0, 0)
            win32gui.SetForegroundWindow(self.target_hwnd)
            ctypes.windll.user32.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.4)
            fg = win32gui.GetForegroundWindow()

        if fg == self.target_hwnd:
            pyautogui.hotkey('ctrl', 'v')
            print(f"📋 Pasted into: {self._get_window_title(self.target_hwnd)}")
        else:
            print(f"⚠️ Target lost focus. Text is in clipboard — paste with Ctrl+V in your target app.")

        self.reset_ui()

    def on_transcription_error(self, error_msg):
        print(f"❌ Error: {error_msg}")
        self.reset_ui()

    def reset_ui(self):
        self.btn_mic.setText("🎙️")
        self.btn_mic.setEnabled(True)
        # Resume tracking for the next recording
        self._focus_timer.start(250)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    widget = DictationWidget()
    widget.show()
    sys.exit(app.exec())