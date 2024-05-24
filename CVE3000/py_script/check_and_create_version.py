import os
import logging
import requests
import chardet
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# 全域變數
#USERNAME = "Sky.Ho"
#PASSWORD = "@Dvan0912H"
#target_version = "TPC-100W-4g-v2.6"

# 全域變數
USERNAME = ""
PASSWORD = ""
PROJECT = ""
VERSION = ""

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

logging.info('Checking and creating version directories...')

# 偵測 feedback.txt 檔案編碼
with open("feedback.txt", "rb") as file:
     raw_data = file.read()
     result = chardet.detect(raw_data)
     encoding = result['encoding']

logging.info('Detected encoding: : %s', encoding)
#print(f"偵測到的編碼：{encoding}")

# 用偵測到的編碼讀取 feedback.txt 文件
with open("feedback.txt", "r", encoding=encoding) as file:
     lines = file.readlines()

# 提取需要的資料並定義成變數
for line in lines:
    if "USERNAME" in line:
        USERNAME = line.split("=")[1].strip().strip('"')
    elif "PASSWORD" in line:
        PASSWORD = line.split("=")[1].strip().strip('"')
    elif "PROJECT" in line:
        PROJECT = line.split("=")[1].strip().strip('"')
    elif "VERSION" in line:
        VERSION = line.split("=")[1].strip().strip('"')
    
# 輸出提取的值
logging.info('USERNAME: %s', USERNAME)
# print("USERNAME:", USERNAME)
logging.info('PASSWORD : %s', PASSWORD)
# print("PASSWORD:", PASSWORD)
logging.info('PROJECT : %s', PROJECT)
# print("PROJECT:", PROJECT)
logging.info('VERSION : %s', VERSION)
# print("VERSION:", VERSION)

# 目標網址
url = "http://advrm.advantech.com:3006/projects/tpc-100w/settings"

# 嘗試啟動 Chrome 瀏覽器，如果沒有，就嘗試 Edge 瀏覽器
try:
    driver = webdriver.Chrome()
except WebDriverException:
    logging.info('Chrome not found, switching to Edge...')
    # print("Chrome not found, switching to Edge...")
    driver = webdriver.Edge()

driver.maximize_window()

# 開啟登入頁面
driver.get(url)

# 找到使用者名稱輸入框並輸入使用者名稱
username_input = driver.find_element(By.ID, "username")
username_input.send_keys(USERNAME)

# 找到密碼輸入框並輸入密碼
password_input = driver.find_element(By.ID, "password")
password_input.send_keys(PASSWORD)

# 提交表單（按下回車鍵）
password_input.send_keys(Keys.RETURN)

##################################################################
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
setting_botton = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "settings"))
)
setting_botton.click()
##################################################################

# 找到版本按鈕並點擊
versions_button = driver.find_element(By.ID, "tab-versions")
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
if VERSION in version_names:
       logging.info(f"Version {VERSION} already exists.")
       # print(f"Version {VERSION} already exists.")
else:

       # 找到「Roadmap」連結並點擊
       roadmap_link = driver.find_element(By.CLASS_NAME, "roadmap")
       roadmap_link.click()

       # 等待頁面載入完成
       WebDriverWait(driver, 10).until(EC.url_contains("/roadmap"))

       # 找到「New_issue」連結並點擊
       new_issue_link = driver.find_element(By.CLASS_NAME, "icon-add")
       new_issue_link.click()

       # 等待新版本頁面載入完成
       WebDriverWait(driver, 20).until(EC.url_contains("/versions/new"))

       # 輸入新版本名稱並提交
       version_name_input = driver.find_element(By.ID, "version_name")
       version_name_input.send_keys(VERSION)
       version_name_input.submit()

       # 開啟登入頁面
       driver.get(url)

       # 找到版本按鈕並點擊
       versions_button = driver.find_element(By.ID, "tab-versions")
       versions_button.click()

       # 等待頁面載入完成
       WebDriverWait(driver, 10).until(EC.url_contains("/versions"))

       # 取得頁面原始碼
       page_source = driver.page_source

       # 使用 BeautifulSoup 解析 HTML 頁面
       soup = BeautifulSoup(page_source, "html.parser")

       # 找到所有版本名稱
       version_names = [link.text.strip() for link in driver.find_elements(By.CSS_SELECTOR, ".name a")]

       # 再次檢查是否成功建立新版本
       if VERSION in [link.text.strip() for link in driver.find_elements(By.CSS_SELECTOR, ".name a")]:
           logging.info(f'New version {VERSION} created successfully.')
           # print(f"New version {VERSION} created successfully.")
       else:
           logging.info(f'Unable to create a new version, {VERSION} already exists')
           # print(f"Unable to create a new version, {VERSION} already exists")

# 讓程式暫停等待使用者輸入
#input("Press Enter to close the browser...")

# 關閉瀏覽器
driver.quit()

