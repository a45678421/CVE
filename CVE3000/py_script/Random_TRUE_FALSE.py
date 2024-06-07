import openpyxl
import glob
import random
import os
import logging

# 设置日志文件路径
log_file_path = '../loading/log.txt'

# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,
    filename=log_file_path,
    filemode='w',
    format='[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    datefmt='%Y%m%d %H:%M:%S',
)

# 设置控制台处理器以显示在终端
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s', datefmt='%Y%m%d %H:%M:%S')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logging.info('Processing Excel files...')

# 查找上一层目录中的 .xlsx 文件
xlsx_files = glob.glob('../Put_the_excel_file_here/*.xlsx')

if not xlsx_files:
    logging.error("No .xlsx files found in the specified directory.")
    raise FileNotFoundError("No .xlsx files found in the specified directory.")

# 打开找到的 .xlsx 文件
file_path = xlsx_files[0]  # 假设只处理找到的第一个文件
workbook = openpyxl.load_workbook(file_path)

# 选择要填充的工作表
sheet = workbook.active

# 找到 Column1.redmine.status 字段的列索引，如果不存在则创建该列
header = [cell.value for cell in sheet[1]]
if 'Column1.redmine.status' not in header:
    header.append('Column1.redmine.status')
    sheet.append(header)
    column_to_fill_index = header.index('Column1.redmine.status') + 1  # openpyxl 列索引从 1 开始
    logging.info('Column "Column1.redmine.status" created.')
else:
    column_to_fill_index = header.index('Column1.redmine.status') + 1

# 随机填充从第二行开始的所有单元格，假设第一行是标题
for row in range(2, sheet.max_row + 1):
    sheet.cell(row=row, column=column_to_fill_index, value=random.choice([True, False]))

# 保存更改
workbook.save(file_path)

logging.info(f'已随机填充文件 {file_path} 中的 Column1.redmine.status 字段。')
print(f'已随机填充文件 {file_path} 中的 Column1.redmine.status 字段。')
