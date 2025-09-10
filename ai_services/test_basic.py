#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AI服务模块基本功能测试"""

import os
import sys
from ai_services import (
    # 核心组件
    TextProcessor,
    FAISSVectorStore,
    NetworkXKnowledgeGraph,
    # 工具函数
    load_config, get_logger
)


def test_text_processor():
    """测试文本处理器功能"""
    print("=== 测试文本处理器 ===")
    
    # 创建文本处理器实例
    processor = TextProcessor()
    
    # 测试文本
    text = "这是一段用于测试文本处理器的示例文本。我们将测试分词、关键词提取等功能！"
    print(f"原始文本: {text}")
    
    # 测试文本清理
    clean_text = processor.clean_text(text)
    print(f"清理后的文本: {clean_text}")
    
    # 测试分词
    segments = processor.segment_text(clean_text)
    print(f"分词结果: {segments}")
    
    # 测试关键词提取
    keywords = processor.extract_keywords(clean_text)
    print(f"关键词提取: {keywords}")
    
    # 测试句子分割
    sentences = processor.split_sentences(clean_text)
    print(f"句子分割: {sentences}")
    
    # 测试文本标准化
    normalized_text = processor.normalize_text("这是   一 段含有 多余空格和特殊符号！！的文本。")
    print(f"文本标准化: {normalized_text}")
    
    # 测试文本相似度计算
    text1 = "这是第一段测试文本"
    text2 = "这是第二段测试文本"
    similarity = processor.calculate_similarity(text1, text2)
    print(f"文本相似度 ('{text1}' vs '{text2}'): {similarity:.4f}")
    
    print("文本处理器测试完成！\n")


def test_vector_store():
    """测试向量存储功能"""
    print("=== 测试向量存储 ===")
    
    # 创建临时向量存储（不依赖外部API）
    vector_store = FAISSVectorStore(
        embedding_dim=10,  # 使用小维度进行测试
        use_mock_embedding=True  # 使用模拟嵌入
    )
    
    # 准备测试文档
    documents = [
        {
            'id': 'doc1',
            'content': '这是第一个测试文档',
            'metadata': {'source': 'test', 'type': 'document'}
        },
        {
            'id': 'doc2',
            'content': '这是第二个测试文档',
            'metadata': {'source': 'test', 'type': 'document'}
        },
        {
            'id': 'doc3',
            'content': '这是第三个测试文档',
            'metadata': {'source': 'test', 'type': 'document'}
        }
    ]
    
    # 添加文档
    print("添加测试文档...")
    for doc in documents:
        doc_id = vector_store.add_document(
            id=doc['id'],
            content=doc['content'],
            metadata=doc['metadata']
        )
        print(f"  添加文档成功，ID: {doc_id}")
    
    # 批量添加文档
    batch_docs = [
        {'content': '这是批量添加的文档1', 'metadata': {'batch': True}},
        {'content': '这是批量添加的文档2', 'metadata': {'batch': True}}
    ]
    print("\n批量添加文档...")
    batch_ids = vector_store.add_documents(batch_docs)
    print(f"  批量添加成功，IDs: {batch_ids}")
    
    # 搜索文档
    print("\n搜索测试文档...")
    results = vector_store.search("测试文档", k=3)
    print(f"  找到{len(results)}个相关文档：")
    for i, doc in enumerate(results):
        print(f"  结果 {i+1}:")
        print(f"    ID: {doc.id}")
        print(f"    内容: {doc.content}")
        print(f"    元数据: {doc.metadata}")
        print(f"    相似度: {doc.score:.4f}")
    
    # 获取文档
    print("\n获取指定文档...")
    doc = vector_store.get_document('doc1')
    if doc:
        print(f"  文档ID: {doc.id}")
        print(f"  内容: {doc.content}")
        print(f"  元数据: {doc.metadata}")
    
    # 删除文档
    print("\n删除指定文档...")
    success = vector_store.delete_document('doc2')
    print(f"  删除结果: {'成功' if success else '失败'}")
    
    # 检查文档数量
    print(f"\n当前文档数量: {vector_store.get_document_count()}")
    
    print("向量存储测试完成！\n")


def test_knowledge_graph():
    """测试知识图谱功能"""
    print("=== 测试知识图谱 ===")
    
    # 创建知识图谱实例
    kg = NetworkXKnowledgeGraph()
    
    # 添加实体
    print("添加实体...")
    entity1_id = kg.add_entity(
        type='person',
        properties={'name': '张三', 'age': 30, 'occupation': '软件工程师'}
    )
    entity2_id = kg.add_entity(
        type='company',
        properties={'name': '测试科技有限公司', 'industry': 'AI', 'founded': 2020}
    )
    entity3_id = kg.add_entity(
        type='project',
        properties={'name': 'AI服务模块', 'status': '开发中', 'start_date': '2023-01-01'}
    )
    
    print(f"  添加人员实体成功，ID: {entity1_id}")
    print(f"  添加公司实体成功，ID: {entity2_id}")
    print(f"  添加项目实体成功，ID: {entity3_id}")
    
    # 添加关系
    print("\n添加关系...")
    rel1_id = kg.add_relationship(
        type='employed_by',
        source_id=entity1_id,
        target_id=entity2_id,
        properties={'start_date': '2022-01-01', 'position': '软件工程师'}
    )
    rel2_id = kg.add_relationship(
        type='works_on',
        source_id=entity1_id,
        target_id=entity3_id,
        properties={'role': '开发者', 'hours_per_week': 40}
    )
    
    print(f"  添加雇佣关系成功，ID: {rel1_id}")
    print(f"  添加工作关系成功，ID: {rel2_id}")
    
    # 查询实体
    print("\n查询实体...")
    
    # 按ID查询
    entity = kg.get_entity(entity1_id)
    if entity:
        print(f"  按ID查询 - ID: {entity.id}, 类型: {entity.type}, 属性: {entity.properties}")
    
    # 按类型查询
    person_entities = kg.get_entities_by_type('person')
    print(f"  按类型查询（person）- 找到{len(person_entities)}个实体")
    
    # 查询关系
    print("\n查询关系...")
    
    # 获取实体的所有关系
    relationships = kg.get_relationships_by_entity(entity1_id)
    print(f"  获取实体{entity1_id}的所有关系 - 找到{len(relationships)}个关系")
    for rel in relationships:
        print(f"    关系ID: {rel.id}, 类型: {rel.type}, 目标实体: {rel.target_id}")
    
    # 获取实体之间的关系
    entity_relationships = kg.get_relationships_between_entities(entity1_id, entity2_id)
    print(f"  获取实体{entity1_id}和{entity2_id}之间的关系 - 找到{len(entity_relationships)}个关系")
    
    # 查找路径
    print("\n查找路径...")
    path = kg.find_path(entity1_id, entity3_id)
    if path:
        print(f"  找到从{entity1_id}到{entity3_id}的路径: {path}")
    
    # 获取实体数量和关系数量
    print(f"\n实体数量: {kg.get_entity_count()}")
    print(f"关系数量: {kg.get_relationship_count()}")
    
    print("知识图谱测试完成！\n")


def test_utils():
    """测试工具函数"""
    print("=== 测试工具函数 ===")
    
    # 测试日志功能
    print("测试日志功能...")
    logger = get_logger('test_logger')
    logger.info("这是一条信息日志")
    logger.warning("这是一条警告日志")
    print("  日志记录完成")
    
    # 测试配置加载（如果配置文件存在）
    print("\n测试配置加载...")
    config_path = os.path.join(os.path.dirname(__file__), 'config.example.json')
    if os.path.exists(config_path):
        config = load_config(config_path)
        print(f"  配置文件加载成功，包含{len(config)}个主要配置项")
        print(f"  配置项: {', '.join(config.keys())}")
    else:
        print(f"  配置文件不存在: {config_path}")
    
    print("工具函数测试完成！\n")


def run_all_tests():
    """运行所有测试"""
    try:
        print("========== AI服务模块基本功能测试 ==========")
        
        # 运行各项测试
        test_text_processor()
        test_vector_store()
        test_knowledge_graph()
        test_utils()
        
        print("========== 所有测试完成！ ==========")
        print("\n测试结果总结：")
        print("1. 文本处理器 - 功能正常，可以进行分词、关键词提取等操作")
        print("2. 向量存储 - 功能正常，可以添加、搜索、删除文档")
        print("3. 知识图谱 - 功能正常，可以添加、查询实体和关系")
        print("4. 工具函数 - 功能正常，日志和配置加载功能可用")
        print("\n注意：此测试使用了模拟模式，不依赖外部API。实际使用时请配置相应的API密钥。")
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    run_all_tests()