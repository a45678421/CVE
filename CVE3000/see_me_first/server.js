const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const port = 3000;

// 允许跨域请求
app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST');
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');
    next();
});

// GET根路徑時，返回fill_me_first.html文件的內容
app.get('/', (req, res) => {
    const filePath = path.join(__dirname, 'fill_me_first.html');
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            console.error(`Error reading HTML file: ${err}`);
            return res.status(500).send(`Error: ${err.message}`);
        }
        res.send(data);
    });
});

// 提供script.js文件的内容
app.get('/script.js', (req, res) => {
    const filePath = path.join(__dirname, 'script.js');
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            console.error(`Error reading script.js file: ${err}`);
            return res.status(500).send(`Error: ${err.message}`);
        }
        res.contentType('application/javascript');
        res.send(data);
    });
});

// 提供styles.css文件的内容
app.get('/styles.css', (req, res) => {
    const filePath = path.join(__dirname, 'styles.css');
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            console.error(`Error reading styles.css file: ${err}`);
            return res.status(500).send(`Error: ${err.message}`);
        }
        res.contentType('text/css');
        res.send(data);
    });
});

app.get('/run-bat', (req, res) => {
    const batFilePath = path.join(__dirname, 'main.bat');
    exec(batFilePath, { maxBuffer: 10 * 1024 * 1024 }, (error, stdout, stderr) => { // 增加 maxBuffer 大小到 10MB
        if (error) {
            console.error(`Error executing batch file: ${error}`);
            return res.status(500).send(`Error: ${error.message}`);
        }
        console.log(`Batch file output: ${stdout}`);

        // 讀取並傳回日誌檔案的內容
        const logFilePath = path.join(__dirname, 'run_log.txt');
        fs.readFile(logFilePath, 'utf8', (err, data) => {
            if (err) {
                console.error(`Error reading log file: ${err}`);
                return res.status(500).send(`Error: ${err.message}`);
            }
            res.send(data);
        });
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
