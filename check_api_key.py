# -*- coding: utf-8 -*-

"""API Key配置检查脚本"""

import json
import os

def check_api_key_config():
    """检查API Key配置是否成功"""
    print("=== API Key配置检查 ===")
    
    # 配置文件路径
    config_path = os.path.join('ai_services', 'config.json')
    
    try:
        # 检查文件是否存在
        if not os.path.exists(config_path):
            print(f"❌ 配置文件不存在: {config_path}")
            return
        
        print(f"1. 找到配置文件: {os.path.abspath(config_path)}")
        
        # 读取配置文件
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("✅ 配置文件读取成功!")
        
        # 检查LLM客户端配置
        llm_clients = config.get('llm_clients', {})
        if not llm_clients:
            print("❌ 配置文件中未找到llm_clients配置")
            return
        
        print(f"\n2. LLM客户端配置检查:")
        print(f"- 已配置的客户端: {list(llm_clients.keys())}")
        
        # 检查默认客户端API Key
        if 'default' in llm_clients:
            default_api_key = llm_clients['default'].get('api_key', '')
            if default_api_key and default_api_key != 'YOUR_OPENAI_API_KEY':
                print(f"✅ 默认客户端API Key已配置 (部分隐藏): {default_api_key[:6]}...{default_api_key[-4:]}")
            else:
                print("❌ 默认客户端API Key未配置或使用了占位符")
        else:
            print("❌ 未找到default客户端配置")
        
        # 检查embedding客户端API Key
        if 'embedding' in llm_clients:
            embedding_api_key = llm_clients['embedding'].get('api_key', '')
            if embedding_api_key and embedding_api_key != 'YOUR_OPENAI_API_KEY':
                print(f"✅ 嵌入客户端API Key已配置 (部分隐藏): {embedding_api_key[:6]}...{embedding_api_key[-4:]}")
            else:
                print("❌ 嵌入客户端API Key未配置或使用了占位符")
        else:
            print("❌ 未找到embedding客户端配置")
        
        # 检查.env文件
        env_path = os.path.join('ai_services', '.env')
        print(f"\n3. 环境变量文件检查:")
        if os.path.exists(env_path):
            print(f"✅ 找到.env文件: {os.path.abspath(env_path)}")
            print("   (注: 环境变量中的API Key优先级低于配置文件)")
        else:
            print("ℹ️ 未找到.env文件")
        
        # 总结
        print("\n📋 配置总结:")
        if all([default_api_key != 'YOUR_OPENAI_API_KEY' for default_api_key in [
                llm_clients.get('default', {}).get('api_key', '')
            ] if default_api_key]):
            print("✅ API Key配置已完成！")
            print("✅ 知识库的AI功能现已可用！")
        else:
            print("❌ API Key配置不完整，请检查config.json文件")
        
    except Exception as e:
        print(f"❌ 检查失败: {str(e)}")
        print("请手动检查config.json文件中的API Key配置是否正确")

if __name__ == "__main__":
    check_api_key_config()