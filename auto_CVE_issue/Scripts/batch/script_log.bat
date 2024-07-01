@echo off
setlocal enabledelayedexpansion

:: Define paths
set "feedbackFile=%~dp0..\..\Text_Files\feedback.txt"
set "shareLocation="
set "scriptDir=%~dp0"
set "logFile=%~dp0..\..\script.log"
set "logDir=%~dp0..\..\Log_Files"

:: Check if CVE_address.txt exists
if not exist "%~dp0..\..\Text_Files\CVE_address.txt" (
    echo CVE_address.txt not found. Exiting.
    exit /b 1
)

:: Read CVE_address.txt and set shareLocation variable
for /f "delims=" %%a in (%~dp0..\..\Text_Files\CVE_address.txt) do (
    set "shareLocation=%%a"
)

:: Display feedback file and share location
echo Feedback File: %feedbackFile%
echo Share Location: %shareLocation%

:: Extract date parts from current date
for /f "tokens=1-3 delims=/ " %%a in ('echo %date%') do (
    set year=%%a
    set month=%%b
    set day=%%c
)

:: Extract time parts from current time
for /f "tokens=1-3 delims=:." %%a in ('echo %time%') do (
    set hour=%%a
    set minute=%%b
    set second=%%c
)

:: Display current time and generate timestamp
echo Current time: %hour%:%minute%:%second%
set "timestamp=%year%%month%%day%_%hour%%minute%%second%"
echo Current timestamp: %timestamp%

:: Create log directory if it does not exist
if not exist "%logDir%" mkdir "%logDir%"

:: Check if log file exists
if exist "%logFile%" (
    echo Log file %logFile% exists.
) else (
    echo Log file %logFile% does not exist.
)

:: Generate new log file name
set "newLogFile=%logDir%\%timestamp%_script.log"
echo New log file name: %newLogFile%

:: Copy script.log to new log file with timestamp and delete the original if it exists
if exist "%logFile%" (
    echo Copying %logFile% to %newLogFile%
    copy "%logFile%" "%newLogFile%"
    if %errorlevel% equ 0 (
        del "%logFile%"
        echo "script.log has been copied to %newLogFile% and the original has been deleted."
    ) else (
        echo "Failed to copy %logFile% to %newLogFile%"
    )
) else (
    echo "Log file %logFile% does not exist. No file was deleted."
)

:: Copy script.log from shareLocation to current directory
echo Copying script.log from %shareLocation% to %~dp0..\..
if exist "%shareLocation%\script.log" (
    copy "%shareLocation%\script.log" "%~dp0..\..\" 
    if %errorlevel% equ 0 (
        echo "Successfully copied script.log from %shareLocation% to %~dp0..\.."
    ) else (
        echo "Failed to copy script.log from %shareLocation% to %~dp0..\.."
    )
) else (
    echo "Log file %shareLocation%\script.log does not exist."
)

endlocal
