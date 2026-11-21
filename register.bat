@echo off
rem Add "Compress with CompScannedPDF" to the PDF right-click menu (current user only, no admin needed)
setlocal
set "EXE=%~dp0CompScannedPDF.exe"

if not exist "%EXE%" (
  echo [ERROR] CompScannedPDF.exe was not found in this folder:
  echo   %~dp0
  echo Put register.bat in the same folder as CompScannedPDF.exe and run it again.
  pause
  exit /b 1
)

set "KEY=HKCU\Software\Classes\SystemFileAssociations\.pdf\shell\CompScannedPDF"
reg add "%KEY%" /ve /d "Compress with CompScannedPDF" /f >nul
reg add "%KEY%" /v "Icon" /d "\"%EXE%\"" /f >nul
reg add "%KEY%\command" /ve /d "\"%EXE%\" \"%%1\"" /f >nul
if errorlevel 1 (
  echo [ERROR] Registration failed.
  pause
  exit /b 1
)

echo Registered: Compress with CompScannedPDF
echo   %EXE%
echo.
echo Windows 11: right-click a PDF, then choose "Show more options".
echo If you move CompScannedPDF.exe later, run register.bat again.
pause
