#!/bin/bash

# Specify the directory containing the .txt files
DIRECTORY="CVE_scan_results"

# Create an output file to store all unique CVE entries
OUTPUT_FILE="unique_cve_entries.txt"
rm -f "$OUTPUT_FILE"

# Loop through each .txt file in the directory
for file in "$DIRECTORY"/*.txt; do
    echo "Processing file: $file"
    # Use grep to search for lines containing "CVE-" and append them to a temporary file
    grep "CVE-" "$file" >> temp_cve_entries.txt
done

# Sort and remove duplicate entries from the temporary file, then save to the output file
sort -u temp_cve_entries.txt > "$OUTPUT_FILE"

# Clean up the temporary file
rm -f temp_cve_entries.txt

# Extract only CVE numbers using awk and save to output file
awk '{print $2}' "$OUTPUT_FILE" > cve_numbers.txt

echo "CVE numbers extracted and saved in cve_numbers.txt."
