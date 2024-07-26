import os
import time
import logging
import pandas as pd
from redminelib import Redmine
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from read_feedback_file import read_feedback_file
from setup_logging import setup_logging
from detect_file_encoding import detect_file_encoding
from init_webdriver import init_webdriver

# Redmine 伺服器的 URL 和 API 金鑰
REDMINE_URL = 'http://advrm.advantech.com:3006/'

# 提取並返回 feedback.txt 文件中的變量
def extract_variables():
    encoding = detect_file_encoding("feedback.txt")
    logging.info('Detected encoding: %s', encoding)

    variables = read_feedback_file("feedback.txt", encoding)
    USERNAME = variables.get('USERNAME', '')
    PASSWORD = variables.get('PASSWORD', '')
    API_KEY = variables.get('API_KEY', '')
    PROJECT = variables.get('PROJECT', '')
    REDMINE_VERSION = variables.get('VERSION', '')
    ASSIGNEE_NAME = variables.get('ASSIGNEE_NAME', '')
    SEVERITY_VALUE = variables.get('SEVERITY_VALUE', '')

    logging.info('Extracted values:')
    logging.info('USERNAME: %s', USERNAME)
    logging.info('PASSWORD: %s', PASSWORD)
    logging.info('PROJECT: %s', PROJECT)
    logging.info('REDMINE_VERSION: %s', REDMINE_VERSION)
    logging.info('ASSIGNEE_NAME: %s', ASSIGNEE_NAME)
    logging.info('SEVERITY_VALUE: %s', SEVERITY_VALUE)

    return USERNAME, PASSWORD, API_KEY, PROJECT, REDMINE_VERSION, ASSIGNEE_NAME, SEVERITY_VALUE

# 讀取 zip_link.txt 文件並返回其內容
def get_zip_link_content(severity_value):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    zip_link_file = f"{severity_value}_zip_link.txt"
    zip_link_path = os.path.join(current_directory, zip_link_file)

    if os.path.exists(zip_link_path):
        encoding = detect_file_encoding(zip_link_path)
        with open(zip_link_path, "r", encoding=encoding) as file:
            zip_link_content = file.read()
            logging.info('zip link: %s', zip_link_content)
            return zip_link_content
    else:
        logging.info('File %s does not exist.', zip_link_path)
        return ""

# 獲取指定的 Redmine 項目和版本的 ID
def get_project_and_version(redmine, project_name, version_name):
    try:
        projects = redmine.project.all()
    except Exception as e:
        logging.error('Error fetching projects: %s', e)
        raise

    target_project = None

    logging.info('Available projects:')
    for project in projects:
        logging.info('Project: %s', project.name)
        if project.name.lower() == project_name.lower():
            target_project = project
            break

    if not target_project:
        logging.error('Project %s not found', project_name)
        raise ValueError(f'Project {project_name} not found')

    project_id = target_project.id
    logging.info('Target project ID: %s', project_id)

    version_id = None
    logging.info('Available versions in project %s:', target_project.name)
    try:
        for version in target_project.versions:
            logging.info('Version: %s', version.name)
            if version.name == version_name:
                version_id = version.id
                break
    except Exception as e:
        logging.error('Error fetching versions: %s', e)
        raise

    if version_id is None:
        logging.error('Version %s not found in project %s', version_name, project_name)
        raise ValueError(f'Version {version_name} not found in project {project_name}')

    logging.info('Target version ID: %s', version_id)

    return project_id, version_id

# 使用 Selenium 獲取指定分配對象的 ID
def get_assignee_id(driver, project_name, assignee_name, username, password):
    login_url = "http://advrm.advantech.com:3006/login"
    driver.get(login_url)

    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(username)

    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    logging.info('Logged in successfully')

    project_jump = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "project-jump"))
    )
    project_jump.click()

    project_list = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.drdn-items.projects.selection"))
    )

    project_link = project_list.find_element(By.CSS_SELECTOR, f"a[title='{project_name}']")
    project_link.click()

    issue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "issues"))
    )
    issue_button.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.icon.icon-add.new-issue")))
    new_issue_button = driver.find_element(By.CSS_SELECTOR, "a.icon.icon-add.new-issue")
    new_issue_button.click()

    tracker_dropdown = Select(driver.find_element(By.ID, "issue_tracker_id"))
    tracker_dropdown.select_by_value("1")

    assignee_dropdown = Select(driver.find_element(By.ID, "issue_assigned_to_id"))
    assignee_id = None
    for option in assignee_dropdown.options:
        if option.text == assignee_name:
            assignee_id = option.get_attribute("value")
            break

    logging.info('Assignee ID: %s', assignee_id)
    return assignee_id

# 讀取 Excel 文件並在 Redmine 中創建問題
def create_redmine_issues(redmine, project_id, version_id, assignee_id, severity_value, zip_link_content):
    folder_path = f"{severity_value}_classify_component"  # 修改資料夾路徑
    file_names = os.listdir(folder_path)

    for file_name in file_names:
        if file_name.endswith('.xlsx'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_excel(file_path)

            # 去掉文件名中的 .xlsx 後綴
            subject = file_name.rsplit('.xlsx', 1)[0]

            # 檢查 COMPONENT 列是否存在
            if 'COMPONENT' not in df.columns:
                logging.error('Column COMPONENT not found in %s', file_name)
                continue

            # 計算 CVE 數量
            cve_count = len(df)

            description_table = ""
            description_detail = ""

            # 按 COMPONENT 分组
            grouped = df.groupby('COMPONENT')

            for component, group in grouped:
                for index, row in group.iterrows():
                    COMPONENT = row.get('COMPONENT', 'N/A')
                    CATEGORY = row.get('CATEGORY', 'N/A')
                    VERSION = row.get('VERSION', 'N/A')
                    Description = row.get('Description', 'N/A')
                    ATTACK_VECTOR = row.get('ATTACK_VECTOR', 'N/A')
                    CVE_link = row.get('CVE_link', 'N/A')
                    CVSS_v2 = row.get('CVSS_v2', 'N/A')
                    CVSS_v3 = row.get('CVSS_v3', 'N/A')
                    CVE_ID = row.get("CVE_ID", "N/A")

                    description_table += f"|_. CVE ID | {CVE_ID}|\n"
                    description_table += f"|_. Component |{COMPONENT}|\n"
                    description_table += f"|_. Category|{CATEGORY}|\n"
                    description_table += f"|_. Version |{VERSION}|\n"
                    description_table += f"|_. zip link | {zip_link_content}|\n"
                    description_table += f"|_. CVE Link |{CVE_link}|\n"
                    description_table += f"|_. CVSS v2 |{CVSS_v2}|\n"
                    description_table += f"|_. CVSS v3| {CVSS_v3}|\n"
                    description_table += f"|_. Description | {Description} |\n\n"

            # 最終描述
            description = f"{COMPONENT} CVE Count: {cve_count}\n\n{description_table}"

            try:
                issue = redmine.issue.create(
                    project_id=project_id,
                    tracker_id=1,
                    subject=subject,
                    description=description,
                    assigned_to_id=assignee_id,
                    custom_fields=[
                        {'id': 6, 'value': version_id},
                        {'id': 54, 'value': severity_value}
                    ]
                )
                logging.info('Created issue %s', issue.id)
            except Exception as e:
                logging.error('Error creating issue for %s: %s', subject, e)

# 主函數保持不變
def main():
    # 設置日誌記錄器
    setup_logging()
    logging.info('Creating Redmine Issue...')

    # 提取變量
    USERNAME, PASSWORD, API_KEY, PROJECT, REDMINE_VERSION, ASSIGNEE_NAME, SEVERITY_VALUE = extract_variables()

    # 讀取 zip_link.txt 文件
    zip_link_content = get_zip_link_content(SEVERITY_VALUE)

    # 初始化 Redmine 連接
    try:
        redmine = Redmine(REDMINE_URL, key=API_KEY)
    except Exception as e:
        logging.error('Error connecting to Redmine: %s', e)
        raise

    # 獲取項目和版本 ID
    try:
        project_id, version_id = get_project_and_version(redmine, PROJECT, REDMINE_VERSION)
    except Exception as e:
        logging.error('Error fetching project or version: %s', e)
        raise

    # 初始化 WebDriver 並獲取分配對象 ID
    driver = init_webdriver()
    try:
        assignee_id = get_assignee_id(driver, PROJECT, ASSIGNEE_NAME, USERNAME, PASSWORD)
    except Exception as e:
        logging.error('Error occurred during Selenium operations: %s', e)
        driver.quit()
        raise

    driver.quit()

    # 創建 Redmine 問題
    try:
        create_redmine_issues(redmine, project_id, version_id, assignee_id, SEVERITY_VALUE, zip_link_content)
    except Exception as e:
        logging.error('Error occurred during issue creation: %s', e)
    finally:
        logging.info('Finished creating issues.')

if __name__ == "__main__":
    # 調用主函數
    main()
