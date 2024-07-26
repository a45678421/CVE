from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
import chardet
import logging

app = Flask(__name__)

# 設定 logging，將日志記錄到 script.log 文件，同時顯示在控制台
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'script.log')

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

# 從配置文件中讀取shareLocation和Scan mode
def get_config():
    config = {'shareLocation': None, 'scanMode': None}
    feedback_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Text_Files', 'feedback.txt'))
    logger.info("Reading configuration from: %s", feedback_file_path)
    try:
        with open(feedback_file_path, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            file.seek(0)
            for line in file:
                decoded_line = line.decode(encoding)
                if decoded_line.startswith('shareLocation:'):
                    config['shareLocation'] = decoded_line.split('shareLocation:')[1].strip()
                elif decoded_line.startswith('Scan mode:'):
                    config['scanMode'] = int(decoded_line.split('Scan mode:')[1].strip())
    except FileNotFoundError:
        logger.error("Configuration file not found at: %s, using default values.", feedback_file_path)
    return config

config = get_config()
if config['shareLocation'] is None or config['scanMode'] is None:
    logger.error("Configuration is invalid, exiting.")
    exit(1)

SCAN_MODE = config['scanMode']
if SCAN_MODE == 2:
    SCAN_RESULTS_DIR = os.path.join(config['shareLocation'], 'nmap_scan', 'CVE_scan_results')
    NMAP_REPORT_PATH = os.path.join(SCAN_RESULTS_DIR, 'nmap_report.html')
elif SCAN_MODE == 3:
    SCAN_RESULTS_DIR1 = os.path.join(config['shareLocation'], 'nmap_scan', 'Port_scan_results')
    SCAN_RESULTS_DIR2 = os.path.join(config['shareLocation'], 'nmap_scan', 'CVE_scan_results')
    NMAP_REPORT_PATH1 = os.path.join(SCAN_RESULTS_DIR1, 'nmap_report.html')
    NMAP_REPORT_PATH2 = os.path.join(SCAN_RESULTS_DIR2, 'nmap_report.html')
else:
    SCAN_RESULTS_DIR = os.path.join(config['shareLocation'], 'nmap_scan', 'Port_scan_results')
    NMAP_REPORT_PATH = os.path.join(config['shareLocation'], 'nmap_report.html')

# 檢查指定路徑是否存在
if SCAN_MODE != 3 and not os.path.exists(SCAN_RESULTS_DIR):
    logger.error("Scan results directory not found: %s", SCAN_RESULTS_DIR)
    exit(1)
elif SCAN_MODE == 3 and (not os.path.exists(SCAN_RESULTS_DIR1) or not os.path.exists(SCAN_RESULTS_DIR2)):
    logger.error("One or both scan results directories not found: %s, %s", SCAN_RESULTS_DIR1, SCAN_RESULTS_DIR2)
    exit(1)

@app.before_request
def check_scan_mode():
    if SCAN_MODE == 3:
        logger.info("Scan mode 3: Displaying both nmap_report and scan results")

@app.route('/')
def index():
    # 列出目錄中的所有HTML文件並去重
    if SCAN_MODE == 3:
        files = list(set([f for f in os.listdir(SCAN_RESULTS_DIR1) if f.endswith('.html')]) |
                     set([f for f in os.listdir(SCAN_RESULTS_DIR2) if f.endswith('.html')]))
    else:
        files = list(set([f for f in os.listdir(SCAN_RESULTS_DIR) if f.endswith('.html')]))
    logger.info("Listing files: %s", files)
    return render_template('index.html', files=files, scan_mode=SCAN_MODE)

@app.route('/view')
def view():
    filename = request.args.get('file')
    if filename and filename.endswith('.html'):
        if SCAN_MODE == 3:
            files = list(set([f for f in os.listdir(SCAN_RESULTS_DIR1) if f.endswith('.html')]) |
                         set([f for f in os.listdir(SCAN_RESULTS_DIR2) if f.endswith('.html')]))
        else:
            files = list(set([f for f in os.listdir(SCAN_RESULTS_DIR) if f.endswith('.html')]))
        logger.info("Viewing file: %s", filename)
        return render_template('view.html', filename=filename, files=files, scan_mode=SCAN_MODE)
    logger.error("File not found: %s", filename)
    return "File not found", 404

@app.route('/get_file/<filename>')
def get_file(filename):
    if filename.endswith('.html'):
        if SCAN_MODE == 3:
            if filename in os.listdir(SCAN_RESULTS_DIR1):
                directory = SCAN_RESULTS_DIR1
            else:
                directory = SCAN_RESULTS_DIR2
        else:
            directory = SCAN_RESULTS_DIR
        logger.info("Sending file: %s", filename)
        return send_from_directory(directory, filename)
    logger.error("File not found: %s", filename)
    return "File not found", 404

@app.route('/nmap_report')
def view_nmap_report():
    if SCAN_MODE == 3:
        if os.path.exists(NMAP_REPORT_PATH1):
            nmap_report_path = NMAP_REPORT_PATH1
        elif os.path.exists(NMAP_REPORT_PATH2):
            nmap_report_path = NMAP_REPORT_PATH2
        else:
            nmap_report_path = None
    else:
        nmap_report_path = NMAP_REPORT_PATH
    
    if nmap_report_path and os.path.exists(nmap_report_path):
        logger.info("Viewing nmap_report.html from the appropriate directory")
        return send_from_directory(os.path.dirname(nmap_report_path), os.path.basename(nmap_report_path))
    else:
        logger.error("nmap_report.html not found at path: %s", nmap_report_path)
        return "nmap_report.html not found", 404

if __name__ == '__main__':
    logger.info("Starting Flask application.")
    app.run(debug=True)
