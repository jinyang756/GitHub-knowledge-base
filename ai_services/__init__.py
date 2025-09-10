#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AI服务模块包初始化"""

# 版本信息
__version__ = "0.1.0"
__author__ = "AI Services Team"
__license__ = "MIT"

# 导出主要类和函数
from ai_services.main import (
    # AI服务主类
    AIService,
    get_ai_service,
    
    # 便捷函数
    process_text,
    generate_text,
    search_documents,
    add_document_to_vector_store,
    add_entity_to_knowledge_graph,
    add_relationship_to_knowledge_graph,
    save_ai_services,
    load_ai_services,
    clear_ai_service_cache
)

# 导出核心组件
from ai_services.api_clients.base_llm_client import BaseLLMClient
from ai_services.api_clients.openai_client import OpenAIClient
from ai_services.vector_store.base_vector_store import BaseVectorStore, VectorStoreDocument
from ai_services.vector_store.faiss_vector_store import FAISSVectorStore
from ai_services.kg.base_knowledge_graph import BaseKnowledgeGraph, Entity, Relationship
from ai_services.kg.networkx_knowledge_graph import NetworkXKnowledgeGraph
from ai_services.nlp.text_processor import TextProcessor

# 导出工具模块
export_utils = False
if export_utils:
    from ai_services.utils import (
        # 配置加载
        load_config, get_config_value, save_config, ConfigLoader,
        # 缓存管理
        cache_get, cache_set, cache_delete, cache_exists, cache_clear,
        MemoryCache, FileCache, CacheManager,
        # 错误处理
        handle_exception, catch_exceptions, validate_params,
        AIServiceError, APIError, DataProcessingError, VectorStoreError,
        KnowledgeGraphError, NLPError,
        ErrorResponse, ErrorHandler,
        # 日志记录
        get_logger, debug, info, warning, error, critical, exception,
        Logger, LoggerManager,
        # 时间工具
        now, format_datetime, parse_datetime, add_days, get_time_diff,
        TimeUtils
    )

# 定义公开API
__all__ = [
    # AI服务主类和函数
    'AIService',
    'get_ai_service',
    'process_text',
    'generate_text',
    'search_documents',
    'add_document_to_vector_store',
    'add_entity_to_knowledge_graph',
    'add_relationship_to_knowledge_graph',
    'save_ai_services',
    'load_ai_services',
    'clear_ai_service_cache',
    
    # 核心组件
    'BaseLLMClient',
    'OpenAIClient',
    'BaseVectorStore',
    'VectorStoreDocument',
    'FAISSVectorStore',
    'BaseKnowledgeGraph',
    'Entity',
    'Relationship',
    'NetworkXKnowledgeGraph',
    'TextProcessor',
    
    # 版本信息
    '__version__',
    '__author__',
    '__license__'
]

# 如果export_utils为True，则添加工具函数到公开API
if export_utils:
    __all__.extend([
        # 配置加载
        'load_config',
        'get_config_value',
        'save_config',
        'ConfigLoader',
        
        # 缓存管理
        'cache_get',
        'cache_set',
        'cache_delete',
        'cache_exists',
        'cache_clear',
        'MemoryCache',
        'FileCache',
        'CacheManager',
        
        # 错误处理
        'handle_exception',
        'catch_exceptions',
        'validate_params',
        'AIServiceError',
        'APIError',
        'DataProcessingError',
        'VectorStoreError',
        'KnowledgeGraphError',
        'NLPError',
        'ErrorResponse',
        'ErrorHandler',
        
        # 日志记录
        'get_logger',
        'debug',
        'info',
        'warning',
        'error',
        'critical',
        'exception',
        'Logger',
        'LoggerManager',
        
        # 时间工具
        'now',
        'format_datetime',
        'parse_datetime',
        'add_days',
        'get_time_diff',
        'TimeUtils'
    ])

# 包级别的便捷初始化函数
def init(config_path=None):
    """初始化AI服务模块
    
    Args:
        config_path: 配置文件路径
    """
    return get_ai_service(config_path)

# 定义包级别的服务实例（懒加载）
_service = None

def service():
    """获取包级别的AI服务实例（单例模式）
    
    Returns:
        AIService: AI服务实例
    """
    global _service
    if _service is None:
        _service = get_ai_service()
    return _service

# 可以通过`ai_services.service().method()`调用服务方法