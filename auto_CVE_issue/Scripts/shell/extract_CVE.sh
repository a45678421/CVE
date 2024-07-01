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
