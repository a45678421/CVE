from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time

# 啟動瀏覽器
driver = webdriver.Chrome()  # 這裡使用 Chrome 瀏覽器，需要安裝對應的 ChromeDriver

# 打開網頁
driver.get("file:///D:/%2306_Kali_Linux/auto_CVE_issue/index.html")

# 填寫表單
driver.find_element(By.ID, "username").send_keys("Sky.Ho")
driver.find_element(By.ID, "password").send_keys("@Dvan0912H")
driver.find_element(By.ID, "targetIpAddress").send_keys("172.17.8.105")
driver.find_element(By.ID, "scanIpAddress").send_keys("172.17.8.18")
driver.find_element(By.ID, "scanusername").send_keys("sky")
driver.find_element(By.ID, "scanpassword").send_keys("1234")
driver.find_element(By.ID, "shareLocation").send_keys("D:\\#06_Kali_Linux\\share")

# 選取下拉選單
target_version = Select(driver.find_element(By.ID, "target_version"))
target_version.select_by_visible_text("TPC-100W-4g-v2.5")



# 點擊 "同意" 選項
driver.find_element(By.ID, "setupYes").click()

# 等待下拉選單可見
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "scanMode")))

scanMode = Select(driver.find_element(By.ID, "scanMode"))
scanMode.select_by_value("2")  # 這裡選擇了 "nmap scan CVE" 的選項，值為 2


# 提交表單
# driver.find_element(By.ID, "submit_button_id").click()  # 填入實際的提交按鈕的 ID 或其他識別符號

# 等待一段時間，確保表單提交完成
time.sleep(5)

# 關閉瀏覽器
# driver.quit()

# 讓程式暫停等待使用者輸入
input("Press Enter to close the browser...")
