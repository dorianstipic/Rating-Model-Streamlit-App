@echo off

REM Get path of requirements.txt from .bat file path
set ENV_FILE=%~dp0requirements.txt

REM Create the environment from the .txt file in the 'Environment' subfolder
call conda create --name streamlit_dashboard_demo python=3.12.5 --file "%ENV_FILE%"

REM Check the exit code of the previous command
IF %ERRORLEVEL% EQU 0 (
    echo Environment 'streamlit_dashboard_demo' has been installed successfully.
) ELSE (
    echo Error: Failed to install the environment 'streamlit_dashboard_demo'.
)

REM Pause to keep the console window open
pause