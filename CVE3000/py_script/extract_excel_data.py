import pandas as pd
import glob
import os
import logging
from setup_logging import setup_logging

# 變數設置
NUM_ROWS = 15000

def create_folders(folders_to_create):
    # 檢查並創建必要的資料夾
    for folder_name in folders_to_create:
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
            logging.info(f'Created folder: {folder_name}')

def read_excel_files_from_directory(directory, num_rows):
    # 查找指定目錄中的 .xlsx 文件，並讀取前 num_rows 行數據
    xlsx_files = glob.glob(os.path.join(directory, '*.xlsx'))

    if xlsx_files:
        for xlsx_file_path in xlsx_files:
            df = pd.read_excel(xlsx_file_path, nrows=num_rows)
            logging.info(f'Read first {num_rows} rows from {xlsx_file_path}')
            logging.info(f'Columns in the file: {df.columns.tolist()}')
            return df
    else:
        logging.error("No .xlsx files found in the parent directory")
        raise FileNotFoundError("No .xlsx files found in the parent directory")

def check_missing_columns(df, selected_columns):
    # 檢查是否所有的選擇列都存在
    missing_columns = [col for col in selected_columns if col not in df.columns]
    if missing_columns:
        logging.error(f'Missing columns: {missing_columns}')
        raise ValueError(f'Missing columns: {missing_columns}')

def save_rows_to_excel(selected_data):
    # 將分數列轉換為數字類型，無法轉換的將變為 NaN
    selected_data['Column1.issue.scorev2'] = pd.to_numeric(selected_data['Column1.issue.scorev2'], errors='coerce')
    selected_data['Column1.issue.scorev3'] = pd.to_numeric(selected_data['Column1.issue.scorev3'], errors='coerce')

    # 逐行保存資料到 Excel 檔和 summary.xlsx
    High_summary_df = pd.DataFrame()
    medium_summary_df = pd.DataFrame()
    low_summary_df = pd.DataFrame()

    for index, row in selected_data.iterrows():
        issue_id = row['Column1.issue.id']
        filename = f'{issue_id}.xlsx'
        
        if (row['Column1.issue.scorev2'] >= 7 or row['Column1.issue.scorev3'] >= 7):
            row_df = pd.DataFrame([row])
            row_df.to_excel(os.path.join('High', filename), index=False)
            logging.info(f'Saved data to High/{filename}, scorev2 or scorev3 >= 7')
            High_summary_df = pd.concat([High_summary_df, row_df], ignore_index=True)
        elif (4 <= row['Column1.issue.scorev2'] <= 6.9 or 4 <= row['Column1.issue.scorev3'] <= 6.9):
            row_df = pd.DataFrame([row])
            row_df.to_excel(os.path.join('Medium', filename), index=False)
            logging.info(f'Saved data to Medium/{filename}, 4 <= scorev2 or scorev3 <= 6.9')
            medium_summary_df = pd.concat([medium_summary_df, row_df], ignore_index=True)
        elif (0 <= row['Column1.issue.scorev2'] <= 3.9 or 0 <= row['Column1.issue.scorev3'] <= 3.9):
            row_df = pd.DataFrame([row])
            row_df.to_excel(os.path.join('Low', filename), index=False)
            logging.info(f'Saved data to Low/{filename}, 0 <= scorev2 or scorev3 <= 3.9')
            low_summary_df = pd.concat([low_summary_df, row_df], ignore_index=True)
        else:
            logging.info(f'Not saved, neither scorev2 nor scorev3 >= 7 or 4 <= scorev2 or scorev3 <= 6.9 or 0 <= scorev2 or scorev3 <= 3.9')

    High_summary_filename = 'High_summary.xlsx'
    High_summary_df.to_excel(os.path.join('summary', High_summary_filename), index=False)
    logging.info(f'Saved High summary data to {High_summary_filename}')

    medium_summary_filename = 'Medium_summary.xlsx'
    medium_summary_df.to_excel(os.path.join('summary', medium_summary_filename), index=False)
    logging.info(f'Saved Medium summary data to {medium_summary_filename}')

    low_summary_filename = 'Low_summary.xlsx'
    low_summary_df.to_excel(os.path.join('summary', low_summary_filename), index=False)
    logging.info(f'Saved Low summary data to {low_summary_filename}')

def main():
    # 設置日誌記錄器
    setup_logging()
    logging.info('Extracting Excel data...')

    # 創建必要的資料夾
    folders_to_create = ['High', 'Medium', 'Low', 'summary']
    create_folders(folders_to_create)

    # 讀取指定目錄中的 .xlsx 文件
    df = read_excel_files_from_directory('../Put_the_excel_file_here', NUM_ROWS)

    # 檢查是否所有的選擇列都存在
    selected_columns = ['Column1.name', 'Column1.layer', 'Column1.version', 'Column1.issue.id', 'Column1.issue.summary', 'Column1.issue.vector', 'Column1.issue.status', 'Column1.issue.scorev2', 'Column1.issue.scorev3', 'Column1.issue.link', 'Column1.redmine.status']
    check_missing_columns(df, selected_columns)

    # 抓取指定列的數據
    selected_data = df[selected_columns]

    # 逐行保存資料到 Excel 檔和 summary.xlsx
    save_rows_to_excel(selected_data)

if __name__ == "__main__":
    # 調用主函數
    main()
