REM Start python_run.bat in a separate command prompt window
REM The "start" command is used to run the batch file in a separate window
REM The "call" command is used to execute the batch file in the current window
REM The "tee.exe -a" command is used to append the log message to the log file
echo Starting python_run.bat... | tee.exe -a "%logFile%"
start "Python Run" cmd /c "call Scripts\batch\python_run.bat"

REM Start ssh.bat in a separate command prompt window
REM The "start" command is used to run the batch file in a separate window
REM The "call" command is used to execute the batch file in the current window
REM The "tee.exe -a" command is used to append the log message to the log file
echo Starting ssh.bat... | tee.exe -a "%logFile%"
start "ssh Run" cmd /c "call Scripts\batch\ssh.bat" 

