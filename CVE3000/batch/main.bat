@echo off

echo Starting new CMD window to execute tasks...
start cmd /k "call "%~dp0execute_tasks.bat""

start cmd /k "call "%~dp0start_python_server.bat""


