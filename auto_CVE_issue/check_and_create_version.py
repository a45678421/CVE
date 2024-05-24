import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# 全域變數
#USERNAME = "Sky.Ho"
#PASSWORD = "@Dvan0912H"
#target_version = "TPC-100W-4g-v2.6"


# 全域變數
USERNAME = ""
PASSWORD = ""
TARGET_VERSION = ""

# 讀取feedback.txt文件
with open("feedback.txt", "r") as file:
     lines = file.readlines()

# 提取username、password和target_version的值
for line in lines:
     if "username:" in line and not "scanusername:" in line:
         USERNAME = line.split(":")[1].strip()
     elif "password:" in line and not "scanpassword:" in line:
         PASSWORD = line.split(":")[1].strip()
     elif "target_version:" in line:
         TARGET_VERSION = line.split(":")[1].strip()

# 輸出提取的值（可選）
print("USERNAME:", USERNAME)
print("PASSWORD:", PASSWORD)
print("TARGET_VERSION:", TARGET_VERSION)


# 目標網址
url = "http://advrm.advantech.com:3006/projects/tpc-100w/settings"

# 啟動 Chrome 瀏覽器
driver = webdriver.Chrome()

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
if TARGET_VERSION in version_names:
       print(f"Version {TARGET_VERSION} already exists.")
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
       version_name_input.send_keys(TARGET_VERSION)
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
       if TARGET_VERSION in [link.text.strip() for link in driver.find_elements(By.CSS_SELECTOR, ".name a")]:
           print(f"New version {TARGET_VERSION} created successfully.")
       else:
           print(f"Unable to create a new version, {TARGET_VERSION} already exists")


# 讓程序暫停等待使用者輸入
#input("Press Enter to close the browser...")

# 關閉瀏覽器
driver.quit()