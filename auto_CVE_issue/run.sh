#!/bin/bash
# sed -i 's/\r$//' run.sh
# 定義feedback.txt檔案路徑
feedback_file="feedback.txt"

# give permission to setup.sh and nmap_port_scan.sh and nmap_port_CVE.sh
chmod +x setup.sh
chmod +x nmap_scan_port.sh
chmod +x nmap_scan_CVE.sh
chmod +x extract_CVE.sh
# Prompt user to choose whether to run setup.sh
# read -p "Do you want to run setup.sh? (yes/no): " RUN_SETUP

sed -i 's/\r$//' setup.sh nmap_scan_port.sh nmap_scan_CVE.sh extract_CVE.sh run.sh

# 讀取 feedback.txt 文件中读取相关信息
RUN_SETUP=$(grep -i "Set installation permission:" "$feedback_file" | cut -d: -f2 | tr -d ' ')
MODE=$(grep -i "Scan mode:" "$feedback_file" | cut -d: -f2 | tr -d ' ')
targetIpAddress=$(grep -i "targetIpAddress:" "$feedback_file" | cut -d: -f2 | tr -d ' ')

echo $RUN_SETUP
echo $MODE
echo $targetIpAddress

# Check user input
if [[ $RUN_SETUP == "yes" ]]; then
    echo "Running setup.sh..."
    bash setup.sh
elif [[ $RUN_SETUP == "no" ]]; then
    echo "Exiting without running setup.sh."
    exit 0
else
    echo "Invalid input. Exiting."
    exit 1
fi

# Function to validate IP address format and range
validate_ip() {
    local ip=$1
    local IFS='.' # Set the internal field separator to '.' for splitting the IP address
    local ip_parts=($ip) # Split the IP address into its parts

    # Check if there are four parts in the IP address
    if [[ ${#ip_parts[@]} != 4 ]]; then
        echo "Invalid IP address format. Please try again."
        return 1
    fi

    # Check if each part of the IP address is within the valid range
    for part in "${ip_parts[@]}"; do
        if ! [[ $part =~ ^[0-9]+$ ]]; then
            echo "Invalid IP address format. Please try again."
            return 1
        elif (( $part < 0 || $part > 255 )); then
            echo "Invalid IP address range. Each part should be between 0 and 255."
            return 1
        fi
    done

    echo "$ip" > target_ip.txt
    return 0
}

# Validate IP address format and range
validate_ip "$targetIpAddress" || { echo "Invalid IP address format or range. Exiting."; exit 1; }

echo "Valid IP address. Target IP saved in target_ip.txt."

# Prompt user for target IP address
# read -p "Please enter the target IP address: " TARGET_IP

# Validate IP address format and range
# while ! validate_ip "$TARGET_IP"; do
    # read -p "Please enter a valid target IP address: " TARGET_IP
# done

# echo "Valid IP address. Target IP saved in target_ip.txt."

# Function to execute nmap_port_scan.sh
execute_port_scan() {
    echo "Executing nmap_scan_port.sh..."
    bash nmap_scan_port.sh
    echo "Port scan completed."
}

# Function to execute nmap_port_CVE.sh
execute_cve_scan() {
    echo "Executing nmap_scan_CVE.sh..."
    bash nmap_scan_CVE.sh
    echo "CVE scan completed."
}

# Prompt user to choose mode
# echo "Please choose a mode:"
# echo "1. Execute nmap_port_scan.sh (Approx. 3 hours)"
# echo "2. Execute nmap_scan_CVE.sh (Approx. 5 minutes)"
# echo "3. Execute both scripts (Approx. 3 hours and 5 minutes)"

# Read user input for mode selection
# read -p "Enter the mode number (1/2/3): " MODE

# Check user input and execute corresponding function
case $MODE in
    1)
        echo "You have selected Mode 1: Execute nmap_port_scan.sh"
        echo "This will take approximately 3 hours."
        execute_port_scan
        ;;
    2)
        echo "You have selected Mode 2: Execute nmap_port_CVE.sh"
        echo "This will take approximately 5 minutes."
        execute_cve_scan
        ;;
    3)
        echo "You have selected Mode 3: Execute both nmap_port_scan.sh and nmap_port_CVE.sh"
        echo "This will take approximately 3 hours and 5 minutes."
        execute_port_scan
        execute_cve_scan
        ;;
    *)
        echo "Invalid mode number. Exiting."
        exit 1
        ;;
esac

# Execute extract_CVE.sh script
bash extract_CVE.sh

# Create nmap_scan directory
mkdir -p nmap_scan

# Move files to nmap_scan directory
case $MODE in
    1)
        sudo cp -rf "Port_scan_results" "nmap_scan/Port_scan_results"
        ;;
    2)
        # Move directory with force (ignoring non-empty target directory)
        sudo cp -rf "CVE_scan_results" "nmap_scan/CVE_scan_results"
        sudo cp -rf "cve_numbers.txt" "nmap_scan/"
        ;;
    3)
        # Move files to nmap_scan directory
        sudo cp -f "CVE_scan_results" "Port_scan_results" "cve_numbers.txt" nmap_scan/
        ;;
    *)
        echo "Invalid mode number. Exiting."
        exit 1
        ;;
esac

# Recursively copy directory and its contents
sudo cp -r "nmap_scan" "/media/sf_share/"

echo "Script execution completed."

exit 0