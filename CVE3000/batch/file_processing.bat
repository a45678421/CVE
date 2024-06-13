@echo on

cd ..
cd py_script

echo Step 8: Moving feedback.txt file...
python -u move_feedback.py 

echo Step 9: Installing necessary packages...
python -u install_packages.py 

echo Step 11: Convert from json to .xlsx
python -u jason_to_excel.py

echo Step 12: Extracting data from Excel file...
python -u extract_excel_data.py 

echo Step 13: Extracting and saving data by txt...
python -u extract_and_save_data_txt.py 

echo Step 15: Compressing files...
python -u compress_files.py 

echo Step 17: summary generate excel file...
python -u summary.py 
 
pause

