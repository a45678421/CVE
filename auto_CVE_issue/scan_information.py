# 讀取feedback.txt的內容
with open('feedback.txt', 'r') as file:
    feedback_data = file.readlines()

# 分析feedback.txt的內容
username = None
password = None
target_version = None
targetIpAddress = None
scanIpAddress = None
scanusername = None
scanpassword = None
shareLocation = None
for line in feedback_data:
    line = line.strip()
    if line.startswith('target_version:'):
        target_version = line.split(':')[1].strip()
    elif line.startswith('targetIpAddress:'):
        targetIpAddress = line.split(':')[1].strip()
    elif line.startswith('scanIPAddress:'):
        scanIpAddress = line.split(':')[1].strip()
    elif line.startswith('scanusername:'):
        scanusername = line.split(':')[1].strip()
    elif line.startswith('scanpassword:'):
        scanpassword = line.split(':')[1].strip()

# 寫入scan_info.txt
if scanIpAddress is not None and scanusername is not None and scanpassword is not None:
    scan_info_data = f'{scanIpAddress}\n{scanusername}\n{scanpassword}'
    with open('scan_info.txt', 'w') as scan_file:
        scan_file.write(scan_info_data)
