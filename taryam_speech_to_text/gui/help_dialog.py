from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QHBoxLayout, QPushButton, QTextBrowser, QVBoxLayout

from taryam_speech_to_text.help_paths import help_markdown_path
from taryam_speech_to_text.i18n import tr


class HelpDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(tr("help.title"))
        self.setMinimumSize(520, 560)
        layout = QVBoxLayout(self)
        browser = QTextBrowser(self)
        browser.setOpenExternalLinks(True)
        path = help_markdown_path()
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            text = tr("help.missing_file")
        browser.setMarkdown(text)
        layout.addWidget(browser)

        row = QHBoxLayout()
        row.addStretch(1)
        close_btn = QPushButton(tr("help.close"))
        close_btn.setToolTip(tr("tooltip.help.close"))
        close_btn.clicked.connect(self.accept)
        row.addWidget(close_btn)
        layout.addLayout(row)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
