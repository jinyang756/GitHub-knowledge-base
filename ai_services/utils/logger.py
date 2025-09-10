#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""日志工具"""

import os
import sys
import logging
import datetime
import traceback
from typing import Optional, Dict, Any, Union, Callable, TypeVar, TextIO


class Logger:
    """日志记录器类"""
    
    # 日志级别映射
    LEVEL_MAP = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    
    def __init__(self,
                 name: str = 'ai_services',
                 level: str = 'info',
                 log_file: Optional[str] = None,
                 console_output: bool = True,
                 file_max_bytes: int = 10 * 1024 * 1024,  # 10MB
                 file_backup_count: int = 5,
                 log_format: Optional[str] = None):
        """初始化日志记录器
        
        Args:
            name: 日志记录器名称
            level: 日志级别
            log_file: 日志文件路径
            console_output: 是否输出到控制台
            file_max_bytes: 单个日志文件最大字节数
            file_backup_count: 备份文件数量
            log_format: 日志格式
        """
        # 创建日志记录器
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.LEVEL_MAP.get(level.lower(), logging.INFO))
        
        # 清除已有的处理器
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # 默认日志格式
        if log_format is None:
            log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # 创建格式化器
        formatter = logging.Formatter(log_format)
        
        # 添加控制台处理器
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # 添加文件处理器
        if log_file:
            # 确保日志目录存在
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
            
            # 使用RotatingFileHandler支持日志轮转
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=file_max_bytes,
                backupCount=file_backup_count,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        
        # 保存配置
        self.name = name
        self.level = level
        self.log_file = log_file
        self.console_output = console_output
    
    def debug(self, message: str, **kwargs: Any) -> None:
        """记录调试信息
        
        Args:
            message: 日志消息
            **kwargs: 额外的日志上下文
        """
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(self._format_message(message, **kwargs))
    
    def info(self, message: str, **kwargs: Any) -> None:
        """记录一般信息
        
        Args:
            message: 日志消息
            **kwargs: 额外的日志上下文
        """
        if self.logger.isEnabledFor(logging.INFO):
            self.logger.info(self._format_message(message, **kwargs))
    
    def warning(self, message: str, **kwargs: Any) -> None:
        """记录警告信息
        
        Args:
            message: 日志消息
            **kwargs: 额外的日志上下文
        """
        if self.logger.isEnabledFor(logging.WARNING):
            self.logger.warning(self._format_message(message, **kwargs))
    
    def error(self, message: str, **kwargs: Any) -> None:
        """记录错误信息
        
        Args:
            message: 日志消息
            **kwargs: 额外的日志上下文
        """
        if self.logger.isEnabledFor(logging.ERROR):
            self.logger.error(self._format_message(message, **kwargs))
    
    def critical(self, message: str, **kwargs: Any) -> None:
        """记录严重错误信息
        
        Args:
            message: 日志消息
            **kwargs: 额外的日志上下文
        """
        if self.logger.isEnabledFor(logging.CRITICAL):
            self.logger.critical(self._format_message(message, **kwargs))
    
    def exception(self, message: str, exc_info: Optional[Exception] = None, **kwargs: Any) -> None:
        """记录异常信息
        
        Args:
            message: 日志消息
            exc_info: 异常对象
            **kwargs: 额外的日志上下文
        """
        if self.logger.isEnabledFor(logging.ERROR):
            if exc_info:
                # 构建完整的异常信息
                exc_type = type(exc_info).__name__
                exc_message = str(exc_info)
                exc_traceback = traceback.format_exc()
                full_message = f"{message}\n{exc_type}: {exc_message}\n{exc_traceback}"
                self.logger.error(full_message)
            else:
                # 使用当前异常上下文
                self.logger.error(self._format_message(message, **kwargs), exc_info=True)
    
    def log(self, level: str, message: str, **kwargs: Any) -> None:
        """记录指定级别的日志
        
        Args:
            level: 日志级别
            message: 日志消息
            **kwargs: 额外的日志上下文
        """
        log_level = self.LEVEL_MAP.get(level.lower(), logging.INFO)
        if self.logger.isEnabledFor(log_level):
            self.logger.log(log_level, self._format_message(message, **kwargs))
    
    def _format_message(self, message: str, **kwargs: Any) -> str:
        """格式化日志消息
        
        Args:
            message: 日志消息
            **kwargs: 额外的日志上下文
            
        Returns:
            str: 格式化后的日志消息
        """
        if kwargs:
            context_str = ', '.join([f"{k}={v}" for k, v in kwargs.items()])
            return f"{message} [{context_str}]"
        return message
    
    def set_level(self, level: str) -> None:
        """设置日志级别
        
        Args:
            level: 日志级别
        """
        log_level = self.LEVEL_MAP.get(level.lower(), logging.INFO)
        self.logger.setLevel(log_level)
        self.level = level
    
    def add_handler(self, handler: logging.Handler) -> None:
        """添加日志处理器
        
        Args:
            handler: 日志处理器
        """
        self.logger.addHandler(handler)
    
    def remove_handler(self, handler: logging.Handler) -> None:
        """移除日志处理器
        
        Args:
            handler: 日志处理器
        """
        self.logger.removeHandler(handler)


class LoggerManager:
    """日志管理器类，管理多个日志记录器"""
    
    def __init__(self):
        """初始化日志管理器"""
        self.loggers: Dict[str, Logger] = {}
        self.default_logger: Optional[Logger] = None
    
    def get_logger(self, name: str, **kwargs: Any) -> Logger:
        """获取或创建日志记录器
        
        Args:
            name: 日志记录器名称
            **kwargs: 日志记录器配置参数
            
        Returns:
            Logger: 日志记录器实例
        """
        if name not in self.loggers:
            self.loggers[name] = Logger(name, **kwargs)
            
            # 设置默认日志记录器（第一个创建的）
            if self.default_logger is None:
                self.default_logger = self.loggers[name]
        
        return self.loggers[name]
    
    def remove_logger(self, name: str) -> None:
        """移除日志记录器
        
        Args:
            name: 日志记录器名称
        """
        if name in self.loggers:
            del self.loggers[name]
            
            # 如果移除的是默认日志记录器，重新设置默认日志记录器
            if self.default_logger and self.default_logger.name == name:
                self.default_logger = next(iter(self.loggers.values()), None)
    
    def set_level_for_all(self, level: str) -> None:
        """设置所有日志记录器的级别
        
        Args:
            level: 日志级别
        """
        for logger in self.loggers.values():
            logger.set_level(level)
    
    def get_default_logger(self) -> Logger:
        """获取默认日志记录器
        
        Returns:
            Logger: 默认日志记录器
        """
        if self.default_logger is None:
            # 如果没有默认日志记录器，创建一个
            self.default_logger = Logger('default')
        
        return self.default_logger
    
    # 代理方法，转发到默认日志记录器
    def debug(self, message: str, **kwargs: Any) -> None:
        """记录调试信息（代理到默认日志记录器）"""
        self.get_default_logger().debug(message, **kwargs)
    
    def info(self, message: str, **kwargs: Any) -> None:
        """记录一般信息（代理到默认日志记录器）"""
        self.get_default_logger().info(message, **kwargs)
    
    def warning(self, message: str, **kwargs: Any) -> None:
        """记录警告信息（代理到默认日志记录器）"""
        self.get_default_logger().warning(message, **kwargs)
    
    def error(self, message: str, **kwargs: Any) -> None:
        """记录错误信息（代理到默认日志记录器）"""
        self.get_default_logger().error(message, **kwargs)
    
    def critical(self, message: str, **kwargs: Any) -> None:
        """记录严重错误信息（代理到默认日志记录器）"""
        self.get_default_logger().critical(message, **kwargs)
    
    def exception(self, message: str, exc_info: Optional[Exception] = None, **kwargs: Any) -> None:
        """记录异常信息（代理到默认日志记录器）"""
        self.get_default_logger().exception(message, exc_info, **kwargs)
    
    def log(self, level: str, message: str, **kwargs: Any) -> None:
        """记录指定级别的日志（代理到默认日志记录器）"""
        self.get_default_logger().log(level, message, **kwargs)


# 创建全局日志管理器实例
global_logger_manager = LoggerManager()

# 创建默认日志记录器
default_logger = global_logger_manager.get_logger('ai_services')

# 便捷函数
def get_logger(name: str, **kwargs: Any) -> Logger:
    """获取或创建日志记录器（便捷函数）
    
    Args:
        name: 日志记录器名称
        **kwargs: 日志记录器配置参数
        
    Returns:
        Logger: 日志记录器实例
    """
    return global_logger_manager.get_logger(name, **kwargs)

def debug(message: str, **kwargs: Any) -> None:
    """记录调试信息（便捷函数）"""
    default_logger.debug(message, **kwargs)

def info(message: str, **kwargs: Any) -> None:
    """记录一般信息（便捷函数）"""
    default_logger.info(message, **kwargs)

def warning(message: str, **kwargs: Any) -> None:
    """记录警告信息（便捷函数）"""
    default_logger.warning(message, **kwargs)

def error(message: str, **kwargs: Any) -> None:
    """记录错误信息（便捷函数）"""
    default_logger.error(message, **kwargs)

def critical(message: str, **kwargs: Any) -> None:
    """记录严重错误信息（便捷函数）"""
    default_logger.critical(message, **kwargs)

def exception(message: str, exc_info: Optional[Exception] = None, **kwargs: Any) -> None:
    """记录异常信息（便捷函数）"""
    default_logger.exception(message, exc_info, **kwargs)

def log(level: str, message: str, **kwargs: Any) -> None:
    """记录指定级别的日志（便捷函数）"""
    default_logger.log(level, message, **kwargs)

def set_level(level: str) -> None:
    """设置默认日志记录器的级别（便捷函数）"""
    default_logger.set_level(level)

def set_level_for_all(level: str) -> None:
    """设置所有日志记录器的级别（便捷函数）"""
    global_logger_manager.set_level_for_all(level)