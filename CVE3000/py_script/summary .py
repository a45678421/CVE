import os
import logging
import chardet
import pandas as pd
from openpyxl import Workbook

# 設置日誌文件路徑
log_file_path = '../loading/log.txt'

# 配置日誌記錄器
logging.basicConfig(
    level=logging.INFO,
    filename=log_file_path,
    filemode='w',
    format='[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    datefmt='%Y%m%d %H:%M:%S',
)

# 設置控制台處理器以顯示在終端
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s', datefmt='%Y%m%d %H:%M:%S')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logging.info(' Summary starting...')

# 創建 summary 目錄
if not os.path.exists('summary'):
    os.makedirs('summary')

# 讀取 feedback.txt 檔並檢測編碼
with open("feedback.txt", "rb") as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

# 讀取 feedback.txt 檔的內容
with open("feedback.txt", "r", encoding=encoding) as file:
    lines = file.readlines()

# 定義需要的變數
VERSION = ""
Redmine_Subject = ""
ASSIGNEE_NAME = ""
SEVERITY_VALUE = ""
zip_link_content = ""

# 提取需要的資料並定義成變數
for line in lines:
    line = line.strip()  # 移除頭尾空白和分行符號
    if line.startswith("VERSION"):
        Redmine_VERSION = line.split("=")[1].strip().strip('"')
    elif line.startswith("ASSIGNEE_NAME"):
        ASSIGNEE_NAME = line.split("=")[1].strip().strip('"')
    elif line.startswith("SEVERITY_VALUE"):
        SEVERITY_VALUE = line.split("=")[1].strip().strip('"')
        folder_path = SEVERITY_VALUE  # 將 SEVERITY_VALUE 的值賦值也給 folder_path

# 輸出提取的值
# print("Redmine_VERSION:", Redmine_VERSION)
logging.info('Redmine_VERSION: %s', Redmine_VERSION)
# print("ASSIGNEE_NAME:", ASSIGNEE_NAME)
logging.info('ASSIGNEE_NAME: %s', ASSIGNEE_NAME)
# print("SEVERITY_VALUE:", SEVERITY_VALUE)
logging.info('SEVERITY_VALUE: %s', SEVERITY_VALUE)
# print("folder_path:", folder_path)
logging.info('folder_path: %s', folder_path)

# 獲取 SEVERITY_VALUE 資料夾中所有 Excel 檔的檔案名
file_names = os.listdir(folder_path)

# 獲取當前指令檔所在目錄的路徑
current_directory = os.path.dirname(os.path.abspath(__file__))

# 讀取 zip_link.txt 檔並列印連結內容
zip_link_file = f"{SEVERITY_VALUE}_zip_link.txt"
zip_link_path = os.path.join(current_directory, zip_link_file)

if os.path.exists(zip_link_path):
    with open(zip_link_path, "r", encoding=encoding) as zip_link_file:
        zip_link_content = zip_link_file.read()
        # print("zip link:", zip_link_content)
        logging.info('zip link: %s', zip_link_content)
else:
    # print(f"文件 {zip_link_path} 不存在。")
    logging.info('文件 %s 不存在。', zip_link_path)

# 初始化一個 DataFrame 來存儲所有資料
columns = [
    'CVE_ID', 'COMPONENT', 'CATEGORY', 'VERSION', 'Description',
    'ATTACK_VECTOR', 'STATUS', 'Threat_level', 'CVSS_v2', 'CVSS_v3', 'CVE_link', 
    'Redmine_Subject', 'Redmine_VERSION', 'ASSIGNEE_NAME', 'SEVERITY_VALUE', 'zip_link_content', 'REDMINE_STATUS'
]
all_data = pd.DataFrame(columns=columns)

# 逐個處理 Excel 文件
for file_name in file_names:
    if file_name.endswith('.xlsx'):
        file_path = os.path.join(folder_path, file_name)
        # print(f"Process files: {file_path}")
        logging.info('Process files: %s', file_path)

        # 讀取 Excel 文件
        df = pd.read_excel(file_path)
        
        # 提取資料並添加到總 DataFrame 中
        for index, row in df.iterrows():
            data = {
                'CVE_ID': row['Column1.issue.id'],
                'COMPONENT': row['Column1.name'],
                'CATEGORY': row['Column1.layer'],
                'VERSION': row['Column1.version'],
                'Description': row['Column1.issue.summary'],
                'ATTACK_VECTOR': row['Column1.issue.vector'],
                'STATUS': row['Column1.issue.status'],
                'Threat_level' : folder_path,
                'CVSS_v2': row['Column1.issue.scorev2'],
                'CVSS_v3': row['Column1.issue.scorev3'],
                'CVE_link': row['Column1.issue.link'],
                'Redmine_Subject': row['Column1.issue.id'],
                'Redmine_VERSION': Redmine_VERSION,
                'ASSIGNEE_NAME': ASSIGNEE_NAME,
                'SEVERITY_VALUE': SEVERITY_VALUE,
                'zip_link_content': zip_link_content,
                'REDMINE_STATUS' : row['Column1.redmine.status']
            }
            all_data = pd.concat([all_data, pd.DataFrame([data])], ignore_index=True)
            
            COMPONENT = row['Column1.name'] # (Component) 用於描述應用程式的組件或模組。
            CATEGORY = row['Column1.layer'] # (Category) 用於描述應用程式的類別或分類。
            VERSION = row['Column1.version'] # (Version) 用於描述應用程式的版本。
            CVE_ID = row['Column1.issue.id'] # (CVE id) 用於描述漏洞的識別碼。
            Description = row['Column1.issue.summary'] # (Description) 用於描述CVE的說明。
            ATTACK_VECTOR = row['Column1.issue.vector'] #（Attack Vector）用於描述攻擊者如何接觸並利用漏洞。
            STATUS = row['Column1.issue.status'] # (Status) 用於描述CVE狀態。
            CVE_link = row['Column1.issue.link'] # (CVE Link) 用於描述CVE的連結，來源自NVD(National Vulnerability Database)。
            CVSS_v2 = row['Column1.issue.scorev2'] # (CVSS v2) 用於描述CVE的CVSS version 2 方式評分的分數。
            CVSS_v3 = row['Column1.issue.scorev3'] # (CVSS v3) 用於描述CVE透過CVSS version 3 方式評分的分數。
            REDMINE_STATUS = row['Column1.redmine.status']
            # print(f'COMPONENT: {COMPONENT}')
            # print(f'CATEGORY: {CATEGORY}')
            # print(f'VERSION: {VERSION}')
            # print(f'CVE_id: {CVE_ID}')
            # print(f'Description: {Description}')
            # print(f'ATTACK_VECTOR: {ATTACK_VECTOR}')
            # print(f'Status: {STATUS}')
            # print(f'CVE Link: {CVE_link}')
            # print(f'CVSS v2: {CVSS_v2}')
            # print(f'CVSS v3: {CVSS_v3}')
            # print(f'Redmine_subject: {CVE_ID}')
            # print("Redmine_VERSION:", Redmine_VERSION)
            # print("ASSIGNEE_NAME:", ASSIGNEE_NAME)
            # print("SEVERITY_VALUE:", SEVERITY_VALUE)
            # print("folder_path:", folder_path)
            # print('-------------------')

            logging.info('COMPONENT : %s', COMPONENT)
            logging.info('CATEGORY: %s', CATEGORY)
            logging.info('VERSION: %s', VERSION)
            logging.info('CVE_id: %s', CVE_ID)
            logging.info('Description: %s', Description)
            logging.info('ATTACK_VECTOR: %s', ATTACK_VECTOR)
            logging.info('Status: %s', STATUS)
            logging.info('CVE Link: %s', CVE_link)
            logging.info('CVSS v2: %s', CVSS_v2)
            logging.info('CVSS v3: %s', CVSS_v3)
            logging.info('Redmine_subject: %s', CVE_ID)
            logging.info('Redmine_VERSION: %s', Redmine_VERSION)
            logging.info('ASSIGNEE_NAME: %s', ASSIGNEE_NAME)
            logging.info('SEVERITY_VALUE: %s', SEVERITY_VALUE)
            logging.info('folder_path: %s', folder_path)
            logging.info('REDMINE_STATUS: %s', REDMINE_STATUS)
            logging.info('-------------------')

# 將總數據保存到新的 Excel 檔中
summary_file_path = os.path.join("summary", f"Remine_summary_for_{SEVERITY_VALUE}_Threat_level.xlsx")
all_data.to_excel(summary_file_path, index=False)

print(f"資料已匯總並保存到 {summary_file_path}")

logging.info(f"資料已匯總並保存到 {summary_file_path}")

