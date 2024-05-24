import os
import time
import logging
import chardet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC

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

logging.info('Verify Utility ...')

def update_feedback_file(username, password):
     with open("feedback.txt", "r", encoding=encoding) as file:
         lines = file.readlines()
    
     with open("feedback.txt", "w", encoding=encoding) as file:
         for line in lines:
             if line.startswith("USERNAME"):
                 file.write(f'USERNAME="{username}"\n')
             elif line.startswith("PASSWORD"):
                 file.write(f'PASSWORD="{password}"\n')
             else:
                 file.write(line)

def get_credentials():
     username = input("Please enter your username: ")
     password = input("Please enter your password: ")
     return username, password

with open("feedback.txt", "rb") as file:
     raw_data = file.read()
     result = chardet.detect(raw_data)
     encoding = result['encoding']

# print(f"檢測到的編碼：{encoding}")
logging.info('Detected encoding: : %s', encoding)

with open("feedback.txt", "r", encoding=encoding) as file:
     lines = file.readlines()

# 定義所需的變數
USERNAME = ""
PASSWORD = ""

# 提取需要的資料並定義成變數
for line in lines:
     line = line.strip() # 移除頭尾空白和換行符
     if line.startswith("USERNAME"):
         USERNAME = line.split("=")[1].strip().strip('"')
     elif line.startswith("PASSWORD"):
         PASSWORD = line.split("=")[1].strip().strip('"')
    
# 輸出提取的值
# print("USERNAME:", USERNAME)
logging.info('USERNAME: %s', USERNAME)
# print("PASSWORD:", PASSWORD)
logging.info('PASSWORD: %s', PASSWORD)

# 嘗試啟動 Chrome 瀏覽器，如果沒有，就嘗試 Edge 瀏覽器
try:
    driver = webdriver.Chrome()
except WebDriverException:
    print("Chrome not found, switching to Edge...")
    driver = webdriver.Edge()

success = False
while not success:
     # 開啟登入頁面
     driver.get("http://advrm.advantech.com:3006/projects/sw-tpc-100w-yocto4-0/issues")

     # 找到使用者名稱輸入框並輸入使用者名
     username_input = driver.find_element(By.ID, "username")
     username_input.clear()
     username_input.send_keys(USERNAME)

     # 找到密碼輸入框並輸入密碼
     password_input = driver.find_element(By.ID, "password")
     password_input.clear()
     password_input.send_keys(PASSWORD)

     # 提交表單（按下Enter）
     password_input.send_keys(Keys.RETURN)

     try:
         # 等待一段時間以確保登錄成功
         WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "loggedas")))
         success = True
         print("登入成功")
         update_feedback_file(USERNAME, PASSWORD)
     except:
         print("登錄失敗，請重新輸入使用者名稱和密碼")
         USERNAME, PASSWORD = get_credentials()