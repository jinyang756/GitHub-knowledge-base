# DOCX 到 Markdown 转换工具

这是一个简单易用的Python脚本，用于将Microsoft Word的DOCX文件自动转换为Markdown格式文档。该工具特别适合需要将Word文档整理到知识库系统中的用户，可以帮助您快速完成文档格式的转换工作。

## 功能特点

- **自动转换标题层级**：识别Word文档中的标题样式，自动转换为相应级别的Markdown标题
- **支持列表格式**：转换项目符号列表和编号列表
- **表格转换**：将Word表格转换为Markdown表格格式
- **引用格式转换**：支持引用样式的转换
- **命令行界面**：简单直观的命令行操作方式
- **批处理能力**：支持单个文件的转换

## 安装要求

使用本工具前，需要安装以下Python库：

- python-docx：用于读取和解析DOCX文件

您可以使用pip安装所需依赖：

```bash
pip install python-docx
```

## 使用方法

### 基本用法

在命令行中运行以下命令：

```bash
python docx_to_markdown.py 输入文件.docx
```

这将在与输入文件相同的目录下生成一个同名的Markdown文件。

### 指定输出文件

您也可以指定输出文件的路径和名称：

```bash
python docx_to_markdown.py 输入文件.docx 输出文件.md
```

### 查看帮助信息

```bash
python docx_to_markdown.py --help
```

## 示例

假设您有一个名为"报告.docx"的文件，想要转换为Markdown格式：

```bash
# 默认输出名称（报告.md）
python docx_to_markdown.py 报告.docx

# 指定输出名称
python docx_to_markdown.py 报告.docx 我的报告.md
```

## 转换规则

工具会按照以下规则进行文档转换：

- **标题**：Word中的"Heading 1"到"Heading 6"样式会被转换为Markdown的`#`到`######`标题
- **列表**：项目符号列表转换为`* `前缀的列表，编号列表统一转换为`1. `前缀的列表
- **表格**：保留表格结构，转换为Markdown表格格式
- **引用**：带有引用样式的段落会被转换为`> `前缀的引用格式
- **代码块**：带有代码样式的段落会被转换为Markdown代码块（这是一个简化处理）

## 注意事项

1. 本工具主要支持标准的Word文档格式，对于特别复杂或包含特殊格式的文档，可能需要手动调整转换后的Markdown内容
2. 图片转换功能尚未实现，转换后的Markdown文件中不会包含原文档中的图片
3. 复杂的格式如脚注、尾注、交叉引用等可能无法完全保留
4. 对于特别长的文档，转换可能需要一定时间

## 进阶使用

### 与知识库集成

您可以将此工具与知识库系统结合使用，例如在添加新文档到知识库前，先用此工具将DOCX文件转换为Markdown格式：

```bash
# 1. 转换文档
python docx_to_markdown.py 新文档.docx docs/分类/新文档.md

# 2. 更新知识库导航
# （手动或通过其他脚本更新_sidebar.md文件）

# 3. 提交更改到版本控制系统
git add docs/分类/新文档.md docs/_sidebar.md
git commit -m "添加新文档"
git push
```

### 批量转换（扩展建议）

如果您需要批量转换多个DOCX文件，可以基于此脚本进行扩展，添加批量处理功能。例如：

```python
import os
import glob

for docx_file in glob.glob('*.docx'):
    convert_docx_to_markdown(docx_file)
```

## 故障排除

如果在使用过程中遇到问题，请检查以下几点：

1. 确保已正确安装python-docx库
2. 检查输入的DOCX文件路径是否正确
3. 确认您有足够的权限读取输入文件和写入输出文件
4. 对于特别复杂的文档，可能需要尝试简化文档结构后再进行转换

## 贡献指南

如果您有任何改进建议或发现了bug，欢迎提交Issue或Pull Request来帮助改进这个工具。

## License

[MIT License](LICENSE)