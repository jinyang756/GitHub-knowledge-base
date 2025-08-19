#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库API服务

该服务提供RESTful API接口，让其他应用可以读取知识库中每个文件夹的内容。

使用方法：
1. 安装依赖: pip install flask markdown
2. 运行服务: python knowledge_base_api.py
3. 访问API: http://localhost:5000/api/categories

API端点说明:
- GET /api/categories - 获取所有分类列表
- GET /api/categories/{category} - 获取指定分类下的文件列表
- GET /api/categories/{category}/{filename} - 获取指定文件的内容
"""

import os
import json
from flask import Flask, jsonify, request, send_from_directory
import markdown
from datetime import datetime

app = Flask(__name__)

# 配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
ALLOWED_EXTENSIONS = {'md', 'markdown', 'txt'}

# 日志函数
def log(message):
    """记录日志信息"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

# 检查文件是否允许访问
def allowed_file(filename):
    """检查文件是否允许访问"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 获取所有分类
def get_all_categories():
    """获取所有分类列表"""
    categories = []
    try:
        # 遍历docs目录下的所有子目录（除了特殊目录）
        special_dirs = ['.vuepress', '.nojekyll', '_sidebar', '_coverpage']
        for item in os.listdir(DOCS_DIR):
            item_path = os.path.join(DOCS_DIR, item)
            if os.path.isdir(item_path) and item not in special_dirs:
                # 检查是否有README.md文件作为分类描述
                readme_path = os.path.join(item_path, 'README.md')
                description = ""
                if os.path.exists(readme_path):
                    try:
                        with open(readme_path, 'r', encoding='utf-8') as f:
                            # 提取README的第一行作为描述
                            first_line = f.readline().strip()
                            # 移除可能的Markdown标题符号
                            if first_line.startswith('#'):
                                description = first_line.lstrip('#').strip()
                    except Exception as e:
                        log(f"读取{readme_path}时出错: {str(e)}")
                
                categories.append({
                    'name': item,
                    'path': item,
                    'description': description,
                    'file_count': len([f for f in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, f)) and allowed_file(f)])
                })
    except Exception as e:
        log(f"获取分类列表时出错: {str(e)}")
    
    return categories

# 获取分类下的文件列表
def get_category_files(category):
    """获取指定分类下的文件列表"""
    files = []
    category_path = os.path.join(DOCS_DIR, category)
    
    try:
        # 检查分类是否存在
        if not os.path.exists(category_path) or not os.path.isdir(category_path):
            return None
        
        # 遍历分类目录下的所有文件
        for item in os.listdir(category_path):
            item_path = os.path.join(category_path, item)
            if os.path.isfile(item_path) and allowed_file(item):
                # 获取文件信息
                stats = os.stat(item_path)
                files.append({
                    'name': item,
                    'path': os.path.join(category, item),
                    'size': stats.st_size,
                    'modified_time': datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })
    except Exception as e:
        log(f"获取{category}分类文件列表时出错: {str(e)}")
    
    return files

# 获取文件内容
def get_file_content(category, filename):
    """获取指定文件的内容"""
    file_path = os.path.join(DOCS_DIR, category, filename)
    
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path) or not os.path.isfile(file_path) or not allowed_file(filename):
            return None
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 获取文件统计信息
        stats = os.stat(file_path)
        
        return {
            'name': filename,
            'category': category,
            'content': content,
            'size': stats.st_size,
            'modified_time': datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        log(f"读取{category}/{filename}文件内容时出错: {str(e)}")
    
    return None

# API端点: 获取所有分类
@app.route('/api/categories', methods=['GET'])
def api_get_categories():
    """获取所有分类的API端点"""
    categories = get_all_categories()
    return jsonify({
        'success': True,
        'data': categories,
        'count': len(categories)
    })

# API端点: 获取指定分类下的文件
@app.route('/api/categories/<category>', methods=['GET'])
def api_get_category_files(category):
    """获取指定分类下文件的API端点"""
    files = get_category_files(category)
    if files is None:
        return jsonify({
            'success': False,
            'error': '分类不存在'
        }), 404
    
    return jsonify({
        'success': True,
        'category': category,
        'data': files,
        'count': len(files)
    })

# API端点: 获取文件内容
@app.route('/api/categories/<category>/<path:filename>', methods=['GET'])
def api_get_file_content(category, filename):
    """获取指定文件内容的API端点"""
    file_content = get_file_content(category, filename)
    if file_content is None:
        return jsonify({
            'success': False,
            'error': '文件不存在或不允许访问'
        }), 404
    
    # 检查是否需要返回HTML格式
    if request.args.get('format') == 'html' and filename.lower().endswith(('.md', '.markdown')):
        try:
            html_content = markdown.markdown(file_content['content'])
            return jsonify({
                'success': True,
                'data': {
                    **file_content,
                    'html_content': html_content
                }
            })
        except Exception as e:
            log(f"转换Markdown到HTML时出错: {str(e)}")
    
    return jsonify({
        'success': True,
        'data': file_content
    })

# 静态文件服务
@app.route('/api/static/<path:filename>')
def serve_static(filename):
    """提供静态文件访问"""
    return send_from_directory(DOCS_DIR, filename)

# 提供管理界面访问
@app.route('/admin.html')
def serve_admin():
    """提供管理界面访问"""
    return send_from_directory(BASE_DIR, 'admin.html')

# 健康检查端点
@app.route('/api/health')
def health_check():
    """API健康检查端点"""
    return jsonify({
        'success': True,
        'status': 'running',
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

# 创建分类端点
@app.route('/api/categories', methods=['POST'])
def create_category():
    """创建新分类的API端点"""
    try:
        data = request.json
        if not data or 'name' not in data:
            return jsonify({
                'success': False,
                'error': '请提供分类名称'
            }), 400
        
        category_name = data['name']
        # 验证分类名称是否合法
        if not category_name or not category_name.strip():
            return jsonify({
                'success': False,
                'error': '分类名称不能为空'
            }), 400
        
        # 检查是否包含非法字符
        import re
        if re.search(r'[^\w\-\u4e00-\u9fa5]', category_name):
            return jsonify({
                'success': False,
                'error': '分类名称只能包含字母、数字、下划线、连字符和中文字符'
            }), 400
        
        category_path = os.path.join(DOCS_DIR, category_name)
        
        # 检查分类是否已存在
        if os.path.exists(category_path):
            return jsonify({
                'success': False,
                'error': '分类已存在'
            }), 400
        
        # 创建分类目录
        os.makedirs(category_path)
        
        # 可选：创建默认的README.md文件
        if 'description' in data:
            readme_path = os.path.join(category_path, 'README.md')
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(f"# {data['description']}\n\n这是 {category_name} 分类的描述文件。")
        
        log(f'分类创建成功: {category_name}')
        
        return jsonify({
            'success': True,
            'message': '分类创建成功',
            'data': {
                'name': category_name,
                'path': category_name,
                'description': data.get('description', ''),
                'file_count': 0
            }
        })
    except Exception as e:
        log(f'创建分类失败: {str(e)}')
        return jsonify({
            'success': False,
            'error': f'创建分类失败: {str(e)}'
        }), 500

# 文件上传端点
@app.route('/api/categories/<category>/upload', methods=['POST'])
def upload_file(category):
    """上传文件到指定分类的API端点"""
    # 检查分类是否存在
    category_path = os.path.join(DOCS_DIR, category)
    if not os.path.exists(category_path) or not os.path.isdir(category_path):
        return jsonify({
            'success': False,
            'error': '分类不存在'
        }), 404
    
    # 检查是否有文件上传
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': '没有文件上传'
        }), 400
    
    file = request.files['file']
    
    # 检查文件名是否为空
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': '文件名不能为空'
        }), 400
    
    # 检查文件类型是否允许
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': f'不支持的文件类型，仅支持: {', '.join(ALLOWED_EXTENSIONS)}'
        }), 400
    
    try:
        # 保存文件到分类目录
        file_path = os.path.join(category_path, file.filename)
        file.save(file_path)
        
        # 获取文件信息
        stats = os.stat(file_path)
        
        log(f'文件上传成功: {category}/{file.filename} ({stats.st_size} bytes)')
        
        return jsonify({
            'success': True,
            'message': '文件上传成功',
            'data': {
                'name': file.filename,
                'category': category,
                'path': os.path.join(category, file.filename),
                'size': stats.st_size,
                'upload_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    except Exception as e:
        log(f'文件上传失败: {str(e)}')
        return jsonify({
            'success': False,
            'error': f'文件上传失败: {str(e)}'
        }), 500

# 删除文档端点
@app.route('/api/categories/<category>/<path:filename>', methods=['DELETE'])
def delete_file(category, filename):
    """删除指定文档的API端点"""
    file_path = os.path.join(DOCS_DIR, category, filename)
    
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path) or not os.path.isfile(file_path) or not allowed_file(filename):
            return jsonify({
                'success': False,
                'error': '文件不存在或不允许访问'
            }), 404
        
        # 删除文件
        os.remove(file_path)
        
        log(f'文件删除成功: {category}/{filename}')
        
        return jsonify({
            'success': True,
            'message': '文件删除成功',
            'data': {
                'name': filename,
                'category': category,
                'path': os.path.join(category, filename)
            }
        })
    except Exception as e:
        log(f'文件删除失败: {str(e)}')
        return jsonify({
            'success': False,
            'error': f'文件删除失败: {str(e)}'
        }), 500

if __name__ == '__main__':
    log("知识库API服务启动中...")
    log(f"文档目录: {DOCS_DIR}")
    log("API服务运行在 http://localhost:5000")
    log("可用端点:")
    log("  - /api/health          - 健康检查")
    log("  - GET /api/categories  - 获取所有分类")
    log("  - POST /api/categories - 创建新分类")
    log("  - /api/categories/{分类名} - 获取分类下的文件")
    log("  - GET /api/categories/{分类名}/{文件名} - 获取文件内容")
    log("  - DELETE /api/categories/{分类名}/{文件名} - 删除文件")
    log("  - /api/categories/{分类名}/upload - 上传文件到分类")
    
    # 启动API服务
    app.run(host='0.0.0.0', port=5000, debug=False)