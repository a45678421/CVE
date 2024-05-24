import subprocess

# Check whether the requests package is installed
try:
     import requests
     print('requests has been installed')
except ImportError:
     # If not installed, perform installation operation
     subprocess.run(['pip', 'install', 'requests'])
     print('Installation of requests completed')

# Check if the BeautifulSoup package is installed
try:
     from bs4 import BeautifulSoup
     print('BeautifulSoup has been installed')
except ImportError:
     # If not installed, perform installation operation
     subprocess.run(['pip', 'install', 'beautifulsoup4'])
     print('Installation of BeautifulSoup completed')

# Check if the Selenium package is installed
try:
     from selenium import webdriver
     print('Selenium has been installed')
except ImportError:
     # If not installed, perform installation operation
     subprocess.run(['pip', 'install', 'selenium'])
     print('Selenium installation completed')

print('Suite check completed')