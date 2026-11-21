@echo off
rem Remove "Compress with CompScannedPDF" from the PDF right-click menu
reg delete "HKCU\Software\Classes\SystemFileAssociations\.pdf\shell\CompScannedPDF" /f >nul 2>&1
reg delete "HKLM\Software\Classes\SystemFileAssociations\.pdf\shell\CompScannedPDF" /f >nul 2>&1
echo Right-click menu entry removed.
echo (An entry registered by the old .reg file may need "Run as administrator" to remove.)
pause
