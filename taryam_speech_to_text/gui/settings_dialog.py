from __future__ import annotations

import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from taryam_speech_to_text.audio.devices import list_input_devices
from taryam_speech_to_text.i18n import EN_US, FR_FR, tr
from taryam_speech_to_text.settings import AppConfig


class SettingsDialog(QDialog):
    def __init__(self, cfg: AppConfig):
        super().__init__()
        self.setWindowTitle(tr("menu.settings"))
        self._cfg = cfg
        root = QVBoxLayout(self)
        form = QFormLayout()

        self.engine_combo = QComboBox()
        self.engine_combo.addItem(tr("engine.local"), "local")
        self.engine_combo.addItem(tr("engine.openai"), "openai")
        self.engine_combo.addItem(tr("engine.gemini"), "gemini")
        self.engine_combo.setCurrentIndex(max(0, self.engine_combo.findData(cfg.engine)))

        self.backend_combo = QComboBox()
        self.backend_combo.addItem(tr("backend.faster"), "faster-whisper")
        self.backend_combo.addItem(tr("backend.whisper"), "openai-whisper")
        self.backend_combo.setCurrentIndex(max(0, self.backend_combo.findData(cfg.local_backend)))

        self.model_combo = QComboBox()
        for val in ("base", "small", "medium", "large-v2", "large-v3"):
            self.model_combo.addItem(val, val)
        self.model_combo.setCurrentIndex(max(0, self.model_combo.findData(cfg.local_model)))

        self.lang_combo = QComboBox()
        self.lang_combo.addItem(tr("lang.auto"), "auto")
        self.lang_combo.addItem(tr("lang.en"), "en")
        self.lang_combo.addItem(tr("lang.fr"), "fr")
        self.lang_combo.setCurrentIndex(max(0, self.lang_combo.findData(cfg.language)))

        self.ui_lang_combo = QComboBox()
        self.ui_lang_combo.addItem("English", EN_US)
        self.ui_lang_combo.addItem("Francais", FR_FR)
        self.ui_lang_combo.setCurrentIndex(max(0, self.ui_lang_combo.findData(cfg.ui_language)))

        self.theme_combo = QComboBox()
        self.theme_combo.addItem(tr("theme.system"), "system")
        self.theme_combo.addItem(tr("theme.light"), "light")
        self.theme_combo.addItem(tr("theme.dark"), "dark")
        self.theme_combo.setCurrentIndex(max(0, self.theme_combo.findData(cfg.theme)))

        self.hotkey_edit = QLineEdit(cfg.hotkey)
        self.device_combo = QComboBox()
        self.device_combo.addItem("(default)", "")
        for name in list_input_devices():
            self.device_combo.addItem(name, name)
        self.device_combo.setCurrentIndex(max(0, self.device_combo.findData(cfg.mic_device)))

        self.auto_paste_check = QCheckBox()
        self.auto_paste_check.setChecked(cfg.auto_paste)
        self.preserve_check = QCheckBox()
        self.preserve_check.setChecked(cfg.preserve_clipboard)

        self.max_duration = QSpinBox()
        self.max_duration.setRange(0, 36000)
        self.max_duration.setValue(cfg.max_record_seconds)

        self.openai_key = QLineEdit(os.environ.get("OPENAI_API_KEY", ""))
        self.openai_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.gemini_key = QLineEdit(os.environ.get("GEMINI_API_KEY", ""))
        self.gemini_key.setEchoMode(QLineEdit.EchoMode.Password)

        self.download_btn = QPushButton(tr("settings.download_model"))

        form.addRow(QLabel(tr("settings.engine")), self.engine_combo)
        form.addRow(QLabel(tr("settings.local_backend")), self.backend_combo)
        form.addRow(QLabel(tr("settings.model")), self.model_combo)
        form.addRow(QLabel(""), self.download_btn)
        form.addRow(QLabel(tr("settings.language")), self.lang_combo)
        form.addRow(QLabel(tr("settings.ui_language")), self.ui_lang_combo)
        form.addRow(QLabel(tr("settings.theme")), self.theme_combo)
        form.addRow(QLabel(tr("settings.hotkey")), self.hotkey_edit)
        form.addRow(QLabel(tr("settings.device")), self.device_combo)
        form.addRow(QLabel(tr("settings.auto_paste")), self.auto_paste_check)
        form.addRow(QLabel(tr("settings.preserve_clipboard")), self.preserve_check)
        form.addRow(QLabel(tr("settings.max_duration")), self.max_duration)
        form.addRow(QLabel("OPENAI_API_KEY"), self.openai_key)
        form.addRow(QLabel("GEMINI_API_KEY"), self.gemini_key)
        root.addLayout(form)

        row = QHBoxLayout()
        self.open_output_btn = QPushButton(tr("settings.open_output"))
        self.reset_btn = QPushButton(tr("settings.reset"))
        self.save_btn = QPushButton(tr("settings.save"))
        self.cancel_btn = QPushButton(tr("settings.cancel"))
        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self.accept)
        row.addWidget(self.open_output_btn)
        row.addWidget(self.reset_btn)
        row.addStretch(1)
        row.addWidget(self.save_btn)
        row.addWidget(self.cancel_btn)
        root.addLayout(row)

        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self._apply_tooltips()

    def _apply_tooltips(self) -> None:
        self.engine_combo.setToolTip(tr("tooltip.settings.engine"))
        self.backend_combo.setToolTip(tr("tooltip.settings.backend"))
        self.model_combo.setToolTip(tr("tooltip.settings.model"))
        self.download_btn.setToolTip(tr("tooltip.settings.download"))
        self.lang_combo.setToolTip(tr("tooltip.settings.lang"))
        self.ui_lang_combo.setToolTip(tr("tooltip.settings.ui_lang"))
        self.theme_combo.setToolTip(tr("tooltip.settings.theme"))
        self.hotkey_edit.setToolTip(tr("tooltip.settings.hotkey"))
        self.device_combo.setToolTip(tr("tooltip.settings.device"))
        self.auto_paste_check.setToolTip(tr("tooltip.settings.auto_paste"))
        self.preserve_check.setToolTip(tr("tooltip.settings.preserve_clipboard"))
        self.max_duration.setToolTip(tr("tooltip.settings.max_duration"))
        self.openai_key.setToolTip(tr("tooltip.settings.openai_key"))
        self.gemini_key.setToolTip(tr("tooltip.settings.gemini_key"))
        self.open_output_btn.setToolTip(tr("tooltip.settings.open_output"))
        self.reset_btn.setToolTip(tr("tooltip.settings.reset"))
        self.save_btn.setToolTip(tr("tooltip.settings.save"))
        self.cancel_btn.setToolTip(tr("tooltip.settings.cancel"))

    def apply_to_config(self, cfg: AppConfig) -> None:
        cfg.engine = self.engine_combo.currentData()
        cfg.local_backend = self.backend_combo.currentData()
        cfg.local_model = self.model_combo.currentData()
        cfg.language = self.lang_combo.currentData()
        cfg.ui_language = self.ui_lang_combo.currentData()
        cfg.theme = self.theme_combo.currentData()
        cfg.hotkey = self.hotkey_edit.text().strip().lower() or "f8"
        cfg.mic_device = self.device_combo.currentData()
        cfg.auto_paste = self.auto_paste_check.isChecked()
        cfg.preserve_clipboard = self.preserve_check.isChecked()
        cfg.max_record_seconds = int(self.max_duration.value())
