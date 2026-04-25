@echo off
setlocal EnableExtensions
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo ERROR: No .venv found. Run projectsetup.bat once on this machine first.
  exit /b 1
)

call "%~dp0.venv\Scripts\activate.bat"
if errorlevel 1 (
  echo ERROR: Could not activate .venv
  exit /b 1
)

python "%~dp0build.py" %*
exit /b %ERRORLEVEL%
