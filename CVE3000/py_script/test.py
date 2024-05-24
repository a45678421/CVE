import os
import chardet
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 定义需要的变量
USERNAME = "Sky.Ho"
PASSWORD = "@Dvan0912H"
Project = "SW::TPC-100W::Yocto4.0"

# 设置 WebDriver
driver = webdriver.Chrome()  # 确保你的环境变量 PATH 中包含 chromedriver

# 开启登入页面
driver.get("http://advrm.advantech.com:3006/login")

# 找到用户名输入框并输入用户名
username_input = driver.find_element(By.ID, "username")
username_input.send_keys(USERNAME)

# 找到密码输入框并输入密码
password_input = driver.find_element(By.ID, "password")
password_input.send_keys(PASSWORD)

# 提交表单（按下Enter）
password_input.send_keys(Keys.RETURN)

#############################################################################################################
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
project_link = project_list.find_element(By.CSS_SELECTOR, f"a[title='{Project}']")
project_link.click()

# 等待 issues 按钮加载并点击
issue_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "issues"))
)
issue_button.click()
###############################################################################################################
print("成功跳转到项目页面")

# 讓程式暫停等待使用者輸入
input("Press Enter to close the browser...")

# 关闭 WebDriver
driver.quit()
