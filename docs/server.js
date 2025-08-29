const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3001;
const PUBLIC_DIR = '.';

// 创建HTTP服务器
const server = http.createServer((req, res) => {
  // 确定请求的文件路径
  let filePath = path.join(PUBLIC_DIR, req.url === '/' ? 'index.html' : req.url);
  
  // 规范化文件路径，防止路径遍历攻击
  filePath = path.normalize(filePath);
  
  // 检查文件路径是否在PUBLIC_DIR范围内
  if (!filePath.startsWith(path.join(process.cwd(), PUBLIC_DIR))) {
    res.writeHead(403, { 'Content-Type': 'text/html' });
    res.end('<h1>403 Forbidden</h1><p>Access to this resource is forbidden.</p>');
    return;
  }
  
  // 检查路径是否为目录
  fs.stat(filePath, (err, stats) => {
    if (err) {
      handleFileError(err, res);
      return;
    }
    
    // 如果是目录，尝试提供index.html
    if (stats.isDirectory()) {
      const indexPath = path.join(filePath, 'index.html');
      
      fs.access(indexPath, fs.constants.F_OK, (err) => {
        if (!err) {
          // 如果目录下有index.html，提供它
          serveFile(indexPath, res);
        } else {
          // 否则，返回404错误
          res.writeHead(404, { 'Content-Type': 'text/html' });
          res.end('<h1>404 Not Found</h1><p>The requested resource could not be found.</p>');
        }
      });
    } else {
      // 如果是文件，直接提供
      serveFile(filePath, res);
    }
  });
});

// 处理文件错误
function handleFileError(error, res) {
  if (error.code === 'ENOENT') {
    // 文件未找到，返回404
    fs.readFile(path.join(PUBLIC_DIR, '404.html'), (err, content) => {
      if (err) {
        // 如果没有自定义404页面，返回默认404页面
        res.writeHead(404, { 'Content-Type': 'text/html' });
        res.end('<h1>404 Not Found</h1><p>The requested resource could not be found on this server.</p>');
      } else {
        res.writeHead(404, { 
          'Content-Type': 'text/html',
          'Cache-Control': 'no-cache, no-store, must-revalidate',
          'Pragma': 'no-cache',
          'Expires': '0'
        });
        res.end(content, 'utf-8');
      }
    });
  } else {
    // 服务器错误，返回500
    console.error('Server Error:', error);
    res.writeHead(500, {
      'Content-Type': 'text/html',
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      'Pragma': 'no-cache',
      'Expires': '0'
    });
    res.end('<h1>500 Internal Server Error</h1><p>The server encountered an error and could not complete your request.</p>');
  }
}

// 提供文件并设置适当的缓存控制
function serveFile(filePath, res) {
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
  
  // 根据文件类型设置不同的缓存策略
  let cacheControl = 'no-cache, no-store, must-revalidate'; // 默认不缓存
  if (['.js', '.css', '.png', '.jpg', '.gif', '.svg', '.woff', '.ttf', '.eot', '.otf'].includes(extname)) {
    cacheControl = 'public, max-age=31536000'; // 静态资源缓存一年
  }
  
  // 读取并提供文件
  fs.readFile(filePath, (error, content) => {
    if (error) {
      handleFileError(error, res);
    } else {
      // 成功读取文件，返回内容
      res.writeHead(200, {
        'Content-Type': contentType,
        'Cache-Control': cacheControl,
        'Last-Modified': new Date().toUTCString()
      });
      res.end(content, 'utf-8');
    }
  });
}

// 启动服务器
server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}/`);
  console.log('Features:');
  console.log('  - Directory index support (serves index.html for directories)');
  console.log('  - Cache control headers for better performance');
  console.log('  - Enhanced error handling with user-friendly messages');
  console.log('  - Path traversal protection');
});