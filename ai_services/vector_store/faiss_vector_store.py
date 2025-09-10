#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""FAISS向量存储实现"""

import json
import os
from typing import Dict, List, Optional, Tuple, Union

from ai_services.vector_store.base_vector_store import BaseVectorStore, VectorStoreDocument

# 尝试导入faiss库
try:
    import faiss
except ImportError:
    print("Warning: faiss library not found. Please install it with 'pip install faiss-cpu'")
    
    # 创建一个模拟的faiss模块用于开发
    class MockFAISS:
        class IndexFlatL2:
            def __init__(self, dimension):
                self.dimension = dimension
                self.vectors = []
                self.ids = []
                
            def add(self, vectors):
                for vector in vectors:
                    self.vectors.append(vector)
                
            def search(self, query_vector, k):
                # 简单模拟搜索，返回前k个向量
                import numpy as np
                distances = np.random.rand(k).tolist()
                indices = list(range(min(k, len(self.vectors))))
                return np.array(distances), np.array(indices)
                
            def remove_ids(self, ids):
                # 简单模拟删除
                for id in ids:
                    if id in self.ids:
                        index = self.ids.index(id)
                        self.ids.pop(index)
                        self.vectors.pop(index)
    
    faiss = MockFAISS()

# 尝试导入numpy库
try:
    import numpy as np
except ImportError:
    print("Warning: numpy library not found. Please install it with 'pip install numpy'")
    
    # 创建一个简单的模拟numpy模块
    class MockNumPy:
        def array(self, data):
            return data
        
        def random(self):
            class Random:
                def rand(self, n):
                    return [0.1] * n
            return Random()
    
    np = MockNumPy()


class FAISSVectorStore(BaseVectorStore):
    """基于FAISS的向量存储实现"""

    def _initialize(self):
        """初始化FAISS向量存储"""
        # 获取维度信息
        self.dimension = self.config.get('dimension', 1536)  # 默认使用OpenAI embedding的维度
        
        # 初始化FAISS索引
        self.index = faiss.IndexFlatL2(self.dimension)  # 使用L2距离
        
        # 存储文档ID到内容的映射
        self.id_to_doc = {}
        
        # 存储文档ID到元数据的映射
        self.id_to_metadata = {}
        
        # 获取嵌入模型（可选）
        self.embedding_model = self.config.get('embedding_model')

    def add_document(
        self,
        document: VectorStoreDocument
    ) -> str:
        """添加单个文档到FAISS向量存储
        
        Args:
            document: 要添加的文档
            
        Returns:
            str: 文档ID
        """
        # 如果没有提供嵌入向量，尝试使用嵌入模型生成
        if document.embedding is None and self.embedding_model:
            document.embedding = self.embedding_model.generate_embedding(document.content)
        
        if document.embedding is None:
            raise ValueError("Document embedding is required")
        
        # 添加向量到FAISS索引
        vector_np = np.array([document.embedding], dtype=np.float32)
        self.index.add(vector_np)
        
        # 存储文档信息
        self.id_to_doc[document.id] = document.content
        if document.metadata:
            self.id_to_metadata[document.id] = document.metadata
        
        return document.id

    def add_documents(
        self,
        documents: List[VectorStoreDocument]
    ) -> List[str]:
        """批量添加文档到FAISS向量存储
        
        Args:
            documents: 要添加的文档列表
            
        Returns:
            List[str]: 文档ID列表
        """
        document_ids = []
        vectors = []
        
        # 准备向量和ID
        for doc in documents:
            # 如果没有提供嵌入向量，尝试使用嵌入模型生成
            if doc.embedding is None and self.embedding_model:
                doc.embedding = self.embedding_model.generate_embedding(doc.content)
            
            if doc.embedding is None:
                raise ValueError(f"Document embedding is required for document {doc.id}")
            
            vectors.append(doc.embedding)
            document_ids.append(doc.id)
            
            # 存储文档信息
            self.id_to_doc[doc.id] = doc.content
            if doc.metadata:
                self.id_to_metadata[doc.id] = doc.metadata
        
        # 批量添加向量到FAISS索引
        vectors_np = np.array(vectors, dtype=np.float32)
        self.index.add(vectors_np)
        
        return document_ids

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
        # 如果没有提供查询向量，尝试使用嵌入模型生成
        if embedding is None and self.embedding_model:
            embedding = self.embedding_model.generate_embedding(query)
        
        if embedding is None:
            raise ValueError("Query embedding is required")
        
        # 执行搜索
        query_vector = np.array([embedding], dtype=np.float32)
        distances, indices = self.index.search(query_vector, min(top_k, self.index.ntotal))
        
        # 准备结果
        results = []
        document_ids = list(self.id_to_doc.keys())
        
        for i, idx in enumerate(indices[0]):
            if 0 <= idx < len(document_ids):
                doc_id = document_ids[idx]
                content = self.id_to_doc[doc_id]
                metadata = self.id_to_metadata.get(doc_id, {})
                
                # 应用筛选条件
                if filters and not self._match_filters(metadata, filters):
                    continue
                
                document = VectorStoreDocument(
                    id=doc_id,
                    content=content,
                    metadata=metadata
                )
                results.append((document, distances[0][i]))
        
        return results

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
        if document_id not in self.id_to_doc:
            return None
        
        return VectorStoreDocument(
            id=document_id,
            content=self.id_to_doc[document_id],
            metadata=self.id_to_metadata.get(document_id, {})
        )

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
        if document_id not in self.id_to_doc:
            return False
        
        # 在FAISS中删除向量（注意：FAISS的IndexFlatL2不直接支持按ID删除，这里需要重建索引）
        # 实际应用中，可能需要使用FAISS的IndexIDMap包装器来支持按ID删除
        # 这里我们简化处理，只从映射中删除
        del self.id_to_doc[document_id]
        if document_id in self.id_to_metadata:
            del self.id_to_metadata[document_id]
        
        # 重建索引
        self._rebuild_index()
        
        return True

    def clear(self) -> None:
        """清空向量存储"""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.id_to_doc.clear()
        self.id_to_metadata.clear()

    def save(self, path: str) -> None:
        """保存向量存储到文件
        
        Args:
            path: 保存路径
        """
        # 确保目录存在
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # 保存FAISS索引
        index_path = f"{path}_index.faiss"
        faiss.write_index(self.index, index_path)
        
        # 保存文档映射
        data = {
            'id_to_doc': self.id_to_doc,
            'id_to_metadata': self.id_to_metadata,
            'dimension': self.dimension
        }
        
        with open(f"{path}_data.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self, path: str) -> None:
        """从文件加载向量存储
        
        Args:
            path: 加载路径
        """
        # 加载FAISS索引
        index_path = f"{path}_index.faiss"
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
        
        # 加载文档映射
        data_path = f"{path}_data.json"
        if os.path.exists(data_path):
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.id_to_doc = data.get('id_to_doc', {})
            self.id_to_metadata = data.get('id_to_metadata', {})
            self.dimension = data.get('dimension', 1536)

    def count(self) -> int:
        """获取向量存储中的文档数量
        
        Returns:
            int: 文档数量
        """
        return len(self.id_to_doc)

    def _match_filters(self, metadata: Dict, filters: Dict) -> bool:
        """检查元数据是否匹配筛选条件
        
        Args:
            metadata: 文档元数据
            filters: 筛选条件
            
        Returns:
            bool: 是否匹配
        """
        for key, value in filters.items():
            if key not in metadata or metadata[key] != value:
                return False
        return True

    def _rebuild_index(self) -> None:
        """重建FAISS索引"""
        # 这是一个简化的实现，实际应用中应该使用更高效的方法
        self.index = faiss.IndexFlatL2(self.dimension)
        document_ids = list(self.id_to_doc.keys())
        
        # 注意：这里假设文档内容中存储了嵌入向量
        # 在实际应用中，应该单独存储嵌入向量或能够重新生成它们