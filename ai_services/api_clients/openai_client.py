#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""OpenAI大模型客户端实现"""

import os
from typing import Dict, List, Optional, Union

from ai_services.api_clients.base_llm_client import BaseLLMClient

# 尝试导入openai库
try:
    import openai
except ImportError:
    print("Warning: openai library not found. Please install it with 'pip install openai'")
    
    # 创建一个模拟的openai模块用于开发
    class MockOpenAI:
        class OpenAI:
            def __init__(self, api_key=None):
                self.api_key = api_key
                
            def chat_completions(self):
                class MockChatCompletions:
                    def create(self, **kwargs):
                        return MockCompletion()
                return MockChatCompletions()
                
            def embeddings(self):
                class MockEmbeddings:
                    def create(self, **kwargs):
                        return MockEmbeddingResponse()
                return MockEmbeddings()
    
    class MockCompletion:
        class Choice:
            message = {"content": "这是一条模拟的响应内容。"}
        choices = [Choice()]
    
    class MockEmbeddingResponse:
        class Data:
            embedding = [0.1] * 1536  # 模拟1536维向量
        data = [Data()]
    
    openai = MockOpenAI()


class OpenAIClient(BaseLLMClient):
    """OpenAI大模型客户端实现"""

    def _initialize(self):
        """初始化OpenAI客户端"""
        # 从配置或环境变量获取API密钥
        self.api_key = self.config.get('api_key', os.environ.get('OPENAI_API_KEY'))
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Please provide it in config or set OPENAI_API_KEY environment variable.")
        
        # 初始化客户端
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # 设置默认模型
        self.default_model = self.config.get('model', 'gpt-3.5-turbo')
        self.embedding_model = self.config.get('embedding_model', 'text-embedding-3-small')

    def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """使用OpenAI模型生成文本
        
        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词（可选）
            max_tokens: 最大生成的token数
            temperature: 生成温度，控制随机性
            **kwargs: 其他模型参数
            
        Returns:
            str: 生成的文本
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # 合并参数
        params = {
            "model": kwargs.pop('model', self.default_model),
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            **kwargs
        }
        
        response = self.client.chat_completions.create(**params)
        return response.choices[0].message["content"]

    def generate_embedding(
        self,
        text: str,
        **kwargs
    ) -> List[float]:
        """使用OpenAI模型生成文本嵌入向量
        
        Args:
            text: 输入文本
            **kwargs: 其他参数
            
        Returns:
            List[float]: 嵌入向量
        """
        params = {
            "model": kwargs.pop('model', self.embedding_model),
            "input": text
        }
        
        response = self.client.embeddings.create(**params)
        return response.data[0].embedding

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """OpenAI多轮对话完成
        
        Args:
            messages: 消息列表，每个消息包含role和content
            max_tokens: 最大生成的token数
            temperature: 生成温度，控制随机性
            **kwargs: 其他模型参数
            
        Returns:
            str: 生成的回复内容
        """
        params = {
            "model": kwargs.pop('model', self.default_model),
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            **kwargs
        }
        
        response = self.client.chat_completions.create(**params)
        return response.choices[0].message["content"]

    def batch_generate(
        self,
        prompts: List[str],
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> List[str]:
        """批量生成文本
        
        Args:
            prompts: 提示词列表
            system_prompt: 系统提示词（可选）
            max_tokens: 最大生成的token数
            temperature: 生成温度，控制随机性
            **kwargs: 其他模型参数
            
        Returns:
            List[str]: 生成的文本列表
        """
        results = []
        for prompt in prompts:
            result = self.generate_text(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )
            results.append(result)
        return results