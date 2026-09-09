@echo off
setlocal
if "%~1"=="" (
  echo Usage: AUDIT_BCKR_DOWNLOAD_TSV_V066.bat ^<EXTRACTED_PACKAGE_DIR^> [SERVER_FILES_DIR]
  exit /b 2
)
set SCRIPT=%~dp0audit_bckr_download_tsv_v066.py
if "%~2"=="" (
  py "%SCRIPT%" "%~1" --out V066_BCKR_SERVER_TSV_AUDIT.json
) else (
  py "%SCRIPT%" "%~1" --server-root "%~2" --out V066_BCKR_SERVER_TSV_AUDIT.json
)
endlocal
