#!/usr/bin/expect -f

# feedback.txt 文件的完整路径
set feedback_file "scan_info.txt"

# 初始化变量
set scanIpAddress ""
set remoteusername ""
set remotepassword ""

# 打开文件并读取变量值
set file_handle [open $feedback_file r]
set scanIpAddress [gets $file_handle]
set remoteusername [gets $file_handle]
set remotepassword [gets $file_handle]
close $file_handle

# 打印提取的数值以供验证
puts "IP: $scanIpAddress"
puts "Username: $remoteusername"
puts "Password: $remotepassword"

# 设置 SSH 连接所需的变量
set ip $scanIpAddress
set username $remoteusername
set password $remotepassword
set remoteDirectory "/home/$username"
set ScriptDirectory "auto_CVE_issue/"
set remoteScript "run.sh"
set exit "exit"

# SSH 连接并执行命令
spawn ssh $username@$ip 

expect {
    "password:" {
        send "$password\r"
        exp_continue
    }
    eof {
        exit
    }
 }

# 切换到远程目录并执行脚本
send "cd $remoteDirectory\r"
send "cd $ScriptDirectory\r"
send "./$remoteScript\r"

expect {
    "password for $username:" {
        send "$password\r"
        exp_continue
    }
    eof {
        exit
    }
}


# 保持交互模式
interact
