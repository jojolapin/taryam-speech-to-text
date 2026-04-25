@echo off
setlocal EnableExtensions
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo ERROR: Python is not on PATH. Install Python 3.11+ from python.org and enable "Add to PATH", then reopen this window.
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo Creating virtual environment in .venv ...
  python -m venv .venv
  if errorlevel 1 (
    echo ERROR: Failed to create .venv
    exit /b 1
  )
) else (
  echo Virtual environment .venv already exists; updating packages.
)

call "%~dp0.venv\Scripts\activate.bat"
if errorlevel 1 (
  echo ERROR: Could not activate .venv
  exit /b 1
)

python -m pip install --upgrade pip
if errorlevel 1 exit /b 1

echo Installing requirements.txt ...
pip install -r "%~dp0requirements.txt"
if errorlevel 1 exit /b 1

echo Installing requirements-build.txt ...
pip install -r "%~dp0requirements-build.txt"
if errorlevel 1 exit /b 1

echo.
echo Done. You can run: run.bat   or build: build.bat
exit /b 0
