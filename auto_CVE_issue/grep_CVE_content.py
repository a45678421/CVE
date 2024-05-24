import requests
from bs4 import BeautifulSoup
import os
import time

# 全域變數
#CVE_number = "CVE-2023-51767"

# 讀 cve_numbers.txt
with open("cve_numbers.txt", "r") as file:
      cve_numbers = file.readlines()

# 遍歷每個 CVE 編號
for cve_number in cve_numbers:
      # 移除空白符號和換行符
      cve_number = cve_number.strip()
    
      # 取得網頁內容
      url = f"https://vulners.com/cve/{cve_number}"
      response = requests.get(url)
      html_content = response.text

      # 解析HTML
      soup = BeautifulSoup(html_content, 'html.parser')

      # 找到標題
      title_tag = soup.find('h1', class_='css-1i5ri9q-header-Content-title')
      title = title_tag.text.strip() if title_tag else f"No Title Found for {cve_number}"
      time.sleep(1)
    
      # 找到內容
      content_div = soup.find('div', class_='css-1ooohex-HTML-container-body')
      if content_div:
          content_paragraphs = content_div.find_all('p')
          content = '\n'.join(paragraph.text.strip() for paragraph in content_paragraphs) if content_paragraphs else f"No Content Found for {cve_number}"
      else:
          content = f"No Content Found for {cve_number}"

      # 建立並寫入.txt檔案
      filename = f"{cve_number}.txt"
      with open(filename, 'w', encoding='utf-8') as file:
          # 寫入內容
          file.write(f"Title: {title}\n\n")
          file.write(f"CVE URL:\n{url}\n\n")
          file.write(f"Description:\n{content}")

      print("檔案已儲存為:", filename)