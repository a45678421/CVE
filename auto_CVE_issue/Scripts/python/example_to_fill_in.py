from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

# 啟動瀏覽器
driver = webdriver.Chrome()  # 這裡使用 Chrome 瀏覽器，需要安裝對應的 ChromeDriver

try:
    # 打開網頁
    driver.get("file:///D:/%2323_TPC-100W-4g-v3.0/CVE_test/testtool/auto_CVE_issue/Web_Files/index.html")

    # 填寫表單
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys("Sky.Ho")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys("@Dvan0912H")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "targetIpAddress"))).send_keys("172.17.8.105")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "scanIpAddress"))).send_keys("172.17.8.18")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "scanusername"))).send_keys("sky")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "scanpassword"))).send_keys("1234")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "shareLocation"))).send_keys("D:\\#06_Kali_Linux\\share")

    # 選取 Assignee 下拉選單
    assignee = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Assignee"))))
    assignee.select_by_visible_text("Sky Ho 何國琳")

    # 選取 Severity 下拉選單
    severity = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Severity"))))
    severity.select_by_visible_text("High")

    # 選取 target_version 下拉選單
    target_version = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "target_version"))))
    target_version.select_by_visible_text("TPC-100W-4g-v2.5")

    # 點擊 "同意" 選項
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "setupYes"))).click()

    # 等待下拉選單可見
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "scanMode")))
    scanMode = Select(driver.find_element(By.ID, "scanMode"))
    scanMode.select_by_value("2")  # 這裡選擇了 "nmap scan CVE" 的選項，值為 2

    # 提交表單
    #driver.find_element(By.ID, "submit_button_id").click()

    # 等待一段時間，確保表單提交完成
    time.sleep(5)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # 讓程式暫停等待使用者輸入
    input("Press Enter to close the browser...")
    driver.quit()