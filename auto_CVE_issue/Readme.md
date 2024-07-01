# Script and Program Descriptions

| Script/Program Name     | Description                                                                                                                    |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| `move_feedback.bat`     | Moves feedback.txt from the download location to the current batch file location and performs data categorization, storing it in auto_CVE_issue, which will be copied to Virtual Box |
| `ssh.bat`               | Executes remote copy to copy auto_CVE_issue to Virtual Box and triggers auto_run.sh                                             |
| `auto_run.sh`           | Executes run.sh and automatically fills in the password when prompted during SSH, ensuring successful execution of scans and avoiding errors due to permission issues |
| `run.sh`                | Controls setup.sh, nmap_scan_CVE.sh, and nmap_scan_Port.sh based on feedback.txt content, then returns all results to the PC, to be used by Python scripts to fetch CVE-related data from the web and upload to Redmine |
| `setup.sh`              | Checks for and installs required tools/packages if they do not exist                                                           |
| `nmap_scan_CVE.sh`      | Scans for CVE vulnerabilities                                                                                                   |
| `nmap_scan_Port.sh`     | Scans for port vulnerabilities                                                                                                  |
| `move_CVE_txt.bat`      | Extracts CVE_numbers.txt from the scanned results in Share File, which contains the scanned CVE numbers, used for web data fetching |
| `install_packages.py`   | Installs required Python packages                                                                                               |
| `compress_files.py`     | Compresses the obtained result folder for easier upload to Redmine, reducing errors and individual file uploads                  |
| `grep_CVE_content.py`   | Fetches data from the web based on CVE numbers and saves them in auto_CVE_issue as CVE-xxxx-xxxx.txt, to be included in Redmine descriptions |
| `check_and_create_version.py` | Checks Redmine for required issue versions, creates one if not found, in preparation for creating issues                  |
| `click_to_create_issue.py` | Creates a bug tracker based on feedback.txt, CVE.txt, and result.zip                                                       |

# SSH Commands
- `sudo systemctl status ssh`: Check SSH service status
- `sudo systemctl enable ssh`: Enable SSH service to start automatically on system boot
- `sudo systemctl start ssh`: Start SSH service
- `sudo systemctl status ssh`: Check SSH service status again to ensure successful start

# Execution Steps
1. Open `Web_Files/index.html` to fill in data (run `python example_to_fill_in.py` if unsure how to fill)
2. Enter SSH Commands on Kali Linux terminal
3. Click `Run.bat` twice
4. Enter scanning terminal user
5. Enter password required for `scp`
6. Wait for automatic execution

# Notes
Before testing, make sure to comment out the following two lines in `click_to_create_issue.py` to avoid accidentally creating an issue:
```python
# create_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create']")
# create_button.click()
