#!/usr/bin/expect -f

# feedback.txt 檔案的完整路徑
set feedback_file "scan_info.txt"

# 初始化變數
set scanIpAddress ""
set remoteusername ""
set remotepassword ""

# 開啟檔案並讀取變數值
set file_handle [open $feedback_file r]
set scanIpAddress [gets $file_handle]
set remoteusername [gets $file_handle]
set remotepassword [gets $file_handle]
close $file_handle

# 列印提取的數值以供驗證
puts "IP: $scanIpAddress"
puts "Username: $remoteusername"
puts "Password: $remotepassword"

# 設定 SSH 連線所需的變數
set ip $scanIpAddress
set username $remoteusername
set password $remotepassword
set remoteDirectory "/home/$username"
set ScriptDirectory "shell/"
set remoteScript "run.sh"

# SSH 連線並執行指令
spawn ssh $username@$ip

expect {
    "Are you sure you want to continue connecting (yes/no/*)?" {
        send "yes\r"
        exp_continue
    }
    "password:" {
        send "$password\r"
        exp_continue
    }
    "Permission denied, please try again." {
        send_user "Password was incorrect.\n"
        exit 1
    }
    "$username@*" {
        send "cd $remoteDirectory\r"
        expect "$username@*"
        send "cd $ScriptDirectory\r"
        expect "$username@*"
        send "./$remoteScript\r"
        exp_continue
    }
}

# 處理執行 run.sh 時可能出現的密碼提示
expect {
    "password for $username:" {
        send "$password\r"
        exp_continue
    }
    "Script execution completed." {
        send "exit\r"
        expect eof
    }
}

# 保持交互模式
interact
