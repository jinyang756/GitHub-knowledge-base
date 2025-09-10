#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AI服务主入口"""

import os
import sys

# 确保当前目录在Python路径中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入工具模块
from ai_services.utils import (
    # 配置加载
    load_config, get_config_value, save_config, 
    # 缓存管理
    cache_get, cache_set, cache_delete, cache_exists, cache_clear,
    # 错误处理
    handle_exception, catch_exceptions, validate_params,
    # 日志记录
    get_logger, debug, info, warning, error, critical, exception,
    # 时间工具
    now, format_datetime, parse_datetime, add_days, get_time_diff
)

# 导入核心服务模块
from ai_services.api_clients.base_llm_client import BaseLLMClient
from ai_services.api_clients.openai_client import OpenAIClient
from ai_services.vector_store.base_vector_store import BaseVectorStore, VectorStoreDocument
from ai_services.vector_store.faiss_vector_store import FAISSVectorStore
from ai_services.kg.base_knowledge_graph import BaseKnowledgeGraph, Entity, Relationship
from ai_services.kg.networkx_knowledge_graph import NetworkXKnowledgeGraph
from ai_services.nlp.text_processor import TextProcessor

# 导入异常类
from ai_services.utils import (
    AIServiceError,
    APIError,
    DataProcessingError,
    VectorStoreError,
    KnowledgeGraphError,
    NLPError
)


class AIService:
    """AI服务主类，整合所有AI服务功能"""
    
    def __init__(self, config_path: str = None):
        """初始化AI服务
        
        Args:
            config_path: 配置文件路径
        """
        # 加载配置
        self.config = {}
        if config_path and os.path.exists(config_path):
            self.config = load_config(config_path)
        
        # 创建日志记录器
        self.logger = get_logger('ai_service')
        
        # 初始化各服务组件
        self._llm_clients = {}
        self._vector_stores = {}
        self._knowledge_graphs = {}
        self._text_processors = {}
        
        # 初始化默认组件
        self._init_default_components()
        
        self.logger.info("AI service initialized successfully")
    
    def _init_default_components(self) -> None:
        """初始化默认组件"""
        # 初始化默认文本处理器
        try:
            self.get_text_processor('default')
        except Exception as e:
            self.logger.error(f"Failed to initialize default text processor: {e}")
        
        # 尝试从配置初始化其他组件
        try:
            if 'llm_clients' in self.config:
                for name, client_config in self.config['llm_clients'].items():
                    try:
                        self.get_llm_client(name, **client_config)
                    except Exception as e:
                        self.logger.error(f"Failed to initialize LLM client '{name}': {e}")
            
            if 'vector_stores' in self.config:
                for name, store_config in self.config['vector_stores'].items():
                    try:
                        self.get_vector_store(name, **store_config)
                    except Exception as e:
                        self.logger.error(f"Failed to initialize vector store '{name}': {e}")
            
            if 'knowledge_graphs' in self.config:
                for name, kg_config in self.config['knowledge_graphs'].items():
                    try:
                        self.get_knowledge_graph(name, **kg_config)
                    except Exception as e:
                        self.logger.error(f"Failed to initialize knowledge graph '{name}': {e}")
        except Exception as e:
            self.logger.error(f"Error initializing components from config: {e}")
    
    def get_llm_client(
        self, 
        name: str = 'default', 
        provider: str = 'openai',
        **kwargs
    ) -> BaseLLMClient:
        """获取或创建大模型客户端
        
        Args:
            name: 客户端名称
            provider: 大模型提供商
            **kwargs: 客户端初始化参数
            
        Returns:
            BaseLLMClient: 大模型客户端实例
        """
        # 检查缓存
        if name in self._llm_clients:
            return self._llm_clients[name]
        
        # 创建新客户端
        client = None
        if provider.lower() == 'openai':
            client = OpenAIClient(**kwargs)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
        
        # 缓存客户端
        self._llm_clients[name] = client
        self.logger.info(f"LLM client '{name}' created with provider '{provider}'")
        
        return client
    
    def get_vector_store(
        self, 
        name: str = 'default', 
        provider: str = 'faiss',
        **kwargs
    ) -> BaseVectorStore:
        """获取或创建向量存储
        
        Args:
            name: 向量存储名称
            provider: 向量存储提供商
            **kwargs: 向量存储初始化参数
            
        Returns:
            BaseVectorStore: 向量存储实例
        """
        # 检查缓存
        if name in self._vector_stores:
            return self._vector_stores[name]
        
        # 创建新向量存储
        vector_store = None
        if provider.lower() == 'faiss':
            vector_store = FAISSVectorStore(**kwargs)
        else:
            raise ValueError(f"Unsupported vector store provider: {provider}")
        
        # 缓存向量存储
        self._vector_stores[name] = vector_store
        self.logger.info(f"Vector store '{name}' created with provider '{provider}'")
        
        return vector_store
    
    def get_knowledge_graph(
        self, 
        name: str = 'default', 
        provider: str = 'networkx',
        **kwargs
    ) -> BaseKnowledgeGraph:
        """获取或创建知识图谱
        
        Args:
            name: 知识图谱名称
            provider: 知识图谱提供商
            **kwargs: 知识图谱初始化参数
            
        Returns:
            BaseKnowledgeGraph: 知识图谱实例
        """
        # 检查缓存
        if name in self._knowledge_graphs:
            return self._knowledge_graphs[name]
        
        # 创建新知识图谱
        knowledge_graph = None
        if provider.lower() == 'networkx':
            knowledge_graph = NetworkXKnowledgeGraph(**kwargs)
        else:
            raise ValueError(f"Unsupported knowledge graph provider: {provider}")
        
        # 缓存知识图谱
        self._knowledge_graphs[name] = knowledge_graph
        self.logger.info(f"Knowledge graph '{name}' created with provider '{provider}'")
        
        return knowledge_graph
    
    def get_text_processor(
        self, 
        name: str = 'default',
        **kwargs
    ) -> TextProcessor:
        """获取或创建文本处理器
        
        Args:
            name: 文本处理器名称
            **kwargs: 文本处理器初始化参数
            
        Returns:
            TextProcessor: 文本处理器实例
        """
        # 检查缓存
        if name in self._text_processors:
            return self._text_processors[name]
        
        # 创建新文本处理器
        text_processor = TextProcessor(**kwargs)
        
        # 缓存文本处理器
        self._text_processors[name] = text_processor
        self.logger.info(f"Text processor '{name}' created")
        
        return text_processor
    
    def process_text(
        self, 
        text: str,
        operations: list = None,
        processor_name: str = 'default'
    ) -> dict:
        """处理文本
        
        Args:
            text: 要处理的文本
            operations: 要执行的操作列表
            processor_name: 文本处理器名称
            
        Returns:
            dict: 处理结果
        """
        if operations is None:
            operations = ['clean', 'segment', 'extract_keywords']
        
        processor = self.get_text_processor(processor_name)
        results = {'original_text': text}
        
        try:
            for op in operations:
                if op == 'clean':
                    results['clean_text'] = processor.clean_text(text)
                elif op == 'segment':
                    results['segments'] = processor.segment_text(
                        results.get('clean_text', text)
                    )
                elif op == 'extract_keywords':
                    results['keywords'] = processor.extract_keywords(
                        results.get('clean_text', text)
                    )
                elif op == 'extract_entities':
                    results['entities'] = processor.extract_entities(
                        results.get('clean_text', text)
                    )
                elif op == 'summarize':
                    results['summary'] = processor.summarize(
                        results.get('clean_text', text)
                    )
                elif op == 'split_sentences':
                    results['sentences'] = processor.split_sentences(
                        results.get('clean_text', text)
                    )
            
            self.logger.info(f"Text processed with operations: {', '.join(operations)}")
        except Exception as e:
            self.logger.error(f"Error processing text: {e}")
            raise
        
        return results
    
    def generate_text(
        self, 
        prompt: str,
        client_name: str = 'default',
        **kwargs
    ) -> str:
        """生成文本
        
        Args:
            prompt: 提示词
            client_name: 大模型客户端名称
            **kwargs: 生成参数
            
        Returns:
            str: 生成的文本
        """
        try:
            client = self.get_llm_client(client_name)
            result = client.generate_text(prompt, **kwargs)
            self.logger.info(f"Text generated with client '{client_name}'")
            return result
        except Exception as e:
            self.logger.error(f"Error generating text: {e}")
            raise
    
    def search_documents(
        self, 
        query: str,
        vector_store_name: str = 'default',
        k: int = 5,
        **kwargs
    ) -> list:
        """搜索文档
        
        Args:
            query: 搜索查询
            vector_store_name: 向量存储名称
            k: 返回的结果数量
            **kwargs: 搜索参数
            
        Returns:
            list: 搜索结果列表
        """
        try:
            vector_store = self.get_vector_store(vector_store_name)
            results = vector_store.search(query, k=k, **kwargs)
            self.logger.info(f"Documents searched with vector store '{vector_store_name}', found {len(results)} results")
            return results
        except Exception as e:
            self.logger.error(f"Error searching documents: {e}")
            raise
    
    def add_document_to_vector_store(
        self, 
        document: dict, 
        vector_store_name: str = 'default',
        **kwargs
    ) -> str:
        """添加文档到向量存储
        
        Args:
            document: 文档数据
            vector_store_name: 向量存储名称
            **kwargs: 添加参数
            
        Returns:
            str: 文档ID
        """
        try:
            # 转换为VectorStoreDocument
            vs_document = VectorStoreDocument(
                id=document.get('id'),
                content=document.get('content', ''),
                metadata=document.get('metadata', {})
            )
            
            vector_store = self.get_vector_store(vector_store_name)
            doc_id = vector_store.add_document(vs_document, **kwargs)
            self.logger.info(f"Document added to vector store '{vector_store_name}': {doc_id}")
            return doc_id
        except Exception as e:
            self.logger.error(f"Error adding document to vector store: {e}")
            raise
    
    def add_entity_to_knowledge_graph(
        self, 
        entity_data: dict,
        kg_name: str = 'default'
    ) -> str:
        """添加实体到知识图谱
        
        Args:
            entity_data: 实体数据
            kg_name: 知识图谱名称
            
        Returns:
            str: 实体ID
        """
        try:
            # 创建实体对象
            entity = Entity(
                id=entity_data.get('id'),
                type=entity_data.get('type', 'entity'),
                properties=entity_data.get('properties', {})
            )
            
            kg = self.get_knowledge_graph(kg_name)
            entity_id = kg.add_entity(entity)
            self.logger.info(f"Entity added to knowledge graph '{kg_name}': {entity_id}")
            return entity_id
        except Exception as e:
            self.logger.error(f"Error adding entity to knowledge graph: {e}")
            raise
    
    def add_relationship_to_knowledge_graph(
        self, 
        relationship_data: dict,
        kg_name: str = 'default'
    ) -> str:
        """添加关系到知识图谱
        
        Args:
            relationship_data: 关系数据
            kg_name: 知识图谱名称
            
        Returns:
            str: 关系ID
        """
        try:
            # 创建关系对象
            relationship = Relationship(
                id=relationship_data.get('id'),
                type=relationship_data.get('type'),
                source_id=relationship_data.get('source_id'),
                target_id=relationship_data.get('target_id'),
                properties=relationship_data.get('properties', {})
            )
            
            kg = self.get_knowledge_graph(kg_name)
            rel_id = kg.add_relationship(relationship)
            self.logger.info(f"Relationship added to knowledge graph '{kg_name}': {rel_id}")
            return rel_id
        except Exception as e:
            self.logger.error(f"Error adding relationship to knowledge graph: {e}")
            raise
    
    def save_all(self) -> None:
        """保存所有服务状态"""
        try:
            # 保存向量存储
            for name, vector_store in self._vector_stores.items():
                try:
                    vector_store.save()
                    self.logger.info(f"Vector store '{name}' saved")
                except Exception as e:
                    self.logger.error(f"Failed to save vector store '{name}': {e}")
            
            # 保存知识图谱
            for name, kg in self._knowledge_graphs.items():
                try:
                    kg.save()
                    self.logger.info(f"Knowledge graph '{name}' saved")
                except Exception as e:
                    self.logger.error(f"Failed to save knowledge graph '{name}': {e}")
            
        except Exception as e:
            self.logger.error(f"Error saving services: {e}")
            raise
    
    def load_all(self) -> None:
        """加载所有服务状态"""
        try:
            # 加载向量存储
            for name, vector_store in self._vector_stores.items():
                try:
                    vector_store.load()
                    self.logger.info(f"Vector store '{name}' loaded")
                except Exception as e:
                    self.logger.error(f"Failed to load vector store '{name}': {e}")
            
            # 加载知识图谱
            for name, kg in self._knowledge_graphs.items():
                try:
                    kg.load()
                    self.logger.info(f"Knowledge graph '{name}' loaded")
                except Exception as e:
                    self.logger.error(f"Failed to load knowledge graph '{name}': {e}")
            
        except Exception as e:
            self.logger.error(f"Error loading services: {e}")
            raise
    
    def clear_cache(self) -> None:
        """清除所有缓存"""
        try:
            cache_clear()
            self.logger.info("Cache cleared")
        except Exception as e:
            self.logger.error(f"Error clearing cache: {e}")
            raise


# 创建全局AI服务实例
global_ai_service = None

def get_ai_service(config_path: str = None) -> AIService:
    """获取或创建全局AI服务实例
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        AIService: AI服务实例
    """
    global global_ai_service
    if global_ai_service is None or (config_path and config_path != getattr(global_ai_service, '_config_path', None)):
        global_ai_service = AIService(config_path)
        global_ai_service._config_path = config_path
    
    return global_ai_service


# 导出主要API
def process_text(
    text: str,
    operations: list = None,
    processor_name: str = 'default',
    config_path: str = None
) -> dict:
    """处理文本（便捷函数）
    
    Args:
        text: 要处理的文本
        operations: 要执行的操作列表
        processor_name: 文本处理器名称
        config_path: 配置文件路径
        
    Returns:
        dict: 处理结果
    """
    service = get_ai_service(config_path)
    return service.process_text(text, operations, processor_name)

def generate_text(
    prompt: str,
    client_name: str = 'default',
    config_path: str = None,
    **kwargs
) -> str:
    """生成文本（便捷函数）
    
    Args:
        prompt: 提示词
        client_name: 大模型客户端名称
        config_path: 配置文件路径
        **kwargs: 生成参数
        
    Returns:
        str: 生成的文本
    """
    service = get_ai_service(config_path)
    return service.generate_text(prompt, client_name, **kwargs)

def search_documents(
    query: str,
    vector_store_name: str = 'default',
    k: int = 5,
    config_path: str = None,
    **kwargs
) -> list:
    """搜索文档（便捷函数）
    
    Args:
        query: 搜索查询
        vector_store_name: 向量存储名称
        k: 返回的结果数量
        config_path: 配置文件路径
        **kwargs: 搜索参数
        
    Returns:
        list: 搜索结果列表
    """
    service = get_ai_service(config_path)
    return service.search_documents(query, vector_store_name, k, **kwargs)

def add_document_to_vector_store(
    document: dict, 
    vector_store_name: str = 'default',
    config_path: str = None,
    **kwargs
) -> str:
    """添加文档到向量存储（便捷函数）
    
    Args:
        document: 文档数据
        vector_store_name: 向量存储名称
        config_path: 配置文件路径
        **kwargs: 添加参数
        
    Returns:
        str: 文档ID
    """
    service = get_ai_service(config_path)
    return service.add_document_to_vector_store(document, vector_store_name, **kwargs)

def add_entity_to_knowledge_graph(
    entity_data: dict,
    kg_name: str = 'default',
    config_path: str = None
) -> str:
    """添加实体到知识图谱（便捷函数）
    
    Args:
        entity_data: 实体数据
        kg_name: 知识图谱名称
        config_path: 配置文件路径
        
    Returns:
        str: 实体ID
    """
    service = get_ai_service(config_path)
    return service.add_entity_to_knowledge_graph(entity_data, kg_name)

def add_relationship_to_knowledge_graph(
    relationship_data: dict,
    kg_name: str = 'default',
    config_path: str = None
) -> str:
    """添加关系到知识图谱（便捷函数）
    
    Args:
        relationship_data: 关系数据
        kg_name: 知识图谱名称
        config_path: 配置文件路径
        
    Returns:
        str: 关系ID
    """
    service = get_ai_service(config_path)
    return service.add_relationship_to_knowledge_graph(relationship_data, kg_name)

def save_ai_services(config_path: str = None) -> None:
    """保存所有AI服务状态（便捷函数）
    
    Args:
        config_path: 配置文件路径
    """
    service = get_ai_service(config_path)
    service.save_all()

def load_ai_services(config_path: str = None) -> None:
    """加载所有AI服务状态（便捷函数）
    
    Args:
        config_path: 配置文件路径
    """
    service = get_ai_service(config_path)
    service.load_all()

def clear_ai_service_cache() -> None:
    """清除AI服务缓存（便捷函数）"""
    global global_ai_service
    if global_ai_service:
        global_ai_service.clear_cache()
    clear_cache()


# 当作为主程序运行时的示例
if __name__ == '__main__':
    try:
        # 创建AI服务实例
        ai_service = AIService()
        
        # 示例：处理文本
        text = "这是一段用于测试的文本内容。我们将使用AI服务来处理它。"
        processed_text = ai_service.process_text(text)
        print("文本处理结果：")
        print(f"关键词：{processed_text.get('keywords')}")
        print(f"分词结果：{processed_text.get('segments')}")
        
        # 示例：创建并添加文档到向量存储
        sample_doc = {
            'content': '这是一个示例文档，用于测试向量存储功能。',
            'metadata': {'source': 'test', 'type': 'example'}
        }
        doc_id = ai_service.add_document_to_vector_store(sample_doc)
        print(f"添加的文档ID：{doc_id}")
        
        # 示例：搜索文档
        results = ai_service.search_documents('测试向量存储')
        print(f"搜索结果数量：{len(results)}")
        
        # 示例：添加实体到知识图谱
        entity_data = {
            'type': 'person',
            'properties': {'name': '测试用户', 'age': 30}
        }
        entity_id = ai_service.add_entity_to_knowledge_graph(entity_data)
        print(f"添加的实体ID：{entity_id}")
        
    except Exception as e:
        exception(f"Error in AI service demo: {e}")
        sys.exit(1)