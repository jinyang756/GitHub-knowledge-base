#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AI服务工具包"""

# 导出配置加载工具
default_config_loader = None

from .config_loader import (
    ConfigLoader,
    global_config_loader,
    load_config,
    get_config_value,
    save_config,
    merge_configs
)

# 导出缓存管理工具
default_cache_manager = None

from .cache_manager import (
    MemoryCache,
    FileCache,
    CacheManager,
    global_cache_manager,
    cache_get,
    cache_set,
    cache_delete,
    cache_exists,
    cache_clear
)

# 导出错误处理工具
default_error_handler = None

from .error_handler import (
    # 基础异常类
    AIServiceError,
    
    # API相关异常
    APIError,
    APIConnectionError,
    APIAuthenticationError,
    APIQuotaExceededError,
    APIRequestError,
    APIResponseError,
    
    # 数据处理相关异常
    DataProcessingError,
    DataFormatError,
    DataNotFoundError,
    DataValidationError,
    
    # 向量存储相关异常
    VectorStoreError,
    VectorStoreIndexError,
    VectorStoreQueryError,
    
    # 知识图谱相关异常
    KnowledgeGraphError,
    KGEntityError,
    KGRelationshipError,
    
    # NLP相关异常
    NLPError,
    NLPParsingError,
    NLPModelError,
    
    # 错误响应和处理器
    ErrorResponse,
    ErrorHandler,
    global_error_handler,
    handle_exception,
    catch_exceptions,
    validate_params
)

# 导出日志工具
default_logger = None

from .logger import (
    Logger,
    LoggerManager,
    global_logger_manager,
    default_logger,
    get_logger,
    debug,
    info,
    warning,
    error,
    critical,
    exception,
    log,
    set_level,
    set_level_for_all
)

# 导出时间工具
default_time_utils = None

from .time_utils import (
    TimeUtils,
    global_time_utils,
    now,
    today,
    yesterday,
    tomorrow,
    format_datetime,
    parse_datetime,
    to_timestamp,
    from_timestamp,
    add_days,
    add_hours,
    add_minutes,
    add_months,
    add_years,
    get_time_diff,
    is_between,
    get_week_start,
    get_week_end,
    get_month_start,
    get_month_end,
    get_year_start,
    get_year_end,
    generate_time_range,
    get_age,
    format_duration
)

# 包版本信息
__version__ = '0.1.0'

# 包描述
__description__ = 'AI服务工具包，提供配置加载、缓存管理、错误处理、日志记录和时间工具等功能'

# 导出所有公共API
__all__ = [
    # 配置加载工具
    'ConfigLoader',
    'global_config_loader',
    'load_config',
    'get_config_value',
    'save_config',
    'merge_configs',
    
    # 缓存管理工具
    'MemoryCache',
    'FileCache',
    'CacheManager',
    'global_cache_manager',
    'cache_get',
    'cache_set',
    'cache_delete',
    'cache_exists',
    'cache_clear',
    
    # 错误处理工具 - 异常类
    'AIServiceError',
    'APIError',
    'APIConnectionError',
    'APIAuthenticationError',
    'APIQuotaExceededError',
    'APIRequestError',
    'APIResponseError',
    'DataProcessingError',
    'DataFormatError',
    'DataNotFoundError',
    'DataValidationError',
    'VectorStoreError',
    'VectorStoreIndexError',
    'VectorStoreQueryError',
    'KnowledgeGraphError',
    'KGEntityError',
    'KGRelationshipError',
    'NLPError',
    'NLPParsingError',
    'NLPModelError',
    
    # 错误处理工具 - 响应和处理器
    'ErrorResponse',
    'ErrorHandler',
    'global_error_handler',
    'handle_exception',
    'catch_exceptions',
    'validate_params',
    
    # 日志工具
    'Logger',
    'LoggerManager',
    'global_logger_manager',
    'default_logger',
    'get_logger',
    'debug',
    'info',
    'warning',
    'error',
    'critical',
    'exception',
    'log',
    'set_level',
    'set_level_for_all',
    
    # 时间工具
    'TimeUtils',
    'global_time_utils',
    'now',
    'today',
    'yesterday',
    'tomorrow',
    'format_datetime',
    'parse_datetime',
    'to_timestamp',
    'from_timestamp',
    'add_days',
    'add_hours',
    'add_minutes',
    'add_months',
    'add_years',
    'get_time_diff',
    'is_between',
    'get_week_start',
    'get_week_end',
    'get_month_start',
    'get_month_end',
    'get_year_start',
    'get_year_end',
    'generate_time_range',
    'get_age',
    'format_duration',
    
    # 包信息
    '__version__',
    '__description__'
]