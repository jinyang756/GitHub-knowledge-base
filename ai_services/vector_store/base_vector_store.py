#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""向量存储客户端基础接口"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Union


class VectorStoreDocument:
    """向量存储文档类"""
    
    def __init__(self, id: str, content: str, metadata: Optional[Dict] = None, embedding: Optional[List[float]] = None):
        self.id = id
        self.content = content
        self.metadata = metadata or {}
        self.embedding = embedding


class BaseVectorStore(ABC):
    """向量存储的抽象基类，定义统一接口"""

    def __init__(self, **kwargs):
        """初始化向量存储
        
        Args:
            **kwargs: 向量存储配置参数
        """
        self.config = kwargs
        self._initialize()

    @abstractmethod
    def _initialize(self):
        """初始化具体的向量存储"""
        pass

    @abstractmethod
    def add_document(
        self,
        document: VectorStoreDocument
    ) -> str:
        """添加单个文档到向量存储
        
        Args:
            document: 要添加的文档
            
        Returns:
            str: 文档ID
        """
        pass

    @abstractmethod
    def add_documents(
        self,
        documents: List[VectorStoreDocument]
    ) -> List[str]:
        """批量添加文档到向量存储
        
        Args:
            documents: 要添加的文档列表
            
        Returns:
            List[str]: 文档ID列表
        """
        pass

    @abstractmethod
    def search(
        self,
        query: str,
        embedding: Optional[List[float]] = None,
        top_k: int = 5,
        filters: Optional[Dict] = None
    ) -> List[Tuple[VectorStoreDocument, float]]:
        """搜索相似文档
        
        Args:
            query: 搜索查询
            embedding: 查询向量（可选，如不提供则自动生成）
            top_k: 返回的最大结果数
            filters: 筛选条件（可选）
            
        Returns:
            List[Tuple[VectorStoreDocument, float]]: 文档和相似度分数的列表
        """
        pass

    @abstractmethod
    def get_document(
        self,
        document_id: str
    ) -> Optional[VectorStoreDocument]:
        """获取指定ID的文档
        
        Args:
            document_id: 文档ID
            
        Returns:
            Optional[VectorStoreDocument]: 文档对象，如果不存在则返回None
        """
        pass

    @abstractmethod
    def delete_document(
        self,
        document_id: str
    ) -> bool:
        """删除指定ID的文档
        
        Args:
            document_id: 文档ID
            
        Returns:
            bool: 是否删除成功
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """清空向量存储"""
        pass

    @abstractmethod
    def save(self, path: str) -> None:
        """保存向量存储到文件
        
        Args:
            path: 保存路径
        """
        pass

    @abstractmethod
    def load(self, path: str) -> None:
        """从文件加载向量存储
        
        Args:
            path: 加载路径
        """
        pass

    def count(self) -> int:
        """获取向量存储中的文档数量
        
        Returns:
            int: 文档数量
        """
        # 这个方法可以在具体实现中被重写以提高效率
        documents = self.list_documents()
        return len(documents)

    def list_documents(self) -> List[VectorStoreDocument]:
        """列出所有文档
        
        Returns:
            List[VectorStoreDocument]: 文档列表
        """
        # 注意：这个方法在大型向量存储中可能会很耗时，具体实现中应当谨慎使用
        raise NotImplementedError("list_documents() is not implemented")