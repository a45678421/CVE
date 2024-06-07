import os
import time
import logging
import chardet
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC

# 定義使用者名稱和密碼
#USERNAME = "Sky.Ho"
#PASSWORD = "@Dvan0912H"
#VERSION = "TPC-100W-4g-v2.5"
#ASSIGNEE_NAME = "Sky Ho 何國琳"
#SEVERITY_VALUE = "High"

# 設置日誌文件路徑
log_file_path = '../loading/log.txt'

# 配置日誌記錄器
logging.basicConfig(
    level=logging.INFO,
    filename=log_file_path,
    filemode='w',
    format='[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    datefmt='%Y%m%d %H:%M:%S',
)

# 設置控制台處理器以顯示在終端
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s', datefmt='%Y%m%d %H:%M:%S')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logging.info('Creating Redmine Issue...')

# 檢測檔案編碼
with open("feedback.txt", "rb") as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

# print(f"檢測到的編碼：{encoding}")
logging.info('Detected encoding: : %s', encoding)

with open("feedback.txt", "r", encoding=encoding) as file:
    lines = file.readlines()

# 定義需要的變數
USERNAME = ""
PASSWORD = ""
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
    elif line.startswith("PROJECT"):
        PROJECT = line.split("=")[1].strip().strip('"')
    elif line.startswith("VERSION"):
        REDMIND_VERSION = line.split("=")[1].strip().strip('"')
    elif line.startswith("ASSIGNEE_NAME"):
        ASSIGNEE_NAME = line.split("=")[1].strip().strip('"')
    elif line.startswith("SEVERITY_VALUE"):
        SEVERITY_VALUE = line.split("=")[1].strip().strip('"')
        folder_path = SEVERITY_VALUE  # 將 SEVERITY_VALUE 的值賦值也給 folder_path
    
# 輸出提取的值
logging.info('Extracted values:')
# print("USERNAME:", USERNAME)
logging.info('USERNAME: %s', USERNAME)
# print("PASSWORD:", PASSWORD)
logging.info('PASSWORD : %s', PASSWORD)
# print("PROJECT:", PROJECT)
logging.info('PROJECT : %s', PROJECT)
# print("REDMIND_VERSION:", REDMIND_VERSION)
logging.info('REDMIND_VERSION : %s', REDMIND_VERSION)
# print("ASSIGNEE_NAME:", ASSIGNEE_NAME)
logging.info('ASSIGNEE_NAME : %s', ASSIGNEE_NAME)
# print("SEVERITY_VALUE:", SEVERITY_VALUE)
logging.info('SEVERITY_VALUE : %s', SEVERITY_VALUE)
# print("folder_path:", folder_path)
logging.info('folder_path : %s', folder_path)

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
        # print("zip link:", zip_link_content)
        logging.info('zip link : %s', zip_link_content)
else:
    # print(f"文件 {zip_link_path} 不存在。")
    logging.info('File %s does not exist.', zip_link_path)

    # 嘗試啟動 Chrome 瀏覽器，如果沒有，就嘗試 Edge 瀏覽器
# 初始化 WebDriver
try:
    driver = webdriver.Chrome()
    logging.info('Using Chrome browser')
except Exception as e:
    logging.warning(f'Chrome browser not available: {e}. Falling back to Edge.')
    driver = webdriver.Edge()
    logging.info('Using Edge browser')

try:
    #driver.maximize_window()
    login_url = "http://advrm.advantech.com:3006/login"
    # 開啟登入頁面
    driver.get(login_url)

    # 找到使用者名稱輸入框並輸入使用者名
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(USERNAME)

    # 找到密碼輸入框並輸入密碼
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(PASSWORD)

    # 提交表單（按下Enter）
    password_input.send_keys(Keys.RETURN)

    logging.info('Logged in successfully')

    # 等待页面加载并显示项目跳转按钮
    project_jump = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "project-jump"))
        )
    project_jump.click()

    # 等待项目列表加载
    project_list = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.drdn-items.projects.selection"))
    )

    # 在项目列表中找到特定项目并点击
    project_link = project_list.find_element(By.CSS_SELECTOR, f"a[title='{PROJECT}']")
    project_link.click()

    # 等待 issues 按钮加载并点击
    issue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "issues"))
        )
    issue_button.click()

    # 逐個處理Excel文件
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
                
                subject = row['Column1.issue.id'] # (Subject) 用於描述Redmine標題 和CVE編號。
                COMPONENT = row['Column1.name'] # (Component) 用於描述應用程式的組件或模組。
                CATEGORY = row['Column1.layer'] # (Category) 用於描述應用程式的類別或分類。
                VERSION = row['Column1.version'] # (Version) 用於描述應用程式的版本。
                Description = row['Column1.issue.summary'] # (Description) 用於描述CVE的說明。
                ATTACK_VECTOR = row['Column1.issue.vector'] #（Attack Vector）用於描述攻擊者如何接觸並利用漏洞。
                STATUS = row['Column1.issue.status'] # (Status) 用於描述CVE狀態。
                CVE_link = row['Column1.issue.link'] # (CVE Link) 用於描述CVE的連結，來源自NVD(National Vulnerability Database)。
                CVSS_v2 = row['Column1.issue.scorev2'] # (CVSS v2) 用於描述CVE的CVSS version 2 方式評分的分數。
                CVSS_v3 = row['Column1.issue.scorev3'] # (CVSS v3) 用於描述CVE透過CVSS version 3 方式評分的分數。
###########################################################################################################

                # 等待頁面加載完畢
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.icon.icon-add.new-issue")))

                # 找到 New issue 按鈕並點擊
                new_issue_button = driver.find_element(By.CSS_SELECTOR, "a.icon.icon-add.new-issue")
                new_issue_button.click()

                # 找到 Tracker 下拉選單並選擇 Bug
                tracker_dropdown = Select(driver.find_element(By.ID, "issue_tracker_id"))
                tracker_dropdown.select_by_value("1")

                # 加入延遲以等待頁面完全加載
                time.sleep(2)

                # print(f'Subject: {subject}')
                logging.info('Subject : %s', subject)
                # print(f'Component: {COMPONENT}')
                logging.info('Component: %s', COMPONENT)
                # print(f'Category: {CATEGORY}')
                logging.info('Category: %s', CATEGORY)
                # print(f'Version: {VERSION}')
                logging.info('Version: %s', VERSION)
                # print(f'Description: {Description}')
                logging.info('Description: %s', Description)
                # print(f'ATTACK_VECTOR: {ATTACK_VECTOR}')
                logging.info('ATTACK_VECTOR: %s', ATTACK_VECTOR)
                # print(f'STATUS: {STATUS}')
                logging.info('STATUS: %s', STATUS)
                # print(f'CVE Link: {CVE_link}')
                logging.info('CVE Link: %s', CVE_link)
                # print(f'zip link: {zip_link_content}')
                logging.info('zip link: %s', zip_link_content)
                # print(f'CVSS v2: {CVSS_v2}')
                logging.info('CVSS v2: %s', CVSS_v2)
                # print(f'CVSS v3: {CVSS_v3}')
                logging.info('CVSS v3: %s', CVSS_v3)
                # print(f'-------------------')
                logging.info('-------------------')

                # 填入 subject
                subject_input = driver.find_element(By.ID, "issue_subject")
                subject_input.send_keys(subject)

                # 填寫 issue description
                description_textarea = driver.find_element(By.ID, "issue_description")
                description_textarea.send_keys(f'Subject: {subject}\nComponent: {COMPONENT}\nCategory: {CATEGORY}\nVersion: {VERSION}\nDescription: {Description}\nzip link: {zip_link_content}\nCVE Link: {CVE_link}\nCVSS v2: {CVSS_v2}\nCVSS v3: {CVSS_v3}\n')

                # 選擇 Assignee 為 Sky
                assignee_dropdown = Select(driver.find_element(By.ID, "issue_assigned_to_id"))
                assignee_dropdown.select_by_visible_text(ASSIGNEE_NAME)

                # 找到下拉式選單元素並建立 Select 對象
                version_dropdown = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.ID, "issue_custom_field_values_6")))
                version_select = Select(version_dropdown)

                # 取得所有選項
                options = version_select.options

                # 建立一個字典用來儲存名詞和對應的值
                options_dict = {}

                # 遍歷所有選項，將名詞和對應的值儲存到字典中
                for option in options:
                    option_text = option.text
                    option_value = option.get_attribute("value")
                    options_dict[option_text] = option_value

                # 找到要選擇的項目的值
                target_option_value = options_dict.get(REDMIND_VERSION)

                # 選擇下拉式選單中對應的項目
                version_select.select_by_value(target_option_value)

                # 選擇 Severity 
                severity_dropdown = Select(driver.find_element(By.ID, "issue_custom_field_values_54"))
                severity_dropdown.select_by_value(SEVERITY_VALUE)


                # 找到 Create 按鈕並點擊
                create_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create']")
                create_button.click()

                # 等待 issues 按钮加载并点击
                issue_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "issues"))
                )
                issue_button.click()

except Exception as e:
        # print("操作過程中發生錯誤:", e)
        logging.debug('操作過程中發生錯誤: %s', e)

finally:
        # 等待一段時間，以便檢查操作結果
        import time

        time.sleep(5)
        # 關閉瀏覽器
        driver.quit()


