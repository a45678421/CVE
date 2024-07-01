@echo off
setlocal enabledelayedexpansion

rem Initialize variables
set "targetDirectory="
set "targetFileName=cve_numbers.txt"
set "cveAddressFile=%~dp0..\..\Text_Files\CVE_address.txt"
set "destinationFolder=%~dp0..\..\Text_Files"

rem Read target directory path from CVE_address.txt
for /f "usebackq delims=" %%A in ("%cveAddressFile%") do (
    set "targetDirectory=%%A"
)

rem Check if target directory variable is set
if not defined targetDirectory (
    echo Error: Target directory not found in %cveAddressFile%.
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
    
    rem Copy cve_numbers.txt to the destination folder
    copy /y "!targetDirectory!\%targetFileName%" "%destinationFolder%\%targetFileName%"
    echo Copied %targetFileName% to "%destinationFolder%\%targetFileName%"

) else (
    echo Error: %targetFileName% not found in !targetDirectory!
)

echo.
echo --------------------------------
echo File search completed!
