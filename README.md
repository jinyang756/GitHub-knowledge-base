# GitHub知识库

## 项目介绍

这是一个基于 **Docsify** 构建的个人知识库系统，用于整理、分享和管理技术文档和学习笔记。该项目已成功部署到GitHub Pages，可以通过仓库的GitHub Pages链接访问。

## 技术特点

- **轻量级文档系统**：使用Docsify构建，无需编译即可运行
- **响应式设计**：适配不同屏幕尺寸的设备
- **丰富的功能**：支持代码高亮、搜索、图片缩放、代码复制等功能
- **易于扩展**：简单的Markdown语法即可创建和维护文档
- **GitHub集成**：直接部署到GitHub Pages，便于分享和协作

## 快速开始

### 前提条件
- 安装Node.js
- 安装docsify-cli：`npm i docsify-cli -g`

### 本地预览

```bash
# 克隆仓库
git clone https://github.com/jinyang756/GitHub-knowledge-base.git

# 进入项目目录
cd GitHub-knowledge-base

# 启动本地服务器
docsify serve docs

# 访问 http://localhost:3000 查看文档
```

## 目录结构

```
├── docs/              # Docsify文档根目录
│   ├── .nojekyll      # 阻止GitHub Pages忽略下划线开头的文件
│   ├── README.md      # 主页内容
│   ├── _coverpage.md  # 封面页配置
│   ├── _sidebar.md    # 侧边栏导航配置
│   ├── index.html     # Docsify主配置文件
│   └── 技术/          # 技术文档分类目录
│       └── Python.md  # Python技术文档
├── vuepress-starter/  # 历史VuePress项目目录（已不再使用）
└── README.md          # 项目说明文件（当前文件）
```

## 部署说明

该项目已配置为自动部署到GitHub Pages。部署时：
1. GitHub Pages会自动识别根目录下的`docs`文件夹
2. `.nojekyll`文件确保GitHub Pages不会忽略下划线开头的文件
3. 所有内容会被托管为静态网站

## 贡献指南

1. Fork本仓库
2. 创建新的分支：`git checkout -b feature/your-feature-name`
3. 提交更改：`git commit -am 'Add some feature'`
4. 推送到分支：`git push origin feature/your-feature-name`
5. 提交Pull Request

## License

MIT License