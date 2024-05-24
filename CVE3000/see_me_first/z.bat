@echo on

set log_file=..\loading\log.txt

echo. > %log_file%

cd .. 
cd py_script

echo Progress: 0% 

echo Step 8: 移動 feedback.txt 檔案...
call move_feedback.bat 
echo Progress: 10% 
echo 10% > ..\loading\progress.txt

echo Step 9: 安裝必要的套件...
python -u install_packages.py 
echo Progress: 20% 
echo 20% > ..\loading\progress.txt

