@echo off
setlocal enabledelayedexpansion

:: Define target directories
set "sourceFolder=%~dp0..\..\Text_Files"
set "shellFolder=%~dp0..\shell"
set "executablesFolder=%~dp0..\..\Executables"

:: Ensure target directory exists
if not exist "%shellFolder%" (
    mkdir "%shellFolder%"
    echo Created directory: "%shellFolder%"
)

:: Copy all files from %sourceFolder% to %shellFolder%
xcopy /s /e /y "%sourceFolder%\*.*" "%shellFolder%"

echo All files copied from "%sourceFolder%" to "%shellFolder%"

:: Use where command to find file location
set filename=feedback.txt
for /f "delims=" %%i in ('where /R %shellFolder% %filename%') do (
    set "file_path=%%i"
    echo File found at: !file_path!
    
    :: Define Execute_shell_script_directory variable, extract part before the last \
    for %%F in ("!file_path!") do set "Execute_shell_script_directory=%%~dpF"
)

:: Output Execute_shell_script_directory for debugging
echo Execute_shell_script_directory: %Execute_shell_script_directory%
echo %Execute_shell_script_directory% > %sourceFolder%\Execute_shell_script_directory.txt
echo %Execute_shell_script_directory% > %shellFolder%\Execute_shell_script_directory.txt

:: Read target host information from feedback.txt
set "feedbackFile=%shellFolder%\feedback.txt"
for /f "tokens=1,2 delims=: " %%a in (%feedbackFile%) do (
    if "%%a"=="scanIpAddress" set ip=%%b
    if "%%a"=="scanpassword" set password=%%b
)

:: Output target host information
echo Target Host IP: %ip%
echo Password: %password%

set /p username=Please enter the username:

:: Set remote host information
set "remoteUser=%username%"
set "remoteHost=%ip%"
set "remoteDirectory=/home/%username%"

:: Output remote host information
echo Remote Host: %remoteHost%
echo Remote User: %remoteUser%
echo Password: %password%
echo Remote Directory: %remoteDirectory%

:: Construct SCP command and output debug information
set "scpCommand=scp -r %Execute_shell_script_directory% %remoteUser%@%remoteHost%:%remoteDirectory%"
echo Executing SCP command: %scpCommand%
%scpCommand%

:: Grant execute permission to run.sh on the remote host
echo Granting execute permission to run.sh on the remote host...
echo %executablesFolder%\plink.exe -ssh %username%@%ip% -pw %password% "cd %remoteDirectory%"
%executablesFolder%\plink.exe -ssh %username%@%ip% -pw %password% "chmod +x %remoteDirectory%/shell/run.sh"
%executablesFolder%\plink.exe -ssh %username%@%ip% -pw %password% "chmod +x %remoteDirectory%/shell/auto_run.sh"

:: Remove \r characters from run.sh file
echo Removing \r characters from run.sh file...
%executablesFolder%\plink.exe -ssh %username%@%ip% -pw %password% "sed -i 's/\r$//' %remoteDirectory%/shell/run.sh"
echo Removing \r characters from auto_run.sh file...
%executablesFolder%\plink.exe -ssh %username%@%ip% -pw %password% "sed -i 's/\r$//' %remoteDirectory%/shell/auto_run.sh"

:: Create remote command file
echo cd %remoteDirectory%/shell > %shellFolder%\remote_command.txt
echo ./auto_run.sh >> %shellFolder%\remote_command.txt

:: Use SSH to connect to the target host and execute auto_run.sh
echo Connecting to the remote host and executing auto_run.sh...
%executablesFolder%\plink.exe -ssh -v %username%@%ip% -pw %password% -m %shellFolder%\remote_command.txt

:: Close CMD window after execution
exit
