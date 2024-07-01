import zipfile
import os
import chardet
import logging
from datetime import datetime

# 設定 logging，將日志記錄到 ../../script.log 文件，同時顯示在控制台
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, '..', '..', 'script.log')

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

def zip_files(source_dir, output_zip):
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(source_dir, '..')))
    logger.info(f'Zipped files from {source_dir} to {output_zip}')

# 設定 CVE_address.txt 的路徑
cve_address_file_path = os.path.join(script_dir, '..', '..', 'Text_Files', 'CVE_address.txt')

# 偵測 CVE_address.txt 檔案編碼
with open(cve_address_file_path, "rb") as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

logger.info(f'Detected encoding: {encoding}')

# 從 CVE_address.txt 檔案讀取來源目錄位置
with open(cve_address_file_path, "r", encoding=encoding) as f:
    source_dir = f.readline().strip()

# 生成壓縮檔案名
current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
zip_file_name = f'{current_time}_nmap_scan_result.zip'

# 設定 Zip_Files 目錄和輸出壓縮檔案的位置
zip_files_dir = os.path.join(script_dir, '..', '..', 'Zip_Files')
if not os.path.exists(zip_files_dir):
    os.makedirs(zip_files_dir)

output_zip = os.path.join(zip_files_dir, zip_file_name)

# 執行壓縮文件
zip_files(source_dir, output_zip)

# 打印輸出壓縮檔案的位置
logger.info(f'Compressed file has been created: {output_zip}')

# 將輸出壓縮檔案的位置儲存到當前腳本位子的 ../../Text_Files 目錄中
output_txt = os.path.join(script_dir, '..', '..', 'Text_Files', 'output_zip_location.txt')
with open(output_txt, 'w') as f:
    f.write(output_zip)

logger.info(f'The location of the output compressed file has been saved to: {output_txt}')
