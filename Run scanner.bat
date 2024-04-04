@echo off
set venv=venv

if exist %venv%\ (
  echo venv %venv% exists
  echo opening %venv% virtual environment..
  call %CD%\%venv%\Scripts\activate.bat
) else (
  echo creating %venv% virtual environment..
  python -m venv %venv%
  echo opening %venv% virtual environment..
  call %CD%\%venv%\Scripts\activate.bat
  echo done. upgrading pip..
  python -m pip install --upgrade pip
  echo done. installing dependencies..
  python -m pip install -r requirements.txt
)
 
echo starting the spider..
python main.py

@pause