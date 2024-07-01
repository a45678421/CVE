import os
import logging
import zipfile
from setup_logging import setup_logging
from read_feedback_file import read_feedback_file
from detect_file_encoding import detect_file_encoding

def main():
    # 設置日誌記錄器
    setup_logging()
    logging.info('Compressing files...')

    # 偵測文件編碼
    encoding = detect_file_encoding("feedback.txt")
    logging.info('Detected encoding: %s', encoding)

    # 讀取 feedback.txt 文件
    variables = read_feedback_file("feedback.txt", encoding)
    VERSION = variables.get('VERSION', '')
    ASSIGNEE_NAME = variables.get('ASSIGNEE_NAME', '')
    SEVERITY_VALUE = variables.get('SEVERITY_VALUE', '')

    logging.info('VERSION: %s', VERSION)
    logging.info('ASSIGNEE_NAME: %s', ASSIGNEE_NAME)
    logging.info('SEVERITY_VALUE: %s', SEVERITY_VALUE)

    # 建立 SEVERITY_VALUE_txt 資料夾
    output_folder = f"{SEVERITY_VALUE}_txt"

    # 設定 summary 資料夾路徑
    summary_folder_path = "summary"

    # 建立 SEVERITY_VALUE_classify_component 資料夾
    classify_component_folder = f"{SEVERITY_VALUE}_classify_component"

    # 定義要壓縮的資料夾
    folders_to_zip = [SEVERITY_VALUE, output_folder, summary_folder_path, classify_component_folder]

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
                        logging.info(f'Added {file_path} to zip archive as {arcname}')
                    for dir in dirs:
                        dir_path = os.path.join(root, dir)
                        arcname = os.path.relpath(dir_path, os.path.join(folder, '..'))
                        zipf.write(dir_path, arcname)
                        logging.info(f'Added directory {dir_path} to zip archive as {arcname}')
            else:
                logging.info(f'資料夾 {folder} 不存在。')

    logging.info(f'資料夾已壓縮為 {zip_file_name}')

if __name__ == "__main__":
    # 調用主函數
    main()
