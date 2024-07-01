import os
import logging
import pandas as pd
from setup_logging import setup_logging
from read_feedback_file import read_feedback_file
from detect_file_encoding import detect_file_encoding

#處理 Excel 文件，提取並保存數據
def process_excel_file(severity_value, encoding, redmine_version, assignee_name):
    # 設置 summary 文件夾路徑
    summary_folder_path = "summary"

    # 建立檔案名稱
    file_name = f"{severity_value}_summary.xlsx"
    file_path = os.path.join(summary_folder_path, file_name)

    # 建立 SEVERITY_VALUE_txt 資料夾
    output_folder = f"{severity_value}_txt"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 檢查檔案是否存在
    if os.path.exists(file_path):
        # 讀取 Excel 文件
        df = pd.read_excel(file_path)

        # 提取資料並打印
        for index, row in df.iterrows():
            COMPONENT = row['Column1.name']
            CATEGORY = row['Column1.layer']
            VERSION = row['Column1.version']
            CVE_ID = row['Column1.issue.id']
            Description = row['Column1.issue.summary']
            ATTACK_VECTOR = row['Column1.issue.vector']
            STATUS = row['Column1.issue.status']
            CVE_link = row['Column1.issue.link']
            CVSS_v2 = row['Column1.issue.scorev2']
            CVSS_v3 = row['Column1.issue.scorev3']
            REDMINE_STATUS = row['Column1.redmine.upload']

            logging.info('Redmine_subject : %s', CVE_ID)
            logging.info('Redmine_VERSION: %s', redmine_version)
            logging.info('ASSIGNEE_NAME: %s', assignee_name)
            logging.info('SEVERITY_VALUE: %s', severity_value)
            logging.info('folder_path: %s', output_folder)
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
                output_file.write(f"Redmine_VERSION: {redmine_version}\n")
                output_file.write(f"ASSIGNEE_NAME: {assignee_name}\n")
                output_file.write(f"SEVERITY_VALUE: {severity_value}\n")
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
        logging.error(f"File {file_path} does not exist.")

def main():
    # 設置日誌記錄器
    setup_logging()
    logging.info('Saving Data to txt...')

    # 檢測文件編碼
    encoding = detect_file_encoding("feedback.txt")
    logging.info('Detected encoding: %s', encoding)

    # 讀取 feedback.txt 文件
    variables = read_feedback_file("feedback.txt", encoding)
    Redmine_VERSION = variables.get('VERSION', '')
    ASSIGNEE_NAME = variables.get('ASSIGNEE_NAME', '')
    SEVERITY_VALUE = variables.get('SEVERITY_VALUE', '')
    folder_path = SEVERITY_VALUE

    logging.info('VERSION: %s', Redmine_VERSION)
    logging.info('ASSIGNEE_NAME: %s', ASSIGNEE_NAME)
    logging.info('SEVERITY_VALUE: %s', SEVERITY_VALUE)
    logging.info('folder_path: %s', folder_path)

    # 處理 Excel 文件
    process_excel_file(SEVERITY_VALUE, encoding, Redmine_VERSION, ASSIGNEE_NAME)

if __name__ == "__main__":
    # 調用主函數
    main()
