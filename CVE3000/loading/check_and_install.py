import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install_packages():
    try:
        import flask
        print("Flask is already installed.")
    except ImportError:
        print("Flask is not installed. Installing now...")
        install("Flask")

    try:
        import chardet
        print("chardet is already installed.")
    except ImportError:
        print("chardet is not installed. Installing now...")
        install("chardet")

if __name__ == "__main__":
    check_and_install_packages()
