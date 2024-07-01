@echo off
setlocal enabledelayedexpansion

rem 設置日誌檔案
set "logFile=%~dp0batch_log.log"

rem 清空日誌文件
echo. > "%logFile%"

(
    cd Scripts/batch
    dir
    call tee.bat

    call move_feedback.bat
) 2>&1 | tee.exe -a "%logFile%"

REM Execute another batch file to run ssh.bat and python_run.bat
start cmd /c "call %~dp0Scripts/batch/run_scripts.bat " 2>&1 | tee.exe -a "%logFile%"

endlocal
pause