$logFilePath = "..\loading\log.txt"

# 清空日志文件
Clear-Content -Path $logFilePath

# 执行批处理文件
& .\execute_tasks.bat | tee $logFilePath 

