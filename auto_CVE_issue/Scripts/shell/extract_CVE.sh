#!/bin/bash

# Define the log function
log() {
    local msg="$1"
    local script_name=$(basename "$0")
    local line_number=${BASH_LINENO[0]}
    local timestamp=$(date +'%Y%m%d %H:%M:%S')
    local formatted_message="[INFO $timestamp $script_name:$line_number] $msg"
    echo "$formatted_message" | tee -a script.log
}

# Specify the directory containing the .txt files
DIRECTORY="CVE_scan_results"

# Create an output file to store all unique CVE entries
OUTPUT_FILE="unique_cve_entries.txt"
rm -f "$OUTPUT_FILE"

log "Removed previous $OUTPUT_FILE if existed."

# Loop through each .txt file in the directory
for file in "$DIRECTORY"/*.txt; do
    log "Processing file: $file"
    # Use grep to search for lines containing "CVE-" and append them to a temporary file
    grep "CVE-" "$file" >> temp_cve_entries.txt
done

log "All CVE entries have been extracted to temp_cve_entries.txt."

# Sort and remove duplicate entries from the temporary file, then save to the output file
sort -u temp_cve_entries.txt > "$OUTPUT_FILE"

log "Sorted unique CVE entries and saved to $OUTPUT_FILE."

# Clean up the temporary file
rm -f temp_cve_entries.txt

log "Removed temporary file temp_cve_entries.txt."

# Extract only CVE numbers using awk and save to output file
awk '{print $2}' "$OUTPUT_FILE" > cve_numbers.txt

log "CVE numbers extracted and saved in cve_numbers.txt."

echo "CVE numbers extracted and saved in cve_numbers.txt."


# 動作流程圖
: '
Start
 |
 |---> 定義 log 函數
 |
 |---> 設置變量 DIRECTORY 和 OUTPUT_FILE
 |
 |---> 刪除之前的 OUTPUT_FILE 文件 (if exist)
 |       |
 |       |---> 記錄刪除操作到日誌
 |
 |---> 遍歷目錄中的所有 .txt 文件
 |       |
 |       |---> 對每個文件使用 grep 搜索 "CVE-" 並附加到臨時文件
 |       |       |
 |       |       |---> 記錄處理過程到日誌
 |
 |---> 記錄提取結果到日誌
 |
 |---> 排序並刪除重複的條目
 |       |
 |       |---> 保存到 OUTPUT_FILE
 |       |
 |       |---> 記錄排序結果到日誌
 |
 |---> 刪除臨時文件
 |       |
 |       |---> 記錄清理操作到日誌
 |
 |---> 提取 CVE 編號
 |       |
 |       |---> 保存到 cve_numbers.txt
 |       |
 |       |---> 記錄提取結果到日誌
 |
 |---> 在控制台顯示最終結果
 |
End
'