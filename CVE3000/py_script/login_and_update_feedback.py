import os
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from redminelib import Redmine
from redminelib.exceptions import AuthError
from setup_logging import setup_logging
from detect_file_encoding import detect_file_encoding
from read_feedback_file import read_feedback_file
from init_webdriver import init_webdriver

def update_feedback_file(username, password, api_key, encoding):
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

def main():
    # 設置日誌記錄器
    setup_logging()
    logging.info('Verify Utility ...')

    # 檢測文件編碼
    encoding = detect_file_encoding("feedback.txt")
    logging.info('Detected encoding: %s', encoding)

    # 讀取 feedback.txt 文件
    variables = read_feedback_file("feedback.txt", encoding)
    USERNAME = variables.get('USERNAME', '')
    PASSWORD = variables.get('PASSWORD', '')
    API_KEY = variables.get('API_KEY', '')

    logging.info('Extracted values:')
    logging.info('USERNAME: %s', USERNAME)
    logging.info('PASSWORD: %s', PASSWORD)
    logging.info('API_KEY: %s', API_KEY)

    # 初始化 WebDriver
    driver = init_webdriver()

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
    update_feedback_file(USERNAME, PASSWORD, API_KEY, encoding)

    # 初始化 Redmine 並驗證 API Key
    if not validate_api_key("http://advrm.advantech.com:3006/", API_KEY):
        while True:
            API_KEY = get_api_key()
            if validate_api_key("http://advrm.advantech.com:3006/", API_KEY):
                update_feedback_file(USERNAME, PASSWORD, API_KEY, encoding)
                break

if __name__ == "__main__":
    main()
