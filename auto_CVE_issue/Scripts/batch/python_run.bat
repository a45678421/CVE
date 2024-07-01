@echo off
setlocal

rem Define variables
set "feedbackFile=%~dp0..\..\Text_Files\feedback.txt"
set "shareLocation="
set "scriptDir=%~dp0"
set "shellFolder=%~dp0..\shell"

rem Check if CVE_address.txt exists
if not exist "%~dp0..\..\Text_Files\CVE_address.txt" (
    echo CVE_address.txt not found. Exiting.
    exit /b 1
)

rem Read CVE_address.txt and set shareLocation variable
for /f "delims=" %%a in (%~dp0..\..\Text_Files\CVE_address.txt) do (
    set "shareLocation=%%a"
)

echo Feedback File: %feedbackFile%
echo Share Location: %shareLocation%

rem Check scan mode and execute corresponding actions
:check_mode
for /f "tokens=1,2 delims== " %%a in (%feedbackFile%) do (
    if /i "%%a"=="Scan" if /i "%%b"=="mode" (
        set /p "mode=" < "%feedbackFile%"
        if "%mode%"=="1" (
            echo "Scan mode is 1. Checking directory..."
            goto check_share_location
        ) else if "%mode%"=="2" (
            echo "Scan mode is 2. Checking directory..."
            goto check_share_location
        ) else if "%mode%"=="3" (
            echo "Scan mode is 3. Skipping operations."
            exit /b 0
        ) else (
            echo "Invalid mode in feedback.txt. Exiting."
            exit /b 1
        )
    )
)

rem Check shareLocation directory in a loop until found
:check_share_location
echo Checking directory: %shareLocation%
if exist "%shareLocation%" (
    echo "Directory '%shareLocation%' found. Executing operations..."
    rem Delete all .txt files in shellFolder
    if exist "%shellFolder%\*.txt" (
        echo Deleting all .txt files in %shellFolder%
        del /q "%shellFolder%\*.txt"
    ) else (
        echo "No .txt files to delete in %shellFolder%"
    )
    call :execute_operations
    call :time_log
) else (
    echo "Directory '%shareLocation%' not found. Waiting for directory..."
    timeout /t 5 >nul
    goto check_share_location
)

goto :eof

rem Execute operations
:execute_operations
echo "Executing script_log.bat..."
call "%scriptDir%script_log.bat"

echo "Executing move_CVE_txt.bat..."
call "%scriptDir%move_CVE_txt.bat"

echo "Executing install_packages.py..."
python "%scriptDir%..\..\Scripts\python\install_packages.py"

echo "Executing compress_files.py..."
python "%scriptDir%..\..\Scripts\python\compress_files.py"

echo "Executing check_and_create_version.py..."
python "%scriptDir%..\..\Scripts\python\check_and_create_version.py"

echo "Executing grep_CVE_content.py..."
python "%scriptDir%..\..\Scripts\python\grep_CVE_content.py"

echo "Executing click_to_create_issue.py..."
python "%scriptDir%..\..\Scripts\python\click_to_create_issue.py"

echo "Operations completed."

goto :eof
