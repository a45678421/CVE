import os
import sys
import logging
import subprocess

# 設置日誌文件路徑
log_file_path = '../loading/log.txt'

# 配置日誌記錄器
logging.basicConfig(
    level=logging.DEBUG,
    filename=log_file_path,
    filemode='w',
    format='[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    datefmt='%Y%m%d %H:%M:%S',
)

# 設置控制台處理器以顯示在終端
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s', datefmt='%Y%m%d %H:%M:%S')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# 重定向標準輸出和標準錯誤到日誌
class LoggingStream:
    def __init__(self, level):
        self.level = level

    def write(self, message):
        if message.strip():
            logging.log(self.level, message.strip())

    def flush(self):
        pass

sys.stdout = LoggingStream(logging.INFO)
sys.stderr = LoggingStream(logging.ERROR)

logging.debug('Install packages ...')

def install_or_update(package):
    """
    安裝或更新指定的包
    """
    try:
        process = subprocess.Popen(
            [sys.executable, '-m', 'pip', 'install', '--upgrade', package],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        logging.info(stdout)
        if process.returncode == 0:
            logging.debug(f"{package} 安裝或更新完成")
        else:
            logging.error(f"安裝或更新 {package} 時出錯: {stderr}")
    except subprocess.CalledProcessError as e:
        logging.error(f"安裝或更新 {package} 時出錯: {e}")

# 更新 pip
install_or_update('pip')

# 需要檢查和安裝的套件列表
packages_to_check = [
    ('requests', 'requests'),
    ('bs4', 'beautifulsoup4'),
    ('selenium', 'selenium'),
    ('pandas', 'pandas'),
    ('openpyxl', 'openpyxl'),
    ('comtypes', 'comtypes'),
    ('pywin32', 'pywin32'),
    ('chardet', 'chardet'),
    ('Redmine', 'python-redmine'),
    ('flask', 'flask'),
    ('tqdm', 'tqdm'),
    # Add pylint related dependency packages
    ('tomlkit', 'tomlkit'),
    ('platformdirs', 'platformdirs'),
    ('mccabe', 'mccabe'),
    ('isort', 'isort'),
    ('dill', 'dill'),
]

# 檢查並安裝所需的包
for package_name, install_name in packages_to_check:
    try:
        __import__(package_name)
        logging.debug(f'{package_name} 已安裝')
        # 使用 install_or_update 函數來確保套件是最新的
        install_or_update(install_name)
    except ImportError:
        logging.debug(f'{package_name} 未安裝，開始安裝...')
        install_or_update(install_name)

logging.debug('All packages installed or updated')
