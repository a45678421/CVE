import os
import logging
import chardet

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
scan_info_file_path = os.path.join(source_folder, 'scan_info.txt')

# 正規化文件位置
feedback_file_path = os.path.normpath(feedback_file_path)
scan_info_file_path = os.path.normpath(scan_info_file_path)

# 打印文件位置
logger.info(f'Feedback file path: {feedback_file_path}')
logger.info(f'Scan info file path: {scan_info_file_path}')

# 偵測 feedback.txt 檔案編碼
with open(feedback_file_path, 'rb') as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

logger.info(f'Detected encoding for feedback.txt: {encoding}')

# 讀取 feedback.txt 的內容
with open(feedback_file_path, 'r', encoding=encoding) as file:
    feedback_data = file.readlines()

# 分析 feedback.txt 的內容
username = None
password = None
target_version = None
targetIpAddress = None
scanIpAddress = None
scanusername = None
scanpassword = None
shareLocation = None
for line in feedback_data:
    line = line.strip()
    if line.startswith('target_version:'):
        target_version = line.split(':')[1].strip()
    elif line.startswith('targetIpAddress:'):
        targetIpAddress = line.split(':')[1].strip()
    elif line.startswith('scanIpAddress:'):
        scanIpAddress = line.split(':')[1].strip()
    elif line.startswith('scanusername:'):
        scanusername = line.split(':')[1].strip()
    elif line.startswith('scanpassword:'):
        scanpassword = line.split(':')[1].strip()

# 寫入 scan_info.txt
if scanIpAddress is not None and scanusername is not None and scanpassword is not None:
    scan_info_data = f'{scanIpAddress}\n{scanusername}\n{scanpassword}'
    with open(scan_info_file_path, 'w', encoding=encoding) as scan_file:
        scan_file.write(scan_info_data)

# 打印 scan_info.txt 內容
logger.info('scan_info.txt content:')
with open(scan_info_file_path, 'r', encoding=encoding) as file:
    logger.info(file.read().strip())
