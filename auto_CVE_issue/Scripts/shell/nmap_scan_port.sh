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
OUTPUT_FOLDER="Port_scan_results"
mkdir -p "$OUTPUT_FOLDER"
log "Created folder $OUTPUT_FOLDER to save scan results."

# Create a combined Excel file
OUTPUT_EXCEL="$OUTPUT_FOLDER/combined.xlsx"
rm -f "$OUTPUT_EXCEL"
log "Prepared $OUTPUT_EXCEL for combined results."

# TCP SYN scan
log "Perform TCP SYN scan..."
sudo nmap -sS -sV -T4 -Pn $TARGET -oN "$OUTPUT_FOLDER/tcp_syn_scan.txt" -oX "$OUTPUT_FOLDER/tcp_syn_scan.xml"
log "TCP SYN scan completed."

# TCP connection scan
log "Perform TCP connection scan..."
sudo nmap -sT -sV -T4 -Pn $TARGET -oN "$OUTPUT_FOLDER/tcp_connect_scan.txt" -oX "$OUTPUT_FOLDER/tcp_connect_scan.xml"
log "TCP connection scan completed."

# TCP ACK scan
log "Perform TCP ACK scan..."
sudo nmap -sA -sV -T4 -Pn $TARGET -oN "$OUTPUT_FOLDER/tcp_ack_scan.txt" -oX "$OUTPUT_FOLDER/tcp_ack_scan.xml"
log "TCP ACK scan completed."

# TCP window scan
log "Perform TCP window scan..."
sudo nmap -sW -sV -T4 -Pn $TARGET -oN "$OUTPUT_FOLDER/tcp_window_scan.txt" -oX "$OUTPUT_FOLDER/tcp_window_scan.xml"
log "TCP window scan completed."

# TCP Maimon scan
log "Perform TCP Maimon scan..."
sudo nmap -sM -sV -T4 -Pn $TARGET -oN "$OUTPUT_FOLDER/tcp_maimon_scan.txt" -oX "$OUTPUT_FOLDER/tcp_maimon_scan.xml"
log "TCP Maimon scan completed."

# UDP scan
log "Perform UDP scan..."
sudo nmap -sU -sV -T4 -Pn $TARGET -oN "$OUTPUT_FOLDER/udp_scan.txt" -oX "$OUTPUT_FOLDER/udp_scan.xml"
log "UDP scan completed."

# TCP Null scan
log "Perform TCP Null scan..."
sudo nmap -sN -sV -T4 -Pn $TARGET -oN "$OUTPUT_FOLDER/tcp_null_scan.txt" -oX "$OUTPUT_FOLDER/tcp_null_scan.xml"
log "TCP Null scan completed."

# TCP FIN scan
log "Perform TCP FIN scan..."
sudo nmap -sF -sV -T4 -Pn $TARGET -oN "$OUTPUT_FOLDER/tcp_fin_scan.txt" -oX "$OUTPUT_FOLDER/tcp_fin_scan.xml"
log "TCP FIN scan completed."

# TCP Xmas scan
log "Perform TCP Xmas scan..."
sudo nmap -sX -sV -T4 -Pn $TARGET -oN "$OUTPUT_FOLDER/tcp_xmas_scan.txt" -oX "$OUTPUT_FOLDER/tcp_xmas_scan.xml"
log "TCP Xmas scan completed."

# Run script scan
log "Execute script scan..."
sudo nmap --script vuln $TARGET -oN "$OUTPUT_FOLDER/script_scan.txt" -oX "$OUTPUT_FOLDER/script_scan.xml"
log "Script scan completed."

log "The scan results are saved in the $OUTPUT_FOLDER folder."

# Convert XML to HTML using xsltproc
log "Convert scan results to HTML..."
for xml_file in $OUTPUT_FOLDER/*.xml; do
    html_file="${xml_file%.xml}.html"
    xsltproc "$xml_file" -o "$html_file"
    log "Converted $xml_file to $html_file."
done

log "Conversion completed. HTML results saved in $OUTPUT_FOLDER folder."

# Define the path to nmap-converter.py
NMAP_CONVERTER="/usr/share/nmap/scripts/nmap-converter/nmap-converter.py"

# Find all XML files in OUTPUT_FOLDER
XML_FILES=$(find "$OUTPUT_FOLDER" -name "*.xml")

# Merge all XML into Excel files
log "Converting XML files to Excel..."

# Loop through each XML file and convert it to Excel
for file in $XML_FILES; do
    python "$NMAP_CONVERTER" "$file" -o "${file%.xml}.xlsx"
    log "Converted $file to ${file%.xml}.xlsx."
done

log "Each Excel file saved in $OUTPUT_FOLDER."

# Convert all XML files to Excel
log "Converting All XML files to Excel..."
python "$NMAP_CONVERTER" "$OUTPUT_FOLDER"/*.xml -o "$OUTPUT_EXCEL"
log "Combined Excel file saved as $OUTPUT_EXCEL."

log "Script execution completed."

exit 0
