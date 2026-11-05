@echo off
cd /d "%~dp0"
if exist .venv\Scripts\python.exe (
  .venv\Scripts\python.exe -m pytest tests -q
) else (
  python -m pytest tests -q
)
pause
