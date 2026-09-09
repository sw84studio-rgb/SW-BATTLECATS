@echo off
setlocal
cd /d "%~dp0"
if "%~1"=="" (
  echo Usage: EXTRACT_BCKR_INSTALLPACK_V065.bat ^<XAPK/APKM/APKS/ZIP/APK-or-folder^> [output-folder]
  echo.
  echo This tool does NOT download, decrypt, or auto-promote game assets.
  echo assets/ extraction is permitted only after exact KR 15.5.0 InstallPack MD5 verification.
  exit /b 2
)
set "INPUT=%~1"
if "%~2"=="" (
  set "OUT=%~dp0..\V065_INSTALLPACK_AUDIT_OUTPUT"
) else (
  set "OUT=%~2"
)
py -3 "%~dp0extract_bckr_installpack_v065.py" "%INPUT%" --output-dir "%OUT%" --extract-assets
if errorlevel 1 python "%~dp0extract_bckr_installpack_v065.py" "%INPUT%" --output-dir "%OUT%" --extract-assets
endlocal
