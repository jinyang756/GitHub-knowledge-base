#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""缓存管理工具"""

import os
import json
import time
import pickle
from typing import Dict, Any, Optional, Union, Callable, TypeVar
from threading import RLock

T = TypeVar('T')


class MemoryCache:
    """内存缓存类"""
    
    def __init__(self, default_ttl: int = 3600):
        """初始化内存缓存
        
        Args:
            default_ttl: 默认缓存过期时间（秒），默认为3600秒（1小时）
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._default_ttl = default_ttl
        self._lock = RLock()  # 可重入锁，支持嵌套获取
    
    def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[int] = None
    ) -> None:
        """设置缓存
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 缓存过期时间（秒），None表示使用默认值
        """
        expire_at = time.time() + (ttl if ttl is not None else self._default_ttl)
        
        with self._lock:
            self._cache[key] = {
                'value': value,
                'expire_at': expire_at
            }
    
    def get(
        self, 
        key: str, 
        default: Any = None
    ) -> Any:
        """获取缓存
        
        Args:
            key: 缓存键
            default: 默认值
            
        Returns:
            Any: 缓存值或默认值
        """
        with self._lock:
            if key not in self._cache:
                return default
            
            item = self._cache[key]
            # 检查是否过期
            if time.time() > item['expire_at']:
                # 惰性删除过期项
                del self._cache[key]
                return default
            
            return item['value']
    
    def delete(self, key: str) -> None:
        """删除缓存项
        
        Args:
            key: 缓存键
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
    
    def exists(self, key: str) -> bool:
        """检查缓存项是否存在且未过期
        
        Args:
            key: 缓存键
            
        Returns:
            bool: 是否存在且未过期
        """
        return self.get(key, default=NotImplemented) is not NotImplemented
    
    def clear(self) -> None:
        """清空缓存"""
        with self._lock:
            self._cache.clear()
    
    def size(self) -> int:
        """获取缓存项数量（包含过期项）
        
        Returns:
            int: 缓存项数量
        """
        with self._lock:
            return len(self._cache)
    
    def clean_expired(self) -> int:
        """清理过期缓存项
        
        Returns:
            int: 清理的过期项数量
        """
        now = time.time()
        expired_keys = []
        
        with self._lock:
            for key, item in self._cache.items():
                if now > item['expire_at']:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self._cache[key]
            
            return len(expired_keys)


class FileCache:
    """文件缓存类"""
    
    def __init__(self, cache_dir: str = './cache'):
        """初始化文件缓存
        
        Args:
            cache_dir: 缓存目录路径
        """
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _get_file_path(self, key: str) -> str:
        """获取缓存文件路径
        
        Args:
            key: 缓存键
            
        Returns:
            str: 文件路径
        """
        # 简单的键到文件名的转换，实际应用中可能需要更复杂的转换
        safe_key = key.replace('/', '_').replace('\\', '_').replace(':', '_')
        return os.path.join(self.cache_dir, f"cache_{safe_key}.pkl")
    
    def _get_meta_path(self, key: str) -> str:
        """获取缓存元数据文件路径
        
        Args:
            key: 缓存键
            
        Returns:
            str: 元数据文件路径
        """
        safe_key = key.replace('/', '_').replace('\\', '_').replace(':', '_')
        return os.path.join(self.cache_dir, f"meta_{safe_key}.json")
    
    def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[int] = None
    ) -> None:
        """设置缓存
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 缓存过期时间（秒），None表示永不过期
        """
        file_path = self._get_file_path(key)
        meta_path = self._get_meta_path(key)
        
        # 保存缓存值
        with open(file_path, 'wb') as f:
            pickle.dump(value, f)
        
        # 保存元数据
        meta = {
            'created_at': time.time(),
            'ttl': ttl
        }
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta, f)
    
    def get(
        self, 
        key: str, 
        default: Any = None
    ) -> Any:
        """获取缓存
        
        Args:
            key: 缓存键
            default: 默认值
            
        Returns:
            Any: 缓存值或默认值
        """
        file_path = self._get_file_path(key)
        meta_path = self._get_meta_path(key)
        
        # 检查文件是否存在
        if not os.path.exists(file_path) or not os.path.exists(meta_path):
            return default
        
        # 读取元数据
        try:
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
        except Exception:
            return default
        
        # 检查是否过期
        if meta.get('ttl') is not None:
            expire_at = meta['created_at'] + meta['ttl']
            if time.time() > expire_at:
                # 删除过期文件
                self.delete(key)
                return default
        
        # 读取缓存值
        try:
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        except Exception:
            return default
    
    def delete(self, key: str) -> None:
        """删除缓存项
        
        Args:
            key: 缓存键
        """
        file_path = self._get_file_path(key)
        meta_path = self._get_meta_path(key)
        
        for path in [file_path, meta_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass
    
    def exists(self, key: str) -> bool:
        """检查缓存项是否存在且未过期
        
        Args:
            key: 缓存键
            
        Returns:
            bool: 是否存在且未过期
        """
        return self.get(key, default=NotImplemented) is not NotImplemented
    
    def clear(self) -> None:
        """清空缓存"""
        for file_name in os.listdir(self.cache_dir):
            file_path = os.path.join(self.cache_dir, file_name)
            if os.path.isfile(file_path) and (file_name.startswith('cache_') or file_name.startswith('meta_')):
                try:
                    os.remove(file_path)
                except Exception:
                    pass


class CacheManager:
    """缓存管理器类，整合多种缓存后端"""
    
    def __init__(self):
        """初始化缓存管理器"""
        self.memory_cache = MemoryCache()
        self.file_cache = FileCache()
    
    def get(
        self, 
        key: str, 
        default: Any = None,
        use_memory: bool = True,
        use_file: bool = False
    ) -> Any:
        """获取缓存
        
        Args:
            key: 缓存键
            default: 默认值
            use_memory: 是否使用内存缓存
            use_file: 是否使用文件缓存
            
        Returns:
            Any: 缓存值或默认值
        """
        if use_memory:
            value = self.memory_cache.get(key, default=NotImplemented)
            if value is not NotImplemented:
                return value
        
        if use_file:
            value = self.file_cache.get(key, default=NotImplemented)
            if value is not NotImplemented:
                # 同步到内存缓存
                self.memory_cache.set(key, value)
                return value
        
        return default
    
    def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[int] = None,
        use_memory: bool = True,
        use_file: bool = False
    ) -> None:
        """设置缓存
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 缓存过期时间（秒）
            use_memory: 是否使用内存缓存
            use_file: 是否使用文件缓存
        """
        if use_memory:
            self.memory_cache.set(key, value, ttl)
        
        if use_file:
            self.file_cache.set(key, value, ttl)
    
    def delete(
        self, 
        key: str,
        use_memory: bool = True,
        use_file: bool = False
    ) -> None:
        """删除缓存
        
        Args:
            key: 缓存键
            use_memory: 是否使用内存缓存
            use_file: 是否使用文件缓存
        """
        if use_memory:
            self.memory_cache.delete(key)
        
        if use_file:
            self.file_cache.delete(key)
    
    def exists(
        self, 
        key: str,
        use_memory: bool = True,
        use_file: bool = False
    ) -> bool:
        """检查缓存是否存在
        
        Args:
            key: 缓存键
            use_memory: 是否使用内存缓存
            use_file: 是否使用文件缓存
            
        Returns:
            bool: 是否存在
        """
        if use_memory and self.memory_cache.exists(key):
            return True
        
        if use_file and self.file_cache.exists(key):
            return True
        
        return False
    
    def clear(
        self,
        use_memory: bool = True,
        use_file: bool = False
    ) -> None:
        """清空缓存
        
        Args:
            use_memory: 是否使用内存缓存
            use_file: 是否使用文件缓存
        """
        if use_memory:
            self.memory_cache.clear()
        
        if use_file:
            self.file_cache.clear()
    
    def get_or_set(
        self, 
        key: str, 
        creator_func: Callable[[], T], 
        ttl: Optional[int] = None,
        use_memory: bool = True,
        use_file: bool = False
    ) -> T:
        """获取缓存，如果不存在则创建并设置
        
        Args:
            key: 缓存键
            creator_func: 创建缓存值的函数
            ttl: 缓存过期时间（秒）
            use_memory: 是否使用内存缓存
            use_file: 是否使用文件缓存
            
        Returns:
            T: 缓存值
        """
        value = self.get(key, default=NotImplemented, use_memory=use_memory, use_file=use_file)
        if value is not NotImplemented:
            return value
        
        # 创建新值
        value = creator_func()
        self.set(key, value, ttl, use_memory, use_file)
        return value

# 创建全局缓存管理器实例
global_cache_manager = CacheManager()

# 便捷函数
def cache_get(
    key: str, 
    default: Any = None,
    use_memory: bool = True,
    use_file: bool = False
) -> Any:
    """获取缓存（便捷函数）
    
    Args:
        key: 缓存键
        default: 默认值
        use_memory: 是否使用内存缓存
        use_file: 是否使用文件缓存
        
    Returns:
        Any: 缓存值或默认值
    """
    return global_cache_manager.get(key, default, use_memory, use_file)

def cache_set(
    key: str, 
    value: Any, 
    ttl: Optional[int] = None,
    use_memory: bool = True,
    use_file: bool = False
) -> None:
    """设置缓存（便捷函数）
    
    Args:
        key: 缓存键
        value: 缓存值
        ttl: 缓存过期时间（秒）
        use_memory: 是否使用内存缓存
        use_file: 是否使用文件缓存
    """
    return global_cache_manager.set(key, value, ttl, use_memory, use_file)

def cache_delete(
    key: str,
    use_memory: bool = True,
    use_file: bool = False
) -> None:
    """删除缓存（便捷函数）
    
    Args:
        key: 缓存键
        use_memory: 是否使用内存缓存
        use_file: 是否使用文件缓存
    """
    return global_cache_manager.delete(key, use_memory, use_file)

def cache_exists(
    key: str,
    use_memory: bool = True,
    use_file: bool = False
) -> bool:
    """检查缓存是否存在（便捷函数）
    
    Args:
        key: 缓存键
        use_memory: 是否使用内存缓存
        use_file: 是否使用文件缓存
        
    Returns:
        bool: 是否存在
    """
    return global_cache_manager.exists(key, use_memory, use_file)

def cache_clear(
    use_memory: bool = True,
    use_file: bool = False
) -> None:
    """清空缓存（便捷函数）
    
    Args:
        use_memory: 是否使用内存缓存
        use_file: 是否使用文件缓存
    """
    return global_cache_manager.clear(use_memory, use_file)