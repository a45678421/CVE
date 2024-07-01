@echo off
setlocal

REM Check for admin rights
REM This function checks if the script is running with admin rights.
REM If not, it requests admin privileges and exits the script.
:checkAdmin
    openfiles >nul 2>&1
    if %errorlevel% neq 0 (
        echo Requesting administrator privileges...
        powershell -command "Start-Process '%~f0' -Verb RunAs"
        exit /b 1
    )

REM Call the function to check for admin rights
call :checkAdmin

REM Variables
REM Define the paths for the source and target files
set "sourcePath=%~dp0..\..\Executables\tee.exe"
set "targetPath=C:\Windows\System32\tee.exe"

REM Check if source file exists
REM If the source file does not exist, display an error message and exit the script.
if not exist "%sourcePath%" (
    echo tee.exe not found in the specified directory. Exiting.
    exit /b 1
)

REM Check if target file exists
REM If the target file already exists, display a message indicating that it will be overwritten.
if exist "%targetPath%" (
    echo tee.exe already exists in C:\Windows\System32. Overwriting.
)

REM Copy the source file to the target location
copy "%sourcePath%" "%targetPath%" /Y

REM Check if the target file was successfully copied
REM If the target file exists, display a success message. Otherwise, display an error message and exit the script.
if exist "%targetPath%" (
    echo tee.exe has been successfully copied to C:\Windows\System32.
) else (
    echo Failed to copy tee.exe to C:\Windows\System32.
    exit /b 1
)

endlocal
pause
