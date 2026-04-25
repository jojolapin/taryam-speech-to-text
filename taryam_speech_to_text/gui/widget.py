from __future__ import annotations

import os
import time
from datetime import datetime

import win32gui
import win32process
from dotenv import set_key
from PySide6.QtCore import QPoint, QThread, QTimer, Qt, Signal
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

from taryam_speech_to_text.audio.capture import AudioCapture, CaptureConfig
from taryam_speech_to_text.copyright import PRODUCT_NAME, copyright_short
from taryam_speech_to_text.gui.about_dialog import AboutDialog
from taryam_speech_to_text.gui.help_dialog import HelpDialog
from taryam_speech_to_text.gui.settings_dialog import SettingsDialog
from taryam_speech_to_text.gui.tray import TrayController
from taryam_speech_to_text.hotkey import GlobalHotkey
from taryam_speech_to_text.i18n import tr
from taryam_speech_to_text.paste.win import PasteController, get_focused_control_hwnd
from taryam_speech_to_text.settings import AppConfig, SettingsStore
from taryam_speech_to_text.theme import stylesheet_for_theme
from taryam_speech_to_text.transcription.registry import get_engine


class WorkerThread(QThread):
    done = Signal(str)
    failed = Signal(str)

    def __init__(self, cfg: AppConfig, wav_path: str):
        super().__init__()
        self.cfg = cfg
        self.wav_path = wav_path

    def run(self):
        try:
            engine = get_engine(self.cfg)
            text = engine.transcribe(self.wav_path, self.cfg.language)
            self.done.emit(text)
        except Exception as exc:
            self.failed.emit(str(exc))


class DictationWidget(QWidget):
    def __init__(self, cfg: AppConfig, store: SettingsStore):
        super().__init__()
        self.cfg = cfg
        self.store = store
        self.target_hwnd = None
        self.target_focused_hwnd = None
        self._paste_target_hwnd = None
        self._paste_focused_hwnd = None
        self._my_pid = os.getpid()
        self._drag = QPoint(0, 0)
        self._worker = None
        self._pulse = 0
        self._dot = ""

        self.capture = AudioCapture(
            CaptureConfig(rate=16000, channels=1, max_record_seconds=cfg.max_record_seconds, mic_device=cfg.mic_device)
        )
        self.capture.level_changed.connect(self._on_level_changed)
        self.capture.error.connect(self._on_capture_error)
        self.paste = PasteController()
        self.paste.done.connect(self._on_paste_done)
        self.hotkey = GlobalHotkey()
        self.hotkey.pressed.connect(self.toggle_recording)
        self.hotkey.error.connect(lambda _: self._set_status(f"{tr('status.error')}: {tr('error.hotkey')}"))
        self.hotkey.set_hotkey(cfg.hotkey)

        self._status_timer = QTimer(self)
        self._status_timer.timeout.connect(self._tick_status)
        self._focus_timer = QTimer(self)
        self._focus_timer.timeout.connect(self._track_foreground_window)
        self._focus_timer.start(250)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setFixedSize(280, 120)
        self.setWindowTitle(f"{PRODUCT_NAME} — {copyright_short()}")
        self._build_ui()
        self._apply_widget_tooltips()
        self.move(cfg.widget_x, cfg.widget_y)
        self._apply_theme()
        self.tray = TrayController(self)
        self._wire_tray()
        self._set_status(tr("status.ready"))

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(8, 8, 8, 8)

        self.root = QFrame()
        self.root.setObjectName("RootFrame")
        root_layout = QVBoxLayout(self.root)
        root_layout.setContentsMargins(12, 10, 12, 10)
        top = QHBoxLayout()

        self.settings_btn = QPushButton("⚙")
        self.settings_btn.clicked.connect(self.open_settings)
        self.mic_btn = QPushButton("🎙")
        self.mic_btn.setObjectName("MicButton")
        self.mic_btn.setFixedSize(48, 48)
        self.mic_btn.clicked.connect(self.toggle_recording)
        self.about_btn = QPushButton("i")
        self.about_btn.clicked.connect(self.show_about)
        top.addWidget(self.settings_btn)
        top.addStretch(1)
        top.addWidget(self.mic_btn)
        top.addStretch(1)
        top.addWidget(self.about_btn)

        self.status = QLabel("")
        self.level = QProgressBar()
        self.level.setRange(0, 100)
        self.level.setValue(0)
        self.level.setTextVisible(False)
        root_layout.addLayout(top)
        root_layout.addWidget(self.status)
        root_layout.addWidget(self.level)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(26)
        shadow.setOffset(0, 5)
        self.root.setGraphicsEffect(shadow)
        outer.addWidget(self.root)
        self._refresh_mic_tooltip()

    def _apply_widget_tooltips(self) -> None:
        self.settings_btn.setToolTip(tr("tooltip.widget.settings"))
        self.about_btn.setToolTip(tr("tooltip.widget.about"))
        self.status.setToolTip(tr("tooltip.widget.status"))
        self.level.setToolTip(tr("tooltip.widget.level"))
        self.root.setToolTip(tr("tooltip.widget.surface"))

    def _refresh_mic_tooltip(self) -> None:
        if not self.mic_btn.isEnabled() or self.mic_btn.text() == "⏳":
            self.mic_btn.setToolTip(tr("tooltip.widget.mic_busy"))
        elif self.mic_btn.text() == "⏹":
            self.mic_btn.setToolTip(tr("tooltip.widget.mic_recording"))
        else:
            self.mic_btn.setToolTip(tr("tooltip.widget.mic_ready"))

    def _wire_tray(self):
        self.tray.start_stop.triggered.connect(self.toggle_recording)
        self.tray.show_hide.triggered.connect(self.toggle_visibility)
        self.tray.settings.triggered.connect(self.open_settings)
        self.tray.help.triggered.connect(self.show_user_guide)
        self.tray.about.triggered.connect(self.show_about)
        self.tray.quit_action.triggered.connect(QApplication.quit)

    def _apply_theme(self):
        self.setStyleSheet(stylesheet_for_theme(self.cfg.theme))

    def _set_status(self, value: str):
        self.status.setText(value)

    def _track_foreground_window(self):
        try:
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            if hwnd and pid != self._my_pid:
                self.target_hwnd = hwnd
                self.target_focused_hwnd = get_focused_control_hwnd(hwnd)
            else:
                self.target_focused_hwnd = None
        except Exception:
            pass

    def _tick_status(self):
        if self.capture.recording:
            elapsed = self.capture.elapsed_seconds()
            mm = elapsed // 60
            ss = elapsed % 60
            self._set_status(f"{tr('status.recording')} {mm:02d}:{ss:02d}")
            if self.cfg.max_record_seconds > 0 and elapsed >= self.cfg.max_record_seconds:
                self.toggle_recording()
        else:
            self._dot = "." if self._dot == "..." else self._dot + "."
            self._set_status(tr("status.transcribing") + self._dot)

    def _on_level_changed(self, level: int):
        self.level.setValue(level)

    def _on_capture_error(self, message: str):
        self._set_status(f"{tr('status.error')}: {message or tr('error.no_mic')}")
        self.mic_btn.setEnabled(True)
        self.mic_btn.setText("🎙")
        self._refresh_mic_tooltip()

    def toggle_recording(self):
        if not self.capture.recording:
            snap_target = self.target_hwnd
            snap_focused = self.target_focused_hwnd
            self._focus_timer.stop()
            self._paste_target_hwnd = snap_target
            self._paste_focused_hwnd = snap_focused
            self.capture.start()
            if not self.capture.recording:
                return
            self.mic_btn.setProperty("recording", True)
            self.mic_btn.style().unpolish(self.mic_btn)
            self.mic_btn.style().polish(self.mic_btn)
            self.mic_btn.setText("⏹")
            self._refresh_mic_tooltip()
            self._status_timer.start(250)
        else:
            self.capture.stop()
            self.mic_btn.setProperty("recording", False)
            self.mic_btn.style().unpolish(self.mic_btn)
            self.mic_btn.style().polish(self.mic_btn)
            self.mic_btn.setEnabled(False)
            self.mic_btn.setText("⏳")
            self._refresh_mic_tooltip()
            self._status_timer.start(300)
            self._worker = WorkerThread(self.cfg, self.capture.output_file)
            self._worker.done.connect(self._on_transcription_done)
            self._worker.failed.connect(self._on_transcription_failed)
            self._worker.start()

    def _on_transcription_done(self, text: str):
        os.makedirs(self.cfg.output_dir, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_file = os.path.join(self.cfg.output_dir, f"transcript_{stamp}.txt")
        try:
            with open(out_file, "w", encoding="utf-8") as fh:
                fh.write(text)
        except Exception:
            pass
        self.paste.copy_and_paste(
            text,
            self._paste_target_hwnd,
            self._paste_focused_hwnd,
            self.cfg.auto_paste,
            self.cfg.preserve_clipboard,
        )

    def _on_transcription_failed(self, message: str):
        self._status_timer.stop()
        self._focus_timer.start(250)
        self.mic_btn.setEnabled(True)
        self.mic_btn.setText("🎙")
        self._refresh_mic_tooltip()
        self._set_status(f"{tr('status.error')}: {message}")

    def _on_paste_done(self, ok: bool, reason: str):
        self._status_timer.stop()
        self._focus_timer.start(250)
        self.mic_btn.setEnabled(True)
        self.mic_btn.setText("🎙")
        self._refresh_mic_tooltip()
        if ok and reason == "pasted":
            self._set_status(tr("status.pasted"))
        elif ok and reason == "clipboard":
            self._set_status(tr("status.clipboard_only"))
        elif not ok and reason == "focus_failed_clipboard":
            self._set_status(tr("status.focus_failed_clipboard"))
        else:
            self._set_status(f"{tr('status.error')}: {reason}")

    def open_settings(self):
        dlg = SettingsDialog(self.cfg)
        dlg.download_btn.clicked.connect(self._download_selected_model)
        dlg.open_output_btn.clicked.connect(self._open_output_folder)
        dlg.reset_btn.clicked.connect(self._reset_defaults)
        if dlg.exec():
            dlg.apply_to_config(self.cfg)
            env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
            env_path = os.path.abspath(env_path)
            set_key(env_path, "OPENAI_API_KEY", dlg.openai_key.text().strip())
            set_key(env_path, "GEMINI_API_KEY", dlg.gemini_key.text().strip())
            self.store.save(self.cfg)
            self.hotkey.set_hotkey(self.cfg.hotkey)
            self.capture.cfg.mic_device = self.cfg.mic_device
            self._apply_theme()

    def _download_selected_model(self):
        try:
            model_name = self.cfg.local_model
            if self.cfg.local_backend == "openai-whisper":
                import whisper

                whisper.load_model(model_name)
            else:
                from faster_whisper import WhisperModel

                WhisperModel(model_name, device="cpu", compute_type="int8")
            self._set_status(f"{model_name} ready")
        except Exception as exc:
            self._set_status(f"{tr('status.error')}: {exc}")

    def _open_output_folder(self):
        os.makedirs(self.cfg.output_dir, exist_ok=True)
        os.startfile(self.cfg.output_dir)

    def _reset_defaults(self):
        self.cfg = AppConfig()
        self.store.save(self.cfg)
        self._apply_theme()

    def show_about(self):
        AboutDialog().exec()

    def show_user_guide(self) -> None:
        HelpDialog().exec()

    def toggle_visibility(self):
        self.hide() if self.isVisible() else self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            pos = event.globalPosition().toPoint() - self._drag
            screen = QApplication.primaryScreen().availableGeometry()
            snap_margin = 12
            if abs(pos.x() - screen.left()) < snap_margin:
                pos.setX(screen.left())
            right = screen.right() - self.width()
            if abs(pos.x() - right) < snap_margin:
                pos.setX(right)
            self.move(pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.cfg.widget_x = self.x()
        self.cfg.widget_y = self.y()
        self.store.save_widget_pos(self.pos())
        event.accept()
