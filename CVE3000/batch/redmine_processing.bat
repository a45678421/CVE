@echo on

cd ..
cd py_script

echo Step 9: Installing necessary packages...
python -u install_packages.py 

echo Step 10: Login and update feedback information...
python -u login_and_update_feedback.py 

echo Step 14: Checking and creating versions...
python -u check_and_create_version.py 

echo Step 16: Uploading zip file and getting zip file link...
python -u upload_zip_and_get_link.py 

echo Step 18: Creating issues...
python -u create_issue_api.py

echo All Redmine steps completed. 
pause

