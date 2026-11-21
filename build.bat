@echo off
rem Build CompScannedPDF.exe (run on Windows with Python installed)
setlocal
cd /d "%~dp0"

python --version >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Python was not found. Install Python and check "Add Python to PATH".
  pause
  exit /b 1
)

if not exist ".venv-build" python -m venv .venv-build
call ".venv-build\Scripts\activate.bat"

python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller
if errorlevel 1 (
  echo [ERROR] Package installation failed.
  pause
  exit /b 1
)

python -m PyInstaller --noconfirm --clean --onefile --windowed --name CompScannedPDF CompScannedPDF.py
if errorlevel 1 (
  echo [ERROR] Build failed.
  pause
  exit /b 1
)

echo.
echo Build complete: %~dp0dist\CompScannedPDF.exe
pause
