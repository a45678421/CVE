@echo off
setlocal enabledelayedexpansion

rem Initialize variables
set "targetDirectory="
set "targetFileName=cve_numbers.txt"

rem Read target directory path from CVE_address.txt
for /f "usebackq delims=" %%A in ("CVE_address.txt") do (
    set "targetDirectory=%%A"
)

rem Check if target directory variable is set
if not defined targetDirectory (
    echo Error: Target directory not found in CVE_address.txt.
    exit /b 1
)

echo Target directory: !targetDirectory!

rem Search for the file in the target directory
echo File search starting...
echo --------------------------------
echo.

echo Searching for %targetFileName% in !targetDirectory!

if exist "!targetDirectory!\%targetFileName%" (
    echo Found %targetFileName% in !targetDirectory!\%targetFileName%
    
    rem Copy cve_numbers.txt to the batch file's directory
    copy /y "!targetDirectory!\%targetFileName%" "%~dp0\%targetFileName%"
    echo Copied %targetFileName% to "%~dp0\%targetFileName%"

) else (
    echo Error: %targetFileName% not found in !targetDirectory!
)

echo.
echo --------------------------------
echo File search completed!


