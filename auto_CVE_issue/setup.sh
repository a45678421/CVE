#!/bin/bash

# Function to clone and update vulners and vulscan repositories
clone_and_update_repos() {
    echo "Cloning and updating vulners and vulscan repositories..."
    sudo git clone https://github.com/vulnersCom/nmap-vulners.git /usr/share/nmap/scripts/nmap-vulners
    sudo git clone https://github.com/scipag/vulscan.git /usr/share/nmap/scripts/vulscan
    cd /usr/share/nmap/scripts/vulscan/utilities/updater/
    sudo chmod +x updateFiles.sh
    sudo ./updateFiles.sh
    echo "Cloning and updating completed."
}

# Function to install and configure nmap_converter
install_and_configure_nmap_converter() {
    echo "Installing and configuring nmap_converter..."
    sudo pip install python-libnmap
    sudo pip install XlsxWriter
    sudo git clone https://github.com/mrschyte/nmap-converter.git /usr/share/nmap/scripts/nmap-converter
    echo "nmap_converter installed and configured."
}

# Function to check if xsltproc is installed
check_xsltproc() {
    if ! command -v xsltproc &> /dev/null; then
        echo "xsltproc is not installed. Installing now..."
        sudo apt update
        sudo apt install -y xsltproc
        echo "xsltproc installed."
    else
        echo "xsltproc is already installed."
    fi
}
# Function to check if resources are already installed
check_resources() {
    if [ ! -d "/usr/share/nmap/scripts/nmap-vulners" ] || [ ! -d "/usr/share/nmap/scripts/vulscan" ] || [ ! -d "/usr/share/nmap/scripts/vulscan/utilities/updater/" ] || [ ! -d "/usr/share/nmap/scripts/nmap-converter" ]; then
        echo "Some resources are missing. Proceeding with installation..."
        clone_and_update_repos
        install_and_configure_nmap_converter
    else
        echo "All resources are already installed."
    fi
}


# Execute setup
echo "Executing setup..."
check_xsltproc
check_resources