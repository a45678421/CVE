from flask import Flask, render_template, request, send_from_directory, abort
import os
import chardet
import logging

app = Flask(__name__)

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

# 從../../Text_Files/feedback.txt文件中讀取shareLocation和Scan mode
def get_config():
    config = {'shareLocation': None, 'scanMode': None}
    with open('../../Text_Files/feedback.txt', 'rb') as file:
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
    return config

# 設置掃描結果文件目錄和掃描模式
config = get_config()
SCAN_RESULTS_DIR = os.path.join(config['shareLocation'], 'Port_scan_results')
SCAN_MODE = config['scanMode']

@app.before_request
def check_scan_mode():
    if SCAN_MODE == 1:
        logger.info("Scan mode 1: Application is not allowed to run.")
        abort(403, description="Scan mode 1: Application is not allowed to run.")

@app.route('/')
def index():
    # 列出目錄中的所有HTML文件
    files = [f for f in os.listdir(SCAN_RESULTS_DIR) if f.endswith('.html')]
    logger.info("Listing files: %s", files)
    return render_template('index.html', files=files)

@app.route('/view')
def view():
    filename = request.args.get('file')
    if filename and filename.endswith('.html'):
        files = [f for f in os.listdir(SCAN_RESULTS_DIR) if f.endswith('.html')]
        logger.info("Viewing file: %s", filename)
        return render_template('view.html', filename=filename, files=files)
    logger.error("File not found: %s", filename)
    return "File not found", 404

@app.route('/get_file/<filename>')
def get_file(filename):
    if filename.endswith('.html'):
        logger.info("Sending file: %s", filename)
        return send_from_directory(SCAN_RESULTS_DIR, filename)
    logger.error("File not found: %s", filename)
    return "File not found", 404

if __name__ == '__main__':
    if SCAN_MODE == 1:
        logger.info("Not in port mode, so not executing.")
    else:
        logger.info("Starting Flask application.")
        app.run(debug=True)
