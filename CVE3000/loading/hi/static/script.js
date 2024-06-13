document.addEventListener('DOMContentLoaded', () => {
    const logContent = document.getElementById('log-content');
    const progressBar = document.getElementById('progress-bar');
    const steps = document.querySelectorAll('.step');

    function updateProgressBar(progress) {
        progressBar.style.width = `${progress}%`;
        steps.forEach((step, index) => {
            if (index < progress / 10) {
                step.classList.add('completed');
                step.classList.remove('active');
            } else if (index === Math.floor(progress / 10)) {
                step.classList.add('active');
            } else {
                step.classList.remove('completed');
                step.classList.remove('active');
            }
        });
    }

    function fetchLogContent() {
        fetch('/log.txt')
            .then(response => response.text())
            .then(content => {
                const logs = content.trim().split('\n');
                logContent.innerHTML = '';
                logs.forEach(log => {
                    const logElement = document.createElement('div');
                    logElement.textContent = log;
                    logContent.appendChild(logElement);
                });
            })
            .catch(error => console.error('Error fetching log.txt:', error));
    }

    function fetchProgressContent() {
        fetch('/progress.txt')
            .then(response => response.text())
            .then(content => {
                const progress = parseInt(content.trim(), 10);
                if (!isNaN(progress)) {
                    updateProgressBar(progress);
                }
            })
            .catch(error => console.error('Error fetching progress.txt:', error));
    }

    fetchLogContent();
    fetchProgressContent();

    setInterval(fetchLogContent, 5000);  // 每5秒刷新一次日志内容
    setInterval(fetchProgressContent, 5000);  // 每5秒刷新一次进度内容
});


const $percent = document.querySelector('.percent');
const $circle = document.querySelector('.circle');

function updateProgress() {
    fetch('/task-progress')
        .then(response => response.json())
        .then(data => {
            let load = data.progress;
            document.querySelector('.percent').innerHTML = load.toFixed(0);
            const circle = document.querySelector('.circle');
            circle.style.background = `conic-gradient(from 0deg at 50% 50%, #6f7bf7 0%, #9bf8f4 ${load}%, #101012 ${load}%)`;
        });
}

// 初始更新進度
updateProgress();

// 定時更新進度，每1.5秒更新一次
setInterval(updateProgress, 1500);