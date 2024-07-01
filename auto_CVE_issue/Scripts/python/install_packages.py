import subprocess
import sys
import logging
import os

# Set logging, record the log to the ../../script.log file, and display it on the console
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, '..', '..', 'script.log')

#Create logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Create file handler
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)

#Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Set log format
formatter = logging.Formatter('[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s', datefmt='%Y%m%d %H:%M:%S')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

#Add handler to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def upgrade_pip():
    """
    Upgrade pip to the latest version.

    This function uses the subprocess module to run the command to upgrade pip.
    The command is created using the sys.executable variable, which refers to the Python interpreter.
    The command uses the -m flag to run the pip module.
    The command specifies the 'install' and '--upgrade' options to upgrade pip.
    """
    # upgrade pip
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    logger.info('pip has been upgraded')

def install_package(package_name, import_name=None):
    """
    Install a Python package if it is not already installed.

    Args:
        package_name (str): The name of the package to install.
        import_name (str, optional): The name of the package to import.
            Defaults to `package_name`.
    """
    # If import_name is not provided, use package_name as import_name
    if import_name is None:
        import_name = package_name

    try:
        # Try to import the package
        __import__(import_name)
        logger.info(f'{package_name} has been installed')
    except ImportError:
        # If not installed, perform installation operation
        subprocess.run([sys.executable, '-m', 'pip', 'install', package_name])
        logger.info(f'Installation of {package_name} completed')

# 升级 pip
upgrade_pip()

# Check if the requests package is installed
install_package('requests')

# Check if the BeautifulSoup package is installed
install_package('beautifulsoup4', 'bs4')

# Check if the Selenium package is installed
install_package('selenium')

# Check if the chardet package is installed
install_package('chardet')

logger.info('Suite check completed')
