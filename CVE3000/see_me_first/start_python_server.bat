@echo off
rem switches to the upper directory
cd..
rem switches to the loading directory
cd loading
rem opens http://127.0.0.1:5000/ in the default browser
start http://127.0.0.1:5000/
rem starts the Flask server
python flask_sever.py
