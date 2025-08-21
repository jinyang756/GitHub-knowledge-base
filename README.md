# GitHub知识库

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
4. 在docs目录下添加或修改文档
5. 提交更改：`git commit -am 'Add some feature'`
6. 推送到分支：`git push origin feature/your-feature-name`
7. 提交Pull Request到原仓库

详细贡献流程请参考[CONTRIBUTING.md](docs/CONTRIBUTING.md)文件。

## License

MIT License