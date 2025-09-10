#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""基础大模型客户端接口"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union


class BaseLLMClient(ABC):
    """大模型客户端的抽象基类，定义统一接口"""

    def __init__(self, **kwargs):
        """初始化客户端
        
        Args:
            **kwargs: 客户端配置参数
        """
        self.config = kwargs
        self._initialize()

    @abstractmethod
    def _initialize(self):
        """初始化具体的大模型客户端"""
        pass

    @abstractmethod
    def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """生成文本
        
        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词（可选）
            max_tokens: 最大生成的token数
            temperature: 生成温度，控制随机性
            **kwargs: 其他模型参数
            
        Returns:
            str: 生成的文本
        """
        pass

    @abstractmethod
    def generate_embedding(
        self,
        text: str,
        **kwargs
    ) -> List[float]:
        """生成文本嵌入向量
        
        Args:
            text: 输入文本
            **kwargs: 其他参数
            
        Returns:
            List[float]: 嵌入向量
        """
        pass

    @abstractmethod
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """多轮对话完成
        
        Args:
            messages: 消息列表，每个消息包含role和content
            max_tokens: 最大生成的token数
            temperature: 生成温度，控制随机性
            **kwargs: 其他模型参数
            
        Returns:
            str: 生成的回复内容
        """
        pass

    def generate_summary(
        self,
        text: str,
        max_length: int = 500,
        **kwargs
    ) -> str:
        """生成文本摘要
        
        Args:
            text: 要摘要的文本
            max_length: 摘要最大长度
            **kwargs: 其他参数
            
        Returns:
            str: 生成的摘要
        """
        summary_prompt = f"请为以下文本生成摘要，控制在{max_length}字以内：\n\n{text}"
        return self.generate_text(summary_prompt, **kwargs)

    def generate_qa(
        self,
        context: str,
        question: str,
        **kwargs
    ) -> str:
        """基于上下文回答问题
        
        Args:
            context: 上下文信息
            question: 问题
            **kwargs: 其他参数
            
        Returns:
            str: 回答内容
        """
        qa_prompt = f"基于以下上下文回答问题：\n\n上下文：{context}\n\n问题：{question}\n\n请直接给出答案，不要添加额外解释。"
        return self.generate_text(qa_prompt, **kwargs)

    def is_healthy(self) -> bool:
        """检查客户端是否健康
        
        Returns:
            bool: 是否健康
        """
        try:
            # 发送一个简单的请求测试连接
            self.generate_text("测试连接", max_tokens=10)
            return True
        except Exception:
            return False