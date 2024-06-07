import os
import logging
import chardet
import zipfile
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

logging.info('Compressing files...')

# 偵測 feedback.txt 檔案編碼
with open("feedback.txt", "rb") as file:
     raw_data = file.read()
     result = chardet.detect(raw_data)
     encoding = result['encoding']

logging.info('Detected encoding: : %s', encoding)
# print(f"偵測到的編碼：{encoding}")

# 用偵測到的編碼讀取 feedback.txt 文件
with open("feedback.txt", "r", encoding=encoding) as file:
     lines = file.readlines()

# 提取需要的資料並定義成變數
for line in lines:
     line = line.strip() # 移除頭尾空白和換行符
     if line.startswith("VERSION"):
         VERSION = line.split("=")[1].strip().strip('"')
     elif line.startswith("ASSIGNEE_NAME"):
         ASSIGNEE_NAME = line.split("=")[1].strip().strip('"')
     elif line.startswith("SEVERITY_VALUE"):
         SEVERITY_VALUE = line.split("=")[1].strip().strip('"')

# 輸出提取的值
logging.info('VERSION: %s', VERSION)
# print("VERSION:", VERSION)
logging.info('ASSIGNEE_NAME: %s', ASSIGNEE_NAME)
# print("ASSIGNEE_NAME:", ASSIGNEE_NAME)
logging.info('SEVERITY_VALUE: %s', SEVERITY_VALUE)
# print("SEVERITY_VALUE:", SEVERITY_VALUE)

# 建立 SEVERITY_VALUE_txt 資料夾
output_folder = f"{SEVERITY_VALUE}_txt"

# 設定 summary 資料夾路徑
summary_folder_path = "summary"

# 定義要壓縮的資料夾
folders_to_zip = [SEVERITY_VALUE, output_folder, summary_folder_path]

# 壓縮檔名
zip_file_name = f"{SEVERITY_VALUE}_archive.zip"

# 建立壓縮文件
with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
     for folder in folders_to_zip:
         if os.path.exists(folder):
             for root, dirs, files in os.walk(folder):
                 for file in files:
                     file_path = os.path.join(root, file)
                     arcname = os.path.relpath(file_path, os.path.join(folder, '..'))
                     zipf.write(file_path, arcname)
                 for dir in dirs:
                     dir_path = os.path.join(root, dir)
                     arcname = os.path.relpath(dir_path, os.path.join(folder, '..'))
                     zipf.write(dir_path, arcname)
         else:
             logging.info(f'資料夾 {folder} 不存在。')
             # print(f"資料夾 {folder} 不存在。")

logging.info(f'資料夾已壓縮為 {zip_file_name}')
# print(f"資料夾已壓縮為 {zip_file_name}")