#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""知识图谱基础接口"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Union, Set


class Entity:
    """知识图谱实体类"""
    
    def __init__(self, id: str, type: str, properties: Optional[Dict] = None):
        """初始化实体
        
        Args:
            id: 实体唯一标识符
            type: 实体类型
            properties: 实体属性字典
        """
        self.id = id
        self.type = type
        self.properties = properties or {}

    def to_dict(self) -> Dict:
        """转换为字典格式
        
        Returns:
            Dict: 实体的字典表示
        """
        return {
            'id': self.id,
            'type': self.type,
            'properties': self.properties
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Entity':
        """从字典创建实体
        
        Args:
            data: 包含实体信息的字典
            
        Returns:
            Entity: 实体对象
        """
        return cls(
            id=data['id'],
            type=data['type'],
            properties=data.get('properties', {})
        )


class Relationship:
    """知识图谱关系类"""
    
    def __init__(self, source_id: str, target_id: str, type: str, properties: Optional[Dict] = None):
        """初始化关系
        
        Args:
            source_id: 源实体ID
            target_id: 目标实体ID
            type: 关系类型
            properties: 关系属性字典
        """
        self.source_id = source_id
        self.target_id = target_id
        self.type = type
        self.properties = properties or {}

    def to_dict(self) -> Dict:
        """转换为字典格式
        
        Returns:
            Dict: 关系的字典表示
        """
        return {
            'source_id': self.source_id,
            'target_id': self.target_id,
            'type': self.type,
            'properties': self.properties
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Relationship':
        """从字典创建关系
        
        Args:
            data: 包含关系信息的字典
            
        Returns:
            Relationship: 关系对象
        """
        return cls(
            source_id=data['source_id'],
            target_id=data['target_id'],
            type=data['type'],
            properties=data.get('properties', {})
        )


class BaseKnowledgeGraph(ABC):
    """知识图谱的抽象基类，定义统一接口"""

    def __init__(self, **kwargs):
        """初始化知识图谱
        
        Args:
            **kwargs: 知识图谱配置参数
        """
        self.config = kwargs
        self._initialize()

    @abstractmethod
    def _initialize(self):
        """初始化具体的知识图谱"""
        pass

    @abstractmethod
    def add_entity(self, entity: Entity) -> bool:
        """添加实体到知识图谱
        
        Args:
            entity: 实体对象
            
        Returns:
            bool: 是否添加成功
        """
        pass

    @abstractmethod
    def add_entities(self, entities: List[Entity]) -> List[bool]:
        """批量添加实体到知识图谱
        
        Args:
            entities: 实体对象列表
            
        Returns:
            List[bool]: 每个实体添加是否成功的结果列表
        """
        pass

    @abstractmethod
    def add_relationship(self, relationship: Relationship) -> bool:
        """添加关系到知识图谱
        
        Args:
            relationship: 关系对象
            
        Returns:
            bool: 是否添加成功
        """
        pass

    @abstractmethod
    def add_relationships(self, relationships: List[Relationship]) -> List[bool]:
        """批量添加关系到知识图谱
        
        Args:
            relationships: 关系对象列表
            
        Returns:
            List[bool]: 每个关系添加是否成功的结果列表
        """
        pass

    @abstractmethod
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """获取指定ID的实体
        
        Args:
            entity_id: 实体ID
            
        Returns:
            Optional[Entity]: 实体对象，如果不存在则返回None
        """
        pass

    @abstractmethod
    def get_entities_by_type(self, entity_type: str) -> List[Entity]:
        """获取指定类型的所有实体
        
        Args:
            entity_type: 实体类型
            
        Returns:
            List[Entity]: 实体列表
        """
        pass

    @abstractmethod
    def get_relationships(self, source_id: Optional[str] = None, target_id: Optional[str] = None, 
                         relationship_type: Optional[str] = None) -> List[Relationship]:
        """获取关系
        
        Args:
            source_id: 源实体ID（可选）
            target_id: 目标实体ID（可选）
            relationship_type: 关系类型（可选）
            
        Returns:
            List[Relationship]: 关系列表
        """
        pass

    @abstractmethod
    def delete_entity(self, entity_id: str) -> bool:
        """删除指定ID的实体
        
        Args:
            entity_id: 实体ID
            
        Returns:
            bool: 是否删除成功
        """
        pass

    @abstractmethod
    def delete_relationship(self, source_id: str, target_id: str, relationship_type: str) -> bool:
        """删除指定的关系
        
        Args:
            source_id: 源实体ID
            target_id: 目标实体ID
            relationship_type: 关系类型
            
        Returns:
            bool: 是否删除成功
        """
        pass

    @abstractmethod
    def update_entity(self, entity: Entity) -> bool:
        """更新实体
        
        Args:
            entity: 实体对象
            
        Returns:
            bool: 是否更新成功
        """
        pass

    @abstractmethod
    def search_entities(self, query: Dict) -> List[Entity]:
        """搜索实体
        
        Args:
            query: 搜索条件
            
        Returns:
            List[Entity]: 匹配的实体列表
        """
        pass

    @abstractmethod
    def get_neighbors(self, entity_id: str, relationship_type: Optional[str] = None) -> List[Tuple[Entity, Relationship]]:
        """获取实体的邻居节点
        
        Args:
            entity_id: 实体ID
            relationship_type: 关系类型（可选）
            
        Returns:
            List[Tuple[Entity, Relationship]]: 邻居实体和关系的列表
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """清空知识图谱"""
        pass

    @abstractmethod
    def save(self, path: str) -> None:
        """保存知识图谱到文件
        
        Args:
            path: 保存路径
        """
        pass

    @abstractmethod
    def load(self, path: str) -> None:
        """从文件加载知识图谱
        
        Args:
            path: 加载路径
        """
        pass

    def count_entities(self) -> int:
        """获取实体数量
        
        Returns:
            int: 实体数量
        """
        raise NotImplementedError("count_entities() is not implemented")

    def count_relationships(self) -> int:
        """获取关系数量
        
        Returns:
            int: 关系数量
        """
        raise NotImplementedError("count_relationships() is not implemented")

    def get_shortest_path(self, source_id: str, target_id: str) -> List[Tuple[Entity, Relationship]]:
        """获取两个实体之间的最短路径
        
        Args:
            source_id: 源实体ID
            target_id: 目标实体ID
            
        Returns:
            List[Tuple[Entity, Relationship]]: 路径上的实体和关系列表
        """
        raise NotImplementedError("get_shortest_path() is not implemented")