from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import QSettings, QPoint

from taryam_speech_to_text.copyright import SETTINGS_APPLICATION, SETTINGS_ORGANIZATION
from taryam_speech_to_text.i18n import detect_system_locale

SETTINGS_VERSION = 2


@dataclass
class AppConfig:
    engine: str = "local"
    local_backend: str = "faster-whisper"
    local_model: str = "base"
    language: str = "auto"
    ui_language: str = "system"
    theme: str = "system"
    hotkey: str = "f8"
    mic_device: str = ""
    auto_paste: bool = True
    preserve_clipboard: bool = False
    max_record_seconds: int = 300
    widget_x: int = 200
    widget_y: int = 200
    output_dir: str = str(Path.home() / "Documents" / "WhisperBridgeOutput")


class SettingsStore:
    def __init__(self) -> None:
        self._qs = QSettings(SETTINGS_ORGANIZATION, SETTINGS_APPLICATION)

    def load(self) -> AppConfig:
        cfg = AppConfig()
        cfg.engine = self._qs.value("engine", cfg.engine)
        cfg.local_backend = self._qs.value("local_backend", cfg.local_backend)
        cfg.local_model = self._qs.value("local_model", cfg.local_model)
        cfg.language = self._qs.value("language", cfg.language)
        cfg.ui_language = self._qs.value("ui_language", cfg.ui_language)
        cfg.theme = self._qs.value("theme", cfg.theme)
        cfg.hotkey = self._qs.value("hotkey", cfg.hotkey)
        cfg.mic_device = self._qs.value("mic_device", cfg.mic_device)
        cfg.auto_paste = self._qs.value("auto_paste", cfg.auto_paste, bool)
        cfg.preserve_clipboard = self._qs.value("preserve_clipboard", cfg.preserve_clipboard, bool)
        cfg.max_record_seconds = int(self._qs.value("max_record_seconds", cfg.max_record_seconds))
        cfg.widget_x = int(self._qs.value("widget_x", cfg.widget_x))
        cfg.widget_y = int(self._qs.value("widget_y", cfg.widget_y))
        cfg.output_dir = self._qs.value("output_dir", cfg.output_dir)
        if cfg.ui_language == "system":
            cfg.ui_language = detect_system_locale()
        stored_ver = int(self._qs.value("settings_version", 0))
        # One-shot: legacy installs had preserve_clipboard default True and a buggy restore path.
        if stored_ver < 2:
            cfg.preserve_clipboard = False
            self._qs.setValue("preserve_clipboard", False)
        if stored_ver < SETTINGS_VERSION:
            self._qs.setValue("settings_version", SETTINGS_VERSION)
        return cfg

    def save(self, cfg: AppConfig) -> None:
        self._qs.setValue("engine", cfg.engine)
        self._qs.setValue("local_backend", cfg.local_backend)
        self._qs.setValue("local_model", cfg.local_model)
        self._qs.setValue("language", cfg.language)
        self._qs.setValue("ui_language", cfg.ui_language)
        self._qs.setValue("theme", cfg.theme)
        self._qs.setValue("hotkey", cfg.hotkey)
        self._qs.setValue("mic_device", cfg.mic_device)
        self._qs.setValue("auto_paste", cfg.auto_paste)
        self._qs.setValue("preserve_clipboard", cfg.preserve_clipboard)
        self._qs.setValue("max_record_seconds", cfg.max_record_seconds)
        self._qs.setValue("widget_x", cfg.widget_x)
        self._qs.setValue("widget_y", cfg.widget_y)
        self._qs.setValue("output_dir", cfg.output_dir)
        self._qs.setValue("settings_version", SETTINGS_VERSION)

    def save_widget_pos(self, pos: QPoint) -> None:
        self._qs.setValue("widget_x", pos.x())
        self._qs.setValue("widget_y", pos.y())
