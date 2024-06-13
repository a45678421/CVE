echo Step 19: Moving folders and ZIP file to the parent directory...

cd ..
cd py_script

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
)
if exist Medium (
    xcopy /E /Y /I Medium moved_folders\Medium
    rmdir /S /Q Medium
    echo Medium folder moved to moved_folders.
)
if exist Low (
    xcopy /E /Y /I Low moved_folders\Low
    rmdir /S /Q Low
    echo Low folder moved to moved_folders.
)
if exist High_txt (
    xcopy /E /Y /I High_txt moved_folders\High_txt
    rmdir /S /Q High_txt
    echo High_txt folder moved to moved_folders. 
)
if exist Medium_txt (
    xcopy /E /Y /I Medium_txt moved_folders\Medium_txt
    rmdir /S /Q Medium_txt
    echo Medium_txt folder moved to moved_folders. 
)
if exist Low_txt (
    xcopy /E /Y /I Low_txt moved_folders\Low_txt
    rmdir /S /Q Low_txt
    echo Low_txt folder moved to moved_folders. 
)
if exist summary (
    xcopy /E /Y /I summary moved_folders\summary
    rmdir /S /Q summary
    echo summary folder moved to moved_folders. 
)
if exist *.zip (
    move /Y *.zip moved_folders
    echo ZIP file moved to moved_folders.
)

REM Move all .txt files to moved_folders
for %%f in (*.txt) do (
    move /Y "%%f" moved_folders
    echo Moved %%f to moved_folders.
)

move /Y moved_folders ..

cd ..

dir 


timeout /t 5

echo All steps completed.

pause
