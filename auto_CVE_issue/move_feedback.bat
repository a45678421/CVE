@echo off
setlocal

set "sourceFolder=%USERPROFILE%\Downloads"
set "destinationFolder=%~dp0"

rem ���� feedback.txt
set "sourceFile=%sourceFolder%\feedback.txt"
if not exist "%sourceFile%" (
    echo File not found: "%sourceFile%"
) else (
    move /y "%sourceFile%" "%destinationFolder%"
    echo Moved feedback.txt successfully.
)

python scan_information.py

python CVE_address.py

rem ���� CVE_address.txt
rem set "sourceFile=%sourceFolder%\CVE_address.txt"
rem if not exist "%sourceFile%" (
    rem echo File not found: "%sourceFile%"
rem ) else (
    rem move /y "%sourceFile%" "%destinationFolder%"
    rem echo Moved CVE_address.txt successfully.
rem )

rem ���� CVE_address.txt
rem set "sourceFile=%sourceFolder%\scan_info.txt"
rem if not exist "%sourceFile%" (
    rem echo File not found: "%sourceFile%"
rem ) else (
    rem move /y "%sourceFile%" "%destinationFolder%"
    rem echo Moved scan_info.txt successfully.
rem )

exit /b 0

