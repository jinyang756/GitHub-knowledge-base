# 豆包AI云盘同步脚本使用指南

本文档详细介绍如何使用`sync_doubao_cloud.py`脚本将豆包AI云盘的内容自动同步到GitHub知识库的国泰海通证券目录。

## 功能概述

该脚本可以实现以下功能：

- 从豆包AI云盘下载指定目录的内容到本地国泰海通证券目录
- 自动检测文件更新并下载最新版本
- 可选地将同步后的更改自动提交到Git仓库
- 记录详细的同步日志，方便排查问题

## 前提条件

在使用此脚本之前，您需要准备以下内容：

1. 安装Python 3.6或更高版本
2. 安装必要的依赖包：`pip install requests`
3. 获取豆包AI云盘的API访问凭证（API Key、Secret Key等）
4. 确认您的GitHub仓库有正确的推送权限

## 配置脚本

在使用脚本之前，您需要编辑`sync_doubao_cloud.py`文件中的配置参数：

```python
# 豆包AI云盘API配置
DOUBAO_API_URL = "https://api.doubao.com/cloud-drive"  # 豆包AI云盘API地址
API_KEY = "YOUR_API_KEY_HERE"  # 您的API Key
SECRET_KEY = "YOUR_SECRET_KEY_HERE"  # 您的Secret Key
CLOUD_DIR_ID = "YOUR_CLOUD_DIRECTORY_ID"  # 要同步的云盘目录ID
```

此外，您还可以根据需要调整以下配置：

```python
# Git配置
ENABLE_GIT_COMMIT = True  # 是否自动提交到Git
```

## 使用方法

### 手动运行同步

在命令行中执行以下命令运行同步脚本：

```bash
# 在项目根目录下运行
python sync_doubao_cloud.py
```

### 设置定时自动同步

为了实现云盘内容更新时自动同步，您可以将脚本设置为定时任务。

#### Windows系统

1. 右键点击任务栏，选择"任务计划程序"
2. 点击"创建基本任务"
3. 按照向导设置任务名称和描述
4. 选择触发频率（如每天、每周或当计算机启动时）
5. 选择"启动程序"操作
6. 在"程序/脚本"中浏览并选择python.exe的路径
7. 在"添加参数"中输入`sync_doubao_cloud.py`
8. 在"起始于"中输入脚本所在的目录路径
9. 完成向导并启用任务

#### macOS/Linux系统

使用crontab设置定时任务：

```bash
# 打开crontab编辑器
crontab -e

# 添加定时任务（每小时执行一次）
0 * * * * cd /path/to/GitHub知识库 && python3 sync_doubao_cloud.py
```

## 日志查看

脚本执行的详细日志保存在项目根目录下的`sync_log.txt`文件中，您可以通过查看此文件了解同步过程和结果。

## 注意事项

1. 请妥善保管您的API密钥和凭证，不要将包含敏感信息的配置文件提交到公共仓库
2. 首次运行脚本时，建议先进行测试，确保配置正确
3. 如果同步的文件较大或数量较多，可能需要较长时间，请耐心等待
4. 定期检查同步日志，确保同步过程正常进行

## 常见问题

### Q: 同步失败，提示"获取云盘文件失败"
A: 请检查您的API配置是否正确，包括API URL、API Key和目录ID

### Q: 文件下载失败
A: 请确认您的网络连接正常，以及云盘文件是否存在且可访问

### Q: Git提交失败
A: 请确认您的Git仓库配置正确，并且有推送权限

### Q: 如何获取豆包AI云盘的API凭证
A: 请参考豆包AI云盘的官方文档或联系客服获取API访问权限

## 定制开发

如果您需要根据特定需求修改同步逻辑，可以编辑脚本中的以下关键函数：

- `get_cloud_files()`: 获取云盘文件列表的逻辑
- `download_file()`: 下载单个文件的逻辑
- `sync_cloud_to_local()`: 整体同步逻辑
- `commit_to_git()`: Git提交逻辑

如有任何问题或建议，请随时联系系统管理员。