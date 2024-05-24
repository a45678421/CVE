@echo off
setlocal

rem 設定變數
rem 從 CVE_address.txt 中讀取內容並設定 feedbackFile 和 shareLocation 變數
for /f "delims=" %%a in (CVE_address.txt) do (
     set "shareLocation=%%a"
     set "feedbackFile=!shareLocation!\feedback.txt"
)

echo Feedback File: %feedbackFile%
echo Share Location: %shareLocation%

rem 循環檢查掃描模式並執行對應操作
:check_mode
for /f "tokens=1,2 delims== " %%a in (%feedbackFile%) do (
      if /i "%%a"=="Scan" if /i "%%b"=="mode" (
          set /p "mode=" < "%feedbackFile%"
          if "%mode%"=="1" (
              echo "Scan mode is 1. Checking directory..."
              call :check_and_execute
          ) else if "%mode%"=="2" (
              echo "Scan mode is 2. Checking directory..."
              call :check_and_execute
          ) else if "%mode%"=="3" (
              echo "Scan mode is 3. Skipping operations."
              exit /b 0
          ) else (
              echo "Invalid mode in feedback.txt. Exiting."
              exit /b 1
          )
      )
)

rem 檢查並執行操作
:check_and_execute
if exist "%shareLocation%" (
      echo "Directory '%shareLocation%' found. Executing operations..."
      call :execute_operations
) else (
      echo "Directory '%shareLocation%' not found. Skipping operations."
)

goto :eof

rem 執行操作
:execute_operations
echo "Executing move_CVE_txt.bat..."
call move_CVE_txt.bat

echo "Executing install_packages.py..."
python install_packages.py

echo "Executing compress_files.py..."
python compress_files.py

echo "Executing check_and_create_version.py..."
python check_and_create_version.py

echo "Executing grep_CVE_content.py..."
python grep_CVE_content.py

echo "Executing click_to_create_issue.py..."
python click_to_create_issue.py

echo "Operations completed."
