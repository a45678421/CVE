@echo off
set "scriptDir=%~dp0"
rem opens http://127.0.0.1:5000/ in the default browser
start http://127.0.0.1:5000/
rem starts the Flask server
python "%scriptDir%..\..\Scripts\python\show_html_reports.py"
