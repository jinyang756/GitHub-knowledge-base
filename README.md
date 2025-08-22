# GitHub知识库

## 项目介绍

这是一个基于docsify构建的证券行业知识库，致力于为投资者和从业人员提供全面、专业、及时的证券市场信息、研究报告和投资策略。知识库采用前后端分离架构，前端使用docsify进行文档展示，支持搜索、主题切换、阅读进度等功能。

## 目录结构

知识库按照内容类型和主题进行分类，主要包括以下目录：

```
├── docs/              # Docsify文档根目录
│   ├── .nojekyll      # 阻止GitHub Pages忽略下划线开头的文件
│   ├── README.md      # 主页内容
│   ├── CONTRIBUTING.md # 贡献指南
│   ├── _coverpage.md  # 封面页配置
│   ├── _sidebar.md    # 侧边栏导航配置
│   ├── index.html     # Docsify主配置文件
│   ├── policy/        # 政策解读相关文档
│   ├── industry/      # 行业分析相关文档
│   ├── strategy/      # 投资策略相关文档
│   ├── risk/          # 风险管理相关文档
│   ├── 技术/          # 技术支持相关文档
│   ├── 国泰海通证券/    # 国泰海通证券相关报告
│   └── 荀玉根合集/     # 荀玉根分析师研究报告合集
├── .gitignore         # Git忽略配置
├── temp/              # 临时文件目录
└── README.md          # 项目说明文件（当前文件）
```

## 功能特点

1. **响应式设计**：适配PC端、平板和手机等多种设备
2. **搜索功能**：支持全文搜索，提供搜索建议和高亮显示
3. **主题切换**：支持亮色/暗黑模式，可根据系统设置自动切换
4. **阅读进度**：显示当前阅读进度，提升阅读体验
5. **代码高亮**：支持多种编程语言的代码高亮显示
6. **图片优化**：支持图片懒加载和点击放大查看
7. **导航优化**：清晰的目录结构和导航系统，方便查找内容

## 快速开始

### 本地预览

1. 确保安装了Node.js环境
2. 安装docsify-cli工具：`npm i docsify-cli -g`
3. 在项目根目录下运行：`docsify serve docs`
4. 打开浏览器访问：`http://localhost:3000`

### 文档编写规范

为了确保知识库内容的一致性和专业性，请遵循以下规范：

- **标题层级**：使用清晰的标题层级（#、##、###等）组织内容
- **重点标记**：对于核心观点、重要数据等，使用<span class="data-number">关键数据</span>样式进行标记
- **结构化表达**：尽量使用列表、表格等结构化形式呈现内容
- **数据来源**：引用的数据需注明来源和时间，确保信息准确性
- **代码规范**：代码示例应遵循行业标准规范，添加必要的注释说明

## 贡献指南

欢迎对知识库进行贡献，具体流程如下：

1. Fork本仓库
2. 创建新的分支：`git checkout -b feature/your-feature-name`
3. 在docs目录下添加或修改文档
4. 提交更改：`git commit -am 'Add some feature'`
5. 推送到远程：`git push origin feature/your-feature-name`
6. 创建Pull Request

详细贡献流程请参考[CONTRIBUTING.md](docs/CONTRIBUTING.md)文件。

## 部署说明

知识库可以部署到多种平台，推荐使用以下方式：

### Vercel部署

1. 登录Vercel账号
2. 导入GitHub仓库
3. 选择项目根目录
4. 配置构建命令：无需特殊配置，Vercel会自动识别docsify项目
5. 部署完成后，即可获得访问链接

### GitHub Pages部署

1. 在项目的Settings中，找到GitHub Pages选项
2. 选择docs目录作为发布源
3. 保存配置后，稍等片刻即可通过GitHub Pages访问

## 联系我们

如有任何问题或建议，请通过以下方式联系我们：

- Email：support@example.com
- GitHub Issues：提交问题和建议

## License

MIT License