from PySide6.QtGui import QGuiApplication

LIGHT_QSS = """
QWidget { color: #202124; }
QFrame#RootFrame {
    background: #f8f9fa;
    border: 1px solid #d2d5da;
    border-radius: 18px;
}
QPushButton#MicButton {
    background: #ffffff;
    border: 1px solid #c6c9ce;
    border-radius: 24px;
}
QPushButton#MicButton[recording="true"] {
    background: #e53935;
    color: #ffffff;
    border: none;
}
QProgressBar {
    border: 1px solid #c6c9ce;
    border-radius: 4px;
    background: #eef1f4;
}
QProgressBar::chunk { background: #1a73e8; border-radius: 3px; }
"""

DARK_QSS = """
QWidget { color: #e8eaed; }
QFrame#RootFrame {
    background: #1f2328;
    border: 1px solid #363a40;
    border-radius: 18px;
}
QPushButton#MicButton {
    background: #2b3138;
    border: 1px solid #454c56;
    border-radius: 24px;
}
QPushButton#MicButton[recording="true"] {
    background: #ef5350;
    color: #ffffff;
    border: none;
}
QProgressBar {
    border: 1px solid #454c56;
    border-radius: 4px;
    background: #20252b;
}
QProgressBar::chunk { background: #8ab4f8; border-radius: 3px; }
"""


def resolve_theme(config_theme: str) -> str:
    if config_theme in ("light", "dark"):
        return config_theme
    style_hints = QGuiApplication.styleHints()
    scheme = style_hints.colorScheme().name.lower()
    return "dark" if "dark" in scheme else "light"


def stylesheet_for_theme(config_theme: str) -> str:
    return DARK_QSS if resolve_theme(config_theme) == "dark" else LIGHT_QSS
