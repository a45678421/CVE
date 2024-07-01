import os
import chardet
import logging

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

# 設定 source_folder 的路徑
source_folder = os.path.join(current_dir, '..', '..', 'Text_Files')
feedback_file_path = os.path.join(source_folder, 'feedback.txt')
cve_address_file_path = os.path.join(source_folder, 'CVE_address.txt')

# 打印文件位置
logger.info(f'Feedback file path: {feedback_file_path}')
logger.info(f'CVE address file path: {cve_address_file_path}')

# 偵測 feedback.txt 檔案編碼
with open(feedback_file_path, 'rb') as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

logger.info(f'Detected encoding: {encoding}')

# 打開文件進行讀取
with open(feedback_file_path, 'r', encoding=encoding) as file:
    content = file.readlines()

# 提取 Share Location 後的值並加上 \nmap_scan
share_locations = []
for line in content:
    if 'shareLocation:' in line:
        share_location = line.split('shareLocation: ')[1].strip()
        share_location_with_nmap_scan = share_location + '\\nmap_scan'
        share_locations.append(share_location_with_nmap_scan)

# 將修改後的值寫入到新文件
with open(cve_address_file_path, 'w', encoding=encoding) as file:
    for location in share_locations:
        file.write(location + '\n')

logger.info('Modified share locations written to CVE_address.txt')

# 打印 CVE_address.txt 內容
with open(cve_address_file_path, 'r', encoding=encoding) as file:
    cve_content = file.read()
    logger.info(f'CVE_address.txt content: {cve_content}')
