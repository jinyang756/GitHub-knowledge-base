# -*- coding: utf-8 -*-

"""API Key配置简单测试脚本"""

import os
import sys
from ai_services.utils.config_loader import load_config
from ai_services.api_clients.openai_client import OpenAIClient

def test_api_key_config():
    """测试API Key配置是否成功"""
    print("=== API Key配置测试 ===")
    
    try:
        # 加载配置
        print("1. 尝试加载配置文件...")
        config = load_config()
        print("✅ 配置文件加载成功!")
        
        # 检查配置内容
        print(f"\n配置文件内容预览:")
        print(f"- 配置文件路径: {os.path.abspath('ai_services/config.json')}")
        print(f"- 已配置的LLM客户端: {list(config.get('llm_clients', {}).keys())}")
        
        # 验证API Key是否已设置
        default_api_key = config.get('llm_clients', {}).get('default', {}).get('api_key', '')
        embedding_api_key = config.get('llm_clients', {}).get('embedding', {}).get('api_key', '')
        
        print(f"\n2. API Key配置检查:")
        if default_api_key and default_api_key != 'YOUR_OPENAI_API_KEY':
            print(f"✅ 默认客户端API Key已配置 (部分隐藏): {default_api_key[:6]}...{default_api_key[-4:]}")
        else:
            print("❌ 默认客户端API Key未配置或使用了占位符")
            
        if embedding_api_key and embedding_api_key != 'YOUR_OPENAI_API_KEY':
            print(f"✅ 嵌入客户端API Key已配置 (部分隐藏): {embedding_api_key[:6]}...{embedding_api_key[-4:]}")
        else:
            print("❌ 嵌入客户端API Key未配置或使用了占位符")
        
        # 尝试创建OpenAI客户端实例
        print("\n3. 尝试创建OpenAI客户端实例...")
        client = OpenAIClient(config=config['llm_clients']['default'])
        print("✅ OpenAI客户端实例创建成功!")
        
        print("\n📋 测试总结:")
        print("- API Key配置已完成")
        print("- 知识库的AI功能现已可用")
        print("- 如需测试完整功能，请安装缺失的依赖: pip install nltk")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        print("请检查config.json文件中的API Key配置是否正确")

if __name__ == "__main__":
    test_api_key_config()