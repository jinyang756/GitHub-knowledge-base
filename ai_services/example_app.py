#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AI服务模块示例应用"""

import os
import sys
from ai_services import (
    # AI服务主类和便捷函数
    get_ai_service, process_text, generate_text, search_documents,
    add_document_to_vector_store, add_entity_to_knowledge_graph,
    add_relationship_to_knowledge_graph,
    # 工具函数
    info, error, exception
)


def main():
    """示例应用主函数"""
    try:
        # 创建AI服务实例
        print("=== 创建AI服务实例 ===")
        ai_service = get_ai_service()
        print("AI服务实例创建成功！\n")
        
        # 示例1：文本处理
        print("=== 示例1：文本处理 ===")
        text = "这是一段用于测试AI服务的文本内容。我们将展示如何使用文本处理功能，包括分词、关键词提取和实体识别等。"
        print(f"原始文本: {text}\n")
        
        # 处理文本
        processed_text = process_text(
            text, 
            operations=['clean', 'segment', 'extract_keywords', 'split_sentences']
        )
        
        # 显示处理结果
        print(f"清理后的文本: {processed_text.get('clean_text')}")
        print(f"分词结果: {processed_text.get('segments')}")
        print(f"关键词: {processed_text.get('keywords')}")
        print(f"句子分割: {processed_text.get('sentences')}\n")
        
        # 示例2：向量存储操作
        print("=== 示例2：向量存储操作 ===")
        
        # 准备一些示例文档
        documents = [
            {
                'content': '这是第一个示例文档，用于测试向量存储功能。',
                'metadata': {'source': 'test', 'type': 'example', 'id': 'doc1'}
            },
            {
                'content': '这是第二个示例文档，包含一些测试数据。',
                'metadata': {'source': 'test', 'type': 'example', 'id': 'doc2'}
            },
            {
                'content': '这是第三个示例文档，用于演示文档搜索功能。',
                'metadata': {'source': 'test', 'type': 'example', 'id': 'doc3'}
            }
        ]
        
        # 添加文档到向量存储
        print("添加文档到向量存储...")
        doc_ids = []
        for doc in documents:
            doc_id = add_document_to_vector_store(doc)
            doc_ids.append(doc_id)
            print(f"  添加文档成功，ID: {doc_id}")
        
        # 搜索文档
        print("\n搜索相关文档...")
        search_queries = ["测试文档", "向量存储", "搜索功能"]
        
        for query in search_queries:
            print(f"\n搜索查询: '{query}'")
            results = search_documents(query, k=2)
            print(f"  找到{len(results)}个相关文档：")
            
            for i, doc in enumerate(results):
                print(f"  结果 {i+1}:")
                print(f"    内容: {doc.content}")
                print(f"    元数据: {doc.metadata}")
                print(f"    相似度: {doc.score:.4f}")
        
        print()
        
        # 示例3：知识图谱操作
        print("=== 示例3：知识图谱操作 ===")
        
        # 添加实体
        print("添加实体到知识图谱...")
        
        # 添加人员实体
        person_id = add_entity_to_knowledge_graph({
            'type': 'person',
            'properties': {'name': '张三', 'age': 30, 'occupation': '软件工程师'}
        })
        print(f"  添加人员实体成功，ID: {person_id}")
        
        # 添加公司实体
        company_id = add_entity_to_knowledge_graph({
            'type': 'company',
            'properties': {'name': '示例科技有限公司', 'industry': 'AI', 'founded': 2020}
        })
        print(f"  添加公司实体成功，ID: {company_id}")
        
        # 添加关系
        print("\n添加关系到知识图谱...")
        
        # 添加雇佣关系
        rel_id = add_relationship_to_knowledge_graph({
            'type': 'employed_by',
            'source_id': person_id,
            'target_id': company_id,
            'properties': {'start_date': '2022-01-01', 'position': '软件工程师'}
        })
        print(f"  添加雇佣关系成功，ID: {rel_id}")
        
        # 获取知识图谱实例，执行更多操作
        kg = ai_service.get_knowledge_graph()
        
        # 查找实体
        print("\n查找实体...")
        
        # 按类型查找实体
        person_entities = kg.get_entities_by_type('person')
        print(f"  找到{len(person_entities)}个人员实体：")
        for entity in person_entities:
            print(f"    ID: {entity.id}, 名称: {entity.properties.get('name')}")
        
        # 按ID查找实体
        company_entity = kg.get_entity(company_id)
        if company_entity:
            print(f"  公司实体: {company_entity.properties.get('name')}, 行业: {company_entity.properties.get('industry')}")
        
        # 保存所有服务状态
        print("\n保存所有服务状态...")
        ai_service.save_all()
        print("  服务状态保存成功！")
        
        print("\n=== 示例应用运行完成 ===")
        print("您已成功体验了AI服务模块的核心功能，包括文本处理、向量存储和知识图谱操作。")
        print("如需了解更多功能，请参考README.md文档或查看源代码。")
        
    except Exception as e:
        exception(f"示例应用运行出错: {e}")
        print(f"错误: {e}")
        print("如果遇到API相关错误，请确保您已正确配置API密钥。")
        print("对于模拟环境中的错误，请注意这可能是因为缺少某些依赖库导致的降级行为。")
        sys.exit(1)


if __name__ == '__main__':
    main()