const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3001;
const PUBLIC_DIR = '.';

// 创建HTTP服务器
const server = http.createServer((req, res) => {
  // 确定请求的文件路径
  let filePath = path.join(PUBLIC_DIR, req.url === '/' ? 'index.html' : req.url);
  
  // 获取文件扩展名
  const extname = String(path.extname(filePath)).toLowerCase();
  
  // 设置内容类型
  const mimeTypes = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.wav': 'audio/wav',
    '.mp4': 'video/mp4',
    '.woff': 'application/font-woff',
    '.ttf': 'application/font-ttf',
    '.eot': 'application/vnd.ms-fontobject',
    '.otf': 'application/font-otf',
    '.wasm': 'application/wasm'
  };
  
  const contentType = mimeTypes[extname] || 'application/octet-stream';
  
  // 读取并提供文件
  fs.readFile(filePath, (error, content) => {
    if (error) {
      if (error.code === 'ENOENT') {
        // 文件未找到，返回404
        fs.readFile(path.join(PUBLIC_DIR, '404.html'), (error, content) => {
          res.writeHead(404, { 'Content-Type': 'text/html' });
          res.end(content, 'utf-8');
        });
      } else {
        // 服务器错误，返回500
        res.writeHead(500);
        res.end(`Server Error: ${error.code}`);
      }
    } else {
      // 成功读取文件，返回内容
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content, 'utf-8');
    }
  });
});

// 启动服务器
server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}/`);
});