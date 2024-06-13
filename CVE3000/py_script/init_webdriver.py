import logging
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

def init_webdriver():
    # 初始化 Selenium WebDriver，嘗試啟動 Chrome 瀏覽器，如果失敗則嘗試 Edge 瀏覽器
    try:
        driver = webdriver.Chrome()
    except WebDriverException:
        logging.info('Chrome not found, switching to Edge...')
        driver = webdriver.Edge()
    driver.maximize_window()
    return driver
