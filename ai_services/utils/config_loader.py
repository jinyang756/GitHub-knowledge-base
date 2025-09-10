#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""配置加载工具"""

import json
import os
import yaml
from typing import Dict, Optional, Any, Union


class ConfigLoader:
    """配置加载器类"""
    
    def __init__(self):
        """初始化配置加载器"""
        self.config_cache = {}
    
    def load_config(
        self, 
        config_path: str, 
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """加载配置文件
        
        Args:
            config_path: 配置文件路径
            use_cache: 是否使用缓存
            
        Returns:
            Dict[str, Any]: 配置字典
        """
        # 检查缓存
        if use_cache and config_path in self.config_cache:
            return self.config_cache[config_path]
        
        # 检查文件是否存在
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        # 根据文件扩展名选择加载方法
        file_ext = os.path.splitext(config_path)[1].lower()
        
        if file_ext == '.json':
            config = self._load_json(config_path)
        elif file_ext in ('.yaml', '.yml'):
            config = self._load_yaml(config_path)
        else:
            raise ValueError(f"Unsupported config file format: {file_ext}")
        
        # 更新缓存
        if use_cache:
            self.config_cache[config_path] = config
        
        return config
    
    def _load_json(self, file_path: str) -> Dict[str, Any]:
        """加载JSON配置文件
        
        Args:
            file_path: JSON文件路径
            
        Returns:
            Dict[str, Any]: 配置字典
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_yaml(self, file_path: str) -> Dict[str, Any]:
        """加载YAML配置文件
        
        Args:
            file_path: YAML文件路径
            
        Returns:
            Dict[str, Any]: 配置字典
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def get_config_value(
        self, 
        config: Dict[str, Any], 
        key_path: str, 
        default: Any = None
    ) -> Any:
        """从配置字典中获取指定路径的值
        
        Args:
            config: 配置字典
            key_path: 键路径，使用点号分隔，如 "api.key"
            default: 默认值
            
        Returns:
            Any: 配置值
        """
        keys = key_path.split('.')
        value = config
        
        try:
            for key in keys:
                if isinstance(value, dict):
                    value = value[key]
                else:
                    return default
            return value
        except (KeyError, TypeError):
            return default
    
    def save_config(
        self, 
        config: Dict[str, Any], 
        file_path: str
    ) -> None:
        """保存配置到文件
        
        Args:
            config: 配置字典
            file_path: 目标文件路径
        """
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # 根据文件扩展名选择保存方法
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.json':
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        elif file_ext in ('.yaml', '.yml'):
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        else:
            raise ValueError(f"Unsupported config file format: {file_ext}")
    
    def merge_configs(
        self, 
        base_config: Dict[str, Any], 
        override_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """合并两个配置字典
        
        Args:
            base_config: 基础配置字典
            override_config: 覆盖配置字典
            
        Returns:
            Dict[str, Any]: 合并后的配置字典
        """
        result = base_config.copy()
        
        for key, value in override_config.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # 递归合并嵌套字典
                result[key] = self.merge_configs(result[key], value)
            else:
                # 直接覆盖值
                result[key] = value
        
        return result
    
    def clear_cache(self) -> None:
        """清除配置缓存"""
        self.config_cache.clear()

# 创建全局配置加载器实例
global_config_loader = ConfigLoader()

# 便捷函数
def load_config(
    config_path: str, 
    use_cache: bool = True
) -> Dict[str, Any]:
    """加载配置文件（便捷函数）
    
    Args:
        config_path: 配置文件路径
        use_cache: 是否使用缓存
        
    Returns:
        Dict[str, Any]: 配置字典
    """
    return global_config_loader.load_config(config_path, use_cache)

def get_config_value(
    config: Dict[str, Any], 
    key_path: str, 
    default: Any = None
) -> Any:
    """从配置字典中获取指定路径的值（便捷函数）
    
    Args:
        config: 配置字典
        key_path: 键路径，使用点号分隔，如 "api.key"
        default: 默认值
        
    Returns:
        Any: 配置值
    """
    return global_config_loader.get_config_value(config, key_path, default)

def save_config(
    config: Dict[str, Any], 
    file_path: str
) -> None:
    """保存配置到文件（便捷函数）
    
    Args:
        config: 配置字典
        file_path: 目标文件路径
    """
    return global_config_loader.save_config(config, file_path)

def merge_configs(
    base_config: Dict[str, Any], 
    override_config: Dict[str, Any]
) -> Dict[str, Any]:
    """合并两个配置字典（便捷函数）
    
    Args:
        base_config: 基础配置字典
        override_config: 覆盖配置字典
        
    Returns:
        Dict[str, Any]: 合并后的配置字典
    """
    return global_config_loader.merge_configs(base_config, override_config)