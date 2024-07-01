import os
import pandas as pd
import logging
from tqdm import tqdm
import read_feedback_file
import setup_logging
import detect_file_encoding

def process_files(severity_value, input_folder_path, output_folder_path):
    # 初始化存儲分類數據的字典
    component_data = {}

    # 遍歷輸入文件夾中的所有Excel文件
    excel_files = [file_name for file_name in os.listdir(input_folder_path) if file_name.endswith('.xlsx')]
    for file_name in tqdm(excel_files, desc=f"處理{severity_value}文件中"):
        file_path = os.path.join(input_folder_path, file_name)

        # 讀取Excel文件
        df = pd.read_excel(file_path)

        # 確保 'Column1.redmine.upload' 列為字符串類型
        df['Column1.redmine.upload'] = df['Column1.redmine.upload'].astype(str)

        # 過濾出符合條件的行
        filtered_df = df[df['Column1.redmine.upload'].str.lower().isin(['true', 'yes', 'y', '1'])]

        # 遍歷過濾後的行，將數據分類到component_data字典中
        for index, row in filtered_df.iterrows():
            component = row['Column1.name']  # 獲取組件名稱
            if component not in component_data:
                component_data[component] = []

            issue_data = {
                'CVE_ID': row['Column1.issue.id'],
                'COMPONENT': row['Column1.name'],
                'CATEGORY': row['Column1.layer'],
                'VERSION': row['Column1.version'],
                'Description': row['Column1.issue.summary'],
                'ATTACK_VECTOR': row['Column1.issue.vector'],
                'STATUS': row['Column1.issue.status'],
                'CVE_link': row['Column1.issue.link'],
                'CVSS_v2': row['Column1.issue.scorev2'],
                'CVSS_v3': row['Column1.issue.scorev3'],
            }
            component_data[component].append(issue_data)

    # 將每個組件的分類數據保存到新的Excel文件中
    for component, data in tqdm(component_data.items(), desc=f"保存{severity_value}文件中"):
        component_df = pd.DataFrame(data)
        output_file_path = os.path.normpath(os.path.join(output_folder_path, f"{component}_cve_issues.xlsx"))
        component_df.to_excel(output_file_path, index=False)

def main():
    # 設置日誌記錄
    setup_logging.setup_logging()

    # 設定 feedback.txt 的相對路徑
    feedback_file_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'feedback.txt'))

    # 檢測文件編碼並讀取內容
    try:
        encoding = detect_file_encoding.detect_file_encoding(feedback_file_path)
        logging.info(f'檢測到的編碼: {encoding}')
        
        variables = read_feedback_file.read_feedback_file(feedback_file_path, encoding)
        SEVERITY_VALUE = variables.get('SEVERITY_VALUE', '')
    except FileNotFoundError:
        logging.error(f'文件未找到錯誤: [Errno 2] 沒有這樣的文件或目錄: {feedback_file_path}')
        encoding = None
        SEVERITY_VALUE = ''
    except Exception as e:
        logging.error(f'發生錯誤: {e}')
        encoding = None
        SEVERITY_VALUE = ''

    logging.info(f'SEVERITY_VALUE: {SEVERITY_VALUE}')

    severity_levels = ['High', 'Medium', 'Low']
    
    # 將 SEVERITY_VALUE 放到首位
    if SEVERITY_VALUE in severity_levels:
        severity_levels.remove(SEVERITY_VALUE)
        severity_levels.insert(0, SEVERITY_VALUE)
    
    # 設定當前目錄
    current_directory = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    
    for severity in severity_levels:
        input_folder_path = os.path.normpath(os.path.join(current_directory, f'./{severity}'))  # 根據 SEVERITY_VALUE 決定輸入文件夾路徑
        output_folder_path = os.path.normpath(os.path.join(current_directory, f'./{severity}_classify_component'))  # 輸出文件夾路徑
        os.makedirs(output_folder_path, exist_ok=True)  # 創建輸出文件夾
        logging.info(f'處理 {severity} 等級的輸入文件夾路徑: {input_folder_path}')
        logging.info(f'處理 {severity} 等級的輸出文件夾路徑: {output_folder_path}')
        
        process_files(severity, input_folder_path, output_folder_path)

    logging.info("所有分類數據已成功保存到新的Excel文件中。")

if __name__ == "__main__":
    main()
