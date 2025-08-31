// HTTP服务器实现，用于本地预览docsify文档

const http = require('http');
const fs = require('fs');
const path = require('path');

// 定义端口号
const PORT = 3000;

// 定义MIME类型映射
const MIME_TYPES = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.md': 'text/markdown',
  '.txt': 'text/plain'
};

// 错误处理函数
function handleError(res, statusCode, message) {
  res.writeHead(statusCode, { 'Content-Type': 'text/html' });
  res.end(`<html><body><h1>${statusCode} ${message}</h1></body></html>`);
}

// 创建HTTP服务器
const server = http.createServer((req, res) => {
  // 规范化路径，防止目录遍历攻击
  let filePath = path.normalize(__dirname + req.url);
  
  // 防止目录遍历攻击
  if (!filePath.startsWith(__dirname)) {
    handleError(res, 403, 'Forbidden');
    return;
  }

  // 检查文件是否存在
  fs.stat(filePath, (err, stats) => {
    if (err) {
      handleError(res, 404, 'Not Found');
      return;
    }

    // 如果是目录，查找index.html
    if (stats.isDirectory()) {
      filePath = path.join(filePath, 'index.html');
      // 检查目录下是否有index.html
      fs.access(filePath, fs.constants.F_OK, (err) => {
        if (err) {
          handleError(res, 404, 'Directory index not found');
          return;
        }
        serveFile(filePath, res);
      });
    } else {
      // 如果是文件，直接提供
      serveFile(filePath, res);
    }
  });
});

// 提供文件的函数
function serveFile(filePath, res) {
  const extname = path.extname(filePath).toLowerCase();
  const contentType = MIME_TYPES[extname] || 'application/octet-stream';

  // 打开文件并读取内容
  fs.readFile(filePath, (err, content) => {
    if (err) {
      handleError(res, 500, 'Internal Server Error');
      return;
    }

    // 设置响应头
    const headers = {
      'Content-Type': contentType,
      'Access-Control-Allow-Origin': '*',
      'Cache-Control': 'public, max-age=86400' // 缓存一天(86400秒)，之前是一年，现在缩短为一天
    };

    // 对于静态资源(JS, CSS, 图片等)设置适当的缓存策略
    // 对于HTML和MD文件，不进行长期缓存
    if (['.html', '.md'].includes(extname)) {
      headers['Cache-Control'] = 'no-cache, no-store, must-revalidate';
      headers['Pragma'] = 'no-cache';
      headers['Expires'] = '0';
    }

    res.writeHead(200, headers);
    res.end(content);
  });
}

// 启动服务器
server.listen(PORT, () => {
  console.log(`服务器运行在 http://localhost:${PORT}/`);
  console.log('按 Ctrl+C 停止服务器');
  console.log('提示：此服务器仅用于本地开发和预览，生产环境请使用专业的Web服务器');
});

// 处理服务器错误
server.on('error', (e) => {
  if (e.code === 'EADDRINUSE') {
    console.error(`端口 ${PORT} 已被占用，请关闭占用该端口的程序或使用其他端口`);
  } else {
    console.error('服务器错误:', e);
  }
});