import os
import time
import logging
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from setup_logging import setup_logging
from detect_file_encoding import detect_file_encoding
from read_feedback_file import read_feedback_file
from init_webdriver import init_webdriver

def create_redmine_issue(driver, wait, username, password, project, redmine_version, assignee_name, severity_value, folder_path, zip_link_content):
    # 開啟登入頁面
    login_url = "http://advrm.advantech.com:3006/login"
    driver.get(login_url)

    # 找到使用者名稱輸入框並輸入使用者名
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(username)

    # 找到密碼輸入框並輸入密碼
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(password)

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
    project_link = project_list.find_element(By.CSS_SELECTOR, f"a[title='{project}']")
    project_link.click()

    # 等待 issues 按钮加载并点击
    issue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "issues"))
    )
    issue_button.click()

    # 獲取SEVERITY資料夾中所有Excel檔的檔案名
    file_names = os.listdir(folder_path)

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
                
                subject = row['Column1.issue.id']
                COMPONENT = row['Column1.name']
                CATEGORY = row['Column1.layer']
                VERSION = row['Column1.version']
                Description = row['Column1.issue.summary']
                ATTACK_VECTOR = row['Column1.issue.vector']
                STATUS = row['Column1.issue.status']
                CVE_link = row['Column1.issue.link']
                CVSS_v2 = row['Column1.issue.scorev2']
                CVSS_v3 = row['Column1.issue.scorev3']

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

                logging.info('Subject : %s', subject)
                logging.info('Component: %s', COMPONENT)
                logging.info('Category: %s', CATEGORY)
                logging.info('Version: %s', VERSION)
                logging.info('Description: %s', Description)
                logging.info('ATTACK_VECTOR: %s', ATTACK_VECTOR)
                logging.info('STATUS: %s', STATUS)
                logging.info('CVE Link: %s', CVE_link)
                logging.info('zip link: %s', zip_link_content)
                logging.info('CVSS v2: %s', CVSS_v2)
                logging.info('CVSS v3: %s', CVSS_v3)
                logging.info('-------------------')

                # 填入 subject
                subject_input = driver.find_element(By.ID, "issue_subject")
                subject_input.send_keys(subject)

                # 填寫 issue description
                description_textarea = driver.find_element(By.ID, "issue_description")
                description_textarea.send_keys(f'Subject: {subject}\nComponent: {COMPONENT}\nCategory: {CATEGORY}\nVersion: {VERSION}\nDescription: {Description}\nzip link: {zip_link_content}\nCVE Link: {CVE_link}\nCVSS v2: {CVSS_v2}\nCVSS v3: {CVSS_v3}\n')

                # 選擇 Assignee 為 Sky
                assignee_dropdown = Select(driver.find_element(By.ID, "issue_assigned_to_id"))
                assignee_dropdown.select_by_visible_text(assignee_name)

                # 找到下拉式選單元素並建立 Select 對象
                version_dropdown = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "issue_custom_field_values_6")))
                version_select = Select(version_dropdown)

                # 取得所有選項
                options = version_select.options

                # 建立一個字典用來儲存名詞和對應的值
                options_dict = {option.text: option.get_attribute("value") for option in options}

                # 找到要選擇的項目的值
                target_option_value = options_dict.get(redmine_version)

                # 選擇下拉式選單中對應的項目
                if target_option_value:
                    version_select.select_by_value(target_option_value)
                else:
                    logging.info('Redmine version not found: %s', redmine_version)

                # 選擇 Severity 
                severity_dropdown = Select(driver.find_element(By.ID, "issue_custom_field_values_54"))
                severity_dropdown.select_by_value(severity_value)

                # 找到 Create 按鈕並點擊
                create_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create']")
                create_button.click()

                # 等待 issues 按钮加载并点击
                issue_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "issues"))
                )
                issue_button.click()

def main():
    # 設置日誌記錄器
    setup_logging()
    logging.info('Creating Redmine Issue...')

    # 檢測文件編碼
    encoding = detect_file_encoding("feedback.txt")
    logging.info('Detected encoding: %s', encoding)

    # 讀取 feedback.txt 文件
    variables = read_feedback_file("feedback.txt", encoding)
    USERNAME = variables.get('USERNAME', '')
    PASSWORD = variables.get('PASSWORD', '')
    PROJECT = variables.get('PROJECT', '')
    REDMINE_VERSION = variables.get('VERSION', '')
    ASSIGNEE_NAME = variables.get('ASSIGNEE_NAME', '')
    SEVERITY_VALUE = variables.get('SEVERITY_VALUE', '')
    folder_path = SEVERITY_VALUE

    logging.info('USERNAME: %s', USERNAME)
    logging.info('PASSWORD: %s', PASSWORD)
    logging.info('PROJECT: %s', PROJECT)
    logging.info('REDMINE_VERSION: %s', REDMINE_VERSION)
    logging.info('ASSIGNEE_NAME: %s', ASSIGNEE_NAME)
    logging.info('SEVERITY_VALUE: %s', SEVERITY_VALUE)
    logging.info('folder_path: %s', folder_path)

    # 獲取當前指令檔所在目錄的路徑
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # 讀取 zip_link.txt 檔並列印連結內容
    zip_link_file = f"{SEVERITY_VALUE}_zip_link.txt"
    zip_link_path = os.path.join(current_directory, zip_link_file)
    zip_link_content = ""

    if os.path.exists(zip_link_path):
        with open(zip_link_path, "r", encoding=encoding) as zip_link_file:
            zip_link_content = zip_link_file.read()
            logging.info('zip link: %s', zip_link_content)
    else:
        logging.info('File %s does not exist.', zip_link_path)

    # 初始化 WebDriver
    driver = init_webdriver()
    wait = WebDriverWait(driver, 10)

    try:
        create_redmine_issue(driver, wait, USERNAME, PASSWORD, PROJECT, REDMINE_VERSION, ASSIGNEE_NAME, SEVERITY_VALUE, folder_path, zip_link_content)
    except Exception as e:
        logging.error('操作過程中發生錯誤: %s', e)
    finally:
        time.sleep(5)  # 等待一段時間，以便檢查操作結果
        driver.quit()

if __name__ == "__main__":
    main()
