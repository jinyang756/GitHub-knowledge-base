#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AI服务模块安装配置"""

from setuptools import setup, find_packages
import os

# 读取README.md作为项目描述
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

# 读取版本号
with open(os.path.join(os.path.dirname(__file__), '__init__.py'), 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip().strip('"')
            break

setup(
    name="ai_services",
    version=version,
    description="AI服务模块 - 知识库智能化升级的核心功能支持",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AI Services Team",
    author_email="ai_services@example.com",
    url="https://github.com/example/ai_services",
    packages=find_packages(),
    package_data={
        'ai_services': ['nlp/stopwords.txt']
    },
    include_package_data=True,
    install_requires=[
        'numpy>=1.20.0',
        'networkx>=2.6.0',
        'openai>=0.27.0',
        'faiss-cpu>=1.7.3',
        'jieba>=0.42.1',
        'scikit-learn>=1.0.0'
    ],
    extras_require={
        'gpu': ['faiss-gpu>=1.7.3'],
        'yaml': ['pyyaml>=6.0'],
        'dev': [
            'pytest>=7.0.0',
            'black>=22.0.0',
            'isort>=5.0.0'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Text Processing :: General',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='ai, llm, vector store, knowledge graph, nlp',
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'ai_service_demo=ai_services.example_app:main',
        ],
    },
    project_urls={
        'Documentation': 'https://github.com/example/ai_services#readme',
        'Bug Reports': 'https://github.com/example/ai_services/issues',
        'Source': 'https://github.com/example/ai_services',
    },
    license='MIT'
)