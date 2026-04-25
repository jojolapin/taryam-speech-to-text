from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from taryam_speech_to_text import __version__
from taryam_speech_to_text.copyright import copyright_notice
from taryam_speech_to_text.gui.help_dialog import HelpDialog
from taryam_speech_to_text.i18n import tr


class AboutDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(tr("menu.about"))
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"{tr('about.version')} {__version__}"))
        layout.addWidget(QLabel(tr("about.text")))
        copy_lbl = QLabel(f"{tr('about.copyright')}: {copyright_notice()}")
        copy_lbl.setWordWrap(True)
        layout.addWidget(copy_lbl)

        row = QHBoxLayout()
        help_btn = QPushButton(tr("about.open_help"))
        help_btn.setToolTip(tr("tooltip.about.open_help"))
        help_btn.clicked.connect(self._open_help)
        ok_btn = QPushButton(tr("about.ok"))
        ok_btn.setToolTip(tr("tooltip.about.ok"))
        ok_btn.clicked.connect(self.accept)
        row.addWidget(help_btn)
        row.addStretch(1)
        row.addWidget(ok_btn)
        layout.addLayout(row)

    def _open_help(self) -> None:
        HelpDialog().exec()
