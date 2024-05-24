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
    //const otherVersionInput = document.getElementById('otherVersion');
    //otherVersionInput.addEventListener('input', function() {
        //if (this.value.trim() !== '') {
            // 如果填入了其他版本，直接設置 target_version 的值為 otherVersion 的值
            //targetVersionSelect.value = this.value.trim();
        //}
        // 取消紅色邊框樣式
        //this.style.border = '';
    //});
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
}


function validateIP(ipAddress) {
    // IP 地址的正規表達式
    var ipPattern = /^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$/;

    // 使用正則表達式檢查 IP 地址格式
    if(ipPattern.test(ipAddress)) {
        return true; // 格式正確
    } else {
        return false; // 格式錯誤
    }
}

// 檢查必填欄位
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
  const setupYes = document.getElementById('setupYes');
  
  setupYes.addEventListener('change', function() {
    toggleScanModeVisibility(this.checked);
  });


// 檢查必填欄位
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

// 在提交表單時動態修改 target_version 的值
//document.getElementById('feedbackForm').addEventListener('submit', function(events) {
    //const targetVersionSelect = document.getElementById('target_version');
    //const otherVersionInput = document.getElementById('otherVersion');

    //if (targetVersionSelect.value === '其他' && otherVersionInput.value.trim() !== '') {
        // 如果選擇了其他且填入了其他版本，將其他版本直接設為 target_version 的值
        //targetVersionSelect.value = otherVersionInput.value.trim();
    //} 
//});

// 在其他選項中填入版本時觸發新增選項到 localStorage 的動作
function saveFormData() {
    const scanIpAddressInput = document.getElementById('scanIpAddress');
    const targetIpAddressInput = document.getElementById('targetIpAddress');
    const shareLocationInput = document.getElementById('shareLocation');
    const scanIpAddressValue = scanIpAddressInput.value.trim();
    const targetIpAddressValue = targetIpAddressInput.value.trim();
    const shareLocationValue = shareLocationInput.value.trim();
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const scanIpAddress = document.getElementById('scanIpAddress').value.trim();
    const targetIpAddress = document.getElementById('targetIpAddress').value.trim();
    const scanModeSelect = document.getElementById('scanMode');
    //const scanUsernameInput = document.getElementById('scanusername');
    //const scanPasswordInput = document.getElementById('scanpassword');
    //const scanUsername = scanUsernameInput.value.trim();
    //const scanPassword = scanPasswordInput.value.trim();
    const scanusername = document.getElementById('scanusername').value.trim();
    const scanpassword = document.getElementById('scanpassword').value.trim();
    var setupYes = document.getElementById("setupYes");
    var setupNo = document.getElementById("setupNo");
    const selectedScanMode = scanModeSelect.value;
    var otherVersionInput = document.getElementById("otherVersion");
    var targetVersion = document.getElementById("target_version").value;
    
    // 检查是否有必填字段为空
    if (username === '') {
        document.getElementById('username').style.border = '1px solid red'; // 將未填寫的欄位邊框變為紅色
        alert('請填寫USERNAME欄位！'); // 顯示彈出提示
        return; // 阻止表單提交
    } else {
        document.getElementById('username').style.border = ''; // 將邊框重設為空
    }

    if (password === '') {
        document.getElementById('password').style.border = '1px solid red'; // 將未填寫的欄位邊框變為紅色
        alert('請填寫PASSWORD欄位！'); // 顯示彈出提示
        return; // 阻止表單提交
    } else {
        document.getElementById('password').style.border = ''; // 將邊框重設為空
    }

    // 檢查IP地址格式
    if (!validateIP(scanIpAddressValue) || !validateIP(targetIpAddressValue)) {
        alert('IP 地址格式錯誤，請輸入正確的 IP 地址。');
        return; // 如果IP地址格式錯誤，停止保存表單數據
    }

    if (targetIpAddress === '') {
        document.getElementById('targetIpAddress').style.border = '1px solid red'; // 將未填寫的欄位邊框變為紅色
        alert('請填寫目標端IP欄位！'); // 顯示彈出提示
        return; // 阻止表單提交
    } else {
        document.getElementById('targetIpAddress').style.border = ''; // 將邊框重設為空
    }

    if (scanIpAddress === '') {
        document.getElementById('scanIpAddress').style.border = '1px solid red'; // 將未填寫的欄位邊框變為紅色
        alert('請填寫掃描端IP欄位！'); // 顯示彈出提示
        return; // 阻止表單提交
    } else {
        document.getElementById('scanIpAddress').style.border = ''; // 將邊框重設為空
    }

    if (scanusername === '') {
        document.getElementById('scanusername').style.border = '1px solid red'; // 將未填寫的欄位邊框變為紅色
        alert('請填寫掃描端USERNAME欄位！'); // 顯示彈出提示
        return; // 阻止表單提交
    } else {
        document.getElementById('scanusername').style.border = ''; // 將邊框重設為空
    }

    if (scanpassword === '') {
        document.getElementById('scanpassword').style.border = '1px solid red'; // 將未填寫的欄位邊框變為紅色
        alert('請填寫掃描端PASSWORD欄位！'); // 顯示彈出提示
        return; // 阻止表單提交
    } else {
        document.getElementById('scanpassword').style.border = ''; // 將邊框重設為空
    }

    if (targetVersion === '') {
        document.getElementById('target_version').style.border = '1px solid red'; // 將未填寫的欄位邊框變為紅色
        alert('請填寫目標版本欄位！'); // 顯示彈出提示
        return; // 阻止表单提交
    } else {
        document.getElementById('target_version').style.border = ''; // 將邊框重設為空
    }

    if (targetVersion === '其他') {
        var otherVersionValue = otherVersionInput.value.trim();
        if (otherVersionValue === '') {
            alert('請填入其他版本！');
            return;
        }
    }
    if (shareLocationValue === '') { // 新增對分享檔案位置的判斷
        document.getElementById('shareLocation').style.border = '1px solid red'; // 將未填寫的欄位邊框變為紅色
        alert('請填寫分享檔案位置欄位！'); // 顯示彈出提示
        return; // 阻止表单提交
    } else {
        document.getElementById('shareLocation').style.border = ''; // 將邊框重設為空
    }

    if (!setupYes.checked && !setupNo.checked) {
        alert('請選擇一個選項!');
        return;
    }

    // 檢查是否選擇了 "同意" 選項
    if (setupYes.checked) {
        if (!selectedScanMode) {
            alert('請選擇掃描模式！');
            return;
        }
    }

    //if (otherVersionValue !== '') {
        // 新增選項到 localStorage
        //addOptionToLocalStorage(otherVersionValue);

        // 直接設置其他版本值給 target_version
        //targetVersionSelect.value = otherVersionValue;

        // 新增選項到選項列表
        //const newOption = document.createElement('option');
        //newOption.value = otherVersionValue;
        //newOption.textContent = otherVersionValue;
        //targetVersionSelect.add(newOption);
    //}
    feedback()
    //saveCVEAddressAndScanInfo(shareLocationValue, scanIpAddress, scanUsername, scanPassword)
}

function feedback() {
    // 獲取表單數據
    const formData = new FormData(document.getElementById('feedbackForm'));
    const targetVersion = formData.get('target_version');
    const otherVersion = formData.get('otherVersion');
    // 將表單數據轉換為文字格式，只保留指定的欄位
    let textData = '';
    textData += `username: ${formData.get('username')}\n`;
    textData += `password: ${formData.get('password')}\n`;
    if (targetVersion !== '其他') {
        textData += `target_version: ${targetVersion}\n`;
      }
    else{
        textData += `target_version: ${otherVersion}\n`;
    }
    textData += `targetIpAddress: ${formData.get('targetIpAddress')}\n`;
    textData += `scanIPAddress: ${formData.get('scanIpAddress')}\n`;
    textData += `scanusername: ${formData.get('scanusername')}\n`;
    textData += `scanpassword: ${formData.get('scanpassword')}\n`;
    textData += `shareLocation: ${formData.get('shareLocation')}\n`;
    textData += `opinion: ${formData.get('opinion')}\n`;
    textData += `category: ${formData.get('category')}\n`;
    textData += `satisfaction: ${formData.get('satisfaction')}\n`;
    textData += `Set installation permission: ${formData.get('setup')}\n`;
    textData += `Scan mode: ${formData.get('scanMode')}\n`;

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
}

//function saveCVEAddressAndScanInfo(shareLocationValue, scanIpAddress, scanUsername, scanPassword) {
    // 創建 CVE_address.txt 檔案
    //const cveAddressData = `${shareLocationValue}\\nmap_scan`;
    //const cveAddressBlob = new Blob([cveAddressData], { type: 'text/plain' });

    // 創建下載 CVE_address.txt 的 a 標籤
    //const cveAddressLink = document.createElement('a');
    //cveAddressLink.href = URL.createObjectURL(cveAddressBlob);
    //cveAddressLink.download = 'CVE_address.txt';
    //cveAddressLink.style.display = 'none';
    //document.body.appendChild(cveAddressLink);
    //cveAddressLink.click();
    //document.body.removeChild(cveAddressLink);

    // 構建要儲存的文本資料
    //const scanInfoData = `Scan IP Address: ${scanIpAddress}\nScan Username: ${scanUsername}\nScan Password: ${scanPassword}`;

    // 創建檔案 Blob
    //const scanInfoBlob = new Blob([scanInfoData], { type: 'text/plain' });

    // 創建下載 scan_info.txt 的 a 標籤
    //const scanInfoLink = document.createElement('a');
    //scanInfoLink.href = URL.createObjectURL(scanInfoBlob);
    //scanInfoLink.download = 'scan_info.txt';
    //scanInfoLink.style.display = 'none';
    //document.body.appendChild(scanInfoLink);
    //scanInfoLink.click();
    //document.body.removeChild(scanInfoLink);
//}