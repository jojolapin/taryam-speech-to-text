from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication

from taryam_speech_to_text import __version__
from taryam_speech_to_text.copyright import PRODUCT_NAME, SETTINGS_ORGANIZATION, copyright_notice
from taryam_speech_to_text.gui.widget import DictationWidget
from taryam_speech_to_text.i18n import detect_system_locale, set_locale
from taryam_speech_to_text.settings import SettingsStore


def main() -> int:
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
    load_dotenv(env_path)
    app = QApplication(sys.argv)
    app.setApplicationName(PRODUCT_NAME)
    app.setApplicationVersion(__version__)
    app.setOrganizationName(SETTINGS_ORGANIZATION)
    if hasattr(app, "setApplicationDisplayName"):
        app.setApplicationDisplayName(PRODUCT_NAME)
    app.setProperty("copyrightNotice", copyright_notice())
    app.setQuitOnLastWindowClosed(False)
    store = SettingsStore()
    cfg = store.load()
    set_locale(cfg.ui_language or detect_system_locale())
    widget = DictationWidget(cfg, store)
    widget.show()
    return app.exec()
