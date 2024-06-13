import os
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from detect_file_encoding import detect_file_encoding
from read_feedback_file import read_feedback_file
from setup_logging import setup_logging
from init_webdriver import init_webdriver

def login(driver, url, username, password):
    # 使用指定的使用者名稱和密碼登錄到指定的 URL
    driver.get(url)
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(username)
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

def navigate_to_project(driver, project_name):
    # 導航到指定的專案
    project_jump = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "project-jump"))
    )
    project_jump.click()
    project_list = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.drdn-items.projects.selection"))
    )
    project_link = project_list.find_element(By.CSS_SELECTOR, f"a[title='{project_name}']")
    project_link.click()
    setting_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "settings"))
    )
    setting_button.click()

def click_settings(driver):
    # 點擊 "Settings" 按鈕
    settings_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.settings"))
    )
    settings_button.click()

def check_and_create_version(driver, version):
    # 檢查是否存在特定版本，如果不存在則創建它
    versions_button = driver.find_element(By.ID, "tab-versions")
    versions_button.click()
    WebDriverWait(driver, 10).until(EC.url_contains("/versions"))

    # 調試信息：打印當前頁面URL和HTML
    logging.info('Current URL: %s', driver.current_url)
    #logging.info('Page HTML: %s', driver.page_source)

    version_names = [link.text.strip() for link in driver.find_elements(By.CSS_SELECTOR, ".name a")]

    if version in version_names:
        logging.info(f"Version {version} already exists.")
    else:
        roadmap_link = driver.find_element(By.CLASS_NAME, "roadmap")
        roadmap_link.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/roadmap"))
        new_issue_link = driver.find_element(By.CLASS_NAME, "icon-add")
        new_issue_link.click()
        WebDriverWait(driver, 20).until(EC.url_contains("/versions/new"))
        version_name_input = driver.find_element(By.ID, "version_name")
        version_name_input.send_keys(version)
        version_name_input.submit()

        click_settings(driver)
        # 等待頁面加載完成後重新檢查版本
        versions_button = driver.find_element(By.ID, "tab-versions")
        versions_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/versions"))
        version_names = [link.text.strip() for link in driver.find_elements(By.CSS_SELECTOR, ".name a")]
        if version in version_names:
            logging.info(f'New version {version} created successfully.')
        else:
            logging.info(f'Unable to create a new version, {version} already exists')

def main():
    # 主函數，負責執行主要邏輯
    setup_logging()
    logging.info('Checking and creating version directories...')

    # 偵測文件編碼
    encoding = detect_file_encoding("feedback.txt")
    logging.info('Detected encoding: %s', encoding)

    # 讀取 feedback.txt 文件
    variables = read_feedback_file("feedback.txt", encoding)
    USERNAME = variables.get('USERNAME', '')
    PASSWORD = variables.get('PASSWORD', '')
    PROJECT = variables.get('PROJECT', '')
    VERSION = variables.get('VERSION', '')

    logging.info('USERNAME: %s', USERNAME)
    logging.info('PASSWORD: %s', PASSWORD)
    logging.info('PROJECT: %s', PROJECT)
    logging.info('VERSION: %s', VERSION)

    # 目標網址
    url = "http://advrm.advantech.com:3006/projects/tpc-100w/settings"

    # 初始化 WebDriver
    driver = init_webdriver()

    try:
        # 登錄
        login(driver, url, USERNAME, PASSWORD)
        # 導航到專案
        navigate_to_project(driver, PROJECT)
        # 檢查並創建版本
        check_and_create_version(driver, VERSION)
    finally:
        # 關閉瀏覽器
        driver.quit()

if __name__ == "__main__":
    # 調用主函數
    main()
