from flask import Flask, jsonify, render_template 
#Flask是一個羽量級的Web框架，用於構建Web應用程式
#jsonify 是Flask中的一個函數，用於將Python字典轉換為JSON
#render_template 是Flask中的一個函數，用於渲染範本
from threading import Thread #Thread 是Python標準庫的一部分，用於創建新的執行緒
import os #os 是Python標準庫的一部分，用於與作業系統進行交互
import time #time 是Python標準庫的一部分，用於獲取當前時間
import random #random 是Python標準庫的一部分，用於生成亂數
import chardet #chardet 是Python標準庫的一部分，用於檢測檔的編碼

app = Flask(__name__)

# 全域變數來存儲任務進度
task_progress = 0
last_progress = None  # 用於存儲上一次讀取的進度值

# 偵測 feedback.txt 檔案編碼
with open("progress.txt", "rb") as file:
     raw_data = file.read()
     result = chardet.detect(raw_data)
     encoding = result['encoding']

print(f"偵測到的編碼：{encoding}")

def read_progress_file():
    global task_progress, last_progress
    while True:
        # 讀取 progress.txt 檔的內容，使用正確的編碼
        with open('progress.txt', 'r', encoding=encoding) as file:  # 使用正確的編碼
            content = file.read().strip()
            if content.isdigit():
                current_progress = int(content)
                if task_progress < 80:
                    # 隨機增加一個值，但不能超過當前進度和任務進度之間的差值
                    increment = random.uniform(1, min(10, current_progress - task_progress + 10))
                    task_progress += increment
                    if task_progress < current_progress:
                        task_progress = current_progress
                elif task_progress < 90:
                    if current_progress >= 80:
                        task_progress += 0.001
                        if task_progress < current_progress:
                            task_progress = current_progress
                        if task_progress > 90:
                            task_progress = 90
                elif task_progress >= 90:
                    if current_progress >= 90 and task_progress < 99.99:
                        # 計算增加的最大值
                        max_increment = min(100 - task_progress, current_progress - task_progress + 10)
                        # 隨機增加一個值，但不能超過 max_increment
                        increment = random.uniform(1, max_increment)
                        if task_progress + increment > current_progress + 10 or task_progress + increment > 100:
                            increment = 1  # 將增加的值設為1
                        task_progress += increment
                last_progress = current_progress

        # 列印當前進度
        print(f"當前進度: {task_progress:.3f}%")
        print(f"上次進度: {last_progress:.3f}%")
        # 輸出當前檔位置
        print("當前文件位置:", os.path.abspath(__file__))

        # 如果任務進度已經達到100%，且當前進度與上次進度不同，以當前進度為准
        if task_progress >= 100 and current_progress != last_progress:
            task_progress = current_progress

        # 每隔一段時間讀取一次檔
        time.sleep(1)

# 在新的執行緒中執行任務，以免阻塞 Flask 伺服器
thread = Thread(target=read_progress_file)
thread.start()

@app.route('/')
def index():
    # 輸出當前檔位置
    print("當前文件位置:", os.path.abspath(__file__))
    # 使用範本引擎渲染 index.html，傳入任務進度
    return render_template('index.html', progress=task_progress)

@app.route('/task-progress')
def get_task_progress():
    global task_progress  # 在函數內部使用全域變數需要聲明
    return jsonify({"progress": task_progress}), 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == '__main__':
    app.run(debug=True)


