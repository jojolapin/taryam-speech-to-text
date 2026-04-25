from __future__ import annotations

from PySide6.QtGui import QAction, QIcon, QPainter, QColor, QPixmap
from PySide6.QtWidgets import QMenu, QSystemTrayIcon

from taryam_speech_to_text.copyright import PRODUCT_NAME, copyright_short
from taryam_speech_to_text.i18n import tr


def _make_icon() -> QIcon:
    pixmap = QPixmap(64, 64)
    pixmap.fill(QColor(0, 0, 0, 0))
    p = QPainter(pixmap)
    p.setBrush(QColor(41, 128, 185))
    p.setPen(QColor(41, 128, 185))
    p.drawEllipse(0, 0, 64, 64)
    p.setBrush(QColor(255, 255, 255))
    p.drawEllipse(18, 14, 28, 36)
    p.end()
    return QIcon(pixmap)


class TrayController:
    def __init__(self, parent):
        self.parent = parent
        self.tray = QSystemTrayIcon(parent)
        self.tray.setIcon(_make_icon())
        self.tray.setToolTip(f"{PRODUCT_NAME}\n{copyright_short()}")

        self.menu = QMenu()
        self.start_stop = QAction(tr("menu.start_stop"), parent)
        self.start_stop.setToolTip(tr("tooltip.menu.start_stop"))
        self.show_hide = QAction(tr("menu.show_hide"), parent)
        self.show_hide.setToolTip(tr("tooltip.menu.show_hide"))
        self.settings = QAction(tr("menu.settings"), parent)
        self.settings.setToolTip(tr("tooltip.menu.settings"))
        self.help = QAction(tr("menu.help"), parent)
        self.help.setToolTip(tr("tooltip.menu.help"))
        self.about = QAction(tr("menu.about"), parent)
        self.about.setToolTip(tr("tooltip.menu.about"))
        self.quit_action = QAction(tr("menu.quit"), parent)
        self.quit_action.setToolTip(tr("tooltip.menu.quit"))

        self.menu.addAction(self.start_stop)
        self.menu.addAction(self.show_hide)
        self.menu.addSeparator()
        self.menu.addAction(self.settings)
        self.menu.addAction(self.help)
        self.menu.addAction(self.about)
        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)
        self.tray.setContextMenu(self.menu)
        self.tray.show()
