import os
import logging
import chardet
import pandas as pd

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

logging.info('Saving Data to txt...')

# 讀取檔案
with open("feedback.txt", "rb") as file:
      raw_data = file.read()
      result = chardet.detect(raw_data)
      encoding = result['encoding']

#print(f"偵測到的編碼：{encoding}")
logging.info('Detected encoding: : %s', encoding)

with open("feedback.txt", "r", encoding=encoding) as file:
      lines = file.readlines()

# 提取需要的資料並定義成變數
for line in lines:
      line = line.strip() # 移除頭尾空白和換行符
      if line.startswith("VERSION"):
          Redmine_VERSION = line.split("=")[1].strip().strip('"')
      elif line.startswith("ASSIGNEE_NAME"):
          ASSIGNEE_NAME = line.split("=")[1].strip().strip('"')
      elif line.startswith("SEVERITY_VALUE"):
          SEVERITY_VALUE = line.split("=")[1].strip().strip('"')
          folder_path = SEVERITY_VALUE # 將 SEVERITY_VALUE 的值賦值也給 folder_path

# 輸出提取的值
# print("VERSION:", Redmine_VERSION)
logging.info('VERSION: %s', Redmine_VERSION)
# print("ASSIGNEE_NAME:", ASSIGNEE_NAME)
logging.info('ASSIGNEE_NAME: %s', ASSIGNEE_NAME)
# print("SEVERITY_VALUE:", SEVERITY_VALUE)
logging.info('SEVERITY_VALUE: %s', SEVERITY_VALUE)
# print("folder_path:", folder_path)
logging.info('folder_path: %s', folder_path)

# 設置 summary 文件夾路徑
summary_folder_path = "summary"

# 建立檔案名稱
file_name = f"{SEVERITY_VALUE}_summary.xlsx"
file_path = os.path.join(summary_folder_path, file_name)

# 建立 SEVERITY_VALUE_txt 資料夾
output_folder = f"{SEVERITY_VALUE}_txt"
if not os.path.exists(output_folder):
      os.makedirs(output_folder)

# 檢查檔案是否存在
if os.path.exists(file_path):
      # 讀取 Excel 文件
      df = pd.read_excel(file_path)

      # 提取資料並打印
      for index, row in df.iterrows():
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
          REDMINE_STATUS = row['Column1.redmine.status'] # (Redmine Status) 用於描述Redmine create issue狀態。
          # 輸出提取的值
      #     print(f'Redmine_subject: {CVE_ID}')    
      #     print("Redmine_VERSION:", Redmine_VERSION) 
      #     print("ASSIGNEE_NAME:", ASSIGNEE_NAME)
      #     print("SEVERITY_VALUE:", SEVERITY_VALUE)
      #     print("folder_path:", folder_path)
      #     print(f'COMPONENT: {COMPONENT}')
      #     print(f'CATEGORY: {CATEGORY}')
      #     print(f'VERSION: {VERSION}')
      #     print(f'CVE_id: {CVE_ID}')
      #     print(f'Description: {Description}')
      #     print(f'ATTACK_VECTOR: {ATTACK_VECTOR}')
      #     print(f'Status: {STATUS}')
      #     print(f'CVE Link: {CVE_link}')
      #     print(f'CVSS v2: {CVSS_v2}')
      #     print(f'CVSS v3: {CVSS_v3}')
      #     print('-------------------')

          logging.info('Redmine_subject : %s', CVE_ID)
          logging.info('Redmine_VERSION: %s', Redmine_VERSION)
          logging.info('ASSIGNEE_NAME: %s', ASSIGNEE_NAME)
          logging.info('SEVERITY_VALUE: %s', SEVERITY_VALUE)
          logging.info('folder_path: %s', folder_path)
          logging.info('COMPONENT: %s', COMPONENT)
          logging.info('CATEGORY: %s', CATEGORY)
          logging.info('VERSION: %s', VERSION)
          logging.info('CVE_id: %s', CVE_ID)
          logging.info('Description: %s', Description)
          logging.info('ATTACK_VECTOR: %s', ATTACK_VECTOR)
          logging.info('Status: %s', STATUS)
          logging.info('CVE Link: %s', CVE_link)
          logging.info('CVSS v2: %s', CVSS_v2)
          logging.info('CVSS v3: %s', CVSS_v3)
          logging.info('REDMINE_STATUS: %s', REDMINE_STATUS)
          logging.info('-------------------')

          # 將輸出內容寫入文件
          output_file_path = os.path.join(output_folder, f"{CVE_ID}.txt")
          with open(output_file_path, "w", encoding=encoding) as output_file:
              output_file.write(f"Redmine_subject: {CVE_ID}\n")
              output_file.write(f"Redmine_VERSION: {Redmine_VERSION}\n")
              output_file.write(f"ASSIGNEE_NAME: {ASSIGNEE_NAME}\n")
              output_file.write(f"SEVERITY_VALUE: {SEVERITY_VALUE}\n")
              output_file.write(f"COMPONENT: {COMPONENT}\n")
              output_file.write(f"CATEGORY: {CATEGORY}\n")
              output_file.write(f"VERSION: {VERSION}\n")
              output_file.write(f"CVE_id: {CVE_ID}\n")
              output_file.write(f"Description: {Description}\n")
              output_file.write(f"ATTACK_VECTOR: {ATTACK_VECTOR}\n")
              output_file.write(f"Status: {STATUS}\n")
              output_file.write(f"CVE Link: {CVE_link}\n")
              output_file.write(f"CVSS v2: {CVSS_v2}\n")
              output_file.write(f"CVSS v3: {CVSS_v3}\n")
              output_file.write(f"REDMINE_STATUS: {REDMINE_STATUS}\n")
else:
      print(f"檔案 {file_path} 不存在。")