import glob
import os
import chardet
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 設定 logging，將日志記錄到 ../../script.log 文件，同時顯示在控制台
current_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(current_dir, '..', '..', 'script.log')

# 創建logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 創建文件handler
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)

# 創建控制台handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 設置日志格式
formatter = logging.Formatter('[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s', datefmt='%Y%m%d %H:%M:%S')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 添加handler到logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 全域變數
USERNAME = ""
PASSWORD = ""
ASSIGNEE_NAME = ""
TARGET_VERSION = ""

# 設定文件路徑
source_folder = os.path.join(current_dir, '..', '..', 'Text_Files')
feedback_file_path = os.path.join(source_folder, 'feedback.txt')
output_zip_location_file_path = os.path.join(source_folder, 'output_zip_location.txt')
cve_numbers_file_path = os.path.join(source_folder, 'cve_numbers.txt')

# 使用 chardet 檢測檔案編碼並讀取文件內容
def read_file_with_chardet(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']

    with open(file_path, 'r', encoding=encoding) as file:
        return file.readlines()

# 讀取 feedback.txt 文件
lines = read_file_with_chardet(feedback_file_path)

# 從 output_zip_location.txt 檔案讀取檔案路徑
file_path = read_file_with_chardet(output_zip_location_file_path)[0].strip()

# 確保文件路徑是規範路徑
file_path = os.path.abspath(file_path)
file_path = os.path.normpath(file_path)
logger.info(f"File path: {file_path}")

# 提取 username、password 和 target_version 的值
for line in lines:
    if "username:" in line and not "scanusername:" in line:
        USERNAME = line.split(":")[1].strip()
    elif "password:" in line and not "scanpassword:" in line:
        PASSWORD = line.split(":")[1].strip()
    elif "target_version:" in line:
        TARGET_VERSION = line.split(":")[1].strip()
    elif "Assignee:" in line:
        ASSIGNEE_NAME = line.split(":")[1].strip()

# 輸出提取的值
logger.info(f"USERNAME: {USERNAME}")
logger.info(f"PASSWORD: {PASSWORD}")
logger.info(f"TARGET_VERSION: {TARGET_VERSION}")
logger.info(f"ASSIGNEE_NAME: {ASSIGNEE_NAME}")

# 讀取 cve_numbers.txt
cve_numbers = read_file_with_chardet(cve_numbers_file_path)

# 遍歷每個 CVE 編號
for cve_number in cve_numbers:
    CVE_NUMBER = cve_number.strip()

    logger.info(f"Processing {CVE_NUMBER}")

    # 判斷是否為 PRION:CVE-XXXX-XXXXX
    if CVE_NUMBER.startswith("PRION:CVE-"):
        logger.info(f"Skipping {CVE_NUMBER} as it starts with PRION")
        continue  # 跳過這個CVE編號

    description_file_name = CVE_NUMBER
    logger.info(f"Description file name: {description_file_name}")

    # 從 CVE 檔案讀取描述內容
    description_files = glob.glob(os.path.join(source_folder, f"{description_file_name}.txt"))
    if description_files:
        description_lines = read_file_with_chardet(description_files[0])
        DESCRIPTION = ''.join(description_lines).strip()
        logger.info(f"Description for {CVE_NUMBER}: {DESCRIPTION}")
    else:
        DESCRIPTION = f"No description available for {CVE_NUMBER}"
        logger.error(DESCRIPTION)

    # 讀取 SEVERITY_VALUE
    severity_file_path = os.path.join(source_folder, f"{CVE_NUMBER}_severity.txt")
    if os.path.exists(severity_file_path):
        SEVERITY_VALUE = read_file_with_chardet(severity_file_path)[0].strip()
        logger.info(f"Severity for {CVE_NUMBER}: {SEVERITY_VALUE}")
    else:
        SEVERITY_VALUE = "Unknown"
        logger.error(f"Severity file not found for {CVE_NUMBER}")

    # 啟動 Chrome 瀏覽器
    driver = webdriver.Chrome()
    logger.info("Started Chrome browser")

    # 開啟登入頁面
    driver.get("http://advrm.advantech.com:3006/login?back_url=http%3A%2F%2Fadvrm.advantech.com%3A3006%2Fprojects%2Ftpc-100w%2Fissues")
    logger.info("Opened login page")

    # 找到使用者名稱輸入框並輸入使用者名稱
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(USERNAME)
    logger.info("Entered username")

    # 找到密碼輸入框並輸入密碼
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(PASSWORD)
    logger.info("Entered password")

    # 提交表單（按下回車鍵）
    password_input.send_keys(Keys.RETURN)
    logger.info("Submitted login form")

    # 找到 New issue 按鈕並點擊
    new_issue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.icon.icon-add.new-issue"))
    )
    new_issue_button.click()
    logger.info("Clicked on New issue button")

    # 找到 Tracker 下拉選單並選擇 Bug
    tracker_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "issue_tracker_id"))
    )
    Select(tracker_dropdown).select_by_value("1")
    logger.info("Selected Bug in Tracker dropdown")

    # 填入 subject
    subject_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "issue_subject"))
    )
    subject_input.send_keys(f"[TPC-100W]{CVE_NUMBER}")
    logger.info(f"Entered subject: [TPC-100W]{CVE_NUMBER}")

    # 填寫 issue description
    description_textarea = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "issue_description"))
    )
    full_description = f"{DESCRIPTION}\n\nSummary attachment : nmap_report.html"
    description_textarea.send_keys(full_description)
    logger.info("Entered issue description with summary attachment note")

    # 等待 Assignee 下拉選單加載並選擇 Assignee
    assignee_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "issue_assigned_to_id"))
    )
    Select(assignee_dropdown).select_by_visible_text(ASSIGNEE_NAME)
    logger.info(f"Selected Assignee: {ASSIGNEE_NAME}")

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
    logger.info(f"Options Dictionary: {options_dict}")

    # 找到要選擇的項目的值
    target_option_text = TARGET_VERSION
    target_option_value = options_dict.get(target_option_text)

    # 選擇下拉式選單中對應的項目
    version_select.select_by_value(target_option_value)
    logger.info(f"Selected Version: {target_option_text}")

    # 選擇 Severity 
    severity_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "issue_custom_field_values_54"))
    )
    Select(severity_dropdown).select_by_value(SEVERITY_VALUE)
    logger.info(f"Selected Severity: {SEVERITY_VALUE}")

    # 等待頁面載入完成
    file_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input.file_selector.filedrop"))
    )

    # 將檔案路徑傳送至 input 元素
    file_input.send_keys(file_path)
    logger.info(f"Uploaded file: {file_path}")

    # 將檔案路徑傳送至 input 元素
    normalized_file_path = os.path.abspath(file_path)
    normalized_html_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'nmap_report.html'))

    # 等待頁面載入完成，並找到文件上傳的input元素
    html_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input.file_selector.filedrop"))
    )

    # 將HTML檔案路徑傳送至 input 元素
    html_input.send_keys(normalized_html_path)
    logger.info(f"Uploaded HTML file: {normalized_html_path}") 

    # 等待最多 10 秒
    wait = WebDriverWait(driver, 10)

    # 找到 Create 按鈕並點擊
    # create_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create']")
    # create_button.click()
    # logger.info("Clicked on Create button")

# 讓程序暫停等待使用者輸入
#logger.info("Waiting for user input...")
#input("Press Enter to close the browser...")

# 關閉瀏覽器
driver.quit()
logger.info("Closed Chrome browser")
logger.info("Done!")
