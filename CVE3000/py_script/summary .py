import os
import logging
import pandas as pd
from setup_logging import setup_logging
from detect_file_encoding import detect_file_encoding
from read_feedback_file import read_feedback_file

#處理 Excel 文件，提取資料並添加到總 DataFrame 中
def process_excel_files(file_names, folder_path, redmine_version, assignee_name, severity_value, zip_link_content):
    columns = [
        'CVE_ID', 'COMPONENT', 'CATEGORY', 'VERSION', 'Description',
        'ATTACK_VECTOR', 'STATUS', 'Threat_level', 'CVSS_v2', 'CVSS_v3', 'CVE_link', 
        'Redmine_Subject', 'Redmine_VERSION', 'ASSIGNEE_NAME', 'SEVERITY_VALUE', 'zip_link_content', 'REDMINE_STATUS'
    ]
    all_data = pd.DataFrame(columns=columns)

    for file_name in file_names:
        if file_name.endswith('.xlsx'):
            file_path = os.path.join(folder_path, file_name)
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
                    'Threat_level': folder_path,
                    'CVSS_v2': row['Column1.issue.scorev2'],
                    'CVSS_v3': row['Column1.issue.scorev3'],
                    'CVE_link': row['Column1.issue.link'],
                    'Redmine_Subject': row['Column1.issue.id'],
                    'Redmine_VERSION': redmine_version,
                    'ASSIGNEE_NAME': assignee_name,
                    'SEVERITY_VALUE': severity_value,
                    'zip_link_content': zip_link_content,
                    'REDMINE_STATUS': row['Column1.redmine.upload']
                }
                all_data = pd.concat([all_data, pd.DataFrame([data])], ignore_index=True)
                
                logging.info('COMPONENT : %s', row['Column1.name'])
                logging.info('CATEGORY: %s', row['Column1.layer'])
                logging.info('VERSION: %s', row['Column1.version'])
                logging.info('CVE_id: %s', row['Column1.issue.id'])
                logging.info('Description: %s', row['Column1.issue.summary'])
                logging.info('ATTACK_VECTOR: %s', row['Column1.issue.vector'])
                logging.info('Status: %s', row['Column1.issue.status'])
                logging.info('CVE Link: %s', row['Column1.issue.link'])
                logging.info('CVSS v2: %s', row['Column1.issue.scorev2'])
                logging.info('CVSS v3: %s', row['Column1.issue.scorev3'])
                logging.info('Redmine_subject: %s', row['Column1.issue.id'])
                logging.info('Redmine_VERSION: %s', redmine_version)
                logging.info('ASSIGNEE_NAME: %s', assignee_name)
                logging.info('SEVERITY_VALUE: %s', severity_value)
                logging.info('folder_path: %s', folder_path)
                logging.info('REDMINE_STATUS: %s', row['Column1.redmine.upload'])
                logging.info('-------------------')

    return all_data

def main():
    # 設置日誌記錄器
    setup_logging()
    logging.info('Summary starting...')

    # 檢測文件編碼
    encoding = detect_file_encoding("feedback.txt")
    logging.info('Detected encoding: %s', encoding)

    # 讀取 feedback.txt 文件
    variables = read_feedback_file("feedback.txt", encoding)
    Redmine_VERSION = variables.get('VERSION', '')
    ASSIGNEE_NAME = variables.get('ASSIGNEE_NAME', '')
    SEVERITY_VALUE = variables.get('SEVERITY_VALUE', '')
    folder_path = SEVERITY_VALUE

    logging.info('Redmine_VERSION: %s', Redmine_VERSION)
    logging.info('ASSIGNEE_NAME: %s', ASSIGNEE_NAME)
    logging.info('SEVERITY_VALUE: %s', SEVERITY_VALUE)
    logging.info('folder_path: %s', folder_path)

    # 創建 summary 目錄
    if not os.path.exists('summary'):
        os.makedirs('summary')

    # 獲取 SEVERITY_VALUE 資料夾中所有 Excel 檔的檔案名
    file_names = os.listdir(folder_path)

    # 獲取當前指令檔所在目錄的路徑
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # 讀取 zip_link.txt 檔並列印連結內容
    zip_link_file = f"{SEVERITY_VALUE}_zip_link.txt"
    zip_link_path = os.path.join(current_directory, zip_link_file)

    zip_link_content = ""
    if os.path.exists(zip_link_path):
        with open(zip_link_path, "r", encoding=encoding) as zip_link_file:
            zip_link_content = zip_link_file.read()
            logging.info('zip link: %s', zip_link_content)
    else:
        logging.info('文件 %s 不存在。', zip_link_path)

    # 處理 Excel 文件並返回總數據 DataFrame
    all_data = process_excel_files(file_names, folder_path, Redmine_VERSION, ASSIGNEE_NAME, SEVERITY_VALUE, zip_link_content)

    # 將總數據保存到新的 Excel 檔中
    summary_file_path = os.path.join("summary", f"Remine_summary_for_{SEVERITY_VALUE}_Threat_level.xlsx")
    all_data.to_excel(summary_file_path, index=False)

    print(f"資料已匯總並保存到 {summary_file_path}")
    logging.info(f"資料已匯總並保存到 {summary_file_path}")

if __name__ == "__main__":
    main()
