import os
import logging
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from setup_logging import setup_logging
from detect_file_encoding import detect_file_encoding
from read_feedback_file import read_feedback_file
from init_webdriver import init_webdriver

def wait_for_progressbar_to_complete(driver, wait):
    try:
        wait.until(lambda driver: driver.find_element(By.CSS_SELECTOR, "div[role='progressbar']").get_attribute("aria-valuenow") == "100")
        logging.info('Progressbar reached 100%')
        icon_locator = (By.CSS_SELECTOR, "a.icon-only.icon-del.remove-upload")
        wait.until(EC.presence_of_element_located(icon_locator))
        logging.info('Icon for file deletion found')
    except WebDriverException as e:
        logging.error(f'Error waiting for progressbar to complete or icon to appear: {e}')
        raise

def upload_file(driver, wait, username, password, project, version, severity_value, file_path, encoding):
    # 開啟登入頁面
    driver.get("http://advrm.advantech.com:3006/projects/sw-tpc-100w-yocto4-0/issues")

    # 找到使用者名稱輸入框並輸入使用者名
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(username)

    # 找到密碼輸入框並輸入密碼
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(password)

    # 提交表單（按下回車鍵）
    password_input.send_keys(Keys.RETURN)

    ##############################################################################################################
    # 等待页面加载并显示项目跳转按钮
    project_jump = wait.until(
        EC.element_to_be_clickable((By.ID, "project-jump"))
    )
    project_jump.click()

    # 等待项目列表加载
    project_list = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.drdn-items.projects.selection"))
    )

    # 在项目列表中找到特定项目并点击
    project_link = project_list.find_element(By.CSS_SELECTOR, f"a[title='{project}']")
    project_link.click()

    ###############################################################################################################
    # 找到並點擊 "Files" 鏈接
    files_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='files']")))
    ActionChains(driver).move_to_element(files_link).click().perform()
    logging.info("已點擊 'Files' 連結")

    # 找到並點擊 "New file" 鏈接
    new_file_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='icon icon-add']")))
    ActionChains(driver).move_to_element(new_file_link).click().perform()
    logging.info("已點擊 'New file' 鏈接")

    # 找到下拉式選單元素並建立 Select 對象
    version_dropdown = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "version_id")))
    version_select = Select(version_dropdown)

    # 取得所有選項
    options = version_select.options

    # 建立一個字典用來儲存名詞和對應的值
    options_dict = {option.text: option.get_attribute("value") for option in options}

    # 找到要選擇的項目的值
    target_option_value = options_dict.get(version)

    # 檢查是否找到對應的版本選項
    if target_option_value:
        # 選擇下拉式選單中對應的項目
        version_select.select_by_value(target_option_value)
        logging.info('Selected version: %s (value: %s)', version, target_option_value)
    else:
        logging.info('Version not found: %s', version)

    # 等待頁面載入完成
    file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.file_selector.filedrop")))

    # 將檔案路徑傳送至 input 元素
    file_input.send_keys(file_path)

    # 等待進度條達到100%並檢查圖示
    wait_for_progressbar_to_complete(driver, wait)

    # 等待元素可點擊
    try:
        add_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Add']"))
        )
        # 模擬點擊操作
        add_button.click()
        logging.info('Add button clicked')
    except WebDriverException as e:
        logging.error(f'Failed to click the Add button: {e}')
        raise

    # 找到要點擊的元件，尋找包含指定 .zip 檔案名稱的所有鏈接
    try:
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, f"//td[@class='filename']/a[contains(text(), '{severity_value}_archive.zip')]")))
        
        # 取得最後一個連結並將其寫入到檔案中
        if elements:
            link = elements[-1].get_attribute('href')
            zip_link_file = f"{severity_value}_zip_link.txt"

            with open(zip_link_file, "w", encoding=encoding) as file:
                file.write(link)
        else:
            logging.error(f'No links found for {severity_value}_archive.zip')
    except WebDriverException as e:
        logging.error(f'Failed to find the zip link: {e}')
        raise

def main():
    # 設置日誌記錄器
    setup_logging()
    logging.info('Uploading zip ...')

    # 檢測文件編碼
    encoding = detect_file_encoding("feedback.txt")
    logging.info('Detected encoding: %s', encoding)

    # 讀取 feedback.txt 文件
    variables = read_feedback_file("feedback.txt", encoding)
    USERNAME = variables.get('USERNAME', '')
    PASSWORD = variables.get('PASSWORD', '')
    PROJECT = variables.get('PROJECT', '')
    VERSION = variables.get('VERSION', '')
    SEVERITY_VALUE = variables.get('SEVERITY_VALUE', '')

    logging.info('USERNAME: %s', USERNAME)
    logging.info('PASSWORD: %s', PASSWORD)
    logging.info('PROJECT: %s', PROJECT)
    logging.info('VERSION: %s', VERSION)
    logging.info('SEVERITY_VALUE: %s', SEVERITY_VALUE)

    # 取得目前執行檔的絕對路徑
    current_file_path = os.path.abspath(__file__)

    # 取得目前執行檔案所在目錄的路徑
    current_directory = os.path.dirname(current_file_path)

    # 建立新的檔案路徑
    file_name = f"{SEVERITY_VALUE}_archive.zip"
    file_path = os.path.join(current_directory, file_name)

    logging.info('File path: %s', file_path)

    # 初始化 WebDriver
    driver = init_webdriver()
    driver.maximize_window()
    wait = WebDriverWait(driver, 20)

    try:
        # 上傳文件
        upload_file(driver, wait, USERNAME, PASSWORD, PROJECT, VERSION, SEVERITY_VALUE, file_path, encoding)
    except Exception as e:
        logging.error('An error occurred during file upload: %s', e)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
