@echo off
setlocal

REM Set the source folder path
set "sourceFolder=%USERPROFILE%\Downloads"

REM Set the destination folder path
set "destinationFolder=%~dp0..\..\Text_Files"

REM Ensure the destination folder exists
if not exist "%destinationFolder%" (
    mkdir "%destinationFolder%"
    echo Created directory: "%destinationFolder%"
)

REM Set the source file path
set "sourceFile=%sourceFolder%\feedback.txt"

REM Check if the source file exists
if not exist "%sourceFile%" (
    echo File not found: "%sourceFile%"
) else (
    REM Move the file to the destination folder
    move /y "%sourceFile%" "%destinationFolder%\feedback.txt"
    echo Moved feedback.txt to: "%destinationFolder%\feedback.txt"
)

REM Set the path to the Python scripts folder
set "pythonScriptFolder=%~dp0..\python"

REM Call the Python scripts
REM The scan_information.py script is used to gather information from the feedback.txt file
REM The CVE_address.py script is used to extract CVE addresses from the feedback.txt file
python "%pythonScriptFolder%\scan_information.py"
python "%pythonScriptFolder%\CVE_address.py"

REM Exit the batch script
exit /b 0

