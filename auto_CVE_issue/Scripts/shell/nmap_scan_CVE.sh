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

# Redirect stdout and stderr to script.log, and keep them in the console
exec > >(tee -a script.log) 2>&1

# Ask the user to enter the target IP address
##read -p "Please enter the target IP address: " TARGET

# Read the target IP address from target_ip.txt
TARGET=$(cat target_ip.txt)

# Check if target_ip.txt is empty
if [ -z "$TARGET" ]; then
    log "Target IP address not found in target_ip.txt. Please make sure the file contains a valid IP address."
    exit 1
fi

log "Target IP address: $TARGET"

# Create a folder to save scan results
OUTPUT_FOLDER="CVE_scan_results"
mkdir -p "$OUTPUT_FOLDER"
log "Created folder $OUTPUT_FOLDER to save scan results."

# Create a combined Excel file
OUTPUT_EXCEL="$OUTPUT_FOLDER/combined.xlsx"
rm -f "$OUTPUT_EXCEL"
log "Prepared $OUTPUT_EXCEL for combined results."

# Define the path to nmap-converter.py
NMAP_CONVERTER="/usr/share/nmap/scripts/nmap-converter/nmap-converter.py"

# List all CSV files
CSV_FILES=("cve.csv" "osvdb.csv" "securitytracker.csv" "exploitdb.csv" "scipvuldb.csv" "xforce.csv" "openvas.csv" "securityfocus.csv")

# Loop through each CSV file and perform a vulnerability scan
for file in "${CSV_FILES[@]}"
do
    log "Perform script scan (using $file)..."
    sudo nmap -sV --script vulners --script-args vulscandb=$file $TARGET -oN "$OUTPUT_FOLDER/script_scan_${file%.csv}.txt" -oX "$OUTPUT_FOLDER/script_scan_${file%.csv}.xml"
    log "Completed script scan for $file, results saved in $OUTPUT_FOLDER/script_scan_${file%.csv}.txt and $OUTPUT_FOLDER/script_scan_${file%.csv}.xml."

    # Convert XML to Excel using NMAP_CONVERTER
    $NMAP_CONVERTER "$OUTPUT_FOLDER/script_scan_${file%.csv}.xml" -o "${OUTPUT_FOLDER}/script_scan_${file%.csv}.xlsx"
    log "Converted XML to Excel for $file, result saved in ${OUTPUT_FOLDER}/script_scan_${file%.csv}.xlsx."
done

# Convert all XML files to Excel
log "Converting all XML files to Excel..."
python "$NMAP_CONVERTER" "$OUTPUT_FOLDER"/*.xml -o "$OUTPUT_EXCEL"
log "All XML files have been converted to Excel and combined in $OUTPUT_EXCEL."

log "All vulnerability scans are completed and the results are saved in the $OUTPUT_FOLDER folder."

exit 0
