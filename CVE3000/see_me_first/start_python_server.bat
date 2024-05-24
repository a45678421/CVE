@echo off
rem 切换到上级目录
cd ..
rem 切换到 loading 目录
cd loading
rem 在默认浏览器中打开 http://127.0.0.1:5000/
start http://127.0.0.1:5000/
rem 启动 Flask 服务器
python flask_sever.py
