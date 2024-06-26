@echo on

cd ..
cd py_script

echo 0% > ..\loading\progress.txt
echo Progress: 0% > ..\loading\progress.txt

echo Step 8: Moving feedback.txt file...
python -u move_feedback.py 
echo Progress: 10% 
echo 10% > ..\loading\progress.txt

echo Step 9: Installing necessary packages...
python -u install_packages.py 
echo Progress: 20%
echo 20% > ..\loading\progress.txt

echo Step 10: Login and update feedback information...
python -u login_and_update_feedback.py 
echo Progress: 30%
echo 30% > ..\loading\progress.txt

echo Step 11: Convert from json to .xlsx
python -u jason_to_excel.py
echo Progress: 35%

echo Step 12: Extracting data from Excel file and classify_cve_by_severity...
python -u cve_level_classifier.py 
echo Progress: 40%
echo 40% > ..\loading\progress.txt

echo Step 13: Extracting and saving data by txt...
python -u extract_and_save_data_txt.py 
echo Progress: 50%
echo 50% > ..\loading\progress.txt

echo Step 14: Classify component data...
python -u classify_component_data.py
echo Progress: 55%
echo 55% > ..\loading\progress.txt

echo Step 15: Checking and creating versions...
python -u check_and_create_version.py 
echo Progress: 60%
echo 60% > ..\loading\progress.txt

echo Step 16: Compressing files...
python -u compress_files.py 
echo Progress: 65%
echo 65% > ..\loading\progress.txt

echo Step 17: Uploading zip file and getting zip file link...
python -u upload_zip_and_get_link.py 
echo Progress: 70%
echo 70% > ..\loading\progress.txt

echo Step 18: summary generate excel file...
python -u summary.py 
echo Progress: 80%
echo 80% > ..\loading\progress.txt

echo Step 19: Creating issues...
python -u create_issue_api.py
echo Progress: 90%
echo 90% > ..\loading\progress.txt

echo Step 20: Moving folders and ZIP file to the parent directory...

REM checks whether the moved_folders directory exists and deletes it if it exists.
if exist ..\moved_folders (
    rmdir /S /Q ..\moved_folders
)

mkdir moved_folders

REM Use xcopy to force overwriting of moved directories and files
if exist High (
    xcopy /E /Y /I High moved_folders\High
    rmdir /S /Q High
    echo High folder moved to moved_folders.
    echo High folder moved to moved_folders. >> ../loading/log.txt
)
if exist Medium (
    xcopy /E /Y /I Medium moved_folders\Medium
    rmdir /S /Q Medium
    echo Medium folder moved to moved_folders.
    echo Medium folder moved to moved_folders. >> ../loading/log.txt 
)
if exist Low (
    xcopy /E /Y /I Low moved_folders\Low
    rmdir /S /Q Low
    echo Low folder moved to moved_folders.
    echo Low folder moved to moved_folders. >> ../loading/log.txt 
)
if exist High_txt (
    xcopy /E /Y /I High_txt moved_folders\High_txt
    rmdir /S /Q High_txt
    echo High_txt folder moved to moved_folders. 
    echo High_txt folder moved to moved_folders. >> ../loading/log.txt
)
if exist Medium_txt (
    xcopy /E /Y /I Medium_txt moved_folders\Medium_txt
    rmdir /S /Q Medium_txt
    echo Medium_txt folder moved to moved_folders. 
    echo Medium_txt folder moved to moved_folders. >> ../loading/log.txt
)
if exist Low_txt (
    xcopy /E /Y /I Low_txt moved_folders\Low_txt
    rmdir /S /Q Low_txt
    echo Low_txt folder moved to moved_folders. 
    echo Low_txt folder moved to moved_folders. >> ../loading/log.txt
)
if exist High_classify_component (
    xcopy /E /Y /I High_classify_component moved_folders\High_classify_component
    rmdir /S /Q High_classify_component
    echo High_classify_component folder moved to moved_folders.
    echo High_classify_component folder moved to moved_folders. >> ../loading/log.txt
)
if exist Medium_classify_component (
    xcopy /E /Y /I Medium_classify_component moved_folders\Medium_classify_component
    rmdir /S /Q Medium_classify_component
    echo Medium_classify_component folder moved to moved_folders.
    echo Medium_classify_component folder moved to moved_folders. >> ../loading/log.txt 
)
if exist Low_classify_component (
    xcopy /E /Y /I Low_classify_component moved_folders\Low_classify_component
    rmdir /S /Q Low_classify_component
    echo Low_classify_component folder moved to moved_folders.
    echo Low_classify_component folder moved to moved_folders. >> ../loading/log.txt 
)
if exist summary (
    xcopy /E /Y /I summary moved_folders\summary
    rmdir /S /Q summary
    echo summary folder moved to moved_folders. 
    echo summary folder moved到 moved_folders. >> ../loading/log.txt
)
if exist *.zip (
    move /Y *.zip moved_folders
    echo ZIP file moved to moved_folders.
    echo ZIP file moved到 moved_folders. >> ../loading/log.txt
)

move /Y moved_folders ..

cd ..

dir 

echo Progress: 100% 
echo 100% > loading\progress.txt

timeout /t 5

echo All steps completed. 
pause
