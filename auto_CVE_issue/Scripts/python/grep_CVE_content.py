import requests
from bs4 import BeautifulSoup
import os
import time
import chardet
import logging
import sys

# 設置控制台編碼為 UTF-8
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# 設定 logging，將日志記錄到 ../../script.log 文件，同時顯示在控制台
current_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(current_dir, '..', '..', 'script.log')

# 創建logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 創建文件handler，確保使用UTF-8編碼
file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
file_handler.setLevel(logging.INFO)

# 創建控制台handler，確保使用UTF-8編碼
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# 設置日志格式
formatter = logging.Formatter('[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s', datefmt='%Y%m%d %H:%M:%S')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 添加handler到logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 設定 cve_numbers.txt 的路徑
cve_numbers_file_path = os.path.join(current_dir, '..', '..', 'Text_Files', 'cve_numbers.txt')
output_folder = os.path.join(current_dir, '..', '..', 'Text_Files')

# 偵測 cve_numbers.txt 檔案編碼
with open(cve_numbers_file_path, 'rb') as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

logger.info(f'Detected encoding for cve_numbers.txt: {encoding}')

# 讀取 cve_numbers.txt
with open(cve_numbers_file_path, 'r', encoding=encoding) as file:
    cve_numbers = file.readlines()

# 遍歷每個 CVE 編號
for cve_number in cve_numbers:
    # 移除空白符號和換行符
    cve_number = cve_number.strip()

    # 跳過以 PRION:CVE- 開頭的CVE編號
    if cve_number.startswith("PRION:CVE-"):
        continue  # 跳過這個CVE編號

    url = f"https://vulners.com/cve/{cve_number}"
    filename = os.path.join(output_folder, f"{cve_number}.txt")

    # 取得網頁內容
    response = requests.get(url)
    html_content = response.text

    # 解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    time.sleep(1)

    # 找到內容
    content_div = soup.find('div', class_='css-1ooohex-HTML-container-body')
    if content_div:
        content_paragraphs = content_div.find_all('p')
        if content_paragraphs:
            content = '\n'.join(paragraph.text.strip() for paragraph in content_paragraphs)
        else:
            content = f"No Content Found for {cve_number}"
            logger.error(content)
    else:
        content = f"No Content Found for {cve_number}"
        logger.error(content)

    # 建立並寫入.txt檔案
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"CVE URL:\n{url}\nhttps://www.prio-n.com/kb/vulnerability/{cve_number}\n\n")
        logger.info(f"CVE URL: {url}")
        file.write(f"Description:\n{content}")
        logger.info(f"Description: {content}")

    # 記錄到日誌
    if "No Content Found" in content:
        logger.error(f"File saved as: {filename}")
    else:
        logger.info(f"File saved as: {filename}")
