import zipfile
import os

def zip_files(source_dir, output_zip):
     with zipfile.ZipFile(output_zip, 'w') as zipf:
         for root, dirs, files in os.walk(source_dir):
             for file in files:
                 zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(source_dir, '..')))

# 從 CVE_address.txt 檔案讀取來源目錄位置
with open('CVE_address.txt', 'r') as f:
     source_dir = f.readline().strip()

# 設定輸出壓縮檔案的位置，與來源目錄位置相同
output_zip = os.path.join(os.path.dirname(source_dir), 'output_zipfile.zip')

zip_files(source_dir, output_zip)

# 打印輸出壓縮檔案的位置
print("壓縮檔案已建立:", output_zip)

# 將輸出壓縮檔案的位置儲存到文字檔案中
output_txt = 'output_zip_location.txt'
with open(output_txt, 'w') as f:
     f.write(output_zip)

print("輸出壓縮檔案的位置已儲存到:", output_txt)