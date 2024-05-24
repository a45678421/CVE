import os
import logging
import chardet
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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

logging.info('uploading zip ...')

with open("feedback.txt", "rb") as file:
      raw_data = file.read()
      result = chardet.detect(raw_data)
      encoding = result['encoding']

# print(f"偵測到的編碼：{encoding}")
logging.info('Detected encoding: : %s', encoding)

with open("feedback.txt", "r", encoding=encoding) as file:
      lines = file.readlines()

# 定義所需的變數
USERNAME = ""
PASSWORD = ""
PROJECT = ""
VERSION = ""
SEVERITY_VALUE=""

# 提取需要的資料並定義成變數
for line in lines:
     line = line.strip() # 移除頭尾空白和換行符
     if line.startswith("USERNAME"):
         USERNAME = line.split("=")[1].strip().strip('"')
     elif line.startswith("PASSWORD"):
         PASSWORD = line.split("=")[1].strip().strip('"')
     elif line.startswith("PROJECT"):
        PROJECT = line.split("=")[1].strip().strip('"')
     elif line.startswith("VERSION"):
         VERSION = line.split("=")[1].strip().strip('"')
     elif line.startswith("SEVERITY_VALUE"):
          SEVERITY_VALUE = line.split("=")[1].strip().strip('"')

# 輸出提取的值
# print("USERNAME:", USERNAME)
logging.info('USERNAME: %s', USERNAME)
# print("PASSWORD:", PASSWORD)
logging.info('PASSWORD: %s', PASSWORD)
# print("PROJECT:", PROJECT)
logging.info('PROJECT: %s', PROJECT)
# print("VERSION:", VERSION)
logging.info('VERSION: %s', VERSION)
# print("SEVERITY_VALUE:", SEVERITY_VALUE)
logging.info('SEVERITY_VALUE: %s', SEVERITY_VALUE)

# 取得目前執行檔的絕對路徑
current_file_path = os.path.abspath(__file__)

# 取得目前執行檔案所在目錄的路徑
current_directory = os.path.dirname(current_file_path)

# 建立新的檔案路徑
file_name = (SEVERITY_VALUE+"_archive.zip")
file_path = os.path.join(current_directory, file_name)

# print("檔案路徑:", file_path)
logging.info('File path: : %s', file_path)

# 嘗試啟動 Chrome 瀏覽器，如果沒有，就嘗試 Edge 瀏覽器
try:
    driver = webdriver.Chrome()
except WebDriverException:
    # print("Chrome not found, switching to Edge...")
    logging.info('Chrome not found, switching to Edge...')
    driver = webdriver.Edge()
driver.maximize_window()

# 開啟登入頁面
driver.get("http://advrm.advantech.com:3006/projects/sw-tpc-100w-yocto4-0/issues")

# 找到使用者名稱輸入框並輸入使用者名
username_input = driver.find_element(By.ID, "username")
username_input.send_keys(USERNAME)

# 找到密碼輸入框並輸入密碼
password_input = driver.find_element(By.ID, "password")
password_input.send_keys(PASSWORD)

# 提交表單（按下回車鍵）
password_input.send_keys(Keys.RETURN)

##############################################################################################################
# 等待頁面載入完成
wait = WebDriverWait(driver, 10)

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

###############################################################################################################
# 找到並點擊 "Files" 鏈接
files_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='files']")))
ActionChains(driver).move_to_element(files_link).click().perform()
print("已點擊 'Files' 連結")

# 找到並點擊 "New file" 鏈接
new_file_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='icon icon-add']")))
ActionChains(driver).move_to_element(new_file_link).click().perform()
print("已點擊 'New file' 鏈接")

# 找到下拉式選單元素並建立 Select 對象
version_dropdown = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "version_id")))
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
target_option_value = options_dict.get(VERSION)

# 檢查是否找到對應的版本選項
if target_option_value:
     # 選擇下拉式選單中對應的項目
     version_select.select_by_value(target_option_value)
    #  print(f"選擇版本：{VERSION} (值：{target_option_value})")
     logging.info('Selected version: %s (value: %s)', VERSION, target_option_value)
else:
    #  print(f"未找到版本：{VERSION}")
     logging.info('Version not found: %s', VERSION)


  # 等待頁面載入完成
wait = WebDriverWait(driver, 30)
file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.file_selector.filedrop")))

# 將檔案路徑傳送至 input 元素
file_input.send_keys(file_path)


# 等待元素可點擊
wait = WebDriverWait(driver, 10) # 設定等待時間為10秒
add_button = wait.until(
     EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='commit'][value='Add']"))
)

# 模擬點擊操作
add_button.click()

# print("已點擊 'Add' 按鈕")
logging.info('Add button clicked')

# 找到要點擊的元件，尋找包含指定 .zip 檔案名稱的鏈接
element = wait.until(EC.presence_of_element_located((By.XPATH, f"//td[@class='filename']/a[contains(text(), '{SEVERITY_VALUE}_archive.zip')]")) )

# 取得連結並將其寫入到檔案中
link = element.get_attribute('href')
zip_link_file = f"{SEVERITY_VALUE}_zip_link.txt"

with open(zip_link_file, "w", encoding=encoding) as file:
     file.write(link)