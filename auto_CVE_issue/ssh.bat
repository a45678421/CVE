@echo off
setlocal enabledelayedexpansion

rem 要搜尋的檔案名
set "filename=feedback.txt"

rem 使用 where 指令搜尋檔案位置
for /f "delims=" %%i in ('where /R \ %filename%') do (
     set "file_path=%%i"
     echo File found at: !file_path!
    
     rem 將檔案位置定義為 localDirectory 變量，截取最後一個 \ 之前的部分
     for %%F in ("!file_path!") do set "localDirectory=%%~dpF"
)

rem 輸出 localDirectory，僅供調試使用
echo localDirectory: %localDirectory%
echo %localDirectory% > localDirectory.txt

rem 读取 scan_info.txt 中的目标主机信息
for /f "tokens=1,2 delims=: " %%a in (feedback.txt) do (
    if "%%a"=="scanIPAddress" set ip=%%b
    if "%%a"=="scanpassword" set password=%%b
)

rem 輸出讀取到的目標主機信息
echo Target Host IP: %ip%
echo Password: %password%

rem 若未從 scan_info.txt 讀取到信息，使用預設值
rem if "%ip%"=="" set ip=172.17.8.18
if "%username%"=="" set username=sky
rem if "%password%"=="" set password=1234

set /p username=Please enter the username (Press Enter to use default sky):

rem 設定遠端主機訊息
set "remoteUser=%username%"
set "remoteHost=%ip%"
set "remoteDirectory=/home/%username%"

rem 產生 SSH 金鑰對
rem ssh-keygen -t rsa -b 2048 -f "%localDirectory%\my_ssh_key" -N ""
REM 使用 plink.exe 通過 SSH 註冊到遠端主機並安裝 sshpass 套件
rem echo Ibstall sshpass package...
rem echo %password% | plink.exe -ssh %username%@%ip% -pw %password% "echo %password% | sudo -S apt install sshpass -y"
rem 將公鑰新增至遠端主機的 authorized_keys 檔案中
rem echo Adding SSH key to authorized_keys file on the remote host...
rem plink.exe -ssh %username%@%ip% -pw %password% "mkdir -p ~/.ssh && touch ~/.ssh/authorized_keys && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keyssh/authorized_keys && cat >> ~/.ssh/authorized_keys" < "%localDirectory%\my_ssh_key.pub"
rem 建置 SCP 命令並輸出偵錯訊息
set "scpCommand=scp -r %localDirectory% %remoteUser%@%remoteHost%:%remoteDirectory%
echo Executing SCP command: %scpCommand%
%scpCommand%

rem 在遠端主機上給予 run.sh 執行權限
echo Granting execute permission to run.sh on the remote host...
plink.exe -ssh %username%@%ip% -pw %password% "chmod +x %remoteDirectory%/auto_CVE_issue/run.sh"
plink.exe -ssh %username%@%ip% -pw %password% "chmod +x %remoteDirectory%/auto_CVE_issue/auto_run.sh"

rem 移除 run.sh 檔案中的 \r 字符
echo Removing \r characters from run.sh file...
plink.exe -ssh %username%@%ip% -pw %password% "sed -i 's/\r$//' %remoteDirectory%/auto_CVE_issue/run.sh"
echo Removing \r characters from auto_run.sh file...
plink.exe -ssh %username%@%ip% -pw %password% "sed -i 's/\r$//' %remoteDirectory%/auto_CVE_issue/auto_run.sh"
rem 建立遠端命令文件
echo cd %remoteDirectory%/auto_CVE_issue > remote_command.txt
rem echo ./run.sh >> remote_command.txt
echo ./auto_run.sh >> remote_command.txt
rem 使用 SSH key 連線到目標主機並執行 run.sh
rem echo Connecting to the remote host and executing run.sh using SSH key...
rem plink.exe -ssh %username%@%ip% -i "%localDirectory%\my_ssh_key" -m remote_command.txt
echo Connecting to the remote host and executing run.sh...
plink.exe -ssh -v %username%@%ip% -pw %password% -m remote_command.txt

rem 在此處新增 pause，以保持視窗打開
rem pause
