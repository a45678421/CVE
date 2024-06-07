import logging
import chardet
import os
import pandas as pd
from redminelib import Redmine
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Redmine 伺服器的 URL 和 API 金鑰
REDMINE_URL  = 'http://advrm.advantech.com:3006/'

# 設置日誌文件路徑
log_file_path = '../loading/log.txt'

# 配置日誌記錄器
logging.basicConfig(
    level=logging.INFO,
    filename=log_file_path,
    filemode='w',
    format='[%(levelname)1.1s %(asctime)s %(module)s:%(message)s',
    datefmt='%Y%m%d %H:%M:%S',
)

# 設置控制台處理器以顯示在終端
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)1.1s %(asctime)s %(module)s:%(message)s', datefmt='%Y%m%d %H:%M:%S')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logging.info('Creating Redmine Issue...')

# 檢測檔案編碼
with open("feedback.txt", "rb") as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

logging.info('Detected encoding: %s', encoding)

with open("feedback.txt", "r", encoding=encoding) as file:
    lines = file.readlines()

# 定義需要的變數
USERNAME = ""
PASSWORD = ""
API_KEY = ""
PROJECT = ""
VERSION = ""
ASSIGNEE_NAME = ""
SEVERITY_VALUE = ""
zip_link_content = ""

# 提取需要的資料並定義成變數
for line in lines:
    line = line.strip()  # 移除頭尾空白和換行符
    if line.startswith("USERNAME"):
        USERNAME = line.split("=")[1].strip().strip('"')
    elif line.startswith("PASSWORD"):
        PASSWORD = line.split("=")[1].strip().strip('"')
    elif line.startswith("API_KEY"):
        API_KEY = line.split("=")[1].strip().strip('"')
    elif line.startswith("PROJECT"):
        PROJECT = line.split("=")[1].strip().strip('"')
    elif line.startswith("VERSION"):
        REDMINE_VERSION = line.split("=")[1].strip().strip('"')
    elif line.startswith("ASSIGNEE_NAME"):
        ASSIGNEE_NAME = line.split("=")[1].strip().strip('"')
    elif line.startswith("SEVERITY_VALUE"):
        SEVERITY_VALUE = line.split("=")[1].strip().strip('"')
        folder_path = SEVERITY_VALUE  # 將 SEVERITY_VALUE 的值賦值也給 folder_path

# 輸出提取的值
logging.info('Extracted values:')
logging.info('USERNAME: %s', USERNAME)
logging.info('PASSWORD : %s', PASSWORD)
logging.info('PROJECT : %s', PROJECT)
logging.info('REDMINE_VERSION : %s', REDMINE_VERSION)
logging.info('ASSIGNEE_NAME : %s', ASSIGNEE_NAME)
logging.info('SEVERITY_VALUE : %s', SEVERITY_VALUE)
logging.info('folder_path : %s', folder_path)
logging.info('REDMINE_API_KEY : %s', API_KEY)

# 獲取SEVERITY資料夾中所有Excel檔的檔案名
file_names = os.listdir(folder_path)

# 獲取當前指令檔所在目錄的路徑
current_directory = os.path.dirname(os.path.abspath(__file__))

# 讀取 zip_link.txt 檔並列印連結內容
zip_link_file = f"{SEVERITY_VALUE}_zip_link.txt"
zip_link_path = os.path.join(current_directory, zip_link_file)

if os.path.exists(zip_link_path):
    with open(zip_link_path, "r", encoding=encoding) as zip_link_file:
        zip_link_content = zip_link_file.read()
        logging.info('zip link : %s', zip_link_content)
else:
    logging.info('File %s does not exist.', zip_link_path)

# 初始化 Redmine 連接
redmine = Redmine(REDMINE_URL, key=API_KEY)

# 搜索項目名稱以找到指定項目
projects = redmine.project.all()
target_project = None

logging.info('Available projects:')
for project in projects:
    logging.info('Project: %s', project.name)
    if project.name.lower() == PROJECT.lower():
        target_project = project

if not target_project:
    logging.error('Project %s not found', PROJECT)
    raise ValueError(f'Project {PROJECT} not found')

PROJECT_ID = target_project.id
logging.info('Target project ID: %s', PROJECT_ID)

# 獲取項目版本 ID
version_id = None
logging.info('Available versions in project %s:', target_project.name)
for version in target_project.versions:
    logging.info('Version: %s', version.name)
    if version.name == REDMINE_VERSION:
        version_id = version.id

if version_id is None:
    logging.error('Version %s not found in project %s', REDMINE_VERSION, PROJECT)
    raise ValueError(f'Version {REDMINE_VERSION} not found in project {PROJECT}')

logging.info('Target version ID: %s', version_id)

# 初始化 WebDriver
try:
    driver = webdriver.Chrome()
    logging.info('Using Chrome browser')
except Exception as e:
    logging.warning(f'Chrome browser not available: {e}. Falling back to Edge.')
    driver = webdriver.Edge()
    logging.info('Using Edge browser')

try:
    login_url = "http://advrm.advantech.com:3006/login"
    driver.get(login_url)

    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(USERNAME)

    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(PASSWORD)

    password_input.send_keys(Keys.RETURN)

    logging.info('Logged in successfully')

    project_jump = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "project-jump"))
    )
    project_jump.click()

    project_list = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.drdn-items.projects.selection"))
    )

    project_link = project_list.find_element(By.CSS_SELECTOR, f"a[title='{PROJECT}']")
    project_link.click()

    issue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "issues"))
    )
    issue_button.click()

    # 創建新 Issue 以獲取分配對象 ID
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.icon.icon-add.new-issue")))
    new_issue_button = driver.find_element(By.CSS_SELECTOR, "a.icon.icon-add.new-issue")
    new_issue_button.click()

    tracker_dropdown = Select(driver.find_element(By.ID, "issue_tracker_id"))
    tracker_dropdown.select_by_value("1")  # 1 是 Bug 的 tracker_id

    assignee_dropdown = Select(driver.find_element(By.ID, "issue_assigned_to_id"))
    for option in assignee_dropdown.options:
        if option.text == ASSIGNEE_NAME:
            assignee_id = option.get_attribute("value")
            break

    logging.info('Assignee ID: %s', assignee_id)
    driver.quit()
except Exception as e:
    logging.error('Error occurred during Selenium operations: %s', e)
    driver.quit()
    raise

try:
    for file_name in file_names:
        if file_name.endswith('.xlsx'):
            file_path = os.path.join(folder_path, file_name)

            # 讀取Excel文件
            df = pd.read_excel(file_path)

            # 提取資料並創建 Redmine Issue
            for index, row in df.iterrows():
                redmine_status = str(row['Column1.redmine.status']).strip().lower()
                if redmine_status in ['false', 'no', 'n', '0', '']:
                    logging.info('Skipping issue creation for %s due to redmine status: %s', row['Column1.issue.id'], redmine_status)
                    continue

                subject = row['Column1.issue.id']  # (Subject) 用於描述Redmine標題 和CVE編號。
                COMPONENT = row['Column1.name']  # (Component) 用於描述應用程式的組件或模組。
                CATEGORY = row['Column1.layer']  # (Category) 用於描述應用程式的類別或分類。
                VERSION = row['Column1.version']  # (Version) 用於描述應用程式的版本。
                Description = row['Column1.issue.summary']  # (Description) 用於描述CVE的說明。
                ATTACK_VECTOR = row['Column1.issue.vector']  #（Attack Vector）用於描述攻擊者如何接觸並利用漏洞。
                STATUS = row['Column1.issue.status']  # (Status) 用於描述CVE狀態。
                CVE_link = row['Column1.issue.link']  # (CVE Link) 用於描述CVE的連結，來源自NVD(National Vulnerability Database)。
                CVSS_v2 = row['Column1.issue.scorev2']  # (CVSS v2) 用於描述CVE的CVSS version 2 方式評分的分數。
                CVSS_v3 = row['Column1.issue.scorev3']  # (CVSS v3) 用於描述CVE透過CVSS version 3 方式評分的分數。

                issue = redmine.issue.create(
                    project_id=PROJECT_ID,
                    tracker_id=1,  # 1 是 Bug 的 tracker_id
                    subject=subject,
                    description=f'Subject: {subject}\nComponent: {COMPONENT}\nCategory: {CATEGORY}\nVersion: {VERSION}\nDescription: {Description}\nzip link: {zip_link_content}\nCVE Link: {CVE_link}\nCVSS v2: {CVSS_v2}\nCVSS v3: {CVSS_v3}\n',
                    assigned_to_id=assignee_id,
                    custom_fields=[
                        {'id': 6, 'value': version_id},
                        {'id': 54, 'value': SEVERITY_VALUE}
                    ]
                )
                logging.info('Created issue %s', issue.id)
                
except Exception as e:
    logging.error('Error occurred during issue creation: %s', e)
finally:
    logging.info('Finished creating issues.')
