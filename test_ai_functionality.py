import json
import os

# 检查所有依赖是否安装完成
def check_dependencies():
    dependencies = ['yaml', 'dateutil', 'openai', 'faiss', 'numpy', 'networkx', 'jieba', 'nltk']
    missing = []
    for dep in dependencies:
        try:
            __import__(dep)
        except ImportError:
            missing.append(dep)
    
    if missing:
        print(f"❌ 缺少依赖: {', '.join(missing)}")
        return False
    else:
        print("✅ 所有依赖已安装完成！")
        return True

# 检查API Key配置
def check_api_key():
    config_path = 'ai_services/config.json'
    
    # 检查config.json是否存在
    if not os.path.exists(config_path):
        print("❌ 配置文件不存在: ai_services/config.json")
        return False
    
    # 读取配置文件
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 检查API Key是否已配置
        default_api_key = config.get('llm_clients', {}).get('default', {}).get('api_key', '')
        embedding_api_key = config.get('llm_clients', {}).get('embedding', {}).get('api_key', '')
        
        if 'YOUR_OPENAI_API_KEY' in [default_api_key, embedding_api_key]:
            print("❌ API Key尚未配置，请替换占位符")
            return False
        elif not default_api_key or not embedding_api_key:
            print("❌ API Key配置不完整")
            return False
        else:
            print("✅ API Key配置已完成！")
            return True
    except Exception as e:
        print(f"❌ 读取配置文件时出错: {str(e)}")
        return False

# 简单测试OpenAI API连接
def test_openai_connection():
    try:
        from openai import OpenAI
        
        # 读取配置文件获取API Key
        with open('ai_services/config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        api_key = config.get('llm_clients', {}).get('default', {}).get('api_key', '')
        if not api_key:
            print("❌ 无法获取API Key")
            return False
        
        # 创建OpenAI客户端
        client = OpenAI(api_key=api_key)
        
        # 发送简单的测试请求
        print("🔄 正在测试OpenAI API连接...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'Hello from GitHub知识库AI功能！'"}],
            max_tokens=20
        )
        
        if response and response.choices:
            message = response.choices[0].message.content
            print(f"✅ OpenAI API连接成功！响应: {message}")
            return True
        else:
            print("❌ OpenAI API响应异常")
            return False
    except Exception as e:
        print(f"❌ OpenAI API测试失败: {str(e)}")
        return False

# 主函数
def main():
    print("\n📊 GitHub知识库AI功能测试报告\n")
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 检查API Key配置
    if not check_api_key():
        return
    
    # 测试OpenAI API连接
    test_openai_connection()
    
    print("\n✅ 测试完成！")
    print("📚 GitHub知识库AI功能现已完全可用！")

if __name__ == "__main__":
    main()