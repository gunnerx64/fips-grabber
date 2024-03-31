@echo off
set venv=venv

if exist %venv%\ (
  echo venv %venv% exists
  echo opening %venv% virtual environment...
  call %CD%\%venv%\Scripts\activate.bat
) else (
  echo creating %venv% virtual environment...
  python -m venv %venv%
  echo opening %venv% virtual environment...
  call %CD%\%venv%\Scripts\activate.bat
  echo done. installing dependencies...
  python -m pip install -r requirements.txt
)

echo running the bot...
python main.py

@pause