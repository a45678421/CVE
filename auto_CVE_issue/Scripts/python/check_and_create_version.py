import os
import chardet
import logging
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 設定 logging，將日志記錄到 ../../script.log 文件，同時顯示在控制台
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, '..', '..', 'script.log')

# 創建logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 創建文件handler
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)

# 創建控制台handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 設置日志格式
formatter = logging.Formatter('[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s', datefmt='%Y%m%d %H:%M:%S')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 添加handler到logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 全域變數
USERNAME = ""
PASSWORD = ""
TARGET_VERSION = ""

# 設定 feedback.txt 的路徑
feedback_file_path = os.path.join(script_dir, '..', '..', 'Text_Files', 'feedback.txt')

# 偵測 feedback.txt 檔案編碼
with open(feedback_file_path, "rb") as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

logger.info('Detected encoding: %s', encoding)

# 讀取 feedback.txt 文件
with open(feedback_file_path, "r", encoding=encoding) as file:
    lines = file.readlines()

# 提取 username、password 和 target_version 的值
for line in lines:
    if "username:" in line and not "scanusername:" in line:
        USERNAME = line.split(":")[1].strip()
    elif "password:" in line and not "scanpassword:" in line:
        PASSWORD = line.split(":")[1].strip()
    elif "target_version:" in line:
        TARGET_VERSION = line.split(":")[1].strip()

# 輸出提取的值（可選）
logger.info("USERNAME: %s", USERNAME)
logger.info("PASSWORD: %s", PASSWORD)
logger.info("TARGET_VERSION: %s", TARGET_VERSION)

# 目標網址
url = "http://advrm.advantech.com:3006/projects/tpc-100w/settings"

# 啟動 Chrome 瀏覽器
driver = webdriver.Chrome()

try:
    # 開啟登入頁面
    driver.get(url)

    # 找到使用者名稱輸入框並輸入使用者名稱
    username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    username_input.send_keys(USERNAME)

    # 找到密碼輸入框並輸入密碼
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(PASSWORD)

    # 提交表單（按下回車鍵）
    password_input.send_keys(Keys.RETURN)

    # 找到版本按鈕並點擊
    versions_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "tab-versions")))
    versions_button.click()

    # 等待頁面載入完成
    WebDriverWait(driver, 10).until(EC.url_contains("/versions"))

    # 取得頁面原始碼
    page_source = driver.page_source

    # 使用 BeautifulSoup 解析 HTML 頁面
    soup = BeautifulSoup(page_source, "html.parser")

    # 找到所有版本名稱
    version_names = [link.text.strip() for link in driver.find_elements(By.CSS_SELECTOR, ".name a")]

    # 檢查是否存在特定版本
    if TARGET_VERSION in version_names:
        logger.info(f"Version {TARGET_VERSION} already exists.")
    else:
        # 找到「Roadmap」連結並點擊
        roadmap_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "roadmap")))
        roadmap_link.click()

        # 等待頁面載入完成
        WebDriverWait(driver, 10).until(EC.url_contains("/roadmap"))

        # 找到「New issue」連結並點擊
        new_issue_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "icon-add")))
        new_issue_link.click()

        # 等待新版本頁面載入完成
        WebDriverWait(driver, 20).until(EC.url_contains("/versions/new"))

        # 輸入新版本名稱並提交
        version_name_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "version_name")))
        version_name_input.send_keys(TARGET_VERSION)
        version_name_input.send_keys(Keys.RETURN)

        # 再次檢查是否成功建立新版本
        driver.get(url)
        versions_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "tab-versions")))
        versions_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/versions"))

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        version_names = [link.text.strip() for link in driver.find_elements(By.CSS_SELECTOR, ".name a")]

        if TARGET_VERSION in version_names:
            logger.info(f"New version {TARGET_VERSION} created successfully.")
        else:
            logger.info(f"Unable to create a new version, {TARGET_VERSION} already exists.")
finally:
    # 關閉瀏覽器
    driver.quit()
