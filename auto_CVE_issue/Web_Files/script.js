window.onload = function () {
    const targetVersionSelect = document.getElementById('target_version');
    const options = loadOptionsFromLocalStorage();
    options.forEach(option => {
        const newOption = document.createElement('option');
        newOption.value = option;
        newOption.textContent = option;
        targetVersionSelect.add(newOption);
    });

    const inputElements = document.querySelectorAll('.validate-input');
    inputElements.forEach(inputElement => {
        inputElement.addEventListener('input', function() {
            if (this.value.trim() !== '') {
                this.style.border = ''; // 取消紅色邊框
                this.classList.remove('error'); // 移除錯誤樣式
            }
        });
    });

    const setupYes = document.getElementById('setupYes');
    const setupNo = document.getElementById('setupNo');
    
    setupYes.addEventListener('change', function() {
        toggleScanModeVisibility(this.checked);
    });
    
    setupNo.addEventListener('change', function() {
        if (this.checked) {
            toggleScanModeVisibility(false);
        }
    });
}

function validateIP(ipAddress) {
    var ipPattern = /^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$/;
    return ipPattern.test(ipAddress);
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

function toggleScanModeVisibility(visible) {
    const scanModeSelect = document.getElementById('scanMode');
    const scanModeLabel = document.getElementById('scanModeLabel');

    if (visible) {
        scanModeLabel.style.display = 'block';
        scanModeSelect.style.display = 'block';
    } else {
        scanModeLabel.style.display = 'none';
        scanModeSelect.style.display = 'none';
    }
}

function saveFormData() {
    const form = document.getElementById('feedbackForm');
    const formData = new FormData(form);
    const requiredFields = document.querySelectorAll('.validate-input');
    let isValid = true;

    requiredFields.forEach(field => {
        if (field.value.trim() === '') {
            field.style.border = '1px solid red';
            field.classList.add('error');
            isValid = false;
        } else {
            field.style.border = '';
            field.classList.remove('error');
        }
    });

    if (!isValid) {
        alert('請填寫所有必填欄位');
        return;
    }

    const scanIpAddress = formData.get('scanIpAddress');
    const targetIpAddress = formData.get('targetIpAddress');
    if (!validateIP(scanIpAddress) || !validateIP(targetIpAddress)) {
        alert('IP 地址格式錯誤，請輸入正確的 IP 地址。');
        return;
    }

    const setupYes = document.getElementById('setupYes').checked;
    if (setupYes && formData.get('scanMode') === '') {
        alert('請選擇掃描模式！');
        return;
    }

    feedback(formData, setupYes);
}

function feedback(formData, setupYes) {
    let textData = '';
    textData += `username: ${formData.get('username')}\n`;
    textData += `password: ${formData.get('password')}\n`;
    textData += `target_version: ${formData.get('target_version') === '其他' ? formData.get('otherVersion') : formData.get('target_version')}\n`;
    textData += `targetIPAddress: ${formData.get('targetIpAddress')}\n`;
    textData += `scanIpAddress: ${formData.get('scanIpAddress')}\n`;
    textData += `scanusername: ${formData.get('scanusername')}\n`;
    textData += `scanpassword: ${formData.get('scanpassword')}\n`;
    textData += `Assignee: ${formData.get('Assignee')}\n`;
    textData += `Severity: ${formData.get('Severity')}\n`;
    textData += `shareLocation: ${formData.get('shareLocation')}\n`;
    textData += `Set installation permission: ${setupYes ? 'yes' : 'no'}\n`;
    if (setupYes) {
        textData += `Scan mode: ${formData.get('scanMode')}\n`;
    }

    const feedbackBlob = new Blob([textData], { type: 'text/plain' });
    const feedbackLink = document.createElement('a');
    feedbackLink.href = URL.createObjectURL(feedbackBlob);
    feedbackLink.download = 'feedback.txt';
    feedbackLink.style.display = 'none';
    document.body.appendChild(feedbackLink);
    feedbackLink.click();
    document.body.removeChild(feedbackLink);
}

function saveOptionsToLocalStorage(options) {
    localStorage.setItem('targetOptions', JSON.stringify(options));
}

function loadOptionsFromLocalStorage() {
    const options = localStorage.getItem('targetOptions');
    return options ? JSON.parse(options) : [];
}

function addOptionToLocalStorage(option) {
    const options = loadOptionsFromLocalStorage();
    if (!options.includes(option)) {
        options.push(option);
        saveOptionsToLocalStorage(options);
    }
}
