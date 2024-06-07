// 儲存選項資料到 localStorage
function saveOptionsToLocalStorage(options) {
    localStorage.setItem('targetOptions', JSON.stringify(options));
}

// 新增選項到 localStorage
function addOptionToLocalStorage(option) {
    const options = loadOptionsFromLocalStorage();
    if (!options.includes(option)) {
        options.push(option);
        saveOptionsToLocalStorage(options);
    }
}

// 從 localStorage 中讀取選項資料
function loadOptionsFromLocalStorage() {
    const options = localStorage.getItem('targetOptions');
    if (options) {
        return JSON.parse(options);
    }
    return [];
}

// 在頁面加載時從 localStorage 中讀取選項並動態生成選項列表
window.onload = function () {
    const targetVersionSelect = document.getElementById('target_version');
    const options = loadOptionsFromLocalStorage();
    options.forEach(option => {
        const newOption = document.createElement('option');
        newOption.value = option;
        newOption.textContent = option;
        targetVersionSelect.add(newOption);
    });

    // 取得需要監聽輸入的輸入框元素
    const inputElements = document.querySelectorAll('.validate-input');

    // 輸入事件監聽器
    inputElements.forEach(inputElement => {
        inputElement.addEventListener('input', function() {
            if (this.value.trim() !== '') {
                this.style.border = ''; // 取消紅色邊框
            }
        });
    });

    const setupYes = document.getElementById('setupYes');
    if (setupYes) {
        setupYes.addEventListener('change', function() {
            toggleScanModeVisibility(this.checked);
        });
    }
}

function toggleScanModeVisibility(checked) {
    const scanModeSelect = document.getElementById('scanMode');
    const scanModeLabel = document.getElementById('scanModeLabel');

    if (checked) {
      scanModeLabel.style.display = 'block'; // 顯示掃描模式的 label
      scanModeSelect.style.display = 'block'; // 顯示掃描模式的選項
    } else {
      scanModeLabel.style.display = 'none'; // 隱藏掃描模式的 label
      scanModeSelect.style.display = 'none'; // 隱藏掃描模式的選項
    }
}

function checkRequiredField(inputElement, errorMessage) {
    const value = inputElement.value.trim();
    if (value === '') {
        inputElement.style.border = '1px solid red';
        alert(errorMessage);
        return false;
    } else {
        inputElement.style.border = '';
        return true;
    }
}

function checkOther(value) {
    const otherVersionInput = document.getElementById('otherVersion');
    if (value === '其他') {
        otherVersionInput.style.display = 'block';
        otherVersionInput.setAttribute('required', 'required');
    } else {
        otherVersionInput.style.display = 'none';
        otherVersionInput.removeAttribute('required');
    }
}

// 在其他選項中填入版本時觸發新增選項到 localStorage 的動作
function saveFormData() {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const project_name = document.getElementById('project_name').value.trim();
    const otherVersionInput = document.getElementById("otherVersion");
    const targetVersion = document.getElementById("target_version").value;
    const assignee = document.getElementById("Assignee").value; // 獲取 Assignee 的值
    const severity = document.querySelector('input[name="SEVERITY_VALUE"]:checked'); // 獲取被選中的 Severity 選項

    if (username === '') {
        document.getElementById('username').style.border = '1px solid red'; // 將未填寫的欄位邊框變為紅色
        swal("請填寫USERNAME欄位！", { icon: "warning" }); // 顯示彈出提示
        return; // 阻止表單提交
    } else {
        if (password === '') {
            document.getElementById('password').style.border = '1px solid red'; // 將未填寫的欄位邊框變為紅色
            swal("請填寫PASSWORD欄位！", { icon: "warning" }); // 顯示彈出提示
            return; // 阻止表單提交
        } else{
            if (project_name === '') {
                document.getElementById('project_name').style.border = '1px solid red';
                swal("請填入專案名稱：", { icon: "warning" }); // 顯示彈出提示
                return;
            }else {
                if (targetVersion === '') {
                    document.getElementById('target_version').style.border = '1px solid red'; // 將未填寫的欄位邊框變為紅色
                    swal("請填寫目標版本欄位！", { icon: "warning" }); // 顯示彈出提示
                    return; // 阻止表單提交
                } else {
                    if (targetVersion === '其他') {
                        const otherVersionValue = otherVersionInput.value.trim();
                        if (otherVersionValue === '') {
                            swal("請填入其他版本！", { icon: "warning" }); // 顯示彈出提示
                            return;
                        }
                    }
                    if (assignee === '') {
                        document.getElementById('Assignee').style.border = '1px solid red'; // 將未填寫的欄位邊框變為紅色
                        swal("請填寫受理人欄位！", { icon: "warning" }); // 顯示彈出提示
                        return; // 阻止表單提交
                    } else {
                        if (!severity) {
                            swal("請選擇 Severity 選項！", { icon: "warning" }); // 顯示彈出提示
                            return;
                        }
                        showSuccessAlert("Please clicked the button!", "OK", feedback);
                    }
                }
            }
        }
    }
}

function feedback() {
    // 獲取表單數據
    const formData = new FormData(document.getElementById('feedbackForm'));
    const targetVersion = formData.get('target_version');
    const otherVersion = formData.get('otherVersion');
    const assignee = formData.get('Assignee'); // 獲取 Assignee 的值
    const severity = formData.get('SEVERITY_VALUE'); // 獲取 Severity 的值
    const otherVersionInput = document.getElementById("otherVersion");
    // 獲取 project 欄位數據
    const project = formData.get('project');
    const projectName = formData.get('project_name');
    const projectVersion = formData.get('project_version');
    const apiKey = formData.get('redmine_api_key'); // 獲取 API Key 的值
    
    // 將表單數據轉換為文字格式，只保留指定的欄位
    let textData = '';
    textData += `USERNAME = "${formData.get('username')}"\n`;
    textData += `PASSWORD = "${formData.get('password')}"\n`;
    textData += `API_KEY = "${apiKey}"\n`;
    let projectString = projectName;

    if (project) {
        projectString = `${project}::${projectString}`;
    }

    if (projectVersion) {
        projectString = `${projectString}::${projectVersion}`;
    }

    textData += `PROJECT = "${projectString}"\n`;
    
    if (targetVersion !== '其他') {
        textData += `VERSION  = "${targetVersion}"\n`;
    } else {
        textData += `VERSION  = "${otherVersion}"\n`;
    }
    textData += `ASSIGNEE_NAME = "${assignee}"\n`; 
    textData += `SEVERITY_VALUE = "${severity}"\n`; 

    // 創建 feedback.txt 檔案
    const feedbackBlob = new Blob([textData], { type: 'text/plain' });

    // 創建下載 feedback.txt 的 a 標籤
    const feedbackLink = document.createElement('a');
    feedbackLink.href = URL.createObjectURL(feedbackBlob);
    feedbackLink.download = 'feedback.txt';
    feedbackLink.style.display = 'none';
    document.body.appendChild(feedbackLink);
    feedbackLink.click();
    document.body.removeChild(feedbackLink);

    // 清空所有欄位的值
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    document.getElementById('redmine_api_key').value = ''; 
    document.getElementById('project').value = '';
    document.getElementById('project_name').value = '';
    document.getElementById('project_version').value = '';
    otherVersionInput.value = '';
    document.getElementById("target_version").value = '';
    document.getElementById("Assignee").value = '';
    document.querySelector('input[name="SEVERITY_VALUE"]:checked').checked = false;
}

function showSuccessAlert(message, buttonText, callback) {
    swal({
        title: "Good job!",
        text: message,
        icon: "success",
        button: buttonText,
    }).then((result) => {
        if (result && typeof callback === "function") {
            callback();
            swal("If you want to run it, click the button below.", {
                buttons: {
                    cancel: "Run away!",
                    catch: {
                        text: "Bring it on!",
                        value: "catch",
                    },
                },
            }).then((value) => {
                switch (value) {
                    case "catch":
                        swal("Sueccessfully!", "You are run now!", "success");
                        fetch('http://localhost:3000/run-bat')
                            .then(response => {
                                if (!response.ok) {
                                    throw new Error('Network response was not ok');
                                }
                                return response.text();
                            })
                            .then(data => {
                                console.log('Response from server:', data);
                                // 輸出到流覽器控制台
                            })
                            .catch(error => {
                                console.error('Error:', error);
                            });
                        break;
                    default:
                        swal("Oh no!", "Why ran away!", "error");
                }
            });
        }
    });
}

