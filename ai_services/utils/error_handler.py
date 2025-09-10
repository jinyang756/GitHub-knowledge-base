#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""错误处理工具"""

import traceback
import logging
import functools
from typing import Optional, Dict, Any, Union, Callable, TypeVar

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ai_services')


# 自定义异常类
def _make_exception_class(name: str, base: type = Exception) -> type:
    """创建自定义异常类的辅助函数"""
    return type(name, (base,), {})

# AI服务基础异常类
AIServiceError = _make_exception_class('AIServiceError')

# API相关异常
APIError = _make_exception_class('APIError', AIServiceError)
APIConnectionError = _make_exception_class('APIConnectionError', APIError)
APIAuthenticationError = _make_exception_class('APIAuthenticationError', APIError)
APIQuotaExceededError = _make_exception_class('APIQuotaExceededError', APIError)
APIRequestError = _make_exception_class('APIRequestError', APIError)
APIResponseError = _make_exception_class('APIResponseError', APIError)

# 数据处理相关异常
DataProcessingError = _make_exception_class('DataProcessingError', AIServiceError)
DataFormatError = _make_exception_class('DataFormatError', DataProcessingError)
DataNotFoundError = _make_exception_class('DataNotFoundError', DataProcessingError)
DataValidationError = _make_exception_class('DataValidationError', DataProcessingError)

# 向量存储相关异常
VectorStoreError = _make_exception_class('VectorStoreError', AIServiceError)
VectorStoreIndexError = _make_exception_class('VectorStoreIndexError', VectorStoreError)
VectorStoreQueryError = _make_exception_class('VectorStoreQueryError', VectorStoreError)

# 知识图谱相关异常
KnowledgeGraphError = _make_exception_class('KnowledgeGraphError', AIServiceError)
KGEntityError = _make_exception_class('KGEntityError', KnowledgeGraphError)
KGRelationshipError = _make_exception_class('KGRelationshipError', KnowledgeGraphError)

# NLP相关异常
NLPError = _make_exception_class('NLPError', AIServiceError)
NLPParsingError = _make_exception_class('NLPParsingError', NLPError)
NLPModelError = _make_exception_class('NLPModelError', NLPError)


class ErrorResponse:
    """错误响应类"""
    
    def __init__(
        self, 
        error_type: str, 
        message: str, 
        error_code: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
        traceback: Optional[str] = None
    ):
        """初始化错误响应
        
        Args:
            error_type: 错误类型
            message: 错误消息
            error_code: 错误代码
            details: 错误详情
            traceback: 异常堆栈信息
        """
        self.error_type = error_type
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.traceback = traceback
        self.timestamp = None  # 可以在to_dict中添加时间戳
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式
        
        Returns:
            Dict[str, Any]: 错误响应字典
        """
        import datetime
        return {
            'error_type': self.error_type,
            'message': self.message,
            'error_code': self.error_code,
            'details': self.details,
            'traceback': self.traceback,
            'timestamp': datetime.datetime.now().isoformat()
        }
    
    def to_json(self) -> str:
        """转换为JSON字符串
        
        Returns:
            str: JSON格式的错误响应
        """
        import json
        return json.dumps(self.to_dict(), ensure_ascii=False)


class ErrorHandler:
    """错误处理器类"""
    
    def __init__(self):
        """初始化错误处理器"""
        self._logger = logger
    
    def handle_exception(
        self, 
        e: Exception, 
        raise_error: bool = False,
        include_traceback: bool = False
    ) -> ErrorResponse:
        """处理异常
        
        Args:
            e: 异常对象
            raise_error: 是否重新抛出异常
            include_traceback: 是否包含堆栈信息
            
        Returns:
            ErrorResponse: 错误响应对象
        """
        # 获取异常类型和消息
        error_type = e.__class__.__name__
        message = str(e)
        
        # 根据异常类型设置错误代码和详情
        error_code = None
        details = {}
        
        if isinstance(e, APIError):
            error_code = 400
            if isinstance(e, APIConnectionError):
                error_code = 503
            elif isinstance(e, APIAuthenticationError):
                error_code = 401
            elif isinstance(e, APIQuotaExceededError):
                error_code = 429
        elif isinstance(e, DataProcessingError):
            error_code = 422
            if isinstance(e, DataNotFoundError):
                error_code = 404
        elif isinstance(e, VectorStoreError):
            error_code = 500
        elif isinstance(e, KnowledgeGraphError):
            error_code = 500
        elif isinstance(e, NLPError):
            error_code = 500
        else:
            error_code = 500
        
        # 获取堆栈信息
        traceback_str = traceback.format_exc() if include_traceback else None
        
        # 记录错误日志
        self._logger.error(f"{error_type}: {message}\n{traceback_str if include_traceback else ''}")
        
        # 创建错误响应
        error_response = ErrorResponse(
            error_type=error_type,
            message=message,
            error_code=error_code,
            details=details,
            traceback=traceback_str
        )
        
        # 重新抛出异常
        if raise_error:
            raise
        
        return error_response
    
    def catch_exceptions(
        self, 
        include_traceback: bool = False,
        return_error_response: bool = True
    ) -> Callable:
        """捕获异常的装饰器
        
        Args:
            include_traceback: 是否包含堆栈信息
            return_error_response: 是否返回错误响应对象
            
        Returns:
            Callable: 装饰后的函数
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    error_response = self.handle_exception(
                        e, 
                        raise_error=False, 
                        include_traceback=include_traceback
                    )
                    
                    if return_error_response:
                        return error_response
                    else:
                        return None
            return wrapper
        return decorator
    
    def validate_params(
        self, 
        params: Dict[str, Any], 
        required_params: list,
        param_types: Optional[Dict[str, type]] = None
    ) -> bool:
        """验证参数
        
        Args:
            params: 参数字典
            required_params: 必需参数列表
            param_types: 参数类型字典
            
        Returns:
            bool: 参数是否有效
            
        Raises:
            DataValidationError: 参数验证失败时抛出
        """
        # 检查必需参数
        missing_params = [param for param in required_params if param not in params]
        if missing_params:
            raise DataValidationError(f"Missing required parameters: {', '.join(missing_params)}")
        
        # 检查参数类型
        if param_types:
            for param, expected_type in param_types.items():
                if param in params and not isinstance(params[param], expected_type):
                    raise DataValidationError(
                        f"Parameter '{param}' should be of type {expected_type.__name__}, "
                        f"got {type(params[param]).__name__} instead"
                    )
        
        return True


# 创建全局错误处理器实例
global_error_handler = ErrorHandler()

# 便捷函数
def handle_exception(
    e: Exception, 
    raise_error: bool = False,
    include_traceback: bool = False
) -> ErrorResponse:
    """处理异常（便捷函数）
    
    Args:
        e: 异常对象
        raise_error: 是否重新抛出异常
        include_traceback: 是否包含堆栈信息
        
    Returns:
        ErrorResponse: 错误响应对象
    """
    return global_error_handler.handle_exception(e, raise_error, include_traceback)

def catch_exceptions(
    include_traceback: bool = False,
    return_error_response: bool = True
) -> Callable:
    """捕获异常的装饰器（便捷函数）
    
    Args:
        include_traceback: 是否包含堆栈信息
        return_error_response: 是否返回错误响应对象
        
    Returns:
        Callable: 装饰后的函数
    """
    return global_error_handler.catch_exceptions(include_traceback, return_error_response)

def validate_params(
    params: Dict[str, Any], 
    required_params: list,
    param_types: Optional[Dict[str, type]] = None
) -> bool:
    """验证参数（便捷函数）
    
    Args:
        params: 参数字典
        required_params: 必需参数列表
        param_types: 参数类型字典
        
    Returns:
        bool: 参数是否有效
        
    Raises:
        DataValidationError: 参数验证失败时抛出
    """
    return global_error_handler.validate_params(params, required_params, param_types)