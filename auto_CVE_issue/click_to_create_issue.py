import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 全域變數
#USERNAME = "Sky.Ho"
#PASSWORD = "@Dvan0912H"
#SUBJECT = "[TPC-100W]Auto Test To Create issue"
USERNAME = ""
PASSWORD = ""
ASSIGNEE_NAME = "YuCheng Lee 李育澄"
# VERSION_VALUE = "1822" # TPC-100W-4g-v2.0
VERSION_VALUE = ""
SEVERITY_VALUE = "Low"


# 讀取feedback.txt文件
with open("feedback.txt", "r") as file:
     lines = file.readlines()
# 從 output_zip_location.txt 檔案讀取檔案路徑
with open("output_zip_location.txt", "r") as file:
     file_path = file.readline().strip()

# 提取username、password和target_version的值
for line in lines:
     if "username:" in line and not "scanusername:" in line:
         USERNAME = line.split(":")[1].strip()
     elif "password:" in line and not "scanpassword:" in line:
         PASSWORD = line.split(":")[1].strip()
     elif "target_version:" in line:
         TARGET_VERSION = line.split(":")[1].strip()

# 輸出提取的值
print("USERNAME:", USERNAME)
print("PASSWORD:", PASSWORD)
print("TARGET_VERSION:", TARGET_VERSION)

# 讀 cve_numbers.txt
with open("cve_numbers.txt", "r") as file:
     for line in file:
         CVE_NUMBER = line.strip()

         # 從 CVE 檔案讀取描述內容
         description_files = glob.glob(f"{CVE_NUMBER}.txt")
         if description_files:
             with open(description_files[0], "r", encoding="utf-8") as desc_file:
                 DESCRIPTION = desc_file.read().strip()
         else:
             DESCRIPTION = f"No description available for {CVE_NUMBER}"

         # 啟動 Chrome 瀏覽器
         driver = webdriver.Chrome()

         # 開啟登入頁面
         driver.get("http://advrm.advantech.com:3006/login?back_url=http%3A%2F%2Fadvrm.advantech.com%3A3006%2Fprojects%2Ftpc-100w%2Fissues")

         # 找到使用者名稱輸入框並輸入使用者名稱
         username_input = driver.find_element(By.ID, "username")
         username_input.send_keys(USERNAME)

         # 找到密碼輸入框並輸入密碼
         password_input = driver.find_element(By.ID, "password")
         password_input.send_keys(PASSWORD)

         # 提交表單（按下回車鍵）
         password_input.send_keys(Keys.RETURN)

         # 找到 New issue 按鈕並點擊
         new_issue_button = driver.find_element(By.CSS_SELECTOR, "a.icon.icon-add.new-issue")
         new_issue_button.click()

         # 找到 Tracker 下拉選單並選擇 Bug
         tracker_dropdown = Select(driver.find_element(By.ID, "issue_tracker_id"))
         tracker_dropdown.select_by_value("1")

         # 填入 subject
         subject_input = driver.find_element(By.ID, "issue_subject")
         subject_input.send_keys(f"[TPC-100W]{CVE_NUMBER} - Auto Test To Create issue")

         # 填寫 issue description
         description_textarea = driver.find_element(By.ID, "issue_description")
         description_textarea.send_keys(DESCRIPTION)

         # 選擇 Assignee 為 Sky
         assignee_dropdown = Select(driver.find_element(By.ID, "issue_assigned_to_id"))
         assignee_dropdown.select_by_visible_text(ASSIGNEE_NAME)

         # 找到下拉式選單元素並建立 Select 對象
         version_dropdown = WebDriverWait(driver, 10).until(
         EC.presence_of_element_located((By.ID, "issue_custom_field_values_6"))
         )
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

         # 輸出字典內容
         print(options_dict)

         # 找到要選擇的項目的值
         target_option_text = "TPC-100W-4g-v2.5"
         target_option_value = options_dict.get(target_option_text)

         # 選擇下拉式選單中對應的項目
         version_select.select_by_value(target_option_value)

         # 選擇 Severity 為 Low
         severity_dropdown = Select(driver.find_element(By.ID, "issue_custom_field_values_54"))
         severity_dropdown.select_by_value(SEVERITY_VALUE)

         # 等待頁面載入完成
         wait = WebDriverWait(driver, 10)
         file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.file_selector.filedrop")))

        # 將檔案路徑傳送至 input 元素
         file_input.send_keys(file_path)
         
        # 等待最多 10 秒
         wait = WebDriverWait(driver, 10)

         # 找到 Create 按鈕並點擊
         # create_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create']")
         # create_button.click()

# 讓程序暫停等待使用者輸入
input("Press Enter to close the browser...")

# 關閉瀏覽器
# driver.quit()