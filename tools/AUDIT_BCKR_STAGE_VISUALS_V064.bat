@echo off
setlocal
if "%~1"=="" (
  echo Usage: AUDIT_BCKR_STAGE_VISUALS_V064.bat ^<extracted_asset_folder^>
  exit /b 2
)
py "%~dp0audit_bckr_stage_visual_assets_v064.py" "%~1" --out "%~dp0..\V064_LOCAL_STAGE_BINARY_SCAN.json"
endlocal
