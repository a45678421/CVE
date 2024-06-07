import os
import logging
import chardet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from redminelib import Redmine
from redminelib.exceptions import AuthError

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

def update_feedback_file(username, password, api_key):
    with open("feedback.txt", "r", encoding=encoding) as file:
        lines = file.readlines()
    
    with open("feedback.txt", "w", encoding=encoding) as file:
        for line in lines:
            if line.startswith("USERNAME"):
                file.write(f'USERNAME="{username}"\n')
            elif line.startswith("PASSWORD"):
                file.write(f'PASSWORD="{password}"\n')
            elif line.startswith("API_KEY"):
                file.write(f'API_KEY="{api_key}"\n')
            else:
                file.write(line)

def get_credentials():
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    return username, password

def get_api_key():
    api_key = input("Please enter your API Key: ")
    return api_key

with open("feedback.txt", "rb") as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

logging.info('Detected encoding: : %s', encoding)

with open("feedback.txt", "r", encoding=encoding) as file:
    lines = file.readlines()

# 定義所需的變數
USERNAME = ""
PASSWORD = ""
API_KEY = ""

# 提取需要的資料並定義成變數
for line in lines:
    line = line.strip() # 移除頭尾空白和換行符
    if line.startswith("USERNAME"):
        USERNAME = line.split("=")[1].strip().strip('"')
    elif line.startswith("PASSWORD"):
        PASSWORD = line.split("=")[1].strip().strip('"')
    elif line.startswith("API_KEY"):
        API_KEY = line.split("=")[1].strip().strip('"')

logging.info('Extracted values:')
logging.info('USERNAME: %s', USERNAME)
logging.info('PASSWORD: %s', PASSWORD)
logging.info('API_KEY: %s', API_KEY)

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
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "loggedas")))
        success = True
        print("登入成功")
    except:
        print("登錄失敗，請重新輸入使用者名稱和密碼")
        USERNAME, PASSWORD = get_credentials()

# 關閉瀏覽器
driver.quit()

# 更新 feedback.txt 文件
update_feedback_file(USERNAME, PASSWORD, API_KEY)

# 初始化 Redmine 並驗證 API Key
def validate_api_key(api_url, api_key):
    try:
        redmine = Redmine(api_url, key=api_key)
        user = redmine.user.get('current')
        logging.info('Authenticated as %s %s', user.firstname, user.lastname)
        return True
    except AuthError:
        logging.error('Invalid API Key. Please check your API Key.')
        return False
    except Exception as e:
        logging.error(f'An error occurred: {e}')
        return False

if not validate_api_key("http://advrm.advantech.com:3006/", API_KEY):
    while True:
        API_KEY = get_api_key()
        if validate_api_key("http://advrm.advantech.com:3006/", API_KEY):
            update_feedback_file(USERNAME, PASSWORD, API_KEY)
            break
