# GitHub知识库

## 项目介绍

这是一个基于 **Docsify** 构建的个人知识库系统，用于整理、分享和管理各类技术文档、学习笔记和行业知识。该项目采用轻量级架构设计，无需编译即可运行，已成功部署到GitHub Pages平台。

## 主要功能

- **轻量级文档系统**：基于Docsify构建，无需编译，即时更新
- **响应式设计**：完美适配桌面、平板和移动设备
- **丰富的文档特性**：支持代码高亮、全文搜索、图片缩放、代码复制等功能
- **简洁的Markdown语法**：使用简单的Markdown语法即可创建和维护专业文档
- **分类管理**：支持多级目录结构，便于内容分类和管理
- **GitHub集成**：直接部署到GitHub Pages，支持版本控制和协作

## 快速开始

### 前提条件
- 安装Node.js环境
- 安装docsify-cli工具：`npm i docsify-cli -g`

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
│   ├── CONTRIBUTING.md # 贡献指南
│   ├── _coverpage.md  # 封面页配置
│   ├── _sidebar.md    # 侧边栏导航配置
│   ├── index.html     # Docsify主配置文件
│   ├── 国泰海通证券/    # 证券行业知识分类
│   │   └── README.md  # 证券分类说明
│   └── 技术/          # 技术文档分类目录
│       └── Python.md  # Python技术文档
├── .gitignore         # Git忽略配置
├── temp/              # 临时文件目录
├── vuepress-starter/  # 历史VuePress项目目录（已不再使用）
└── README.md          # 项目说明文件（当前文件）
```

## 文档分类

### 技术文档
- 包含各类编程语言、开发框架和工具的学习笔记
- 当前已收录Python相关技术文档

### 行业知识
- 包含特定行业的专业知识和研究资料
- 当前已收录国泰海通证券相关内容

## 部署指南

### GitHub Pages自动部署

该项目已配置为支持GitHub Pages自动部署：
1. 将项目推送到GitHub仓库后，在仓库设置中启用GitHub Pages
2. 选择`main branch / docs folder`作为来源
3. GitHub Pages会自动识别并部署docs目录中的内容
4. `.nojekyll`文件确保GitHub Pages不会忽略下划线开头的配置文件

### 自定义部署

如需部署到其他平台，可以：
1. 将docs目录中的所有文件复制到目标服务器
2. 配置Web服务器以正确提供静态文件
3. 确保服务器支持SPA路由（如果使用了路由功能）

## 文档编写指南

### 基本格式
- 使用标准Markdown语法编写文档
- 文件名使用英文或中文，扩展名必须为`.md`
- 重要内容请添加适当的标题层级，便于导航

### 内容规范
- 文档内容应保持专业性和准确性
- 添加适当的示例代码和截图以增强说明效果
- 对于重要概念，提供清晰的解释和实际应用场景

## 贡献指南

1. Fork本仓库到您的GitHub账号
2. 克隆Fork后的仓库到本地
3. 创建新的分支：`git checkout -b feature/your-feature-name`
4. 在docs目录下添加或修改文档
5. 提交更改：`git commit -am 'Add some feature'`
6. 推送到分支：`git push origin feature/your-feature-name`
7. 提交Pull Request到原仓库

详细贡献流程请参考[CONTRIBUTING.md](docs/CONTRIBUTING.md)文件。

## License

MIT License