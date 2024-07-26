import os
import pandas as pd
from tqdm import tqdm

# 獲取當前腳本所在的目錄
current_dir = os.path.dirname(os.path.abspath(__file__))

# 指定Excel檔案的資料夾路徑
folders = {
    'High_classify_component': 'High Risk Modules',
    'Medium_classify_component': 'Medium Risk Modules',
    'Low_classify_component': 'Low Risk Modules'
}

# 初始化HTML內容
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CVE Issues</title>
    <style>
        body {
            display: flex;
        }
        #sidebar {
            width: 25%;
            background-color: #f2f2f2;
            padding: 10px;
            box-shadow: 2px 0 5px rgba(0,0,0,0.1);
            overflow-y: auto;
            height: 100%;
        }
        #content {
            width: 75%;
            padding: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        .hidden {
            display: none;
        }
        h3 {
            font-size: 1.2em;
            margin: 0.5em 0;
            cursor: pointer;
        }
        h2 {
            font-size: 1.2em;
            margin: 0.5em 0;
        }
        h4 {
            font-size: 1em;
            margin: 0.3em 0;
            cursor: pointer;
        }

        #searchInput {
        width: 100%;
        padding: 12px 20px;
        margin: 8px 0;
        box-sizing: border-box;
        border: 2px solid #ccc;
        border-radius: 4px;
        }

        #searchInput:focus {
            border: 2px solid #555;
        }
    </style>
    <script>
        function toggleCategory(id) {
            var category = document.getElementById(id);
            if (category.classList.contains('hidden')) {
                category.classList.remove('hidden');
            } else {
                category.classList.add('hidden');
            }
        }
        function showContent(id) {
            var contents = document.getElementsByClassName('file-content');
            for (var i = 0; i < contents.length; i++) {
                contents[i].classList.add('hidden');
            }
            document.getElementById(id).classList.remove('hidden');
        }
        function toggleSubCategory(id) {
            var subcategories = document.getElementsByClassName(id);
            for (var i = 0; i < subcategories.length; i++) {
                if (subcategories[i].classList.contains('hidden')) {
                    subcategories[i].classList.remove('hidden');
                } else {
                    subcategories[i].classList.add('hidden');
                }
            }
        }
        function searchTable() {
            var input, filter, tables, tr, td, i, j, txtValue;
            input = document.getElementById("searchInput");
            filter = input.value.toUpperCase();
            tables = document.getElementsByTagName("table");
            for (i = 0; i < tables.length; i++) {
                tr = tables[i].getElementsByTagName("tr");
                for (j = 1; j < tr.length; j++) {
                    tr[j].style.display = "none";
                    td = tr[j].getElementsByTagName("td");
                    for (var k = 0; k < td.length; k++) {
                        if (td[k]) {
                            txtValue = td[k].textContent || td[k].innerText;
                            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                                tr[j].style.display = "";
                                break;
                            }
                        }
                    }
                }
            }
        }
    </script>
</head>
<body>
    <div id="sidebar">
        <h2>Files</h2>
        <input type="text" id="searchInput" onkeyup="searchTable()" placeholder="Search for files..">
"""

# 初始化總數計算變量
overall_ignored_total = 0
overall_patched_total = 0
overall_unpatched_total = 0

# 遍歷資料夾中的所有Excel檔案，創建側邊欄表格行和內容區域
content = ""
total_cve_counts = {}
overall_total_cve_count = 0  # 用於存儲所有分類的總CVE數
status_counts = {
    'High Risk Modules': {'ignored': 0, 'patched': 0, 'unpatched': 0},
    'Medium Risk Modules': {'ignored': 0, 'patched': 0, 'unpatched': 0},
    'Low Risk Modules': {'ignored': 0, 'patched': 0, 'unpatched': 0}
}

# 初始化每個分類的總CVE數
for folder, classification in folders.items():
    total_cve_counts[classification] = 0

# 增加總CVE數顯示
html_content += "<h3 onclick=\"toggleCategory('cve_total_counts')\">CVE Total Counts</h3>\n"
html_content += "<div id=\"cve_total_counts\" class=\"hidden\">\n<ul>\n"
html_content += f"<li id=\"total_all\">CVE total counts for All: {overall_total_cve_count}</li>\n"
for classification in folders.values():
    html_content += f"<li id=\"total_{classification.replace(' ', '_').lower()}\">CVE total counts for {classification}: {total_cve_counts.get(classification, 0)}</li>\n"
html_content += f"<li id=\"ignored_all\">Total Ignored: {overall_ignored_total}</li>\n"
html_content += f"<li id=\"patched_all\">Total Patched: {overall_patched_total}</li>\n"
html_content += f"<li id=\"unpatched_all\">Total Unpatched: {overall_unpatched_total}</li>\n"
html_content += "</ul>\n</div>\n"

for folder, classification in folders.items():
    # 計算該分類中的文件數量和CVE總數
    file_count = len([name for name in os.listdir(folder) if name.endswith('.xlsx')])
    total_cve_count = 0
    
    html_content += f"<h3 onclick=\"toggleSubCategory('{classification.replace(' ', '_').lower()}_subcategory')\" style=\"cursor:pointer;\">{classification} : {file_count}</h3>\n"
    html_content += f"<div class=\"{classification.replace(' ', '_').lower()}_subcategory hidden\">\n"
    
    ignored_total = 0
    patched_total = 0
    unpatched_total = 0
    
    ignored_content = ""
    patched_content = ""
    unpatched_content = ""
    
    for idx, file_name in enumerate(tqdm(os.listdir(folder), desc=f"Processing {classification}")):
        if file_name.endswith('.xlsx'):
            file_path = os.path.join(folder, file_name)
            df = pd.read_excel(file_path)
            
            ignored_count = df[df['STATUS'] == 'Ignored'].shape[0]
            patched_count = df[df['STATUS'] == 'Patched'].shape[0]
            unpatched_count = df[df['STATUS'] == 'Unpatched'].shape[0]
            
            ignored_total += ignored_count
            patched_total += patched_count
            unpatched_total += unpatched_count
            
            overall_ignored_total += ignored_count
            overall_patched_total += patched_count
            overall_unpatched_total += unpatched_count
            
            status_counts[classification]['ignored'] += ignored_count
            status_counts[classification]['patched'] += patched_count
            status_counts[classification]['unpatched'] += unpatched_count
            
            ignored_content += f"<tr onclick=\"showContent('{classification.replace(' ', '_').lower()}_ignored_{idx}')\"><td>{file_name}</td><td>{ignored_count}</td></tr>\n"
            
            content += f'<div id="{classification.replace(' ', '_').lower()}_ignored_{idx}" class="file-content hidden">\n'
            content += f"<h2>{file_name} - Ignored</h2>\n"
            content += """
            <table>
                <thead>
                    <tr>
                        <th>CVE_ID</th>
                        <th>COMPONENT</th>
                        <th>CATEGORY</th>
                        <th>VERSION</th>
                        <th>CVE_link</th>
                        <th>CVSS_v2</th>
                        <th>CVSS_v3</th>
                        <th>STATUS</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            for index, row in df[df['STATUS'] == 'Ignored'].iterrows():
                content += f"""
                <tr>
                    <td>{row['CVE_ID']}</td>
                    <td>{row['COMPONENT']}</td>
                    <td>{row['CATEGORY']}</td>
                    <td>{row['VERSION']}</td>
                    <td><a href="{row['CVE_link']}">{row['CVE_link']}</a></td>
                    <td>{row['CVSS_v2']}</td>
                    <td>{row['CVSS_v3']}</td>
                    <td>{row['STATUS']}</td>
                </tr>
                """
            
            content += """
                </tbody>
            </table>
            <br>
            </div>
            """
            
            patched_content += f"<tr onclick=\"showContent('{classification.replace(' ', '_').lower()}_patched_{idx}')\"><td>{file_name}</td><td>{patched_count}</td></tr>\n"
            
            content += f'<div id="{classification.replace(' ', '_').lower()}_patched_{idx}" class="file-content hidden">\n'
            content += f"<h2>{file_name} - Patched</h2>\n"
            content += """
            <table>
                <thead>
                    <tr>
                        <th>CVE_ID</th>
                        <th>COMPONENT</th>
                        <th>CATEGORY</th>
                        <th>VERSION</th>
                        <th>CVE_link</th>
                        <th>CVSS_v2</th>
                        <th>CVSS_v3</th>
                        <th>STATUS</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            for index, row in df[df['STATUS'] == 'Patched'].iterrows():
                content += f"""
                <tr>
                    <td>{row['CVE_ID']}</td>
                    <td>{row['COMPONENT']}</td>
                    <td>{row['CATEGORY']}</td>
                    <td>{row['VERSION']}</td>
                    <td><a href="{row['CVE_link']}">{row['CVE_link']}</a></td>
                    <td>{row['CVSS_v2']}</td>
                    <td>{row['CVSS_v3']}</td>
                    <td>{row['STATUS']}</td>
                </tr>
                """
            
            content += """
                </tbody>
            </table>
            <br>
            </div>
            """
            
            unpatched_content += f"<tr onclick=\"showContent('{classification.replace(' ', '_').lower()}_unpatched_{idx}')\"><td>{file_name}</td><td>{unpatched_count}</td></tr>\n"
            
            content += f'<div id="{classification.replace(' ', '_').lower()}_unpatched_{idx}" class="file-content hidden">\n'
            content += f"<h2>{file_name} - Unpatched</h2>\n"
            content += """
            <table>
                <thead>
                    <tr>
                        <th>CVE_ID</th>
                        <th>COMPONENT</th>
                        <th>CATEGORY</th>
                        <th>VERSION</th>
                        <th>CVE_link</th>
                        <th>CVSS_v2</th>
                        <th>CVSS_v3</th>
                        <th>STATUS</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            for index, row in df[df['STATUS'] == 'Unpatched'].iterrows():
                content += f"""
                <tr>
                    <td>{row['CVE_ID']}</td>
                    <td>{row['COMPONENT']}</td>
                    <td>{row['CATEGORY']}</td>
                    <td>{row['VERSION']}</td>
                    <td><a href="{row['CVE_link']}">{row['CVE_link']}</a></td>
                    <td>{row['CVSS_v2']}</td>
                    <td>{row['CVSS_v3']}</td>
                    <td>{row['STATUS']}</td>
                </tr>
                """
            
            content += """
                </tbody>
            </table>
            <br>
            </div>
            """
    
    total_cve_counts[classification] += ignored_total + patched_total + unpatched_total
    overall_total_cve_count += ignored_total + patched_total + unpatched_total
    
    html_content += f"<h4 onclick=\"toggleCategory('{classification.replace(' ', '_').lower()}_ignored')\">Ignored: {ignored_total}</h4>\n"
    html_content += f"<div id=\"{classification.replace(' ', '_').lower()}_ignored\" class=\"hidden\">\n"
    html_content += f"<table>\n<thead>\n<tr>\n<th>File Name</th>\n<th>CVE Count</th></tr>\n</thead>\n<tbody>\n"
    html_content += ignored_content + "</tbody>\n</table>\n</div>\n"
    
    html_content += f"<h4 onclick=\"toggleCategory('{classification.replace(' ', '_').lower()}_patched')\">Patched: {patched_total}</h4>\n"
    html_content += f"<div id=\"{classification.replace(' ', '_').lower()}_patched\" class=\"hidden\">\n"
    html_content += f"<table>\n<thead>\n<tr>\n<th>File Name</th>\n<th>CVE Count</th></tr>\n</thead>\n<tbody>\n"
    html_content += patched_content + "</tbody>\n</table>\n</div>\n"
    
    html_content += f"<h4 onclick=\"toggleCategory('{classification.replace(' ', '_').lower()}_unpatched')\">Unpatched: {unpatched_total}</h4>\n"
    html_content += f"<div id=\"{classification.replace(' ', '_').lower()}_unpatched\" class=\"hidden\">\n"
    html_content += f"<table>\n<thead>\n<tr>\n<th>File Name</th>\n<th>CVE Count</th></tr>\n</thead>\n<tbody>\n"
    html_content += unpatched_content + "</tbody>\n</table>\n</div>\n"
    
    html_content += "</div>\n"

# 更新CVE總數的顯示
html_content = html_content.replace(f"CVE total counts for All: 0", f"CVE total counts for All: {overall_total_cve_count}")
for classification in folders.values():
    html_content = html_content.replace(f"CVE total counts for {classification}: 0", f"CVE total counts for {classification}: {total_cve_counts[classification]}")
html_content = html_content.replace(f"Total Ignored: 0", f"Total Ignored: {overall_ignored_total}")
html_content = html_content.replace(f"Total Patched: 0", f"Total Patched: {overall_patched_total}")
html_content = html_content.replace(f"Total Unpatched: 0", f"Total Unpatched: {overall_unpatched_total}")

# 完成HTML結構
html_content += """
    </div>
    <div id="content">
""" + content + """
    </div>
</body>
</html>
"""

# 保存HTML文件到 ../report_template/template 資料夾
output_file_path = os.path.join(current_dir, 'CVE_Issues.html')
with open(output_file_path, 'w') as file:
    file.write(html_content)

print(f"HTML文件已保存到: {output_file_path}")
