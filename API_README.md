# 知识库API服务

这是一个用于访问GitHub知识库内容的RESTful API服务，允许其他应用程序读取知识库中每个文件夹和文件的内容。

## 功能特点

- 获取所有分类（文件夹）列表
- 获取指定分类下的文件列表
- 获取指定文件的内容
- 支持Markdown格式转换为HTML
- 提供健康检查端点

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动API服务

```bash
python knowledge_base_api.py
```

服务将在 http://localhost:5000 启动

## API端点说明

### 健康检查

```
GET /api/health
```

**描述**：检查API服务是否正常运行

**响应示例**：
```json
{
  "success": true,
  "status": "running",
  "time": "2025-08-20 08:00:00"
}
```

### 获取所有分类

```
GET /api/categories
```

**描述**：获取知识库中的所有分类（文件夹）列表

**响应示例**：
```json
{
  "success": true,
  "data": [
    {
      "name": "国泰海通证券",
      "path": "国泰海通证券",
      "description": "国泰海通证券分类",
      "file_count": 1
    },
    {
      "name": "技术",
      "path": "技术",
      "description": "技术相关文档",
      "file_count": 1
    }
  ],
  "count": 2
}
```

### 获取分类下的文件

```
GET /api/categories/{category}
```

**描述**：获取指定分类下的所有文件列表

**参数**：
- `category`: 分类名称

**响应示例**：
```json
{
  "success": true,
  "category": "国泰海通证券",
  "data": [
    {
      "name": "README.md",
      "path": "国泰海通证券/README.md",
      "size": 500,
      "modified_time": "2025-08-20 07:00:00"
    }
  ],
  "count": 1
}
```

### 获取文件内容

```
GET /api/categories/{category}/{filename}
```

**描述**：获取指定文件的内容

**参数**：
- `category`: 分类名称
- `filename`: 文件名
- `format`: 可选参数，设置为`html`可返回Markdown转换后的HTML内容

**响应示例**（普通文本）：
```json
{
  "success": true,
  "data": {
    "name": "README.md",
    "category": "国泰海通证券",
    "content": "# 国泰海通证券分类\n\n欢迎访问...",
    "size": 500,
    "modified_time": "2025-08-20 07:00:00"
  }
}
```

**响应示例**（带HTML格式）：
```json
{
  "success": true,
  "data": {
    "name": "README.md",
    "category": "国泰海通证券",
    "content": "# 国泰海通证券分类\n\n欢迎访问...",
    "size": 500,
    "modified_time": "2025-08-20 07:00:00",
    "html_content": "<h1>国泰海通证券分类</h1>\n<p>欢迎访问...</p>"
  }
}
```

## 支持的文件类型

API目前支持访问以下类型的文件：
- Markdown文件（.md, .markdown）
- 文本文件（.txt）

## 错误处理

API会返回适当的HTTP状态码和错误信息，常见的错误情况包括：

- 404 Not Found：请求的分类或文件不存在
- 500 Internal Server Error：服务器内部错误

错误响应格式：
```json
{
  "success": false,
  "error": "错误描述信息"
}
```

## 部署说明

### 开发环境

直接运行Python脚本：
```bash
python knowledge_base_api.py
```

### 生产环境

推荐使用WSGI服务器如Gunicorn部署：

```bash
# 安装Gunicorn
pip install gunicorn

# 启动服务
gunicorn -w 4 -b 0.0.0.0:5000 knowledge_base_api:app
```

## 安全注意事项

- 默认配置下，API服务仅允许访问指定类型的文件
- 在生产环境中，请考虑添加适当的身份验证和授权机制
- 建议配置防火墙规则，限制API服务的访问范围

## 扩展建议

- 添加API密钥认证
- 实现文件内容搜索功能
- 添加分页支持以处理大量文件
- 支持更多文件格式的转换

## 日志

API服务会在控制台输出运行日志，包括请求处理情况和错误信息。