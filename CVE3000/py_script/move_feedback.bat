@echo off
setlocal

set "sourceFolder=%USERPROFILE%\Downloads"
set "destinationFolder=%~dp0"

rem move feedback.txt
set "sourceFile=%sourceFolder%\feedback.txt"
if not exist "%sourceFile%" (
    echo File not found: "%sourceFile%"
) else (
    move /y "%sourceFile%" "%destinationFolder%"
    echo Moved feedback.txt successfully.
)

exit /b 0

