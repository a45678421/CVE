@echo off
rem switches to the upper directory
cd..
rem switches to the loading directory
cd loading
rem delete log.txt if it exists
if exist log.txt del log.txt
rem delete progress.txt if it exists
if exist progress.txt del progress.txt
rem check and install the required Python packages
python check_and_install.py
rem opens http://127.0.0.1:5000/ in the default browser
start http://127.0.0.1:5000/
rem starts the Flask server
python flask_sever.py

