import pandas as pd
import glob
import os
import logging

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

logging.info('Extracting Excel data...')

# 檢查並創建必要的資料夾
folders_to_create = ['High', 'Medium', 'Low', 'summary']
for folder_name in folders_to_create:
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        logging.info(f'Created folder: {folder_name}')

# 查找上一層目錄中的 .xlsx 文件
xlsx_files = glob.glob('../Put_the_excel_file_here/*.xlsx')

# 如果找到匹配的文件，讀取第一個 .xlsx 文件的前num_rows行資料
num_rows = 15000
if xlsx_files:
    for xlsx_file_path in xlsx_files:
        df = pd.read_excel(xlsx_file_path, nrows=num_rows)
        logging.info(f'Read first {num_rows} rows from {xlsx_file_path}')
        logging.info(f'Columns in the file: {df.columns.tolist()}')
else:
    logging.error("No .xlsx files found in the parent directory")
    raise FileNotFoundError("No .xlsx files found in the parent directory")

# 抓取指定列的數據
selected_columns = ['Column1.name', 'Column1.layer', 'Column1.version', 'Column1.issue.id', 'Column1.issue.summary', 'Column1.issue.vector', 'Column1.issue.status', 'Column1.issue.scorev2', 'Column1.issue.scorev3', 'Column1.issue.link', 'Column1.redmine.status']

# 檢查是否所有的選擇列都存在
missing_columns = [col for col in selected_columns if col not in df.columns]
if missing_columns:
    logging.error(f'Missing columns: {missing_columns}')
    raise ValueError(f'Missing columns: {missing_columns}')

selected_data = df[selected_columns]

# 創建空的DataFrame來保存summary.xlsx中的資料
High_summary_df = pd.DataFrame()
medium_summary_df = pd.DataFrame()
low_summary_df = pd.DataFrame()

# 逐行保存資料到Excel檔和summary.xlsx
for index, row in selected_data.iterrows():
    issue_id = row['Column1.issue.id']
    filename = f'{issue_id}.xlsx'
    
    # 檢查scorev2和scorev3是否有一列大於等於7
    if row['Column1.issue.scorev2'] >= 7 or row['Column1.issue.scorev3'] >= 7:
        # 保存當前行資料到High資料夾
        row_df = pd.DataFrame([row])  # 創建包含當前行資料的DataFrame
        row_df.to_excel(os.path.join('High', filename), index=False)
        logging.info(f'Saved data to High/{filename}, scorev2 or scorev3 >= 7')
        
        # 將當前行資料添加到summary_df中
        High_summary_df = pd.concat([High_summary_df, row_df], ignore_index=True)
        logging.info(f'Appended data to High_summary.xlsx, scorev2 or scorev3 >= 7')
    elif 4 <= row['Column1.issue.scorev2'] <= 6.9 or 4 <= row['Column1.issue.scorev3'] <= 6.9:
        # 保存當前行資料到Medium資料夾
        row_df = pd.DataFrame([row])  # 創建包含當前行資料的DataFrame
        row_df.to_excel(os.path.join('Medium', filename), index=False)
        logging.info(f'Saved data to Medium/{filename}, 4 <= scorev2 or scorev3 <= 6.9')
        
        # 將當前行資料添加到medium_summary_df中
        medium_summary_df = pd.concat([medium_summary_df, row_df], ignore_index=True)
        logging.info(f'Appended data to Medium_summary.xlsx, 4 <= scorev2 or scorev3 <= 6.9')
    elif 0 <= row['Column1.issue.scorev2'] <= 3.9 or 0 <= row['Column1.issue.scorev3'] <= 3.9:
        # 保存當前行資料到Low資料夾
        row_df = pd.DataFrame([row])  # 創建包含當前行資料的DataFrame
        row_df.to_excel(os.path.join('Low', filename), index=False)
        logging.info(f'Saved data to Low/{filename}, 0 <= scorev2 or scorev3 <= 3.9')
        
        # 將當前行資料添加到low_summary_df中
        low_summary_df = pd.concat([low_summary_df, row_df], ignore_index=True)
        logging.info(f'Appended data to Low_summary.xlsx, 0 <= scorev2 or scorev3 <= 3.9')
    else:
        logging.info(f'Not saved, neither scorev2 nor scorev3 > 7 or 4 <= scorev2 or scorev3 <= 6.9 or 0 <= scorev2 or scorev3 <= 3.9')

# 將High_summary_df保存到summary.xlsx檔中（存儲在當前工作目錄）
High_summary_filename = 'High_summary.xlsx'
High_summary_df.to_excel(os.path.join('summary', High_summary_filename), index=False)
logging.info(f'Saved High summary data to {High_summary_filename}')

# 將medium_summary_df保存到medium_summary.xlsx檔中（存儲在當前工作目錄）
medium_summary_filename = 'Medium_summary.xlsx'
medium_summary_df.to_excel(os.path.join('summary', medium_summary_filename), index=False)
logging.info(f'Saved Medium summary data to {medium_summary_filename}')

# 將low_summary_df保存到low_summary.xlsx檔中（存儲在當前工作目錄）
low_summary_filename = 'Low_summary.xlsx'
low_summary_df.to_excel(os.path.join('summary', low_summary_filename), index=False)
logging.info(f'Saved Low summary data to {low_summary_filename}')
