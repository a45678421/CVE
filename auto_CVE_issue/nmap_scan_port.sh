#!/bin/bash

# Ask the user to enter the target IP address
##read -p "Please enter the target IP address: " TARGET

# Read the target IP address from target_ip.txt
TARGET=$(cat target_ip.txt)

# Check if target_ip.txt is empty
if [ -z "$TARGET" ]; then
    echo "Target IP address not found in target_ip.txt. Please make sure the file contains a valid IP address."
    exit 1
fi

# Create a folder to save scan results
OUTPUT_FOLDER="Port_scan_results" 
mkdir -p "$OUTPUT_FOLDER" 

# Create a combined Excel file
OUTPUT_EXCEL="$OUTPUT_FOLDER/combined.xlsx"
rm -f "$OUTPUT_EXCEL"

# TCP SYN scan
echo "Perform TCP SYN scan..." 
sudo nmap -sS -sV -T4 -Pn $TARGET -oN "$OUTPUT_FOLDER/tcp_syn_scan.txt" -oX "$OUTPUT_FOLDER/tcp_syn_scan.xml" 

# TCP connection scan
echo "Perform TCP connection scan..." 
sudo nmap -sT -sV -T4 -Pn $TARGET -oN "$OUTPUT_FOLDER/tcp_connect_scan.txt" -oX "$OUTPUT_FOLDER/tcp_connect_scan.xml" 

# TCP ACK scan
echo "Perform TCP ACK scan..." 
sudo nmap -sA -sV -T4 -Pn $TARGET -oN "$OUTPUT_FOLDER/tcp_ack_scan.txt" -oX "$OUTPUT_FOLDER/tcp_ack_scan.xml" 

# TCP window scan
echo "Perform TCP window scan..." 
sudo nmap -sW -sV -T4 -Pn $TARGET -oN "$OUTPUT_FOLDER/tcp_window_scan.txt" -oX "$OUTPUT_FOLDER/tcp_window_scan.xml" 

# TCP Maimon scan
echo "Perform TCP Maimon scan..." 
sudo nmap -sM -sV -T4 -Pn $TARGET -oN "$OUTPUT_FOLDER/tcp_maimon_scan.txt" -oX "$OUTPUT_FOLDER/tcp_maimon_scan.xml" 

# UDP scan
echo "Perform UDP scan..." 
sudo nmap -sU -sV -T4 -Pn $TARGET -oN "$OUTPUT_FOLDER/udp_scan.txt" -oX "$OUTPUT_FOLDER/udp_scan.xml" 

# TCP Null scan
echo "Perform TCP Null scan..." 
sudo nmap -sN -sV -T4 -Pn $TARGET -oN "$OUTPUT_FOLDER/tcp_null_scan.txt" -oX "$OUTPUT_FOLDER/tcp_null_scan.xml" 

# TCP FIN scan
echo "Perform TCP FIN scan..." 
sudo nmap -sF -sV -T4 -Pn $TARGET -oN "$OUTPUT_FOLDER/tcp_fin_scan.txt" -oX "$OUTPUT_FOLDER/tcp_fin_scan.xml" 

# TCP Xmas scan
echo "Perform TCP Xmas scan..." 
sudo nmap -sX -sV -T4 -Pn $TARGET -oN "$OUTPUT_FOLDER/tcp_xmas_scan.txt" -oX "$OUTPUT_FOLDER/tcp_xmas_scan.xml" 

# Run script scan
echo "Execute script scan..." 
sudo nmap --script vuln $TARGET -oN "$OUTPUT_FOLDER/script_scan.txt" -oX "$OUTPUT_FOLDER/script_scan.xml" 

echo "The scan results are saved in the $OUTPUT_FOLDER folder." 

# Convert XML to HTML using xsltproc
echo "Convert scan results to HTML..." 
for xml_file in $OUTPUT_FOLDER/*.xml; do
     html_file="${xml_file%.xml}.html" 
     xsltproc "$xml_file" -o "$html_file" 
done

echo "Conversion completed. HTML results saved in $OUTPUT_FOLDER folder."

# Define the path to nmap-converter.py
NMAP_CONVERTER="/usr/share/nmap/scripts/nmap-converter/nmap-converter.py"

# Find all XML files in OUTPUT_FOLDER
XML_FILES=$(find "$OUTPUT_FOLDER" -name "*.xml")

# Merge all XML into Excel files
echo "Converting XML files to Excel..."

# Loop through each XML file and convert it to Excel
for file in $XML_FILES; do
  python "$NMAP_CONVERTER" "$file" -o "${file%.xml}.xlsx"
done

echo "Each Excel files saved in $OUTPUT_FOLDER."

# Convert all XML files to Excel
echo "Converting All XML files to Excel..."
python "$NMAP_CONVERTER" "$OUTPUT_FOLDER"/*.xml -o "$OUTPUT_EXCEL"

echo "Combined Excel file saved as $OUTPUT_EXCEL."

exit