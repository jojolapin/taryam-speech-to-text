# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None
icon_path = "app.ico" if os.path.isfile("app.ico") else None
spec_root = os.path.dirname(os.path.abspath(SPEC))
_help_src = os.path.join(spec_root, "taryam_speech_to_text", "docs", "HELP.md")
datas = []
if os.path.isfile(_help_src):
    datas.append((_help_src, "taryam_speech_to_text/docs"))

a = Analysis(
    ["run.py"],
    pathex=[os.curdir],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtWidgets",
        "numpy",
        "sounddevice",
        "soundfile",
        "pyperclip",
        "pyautogui",
        "keyboard",
        "win32gui",
        "win32con",
        "win32process",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="WhisperBridge",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)
