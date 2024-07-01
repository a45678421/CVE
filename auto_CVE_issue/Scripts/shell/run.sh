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

# sed -i 's/\r$//' run.sh
# Define the feedback.txt file path
feedback_file="feedback.txt"

# Give permission to setup.sh, nmap_port_scan.sh, and nmap_port_CVE.sh
chmod +x setup.sh
chmod +x nmap_scan_port.sh
chmod +x nmap_scan_CVE.sh
chmod +x extract_CVE.sh

log "Set execute permissions for setup.sh, nmap_scan_port.sh, nmap_scan_CVE.sh, and extract_CVE.sh."

# Prompt user to choose whether to run setup.sh
# read -p "Do you want to run setup.sh? (yes/no): " RUN_SETUP

sed -i 's/\r$//' setup.sh nmap_scan_port.sh nmap_scan_CVE.sh extract_CVE.sh run.sh

log "Removed carriage returns from shell scripts."

# Read related information from feedback.txt file
RUN_SETUP=$(grep -i "Set installation permission:" "$feedback_file" | cut -d: -f2 | tr -d ' ')
MODE=$(grep -i "Scan mode:" "$feedback_file" | cut -d: -f2 | tr -d ' ')
targetIpAddress=$(grep -i "targetIpAddress:" "$feedback_file" | cut -d: -f2 | tr -d ' ')

log "RUN_SETUP: $RUN_SETUP"
log "MODE: $MODE"
log "targetIpAddress: $targetIpAddress"

# Check user input
if [[ $RUN_SETUP == "yes" ]]; then
    log "Running setup.sh..."
    bash setup.sh
elif [[ $RUN_SETUP == "no" ]]; then
    log "Exiting without running setup.sh."
    exit 0
else
    log "Invalid input. Exiting."
    exit 1
fi

# Function to validate IP address format and range
validate_ip() {
    local ip=$1
    local IFS='.' # Set the internal field separator to '.' for splitting the IP address
    local ip_parts=($ip) # Split the IP address into its parts

    # Check if there are four parts in the IP address
    if [[ ${#ip_parts[@]} != 4 ]]; then
        log "Invalid IP address format. Please try again."
        return 1
    fi

    # Check if each part of the IP address is within the valid range
    for part in "${ip_parts[@]}"; do
        if ! [[ $part =~ ^[0-9]+$ ]]; then
            log "Invalid IP address format. Please try again."
            return 1
        elif (( $part < 0 || $part > 255 )); then
            log "Invalid IP address range. Each part should be between 0 and 255."
            return 1
        fi
    done

    echo "$ip" > target_ip.txt
    log "Valid IP address. Target IP saved in target_ip.txt."
    return 0
}

# Validate IP address format and range
validate_ip "$targetIpAddress" || { log "Invalid IP address format or range. Exiting."; exit 1; }

# Prompt user for target IP address
# read -p "Please enter the target IP address: " TARGET_IP

# Validate IP address format and range
# while ! validate_ip "$TARGET_IP"; do
    # read -p "Please enter a valid target IP address: " TARGET_IP
# done

# echo "Valid IP address. Target IP saved in target_ip.txt."

# Function to execute nmap_port_scan.sh
execute_port_scan() {
    log "Executing nmap_scan_port.sh..."
    bash nmap_scan_port.sh
    log "Port scan completed."
}

# Function to execute nmap_port_CVE.sh
execute_cve_scan() {
    log "Executing nmap_scan_CVE.sh..."
    bash nmap_scan_CVE.sh
    log "CVE scan completed."
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
        log "You have selected Mode 1: Execute nmap_port_scan.sh"
        log "This will take approximately 3 hours."
        execute_port_scan
        ;;
    2)
        log "You have selected Mode 2: Execute nmap_scan_CVE.sh"
        log "This will take approximately 5 minutes."
        execute_cve_scan
        ;;
    3)
        log "You have selected Mode 3: Execute both nmap_port_scan.sh and nmap_port_CVE.sh"
        log "This will take approximately 3 hours and 5 minutes."
        execute_port_scan
        execute_cve_scan
        ;;
    *)
        log "Invalid mode number. Exiting."
        exit 1
        ;;
esac

# Execute extract_CVE.sh script
log "Executing extract_CVE.sh..."
bash extract_CVE.sh

# Create nmap_scan directory
mkdir -p nmap_scan
log "Created nmap_scan directory."

# Move files to nmap_scan directory
case $MODE in
    1)
        sudo cp -rf "Port_scan_results" "nmap_scan/Port_scan_results"
        log "Copied Port_scan_results to nmap_scan directory."
        ;;
    2)
        # Move directory with force (ignoring non-empty target directory)
        sudo cp -rf "CVE_scan_results" "nmap_scan/CVE_scan_results"
        sudo cp -rf "cve_numbers.txt" "nmap_scan/"
        log "Copied CVE_scan_results and cve_numbers.txt to nmap_scan directory."
        ;;
    3)
        # Move files to nmap_scan directory
        sudo cp -f "CVE_scan_results" "Port_scan_results" "cve_numbers.txt" nmap_scan/
        log "Copied CVE_scan_results, Port_scan_results, and cve_numbers.txt to nmap_scan directory."
        ;;
    *)
        log "Invalid mode number. Exiting."
        exit 1
        ;;
esac

# Copy script.log to nmap_scan directory
sudo cp script.log "nmap_scan/"
log "Copied script.log to nmap_scan/."

# Recursively copy directory and its contents
log "Copied nmap_scan directory to /media/sf_share/."
log "Script execution completed."
sudo cp -r "nmap_scan" "/media/sf_share/"

echo "Script execution completed."

exit 0
