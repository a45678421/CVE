import logging
import os

def setup_logging():
    # 獲取當前腳本的目錄
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 設置日誌記錄器
    logger = logging.getLogger('')
    logger.setLevel(logging.INFO)

    # 創建控制台處理器並設置級別為 INFO
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s', datefmt='%Y%m%d %H:%M:%S')
    console.setFormatter(formatter)
    logger.addHandler(console)

    #'w'：寫入模式（write mode），如果文件已經存在，會覆蓋文件的內容。這意味著每次運行腳本時，之前的日誌記錄會被刪除，只保留新寫入的日誌記錄。
    #'a'：追加模式（append mode），如果文件已經存在，新的日誌記錄會被追加到文件的末尾，而不會刪除之前的日誌記錄。

    # 創建 log.txt 文件處理器並設置為覆蓋模式
    log_file_path = os.path.join(current_dir, '../loading/log.txt')
    log_file_handler = logging.FileHandler(log_file_path, mode='w')
    log_file_handler.setLevel(logging.INFO)
    log_file_handler.setFormatter(formatter)
    logger.addHandler(log_file_handler)

    # 創建 all_log.txt 文件處理器並設置為追加模式
    all_log_file_path = os.path.join(current_dir, '../loading/all_log.txt')
    all_log_file_handler = logging.FileHandler(all_log_file_path, mode='a')
    all_log_file_handler.setLevel(logging.INFO)
    all_log_file_handler.setFormatter(formatter)
    logger.addHandler(all_log_file_handler)

