import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


# 嘗試啟動 Chrome 瀏覽器
try:
    driver = webdriver.Chrome()
except WebDriverException:
    print("Chrome not found, switching to Edge...")
    driver = webdriver.Edge()

# 打開網頁
driver.get("file:///C:/Users/sky.ho/Desktop/CVE3000/see_me_first/fill_me_first.html") #Please open fill_me_first.html first and then copy the link here

# 填寫表單
driver.find_element(By.ID, "username").send_keys("Sky.Ho")
driver.find_element(By.ID, "password").send_keys("@Dvan0912H")


# 選擇項目
project = Select(driver.find_element(By.ID, "project"))
project.select_by_visible_text("SW")

# 選擇項目
driver.find_element(By.ID, "project_name").send_keys("TPC-100W")

# 選擇版本
driver.find_element(By.ID, "project_version").send_keys("Yocto4.0")


# 選擇目標版本
target_version = Select(driver.find_element(By.ID, "target_version"))
target_version.select_by_visible_text("TPC-100W-4g-v2.5")

# 選擇受理人
assignee = Select(driver.find_element(By.ID, "Assignee"))
assignee.select_by_visible_text("Sky Ho 何國琳")

# 選擇嚴重程度
severity = driver.find_element(By.ID, "high")
severity.click()

# 提交表單
#driver.find_element(By.ID, "submit_button_id").click()

# 讓程序暫停等待使用者輸入
input("Press Enter to close the browser...")

# 關閉瀏覽器
# driver.quit()