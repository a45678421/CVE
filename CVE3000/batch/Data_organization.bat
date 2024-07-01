echo Step 19: Moving folders and ZIP file to the parent directory...

cd ..
cd py_script

REM checks whether the moved_folders directory exists and deletes it if it exists.
if exist ..\moved_folders (
    rmdir /S /Q ..\moved_folders
)

mkdir moved_folders

REM Use xcopy to force overwriting of moved directories and files
for /d %%D in (*) do (
    if not "%%D" == "__pycache__" (
        xcopy /E /Y /I "%%D" moved_folders\"%%D"
        rmdir /S /Q "%%D"
        echo Folder %%D moved to moved_folders.
    )
)

for %%F in (*) do (
    if not "%%~xF" == ".py" (
        if not "%%~nxF" == "moved_folders" (
            move /Y "%%F" moved_folders
            echo File %%F moved to moved_folders.
        )
    )
)

move /Y moved_folders ..

cd ..

dir 

timeout /t 5

echo All steps completed.

pause
