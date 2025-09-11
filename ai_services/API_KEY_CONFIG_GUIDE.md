# API Key 配置指南

本知识库的AI服务功能需要配置OpenAI API Key才能正常使用。本指南将详细说明如何获取和配置API Key。

## 一、获取OpenAI API Key

1. 访问 [OpenAI官方网站](https://platform.openai.com/)
2. 登录或注册OpenAI账号
3. 点击右上角头像，选择 "View API keys"
4. 点击 "Create new secret key" 按钮
5. 复制生成的API Key并妥善保管（关闭窗口后将无法再次查看）

## 二、配置方法（两种方式选其一）

### 方法一：配置文件方式（推荐）

1. 打开 `ai_services/config.json` 文件
2. 找到以下两处配置：
   ```json
   "api_key": "YOUR_OPENAI_API_KEY"
   ```
3. 将 `"YOUR_OPENAI_API_KEY"` 替换为您实际的OpenAI API Key
4. 保存文件

### 方法二：环境变量方式

1. 打开 `ai_services/.env` 文件（已自动创建）
2. 找到以下配置：
   ```
   OPENAI_API_KEY="您的OpenAI API Key"
   ```
3. 将 `"您的OpenAI API Key"` 替换为您实际的OpenAI API Key
4. 保存文件

## 三、两种配置方式的区别

- **优先级**：配置文件（config.json）中的API Key优先级高于环境变量（.env）
- **使用场景**：
  - 配置文件方式适合固定环境的部署
  - 环境变量方式适合开发环境或需要频繁切换API Key的场景
- **安全性**：两种方式都已被.gitignore保护，确保API Key不会被提交到代码仓库

## 四、验证配置是否成功

配置完成后，您可以运行以下命令来验证API Key是否配置成功：

```bash
python -m ai_services.test_basic
```

## 五、注意事项

1. 请妥善保管您的API Key，不要分享给他人
2. API Key有使用额度限制，请定期检查您的OpenAI账号使用情况
3. 如果遇到API调用错误，请检查API Key是否正确配置，以及是否有足够的使用额度
4. 如需更新API Key，只需修改相应的配置文件并重启服务即可

如有任何问题，请参考项目中的 `ai_services/README.md` 文件或联系技术支持。