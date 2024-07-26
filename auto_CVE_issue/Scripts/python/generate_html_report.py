import re
import os
import chardet
import logging
from datetime import datetime

# 設定 logging，將日志記錄到 ../../script.log 文件，同時顯示在控制台
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, '..', '..', 'script.log')

# 創建logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 創建文件handler
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)

# 創建控制台handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 設置日志格式
formatter = logging.Formatter('[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s', datefmt='%Y%m%d %H:%M:%S')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 添加handler到logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def read_feedback_file(file_name):
    """
    讀取feedback文件以獲取共享目錄位置
    """
    if not os.path.exists(file_name):
        logger.error(f"文件未找到: {file_name}")
        raise FileNotFoundError(f"文件未找到: {file_name}")

    with open(file_name, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        logger.info(f"Detected encoding: {encoding}")
    with open(file_name, 'r', encoding=encoding) as file:
        feedback_output = file.read()
    match = re.search(r'shareLocation:\s*(.+)', feedback_output)
    logger.info(f"Found shareLocation: {match.group(1)}")
    if match:
        return match.group(1)
    elif 'shareLocation' in feedback_output:
        logger.error("未能在feedback文件中找到shareLocation")
        raise ValueError("未能在feedback文件中找到shareLocation")

def read_nmap_output(file_name):
    """
    讀取Nmap掃描結果
    """
    if not os.path.exists(file_name):
        logger.error(f"文件未找到: {file_name}")
        raise FileNotFoundError(f"文件未找到: {file_name}")

    with open(file_name, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
    with open(file_name, 'r', encoding=encoding) as file:
        nmap_output = file.read()
    return nmap_output

def parse_host_info(nmap_output):
    """
    解析主機信息
    """
    host_info_pattern = re.compile(r'Nmap scan report for (.+)\nHost is up \((.+) latency\).')
    host_info = host_info_pattern.search(nmap_output)
    if host_info:
        host = host_info.group(1)
        latency = host_info.group(2)
        return host, latency
    else:
        return None, None

def parse_mac_address(nmap_output):
    """
    解析MAC地址信息
    """
    mac_address_pattern = re.compile(r'MAC Address: ([0-9A-Fa-f:]+) \((.+)')
    mac_address_info = mac_address_pattern.search(nmap_output)
    if mac_address_info:
        mac_address = mac_address_info.group(1)
        mac_vendor = mac_address_info.group(2)
        return mac_address, mac_vendor
    else:
        return None, None

def parse_ports(nmap_output):
    """
    解析端口信息
    """
    port_info_pattern = re.compile(r'(\d+/tcp)\s+(\w+)\s+(\w+)\s*(.*)\n')
    ports_info = port_info_pattern.findall(nmap_output)
    
    valid_versions = ["open", "filtered", "closed"]  # 常見的端口狀態
    cleaned_ports_info = []

    for port, state, service, version in ports_info:
        if not version.strip() or any(state in version for state in valid_versions):
            version = "N/A"
        cleaned_ports_info.append((port, state, service, version))
    
    return cleaned_ports_info

def parse_cve_info(nmap_output):
    """
    解析CVE信息
    """
    cve_info_pattern = re.compile(r'\|_*\s+(CVE-\d{4}-\d{4,7})\s+(\d+\.\d)\s+(https://vulners.com/.*?)\s')
    cve_info = cve_info_pattern.findall(nmap_output)
    return cve_info

def get_severity(cvss_score):
    """
    根據CVSS評分分級漏洞嚴重性
    """
    score = float(cvss_score)
    if 0.1 <= score <= 3.9:
        return "Low"
    elif 4.0 <= score <= 6.9:
        return "Medium"
    elif 7.0 <= score <= 8.9:
        return "High"
    elif 9.0 <= score <= 10.0:
        return "Critical"
    else:
        return "Unknown"

def generate_html_report(nmap_output_file, template_file_name, original_file_name):
    """
    根據Nmap掃描結果和HTML模板生成報告
    """
    # 读取Nmap掃描結果
    nmap_output = read_nmap_output(nmap_output_file)

    # 讀取HTML模板
    with open(template_file_name, 'r', encoding='utf-8') as file:
        html_template = file.read()

    # 添加.ico圖標引用到模板
    icon_link = '<link rel="icon" type="image/x-icon" href="images/favicon_vulnerability.ico">'
    if '<head>' in html_template:
        html_template = html_template.replace('<head>', f'<head>\n    {icon_link}')
    else:
        logger.warning("未能找到<head>標籤，無法添加.ico圖標引用")

    # 解析掃描結果
    host, latency = parse_host_info(nmap_output)
    mac_address, mac_vendor = parse_mac_address(nmap_output)
    ports_info = parse_ports(nmap_output)
    cve_info = parse_cve_info(nmap_output)

    # 提取掃描命令
    scan_command_pattern = re.compile(r'# Nmap .+ as: (nmap .+)')
    scan_command_match = scan_command_pattern.search(nmap_output)
    if scan_command_match:
        scan_command = scan_command_match.group(1)
        logger.info(f"Scan command: {scan_command}")
    else:
        scan_command = "Unknown"
        logger.warning("Scan command not found in the Nmap output")

    # 記錄解析到的主機信息
    if host:
        logger.info(f"Host: {host}")
        logger.info(f"Latency: {latency}")
    else:
        logger.warning("未能解析到主機信息")

    # 記錄解析到的MAC地址信息
    if mac_address:
        logger.info(f"MAC Address: {mac_address}")
        logger.info(f"MAC Vendor: {mac_vendor}")
    else:
        logger.warning("未能解析到MAC地址信息")

    # 記錄解析到的端口信息
    logger.info("端口信息:")
    for port, state, service, version in ports_info:
        logger.info(f"Port: {port}, State: {state}, Service: {service}, Version: {version}")

    # 準備開放和關閉的HTML內容
    ports_html = "<h2>開放端口和服務</h2>"
    closed_ports_html = "<h2>關閉的端口</h2><ul>"

    open_ports = []
    closed_ports = []

    # 先找出所有包含'closed'的行
    closed_ports_pattern = re.compile(r'(\d+/tcp)\s+closed\s+(\w+-?\w+)')
    closed_ports_matches = closed_ports_pattern.findall(nmap_output)

    # 記錄找到的關閉端口行
    logger.info("找到的關閉端口行:")
    for match in closed_ports_matches:
        logger.info(f"Port: {match[0]}, Service: {match[1]}")
        closed_ports.append((match[0], match[1]))

    # 判斷端口是否開放或關閉
    for port, state, service, version in ports_info:
        if state == 'open':
            open_ports.append((port, service, version))

    # 記錄開放和關閉的端口
    logger.info("開放端口:")
    for port, service, version in open_ports:
        logger.info(f"Port: {port}, Service: {service}, Version: {version}")

    logger.info("關閉端口:")
    for port, service in closed_ports:
        logger.info(f"Port: {port}, Service: {service}")

    # 準備開放端口的HTML內容
    for port, service, version in open_ports:
        ports_html += f"<p><strong>{port} - {service}</strong></p>"
        if version != "N/A":
            ports_html += f"<p>服務版本: {version}</p>"

    # 準備關閉端口的HTML內容
    if closed_ports:
        for port, service in closed_ports:
            closed_ports_html += f"<li>{port} - {service} (closed)</li>"
        closed_ports_html += "</ul>"
    else:
        closed_ports_html = ""

    # 準備檢測到的漏洞的HTML內容
    vulnerabilities_html = "<h2>檢測到的漏洞和詳情</h2>"

    # 記錄解析到的CVE信息
    logger.info("CVE信息:")
    for cve_id, cvss, url in cve_info:
        severity = get_severity(cvss)
        logger.info(f"CVE ID: {cve_id}, CVSS: {cvss}, Severity: {severity}, URL: {url}")
        vulnerabilities_html += f"""
        <div class="vul-details">
            <p class="vul-title">{cve_id}</p>
            <p class="vul-info"><strong>CVSS評分:</strong> {cvss} ({severity})</p>
            <p class="vul-info"><strong>相關資源:</strong></p>
            <ul>
                <li><a href="{url}">Vulners</a></li>
                <li><a href="https://github.com/search?q={cve_id}">Github Exploits</a></li>
                <li><a href="https://www.seebug.org/search/?keywords={cve_id}">Seebug</a></li>
                <li><a href="https://packetstormsecurity.com/search/?q={cve_id}">Packetstorm</a></li>
                <li><a href="https://nvd.nist.gov/vuln/detail/{cve_id}">NVD</a></li>
            </ul>
        </div>
        """

    # 填充模板中的占位符
    html_content = html_template.format(
        host=host,
        latency=latency,
        mac_address=mac_address,
        mac_vendor=mac_vendor,
        ports_html=ports_html,
        vulnerabilities_html=vulnerabilities_html,
        closed_ports_html=closed_ports_html,
        scan_command=scan_command,
        original_file_name=original_file_name  # 添加原始文件名到模板
    )

    # 將最後的HTML內容寫入檔案
    output_file_name = os.path.join(os.path.dirname(nmap_output_file), f"{os.path.splitext(original_file_name)[0]}.html")
    with open(output_file_name, 'w', encoding='utf-8') as file:
        file.write(html_content)

    logger.info("HTML報告已生成：" + output_file_name)

if __name__ == '__main__':
    # 讀取共享目錄位置
    feedback_file = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../Text_Files/feedback.txt'))
    logger.info("feedback.txt 檔案位置：" + feedback_file)
    share_location = read_feedback_file(feedback_file)
    logger.info("共享目錄位置：" + share_location)
    nmap_directory = os.path.normpath(os.path.join(share_location, 'nmap_scan/CVE_scan_results'))
    logger.info("掃描結果目錄位置：" + nmap_directory)
    # 讀取HTML模板
    template_file = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../Web_Files/template.html'))
    logger.info("HTML模板檔案位置：" + template_file)

    for file_name in os.listdir(nmap_directory):
        if file_name.endswith('.txt'):
            nmap_output_file = os.path.join(nmap_directory, file_name)
            logger.info("處理檔案：" + nmap_output_file)
            generate_html_report(nmap_output_file, template_file, file_name)

