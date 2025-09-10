# AI服务模块

## 简介

这是一个全面的AI服务模块，为知识库智能化升级提供核心功能支持。该模块整合了大语言模型API调用、向量存储、知识图谱构建和自然语言处理等关键功能，旨在提供一套完整的AI能力基础设施。

## 目录结构

```
ai_services/
├── api_clients/           # API客户端模块
│   ├── base_llm_client.py # 基础大模型客户端抽象基类
│   └── openai_client.py   # OpenAI客户端实现
├── vector_store/          # 向量存储模块
│   ├── base_vector_store.py  # 向量存储基础接口
│   └── faiss_vector_store.py # FAISS向量存储实现
├── kg/                    # 知识图谱模块
│   ├── base_knowledge_graph.py    # 知识图谱基础接口
│   └── networkx_knowledge_graph.py # NetworkX知识图谱实现
├── nlp/                   # 自然语言处理模块
│   └── text_processor.py  # 文本处理器实现
├── utils/                 # 工具模块
│   ├── config_loader.py   # 配置加载工具
│   ├── cache_manager.py   # 缓存管理工具
│   ├── error_handler.py   # 错误处理工具
│   ├── logger.py          # 日志工具
│   ├── time_utils.py      # 时间工具
│   └── __init__.py        # 工具模块初始化
├── main.py                # AI服务主入口
├── config.example.json    # 配置文件示例
└── README.md              # 说明文档
```

## 功能特性

### 1. 大语言模型集成
- 支持OpenAI API调用
- 统一的接口设计，易于扩展支持其他模型
- 文本生成、嵌入向量生成、多轮对话功能

### 2. 向量存储
- 基于FAISS的高性能向量检索
- 支持文档的添加、搜索、删除等操作
- 支持向量的持久化存储和加载

### 3. 知识图谱
- 基于NetworkX的知识图谱实现
- 支持实体和关系的增删改查
- 支持路径查找和图分析

### 4. 自然语言处理
- 中英文分词
- 关键词提取（TF-IDF、TextRank）
- 实体识别
- 文本清理和标准化
- 文本相似度计算
- 文本摘要提取

### 5. 工具支持
- 配置管理
- 缓存系统
- 统一错误处理
- 结构化日志
- 时间工具

## 安装说明

### 环境要求
- Python 3.8+ 

### 安装依赖

```bash
# 基本依赖
pip install numpy networkx

# OpenAI支持
pip install openai

# 高性能向量存储
pip install faiss-cpu  # 或 faiss-gpu

# NLP工具（可选）
pip install jieba scikit-learn
```

## 快速开始

### 基本使用

```python
from ai_services import get_ai_service

# 创建AI服务实例
ai_service = get_ai_service()

# 处理文本
text = "这是一段用于测试的文本内容。"
processed_text = ai_service.process_text(text)
print(f"关键词：{processed_text.get('keywords')}")

# 添加文档到向量存储
doc = {
    'content': '这是一个示例文档',
    'metadata': {'source': 'test'}
}
doc_id = ai_service.add_document_to_vector_store(doc)

# 搜索文档
results = ai_service.search_documents('示例文档')
print(f"找到{len(results)}个相关文档")

# 添加实体到知识图谱
entity = {
    'type': 'person',
    'properties': {'name': '张三', 'age': 30}
}
entity_id = ai_service.add_entity_to_knowledge_graph(entity)

# 保存所有服务状态
ai_service.save_all()
```

### 使用配置文件

```python
from ai_services import get_ai_service

# 使用配置文件创建AI服务实例
ai_service = get_ai_service('ai_services/config.json')
```

### 使用便捷函数

```python
from ai_services import process_text, generate_text, search_documents

# 处理文本
result = process_text("这是一段文本", operations=['clean', 'segment', 'extract_keywords'])

# 生成文本
text = generate_text("写一段关于AI的介绍", client_name='default')

# 搜索文档
results = search_documents("AI技术", vector_store_name='default', k=5)
```

## 配置说明

复制`config.example.json`为`config.json`并根据需要修改配置。配置文件包含以下主要部分：

### 1. 大语言模型配置（llm_clients）
- `provider`: 模型提供商（如'openai'）
- `api_key`: API密钥
- `model`: 模型名称
- `temperature`: 生成温度
- `max_tokens`: 最大生成token数

### 2. 向量存储配置（vector_stores）
- `provider`: 向量存储提供商（如'faiss'）
- `index_path`: 索引文件保存路径
- `embedding_dim`: 嵌入向量维度
- `similarity_metric`: 相似度计算方法
- `llm_client_name`: 使用的LLM客户端名称

### 3. 知识图谱配置（knowledge_graphs）
- `provider`: 知识图谱提供商（如'networkx'）
- `graph_path`: 图数据保存路径
- `directed`: 是否为有向图
- `multigraph`: 是否为多重图

### 4. 文本处理器配置（text_processors）
- `language`: 语言类型
- `segmentation_mode`: 分词模式
- `stopwords_path`: 停用词文件路径
- `keywords_top_n`: 关键词提取数量
- `keywords_method`: 关键词提取方法

### 5. 工具配置（utils）
- `cache`: 缓存配置
- `logging`: 日志配置
- `error_handling`: 错误处理配置

## 模块说明

### 1. API客户端模块

提供统一的大语言模型API调用接口，目前支持OpenAI。设计上采用了抽象基类模式，方便扩展支持其他模型提供商。

### 2. 向量存储模块

提供高效的向量存储和检索功能，基于FAISS实现高性能相似度搜索。支持文档的添加、批量添加、搜索、删除等操作，并支持持久化存储。

### 3. 知识图谱模块

提供知识表示和推理能力，基于NetworkX实现。支持实体和关系的管理，以及图分析和路径查找等功能，适用于构建领域知识库。

### 4. 自然语言处理模块

提供全面的文本处理功能，包括分词、关键词提取、实体识别、文本清理、标准化、相似度计算和摘要提取等，支持中英文处理。

### 5. 工具模块

提供配置加载、缓存管理、错误处理、日志记录和时间工具等基础设施，为其他模块提供通用支持。

## API参考

### AI服务主类（AIService）

```python
# 创建服务实例
service = AIService(config_path=None)

# 获取组件实例
llm_client = service.get_llm_client(name='default', provider='openai', **kwargs)
vector_store = service.get_vector_store(name='default', provider='faiss', **kwargs)
knowledge_graph = service.get_knowledge_graph(name='default', provider='networkx', **kwargs)
text_processor = service.get_text_processor(name='default', **kwargs)

# 文本处理
service.process_text(text, operations=None, processor_name='default')

# 文本生成
service.generate_text(prompt, client_name='default', **kwargs)

# 文档搜索
service.search_documents(query, vector_store_name='default', k=5, **kwargs)

# 保存/加载服务状态
service.save_all()
service.load_all()
```

### 便捷函数

```python
# 处理文本
process_text(text, operations=None, processor_name='default', config_path=None)

# 生成文本
generate_text(prompt, client_name='default', config_path=None, **kwargs)

# 搜索文档
search_documents(query, vector_store_name='default', k=5, config_path=None, **kwargs)

# 保存/加载服务状态
save_ai_services(config_path=None)
load_ai_services(config_path=None)

# 清除缓存
clear_ai_service_cache()
```

## 示例代码

### 1. 文本处理示例

```python
from ai_services import process_text

# 处理一段金融文本
text = "央行今日宣布下调MLF利率10个基点，释放流动性约5000亿元。"
results = process_text(
    text, 
    operations=['clean', 'segment', 'extract_keywords', 'extract_entities']
)

print("原始文本:", results['original_text'])
print("分词结果:", results['segments'])
print("关键词:", results['keywords'])
print("实体:", results['entities'])
```

### 2. 向量存储示例

```python
from ai_services import get_ai_service

# 创建服务实例
service = get_ai_service()

# 准备一些金融文档
documents = [
    {
        'content': '央行下调MLF利率10个基点，释放流动性。',
        'metadata': {'type': 'monetary_policy', 'date': '2023-01-01'}
    },
    {
        'content': '证监会发布新的上市公司信息披露管理办法。',
        'metadata': {'type': 'regulation', 'date': '2023-01-02'}
    },
    {
        'content': '财政部：2023年积极的财政政策要加力提效。',
        'metadata': {'type': 'fiscal_policy', 'date': '2023-01-03'}
    }
]

# 添加文档到向量存储
for doc in documents:
    service.add_document_to_vector_store(doc)

# 搜索相关文档
results = service.search_documents('货币政策调整', k=2)
print(f"找到{len(results)}个相关文档")
for i, doc in enumerate(results):
    print(f"结果 {i+1}: ", doc.content)
    print(f"元数据: ", doc.metadata)
    print(f"相似度: ", doc.score)
    print()

# 保存向量存储
vector_store = service.get_vector_store()
vector_store.save()
```

### 3. 知识图谱示例

```python
from ai_services import get_ai_service

# 创建服务实例
service = get_ai_service()

# 添加实体
bank_id = service.add_entity_to_knowledge_graph({
    'type': 'financial_institution',
    'properties': {'name': '中国人民银行', 'type': '央行', 'founded': '1948'}
})

policy_id = service.add_entity_to_knowledge_graph({
    'type': 'policy',
    'properties': {'name': '下调MLF利率', 'date': '2023-01-01'}
})

# 添加关系
service.add_relationship_to_knowledge_graph({
    'type': 'issued_by',
    'source_id': policy_id,
    'target_id': bank_id,
    'properties': {'date': '2023-01-01'}
})

# 获取知识图谱实例
kg = service.get_knowledge_graph()

# 查找实体
entities = kg.get_entities_by_type('financial_institution')
print("金融机构实体:")
for entity in entities:
    print(f"ID: {entity.id}, 名称: {entity.properties.get('name')}")

# 保存知识图谱
kg.save()
```

## 注意事项

1. **API密钥管理**：请妥善保管您的API密钥，建议通过环境变量或配置文件安全管理，不要直接硬编码在代码中。

2. **依赖处理**：本模块设计了依赖缺失时的优雅降级，如无FAISS时会使用模拟实现，但建议安装所有必要依赖以获得最佳性能。

3. **数据存储**：向量存储和知识图谱的数据默认保存在`../docs`目录下，请确保该目录有写入权限。

4. **配置文件**：首次使用时，请复制`config.example.json`为`config.json`并根据实际情况修改配置。

5. **日志管理**：日志默认输出到控制台和`../logs`目录下的文件中，请定期清理日志文件以避免占用过多磁盘空间。

## 开发说明

本模块采用模块化设计，便于扩展和维护：

- 如需添加新的LLM客户端，请继承`BaseLLMClient`抽象基类
- 如需添加新的向量存储实现，请继承`BaseVectorStore`抽象基类
- 如需添加新的知识图谱实现，请继承`BaseKnowledgeGraph`抽象基类
- 工具函数请添加到`utils`目录下，并在`__init__.py`中导出

## 版本信息

版本: 0.1.0

## 许可证

MIT License