#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""基于NetworkX的知识图谱实现"""

import json
import os
from typing import Dict, List, Optional, Tuple, Union, Set

from ai_services.kg.base_knowledge_graph import BaseKnowledgeGraph, Entity, Relationship

# 尝试导入networkx库
try:
    import networkx as nx
except ImportError:
    print("Warning: networkx library not found. Please install it with 'pip install networkx'")
    
    # 创建一个简单的模拟networkx模块
    class MockNetworkX:
        class DiGraph:
            def __init__(self):
                self.nodes = {}
                self.edges = {}
                
            def add_node(self, node, **attr):
                self.nodes[node] = attr
                
            def add_edge(self, u, v, **attr):
                if u not in self.edges:
                    self.edges[u] = {}
                self.edges[u][v] = attr
                
            def has_node(self, node):
                return node in self.nodes
                
            def has_edge(self, u, v):
                return u in self.edges and v in self.edges[u]
                
            def remove_node(self, node):
                if node in self.nodes:
                    del self.nodes[node]
                # 移除所有与该节点相关的边
                if node in self.edges:
                    del self.edges[node]
                for u in list(self.edges.keys()):
                    if node in self.edges[u]:
                        del self.edges[u][node]
                        
            def remove_edge(self, u, v):
                if u in self.edges and v in self.edges[u]:
                    del self.edges[u][v]
                    
            def nodes(self):
                return self.nodes
                
            def edges(self):
                return self.edges
                
            def neighbors(self, node):
                if node in self.edges:
                    return list(self.edges[node].keys())
                return []
    
    nx = MockNetworkX()


class NetworkXKnowledgeGraph(BaseKnowledgeGraph):
    """基于NetworkX的知识图谱实现"""

    def _initialize(self):
        """初始化NetworkX知识图谱"""
        # 创建有向图
        self.graph = nx.DiGraph()
        
        # 用于存储实体和关系的类型索引
        self.entity_types = {}
        self.relationship_types = {}

    def add_entity(self, entity: Entity) -> bool:
        """添加实体到知识图谱
        
        Args:
            entity: 实体对象
            
        Returns:
            bool: 是否添加成功
        """
        try:
            # 添加节点到图中
            self.graph.add_node(entity.id, type=entity.type, **entity.properties)
            
            # 更新实体类型索引
            if entity.type not in self.entity_types:
                self.entity_types[entity.type] = set()
            self.entity_types[entity.type].add(entity.id)
            
            return True
        except Exception as e:
            print(f"Error adding entity: {e}")
            return False

    def add_entities(self, entities: List[Entity]) -> List[bool]:
        """批量添加实体到知识图谱
        
        Args:
            entities: 实体对象列表
            
        Returns:
            List[bool]: 每个实体添加是否成功的结果列表
        """
        results = []
        for entity in entities:
            results.append(self.add_entity(entity))
        return results

    def add_relationship(self, relationship: Relationship) -> bool:
        """添加关系到知识图谱
        
        Args:
            relationship: 关系对象
            
        Returns:
            bool: 是否添加成功
        """
        try:
            # 确保源实体和目标实体存在
            if not self.graph.has_node(relationship.source_id):
                print(f"Source entity {relationship.source_id} does not exist")
                return False
            if not self.graph.has_node(relationship.target_id):
                print(f"Target entity {relationship.target_id} does not exist")
                return False
            
            # 添加边到图中
            self.graph.add_edge(
                relationship.source_id,
                relationship.target_id,
                type=relationship.type,
                **relationship.properties
            )
            
            # 更新关系类型索引
            if relationship.type not in self.relationship_types:
                self.relationship_types[relationship.type] = set()
            self.relationship_types[relationship.type].add((relationship.source_id, relationship.target_id))
            
            return True
        except Exception as e:
            print(f"Error adding relationship: {e}")
            return False

    def add_relationships(self, relationships: List[Relationship]) -> List[bool]:
        """批量添加关系到知识图谱
        
        Args:
            relationships: 关系对象列表
            
        Returns:
            List[bool]: 每个关系添加是否成功的结果列表
        """
        results = []
        for relationship in relationships:
            results.append(self.add_relationship(relationship))
        return results

    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """获取指定ID的实体
        
        Args:
            entity_id: 实体ID
            
        Returns:
            Optional[Entity]: 实体对象，如果不存在则返回None
        """
        if not self.graph.has_node(entity_id):
            return None
        
        # 获取节点属性
        node_attrs = self.graph.nodes[entity_id]
        entity_type = node_attrs.pop('type')
        
        return Entity(
            id=entity_id,
            type=entity_type,
            properties=node_attrs
        )

    def get_entities_by_type(self, entity_type: str) -> List[Entity]:
        """获取指定类型的所有实体
        
        Args:
            entity_type: 实体类型
            
        Returns:
            List[Entity]: 实体列表
        """
        entities = []
        
        if entity_type in self.entity_types:
            for entity_id in self.entity_types[entity_type]:
                entity = self.get_entity(entity_id)
                if entity:
                    entities.append(entity)
        
        return entities

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
        relationships = []
        
        # 遍历所有边
        for u, v, attrs in self.graph.edges(data=True):
            # 检查源实体ID
            if source_id is not None and u != source_id:
                continue
            # 检查目标实体ID
            if target_id is not None and v != target_id:
                continue
            # 检查关系类型
            if relationship_type is not None and attrs.get('type') != relationship_type:
                continue
            
            # 创建关系对象
            rel = Relationship(
                source_id=u,
                target_id=v,
                type=attrs.pop('type'),
                properties=attrs
            )
            relationships.append(rel)
        
        return relationships

    def delete_entity(self, entity_id: str) -> bool:
        """删除指定ID的实体
        
        Args:
            entity_id: 实体ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            if not self.graph.has_node(entity_id):
                return False
            
            # 获取实体类型
            entity_type = self.graph.nodes[entity_id].get('type')
            
            # 从图中删除节点
            self.graph.remove_node(entity_id)
            
            # 从实体类型索引中删除
            if entity_type and entity_type in self.entity_types:
                self.entity_types[entity_type].discard(entity_id)
                # 如果类型为空，则删除该类型
                if not self.entity_types[entity_type]:
                    del self.entity_types[entity_type]
            
            # 从关系类型索引中删除相关的关系
            for rel_type in list(self.relationship_types.keys()):
                # 查找与该实体相关的关系
                to_remove = set()
                for (u, v) in self.relationship_types[rel_type]:
                    if u == entity_id or v == entity_id:
                        to_remove.add((u, v))
                
                # 删除相关关系
                for edge in to_remove:
                    self.relationship_types[rel_type].remove(edge)
                
                # 如果类型为空，则删除该类型
                if not self.relationship_types[rel_type]:
                    del self.relationship_types[rel_type]
            
            return True
        except Exception as e:
            print(f"Error deleting entity: {e}")
            return False

    def delete_relationship(self, source_id: str, target_id: str, relationship_type: str) -> bool:
        """删除指定的关系
        
        Args:
            source_id: 源实体ID
            target_id: 目标实体ID
            relationship_type: 关系类型
            
        Returns:
            bool: 是否删除成功
        """
        try:
            if not self.graph.has_edge(source_id, target_id):
                return False
            
            # 检查关系类型是否匹配
            edge_attrs = self.graph.edges[source_id, target_id]
            if edge_attrs.get('type') != relationship_type:
                return False
            
            # 从图中删除边
            self.graph.remove_edge(source_id, target_id)
            
            # 从关系类型索引中删除
            if relationship_type in self.relationship_types:
                self.relationship_types[relationship_type].discard((source_id, target_id))
                # 如果类型为空，则删除该类型
                if not self.relationship_types[relationship_type]:
                    del self.relationship_types[relationship_type]
            
            return True
        except Exception as e:
            print(f"Error deleting relationship: {e}")
            return False

    def update_entity(self, entity: Entity) -> bool:
        """更新实体
        
        Args:
            entity: 实体对象
            
        Returns:
            bool: 是否更新成功
        """
        try:
            if not self.graph.has_node(entity.id):
                return False
            
            # 获取旧的实体类型
            old_type = self.graph.nodes[entity.id].get('type')
            
            # 更新节点属性
            self.graph.nodes[entity.id].clear()
            self.graph.nodes[entity.id]['type'] = entity.type
            self.graph.nodes[entity.id].update(entity.properties)
            
            # 更新实体类型索引
            if old_type != entity.type:
                # 从旧类型中删除
                if old_type and old_type in self.entity_types:
                    self.entity_types[old_type].discard(entity.id)
                    if not self.entity_types[old_type]:
                        del self.entity_types[old_type]
                
                # 添加到新类型
                if entity.type not in self.entity_types:
                    self.entity_types[entity.type] = set()
                self.entity_types[entity.type].add(entity.id)
            
            return True
        except Exception as e:
            print(f"Error updating entity: {e}")
            return False

    def search_entities(self, query: Dict) -> List[Entity]:
        """搜索实体
        
        Args:
            query: 搜索条件，支持类型和属性过滤
            
        Returns:
            List[Entity]: 匹配的实体列表
        """
        entities = []
        
        # 提取查询条件
        entity_type = query.get('type')
        properties = {k: v for k, v in query.items() if k != 'type'}
        
        # 确定要搜索的实体ID集合
        entity_ids = set()
        
        if entity_type:
            # 如果指定了类型，只搜索该类型的实体
            if entity_type in self.entity_types:
                entity_ids = self.entity_types[entity_type].copy()
        else:
            # 否则搜索所有实体
            entity_ids = set(self.graph.nodes)
        
        # 按属性过滤实体
        for entity_id in entity_ids:
            entity = self.get_entity(entity_id)
            if entity:
                # 检查所有属性是否匹配
                match = True
                for prop_name, prop_value in properties.items():
                    if entity.properties.get(prop_name) != prop_value:
                        match = False
                        break
                
                if match:
                    entities.append(entity)
        
        return entities

    def get_neighbors(self, entity_id: str, relationship_type: Optional[str] = None) -> List[Tuple[Entity, Relationship]]:
        """获取实体的邻居节点
        
        Args:
            entity_id: 实体ID
            relationship_type: 关系类型（可选）
            
        Returns:
            List[Tuple[Entity, Relationship]]: 邻居实体和关系的列表
        """
        neighbors = []
        
        if not self.graph.has_node(entity_id):
            return neighbors
        
        # 遍历所有出边
        for neighbor_id, attrs in self.graph[entity_id].items():
            # 检查关系类型
            if relationship_type is not None and attrs.get('type') != relationship_type:
                continue
            
            # 获取邻居实体
            neighbor_entity = self.get_entity(neighbor_id)
            if neighbor_entity:
                # 创建关系对象
                rel = Relationship(
                    source_id=entity_id,
                    target_id=neighbor_id,
                    type=attrs.pop('type'),
                    properties=attrs
                )
                neighbors.append((neighbor_entity, rel))
        
        return neighbors

    def clear(self) -> None:
        """清空知识图谱"""
        self.graph = nx.DiGraph()
        self.entity_types.clear()
        self.relationship_types.clear()

    def save(self, path: str) -> None:
        """保存知识图谱到文件
        
        Args:
            path: 保存路径
        """
        # 确保目录存在
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # 准备数据
        data = {
            'entities': [],
            'relationships': []
        }
        
        # 保存实体
        for entity_id in self.graph.nodes:
            entity = self.get_entity(entity_id)
            if entity:
                data['entities'].append(entity.to_dict())
        
        # 保存关系
        for u, v, attrs in self.graph.edges(data=True):
            rel_type = attrs.pop('type')
            rel = Relationship(
                source_id=u,
                target_id=v,
                type=rel_type,
                properties=attrs
            )
            data['relationships'].append(rel.to_dict())
        
        # 保存到文件
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self, path: str) -> None:
        """从文件加载知识图谱
        
        Args:
            path: 加载路径
        """
        if not os.path.exists(path):
            print(f"File {path} does not exist")
            return
        
        # 清空当前图谱
        self.clear()
        
        # 从文件读取数据
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 加载实体
        for entity_data in data.get('entities', []):
            entity = Entity.from_dict(entity_data)
            self.add_entity(entity)
        
        # 加载关系
        for rel_data in data.get('relationships', []):
            rel = Relationship.from_dict(rel_data)
            self.add_relationship(rel)

    def count_entities(self) -> int:
        """获取实体数量
        
        Returns:
            int: 实体数量
        """
        return len(self.graph.nodes)

    def count_relationships(self) -> int:
        """获取关系数量
        
        Returns:
            int: 关系数量
        """
        return len(self.graph.edges)

    def get_shortest_path(self, source_id: str, target_id: str) -> List[Tuple[Entity, Relationship]]:
        """获取两个实体之间的最短路径
        
        Args:
            source_id: 源实体ID
            target_id: 目标实体ID
            
        Returns:
            List[Tuple[Entity, Relationship]]: 路径上的实体和关系列表
        """
        try:
            if not (self.graph.has_node(source_id) and self.graph.has_node(target_id)):
                return []
            
            # 使用NetworkX的最短路径算法
            # 注意：这里使用的是简单的最短路径，实际应用中可能需要根据关系权重计算
            path = nx.shortest_path(self.graph, source=source_id, target=target_id)
            
            # 构建返回结果
            result = []
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                
                # 获取实体
                entity = self.get_entity(v)
                if not entity:
                    continue
                
                # 获取关系
                edge_attrs = self.graph.edges[u, v]
                rel_type = edge_attrs.pop('type')
                rel = Relationship(
                    source_id=u,
                    target_id=v,
                    type=rel_type,
                    properties=edge_attrs
                )
                
                result.append((entity, rel))
            
            return result
        except nx.NetworkXNoPath:
            print(f"No path exists between {source_id} and {target_id}")
            return []
        except Exception as e:
            print(f"Error finding shortest path: {e}")
            return []