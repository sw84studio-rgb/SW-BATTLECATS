@echo off
setlocal
if "%~2"=="" (
  echo Usage: AUDIT_ENEMY_CASTLE_ROW_INDEX_V067.bat ^<KR_RAW_ROOT^> ^<enemyBaseRegistry.jgz^>
  exit /b 2
)
py "%~dp0audit_enemy_castle_row_index_v067.py" "%~1" "%~2" --out V067_ENEMY_BASE_ROW_INDEX_AUDIT.json
endlocal
