document.addEventListener('DOMContentLoaded', () => {
    const logContent = document.getElementById('log-content');
    const logFileInput = document.getElementById('log-file-input');
    const progressFileInput = document.getElementById('progress-file-input');
    const steps = {
        10: 'step-vm',
        20: 'step-engine',
        30: 'step-prepare-vm',
        40: 'step-storage',
        50: 'step-finish'
    };
    const progressBar = document.getElementById('progress-bar');

    // 读取 log.txt 文件
    logFileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const text = e.target.result;
                const logs = text.split('\n').filter(line => line.trim() !== '').slice(-25); // 读取最后25行
                logContent.innerHTML = ''; // 清空现有内容
                logs.forEach(log => {
                    const logElement = document.createElement('div');
                    logElement.textContent = log;
                    logContent.appendChild(logElement);
                });
            };
            reader.readAsText(file);
        }
    });

    // 读取 progress.txt 文件并更新步骤状态
    progressFileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const progress = parseInt(e.target.result.trim(), 10);
                let progressBarWidth = 0;

                Object.keys(steps).forEach(key => {
                    const stepElement = document.getElementById(steps[key]);
                    if (progress >= key) {
                        stepElement.classList.add('completed');
                        stepElement.classList.remove('current');
                        progressBarWidth = (key / 50) * 100;
                    } else {
                        stepElement.classList.remove('completed');
                        stepElement.classList.remove('current');
                    }
                });

                // 设置当前步骤
                if (progress < 50) {
                    const nextStep = steps[progress + 10];
                    document.getElementById(nextStep).classList.add('current');
                }

                // 更新进度条
                progressBar.style.width = progressBarWidth + '%';
            };
            reader.readAsText(file);
        }
    });

    document.getElementById('cancel-button').addEventListener('click', () => {
        alert('Deployment canceled');
    });

    document.getElementById('prepare-vm-button').addEventListener('click', () => {
        alert('Prepare VM process started');
    });
});
