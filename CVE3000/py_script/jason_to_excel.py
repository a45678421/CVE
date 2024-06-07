import json
import logging
import chardet
import pandas as pd
import glob
import os

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


def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']


def json_to_excel(json_file_path, excel_file_path):
    # 偵測 JSON 檔案的編碼方式
    encoding = detect_encoding(json_file_path)
    logging.info('Detected encoding: : %s', encoding)
    
    # 讀取 JSON 檔案
    with open(json_file_path, 'r', encoding=encoding) as file:
        data = json.load(file)
    
    # 準備資料轉換
    rows = []
    for package in data.get('package', []):
        for issue in package.get('issue', []):
            row = {
                'Column1.name': package.get('name'),
                'Column1.layer': package.get('layer'),
                'Column1.version': package.get('version'),
                'Column1.issue.id': issue.get('id'),
                'Column1.issue.summary': issue.get('summary'),
                'Column1.issue.scorev2': issue.get('scorev2'),
                'Column1.issue.scorev3': issue.get('scorev3'),
                'Column1.issue.vector': issue.get('vector'),
                'Column1.issue.status': issue.get('status'),
                'Column1.issue.link': issue.get('link'),
            }
            rows.append(row)
            for key, value in row.items():
                logging.info(f"'{key}': '{value}'")
            logging.info('=============================================================')
    
    # 將資料轉換成 DataFrame
    df = pd.DataFrame(rows)
    
    # 將 DataFrame 儲存為 Excel 檔案
    df.to_excel(excel_file_path, index=False)

# 獲取當前執行檔的絕對路徑
current_file_path = os.path.abspath(__file__)

# 獲取當前執行檔的目錄
current_directory = os.path.dirname(current_file_path)

# 獲取當前執行檔目錄的上一層目錄
parent_directory = os.path.dirname(current_directory)

# 將目錄中所有 JSON 檔案轉換為 Excel
json_directory = os.path.join(parent_directory, 'Put_the_json_file_here')
json_files = glob.glob(os.path.join(json_directory, '*.json'))

if not json_files:
    logging.error("There is no json file in the Put_the_json_file_here folder")
    print("There is no json file in the Put_the_json_file_here folder")
else:
    output_directory = os.path.join(parent_directory, 'Put_the_excel_file_here')  # 存放 Excel 檔案的路徑

    for json_file_path in json_files:
        excel_file_name = os.path.splitext(os.path.basename(json_file_path))[0] + '.xlsx'
        excel_file_path = os.path.join(output_directory, excel_file_name)
        json_to_excel(json_file_path, excel_file_path)
        logging.info('Converted %s to %s', json_file_path, excel_file_path)
