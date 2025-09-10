#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# 定义要创建的目录结构
dirs_to_create = [
    'ai_services/nlp',
    'ai_services/kg',
    'ai_services/vector_store',
    'ai_services/api_clients',
    'ai_services/utils',
    'docs/.ai_cache',  # AI缓存目录
    'docs/.vector_store'  # 向量存储目录
]

# 项目根目录
root_dir = os.path.dirname(os.path.abspath(__file__))

# 创建目录
for dir_path in dirs_to_create:
    full_path = os.path.join(root_dir, dir_path)
    try:
        os.makedirs(full_path, exist_ok=True)
        print(f"已创建目录: {full_path}")
    except Exception as e:
        print(f"创建目录 {full_path} 失败: {str(e)}")

print("所有目录创建完成!")