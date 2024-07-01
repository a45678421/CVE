#!/bin/bash

# Define the log function
# Logs a message to script.log, along with the script name, line number, and timestamp.
#
# Args:
#   msg (str): The message to be logged.
#
# Returns:
#   None
log() {
    # Get the message from the first argument
    local msg="$1"

    # Get the name of the script
    local script_name=$(basename "$0")

    # Get the line number of the caller
    local line_number=${BASH_LINENO[0]}

    # Get the current timestamp
    local timestamp=$(date +'%Y%m%d %H:%M:%S')

    # Format the message with the timestamp, script name, line number, and message
    local formatted_message="[INFO $timestamp $script_name:$line_number] $msg"

    # Print the formatted message to script.log
    echo "$formatted_message" | tee -a script.log
}

# Redirect stdout and stderr to script.log, and keep them in the console
exec > >(tee -a script.log) 2>&1

# Function to clone and update vulners and vulscan repositories
# Function to clone and update vulners and vulscan repositories
#
# This function clones the vulners and vulscan repositories from their respective GitHub repositories
# and updates them to the latest version.
#
# Returns:
#   None
clone_and_update_repos() {
    # Log that the cloning and updating process has started
    log "Cloning and updating vulners and vulscan repositories..."

    # Clone the vulners repository to the specified directory
    sudo git clone https://github.com/vulnersCom/nmap-vulners.git /usr/share/nmap/scripts/nmap-vulners

    # Clone the vulscan repository to the specified directory
    sudo git clone https://github.com/scipag/vulscan.git /usr/share/nmap/scripts/vulscan

    # Change the working directory to the updater directory of the vulscan repository
    cd /usr/share/nmap/scripts/vulscan/utilities/updater/

    # Change the permissions of the updateFiles.sh script to make it executable
    sudo chmod +x updateFiles.sh

    # Run the updateFiles.sh script to update the vulscan repositories
    sudo ./updateFiles.sh

    # Log that the cloning and updating process has completed
    log "Cloning and updating completed."
}

# Function to install and configure nmap_converter
# Function to install and configure nmap_converter
#
# This function installs and configures the nmap_converter utility.
# It installs the required Python packages using pip, clones the nmap_converter
# repository from GitHub, and logs the installation and configuration process.
#
# Returns:
#   None
install_and_configure_nmap_converter() {
    # Log the start of the installation and configuration process
    log "Installing and configuring nmap_converter..."

    # Install the required Python packages using pip
    sudo pip install python-libnmap
    sudo pip install XlsxWriter

    # Clone the nmap_converter repository to the specified directory
    sudo git clone https://github.com/mrschyte/nmap-converter.git /usr/share/nmap/scripts/nmap-converter

    # Log the completion of the installation and configuration process
    log "nmap_converter installed and configured."
}

# Function to check if xsltproc is installed
# Function to check if xsltproc is installed
#
# This function checks if the xsltproc utility is installed on the system.
# If it is not installed, it installs it using apt.
#
# Returns:
#   None
check_xsltproc() {
    # Check if xsltproc is installed
    if ! command -v xsltproc &> /dev/null; then
        # If xsltproc is not installed, log the installation process and install it
        log "xsltproc is not installed. Installing now..."
        sudo apt update
        sudo apt install -y xsltproc
        log "xsltproc installed."
    else
        # If xsltproc is already installed, log that it is already installed
        log "xsltproc is already installed."
    fi
}

# Function to check if resources are already installed
# Function to check if resources are already installed
# It checks if the required directories exist or not
# If any of the directories are missing, it proceeds with the installation
# Otherwise, it logs that all resources are already installed
check_resources() {
    # Check if the required directories exist
    # If any of the directories are missing, proceed with installation
    if [ ! -d "/usr/share/nmap/scripts/nmap-vulners" ] || \
       [ ! -d "/usr/share/nmap/scripts/vulscan" ] || \
       [ ! -d "/usr/share/nmap/scripts/vulscan/utilities/updater/" ] || \
       [ ! -d "/usr/share/nmap/scripts/nmap-converter" ]; then
        log "Some resources are missing. Proceeding with installation..."
        clone_and_update_repos
        install_and_configure_nmap_converter
    else
        # Log that all resources are already installed
        log "All resources are already installed."
    fi
}

# Execute setup
log "Executing setup..."
check_xsltproc
check_resources

log "Setup completed."

exit 0
