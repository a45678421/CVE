// script.js

// 獲取游標跟隨元素和文檔中的 Canvas 元素
const cursor = document.querySelector('.cursor');
const canvas = document.getElementById('canvas');

// 監聽文檔中的滑鼠移動事件
document.addEventListener('mousemove', (e) => {
    // 獲取滑鼠的位置
    const x = e.clientX;
    const y = e.clientY;

    // 設置游標跟隨元素的位置
    cursor.style.left = `${x}px`;
    cursor.style.top = `${y}px`;
});

// 設置 Canvas 的寬度和高度為視窗的寬度和高度
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// 創建粒子陣列
let particlesArray = [];

// 定義粒子類
class Particle {
    constructor(x, y, size, color, weight) {
        this.x = x;
        this.y = y;
        this.size = size;
        this.color = color;
        this.weight = weight;
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false);
        ctx.fillStyle = this.color;
        ctx.fill();
    }

    update() {
        this.size -= 0.05;
        if (this.size < 0) {
            this.size = 0;
        }
        this.y += this.weight;
        this.weight += 0.05;

        if (this.y > canvas.height) {
            this.y = 0 - this.size;
            this.weight = Math.random() * 2 + 0.5;
            this.x = Math.random() * canvas.width * 1.3;
        }
    }
}

// 初始化粒子陣列
function init() {
    particlesArray = [];
}

// 動畫函數，更新粒子的位置並繪製粒子
function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < particlesArray.length; i++) {
        particlesArray[i].update();
        particlesArray[i].draw();
    }
    requestAnimationFrame(animate);
}

// 設置 Canvas 大小和初始化粒子陣列
function setupCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    init();
}

// 監聽視窗大小變化事件，重新設置 Canvas 大小和初始化粒子陣列
window.addEventListener('resize', setupCanvas);

// 獲取 Canvas 的 2D 上下文
const ctx = canvas.getContext('2d');

// 監聽滑鼠移動事件，在滑鼠位置創建多個粒子
canvas.addEventListener('mousemove', function(event) {
    for (let i = 0; i < 5; i++) { // 創建多個粒子
        let x = event.clientX + Math.random() * 6 - 3; // 隨機偏移
        let y = event.clientY + Math.random() * 6 - 3; // 隨機偏移
        let size = Math.random() * 10 + 1;
        let color = `hsl(${Math.random() * 360}, 100%, 50%)`; // 隨機顏色
        let weight = 1;
        particlesArray.push(new Particle(x, y, size, color, weight));
    }
});

// 初始化 Canvas 大小和粒子陣列，開始動畫
setupCanvas();
animate();

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



