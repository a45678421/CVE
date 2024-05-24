# 打開文件進行讀取
with open('feedback.txt', 'r') as file:
    content = file.readlines()

# 提取Share Location後的值並加上\nmap_scan
share_locations = []
for line in content:
    if 'shareLocation:' in line:
        share_location = line.split('shareLocation: ')[1].strip()
        share_location_with_nmap_scan = share_location + '\\nmap_scan'
        share_locations.append(share_location_with_nmap_scan)

# 將修改後的值寫入到新文件
with open('CVE_address.txt', 'w') as file:
    for location in share_locations:
        file.write(location + '\n')