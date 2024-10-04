@echo off

REM Activate conda environment
call activate streamlit_dashboard_demo

REM Run the Python script
streamlit run .\Data_Upload_and_Information.py

REM Check the exit code 
IF %ERRORLEVEL% EQU 0 (
    echo Check the default browser.
) ELSE (
    echo Error: Error running the file.
)

REM Dectivate conda environment
call deactivate

REM Pause to keep the console window open
REM pause