#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文档格式转换工具：将DOCX文件转换为Markdown格式

使用方法:
    python docx_to_markdown.py 输入文件.docx [输出文件.md]

如果不指定输出文件，默认使用与输入文件同名的.md文件
"""

import os
import sys
import re
from docx import Document


def convert_docx_to_markdown(input_file, output_file=None):
    """
    将DOCX文件转换为Markdown格式
    
    Args:
        input_file (str): 输入的DOCX文件路径
        output_file (str, optional): 输出的Markdown文件路径
    
    Returns:
        str: 生成的Markdown文件路径
    """
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"错误：找不到输入文件 '{input_file}'")
        sys.exit(1)
    
    # 检查文件扩展名是否为docx
    if not input_file.lower().endswith('.docx'):
        print(f"错误：输入文件必须是.docx格式")
        sys.exit(1)
    
    # 如果未指定输出文件，则使用输入文件的名称，将扩展名改为.md
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + '.md'
    
    try:
        # 读取DOCX文件
        doc = Document(input_file)
        
        # 创建Markdown内容
        markdown_content = []
        
        for para in doc.paragraphs:
            # 跳过空段落
            if not para.text.strip():
                markdown_content.append('')
                continue
            
            try:
                # 处理标题
                if para.style and para.style.name and para.style.name.startswith('Heading'):
                    # 提取标题级别（1-9）
                    try:
                        level = int(para.style.name.replace('Heading ', ''))
                        if 1 <= level <= 6:  # Markdown最多支持6级标题
                            markdown_content.append(f"{'#' * level} {para.text}")
                        else:
                            # 级别超过6的标题，使用普通段落
                            markdown_content.append(para.text)
                    except ValueError:
                        # 无法解析标题级别，作为普通段落处理
                        markdown_content.append(para.text)
                
                # 处理列表（项目符号和编号）
                elif para.style and para.style.name and para.style.name.startswith('List Bullet'):
                    markdown_content.append(f"* {para.text}")
                elif para.style and para.style.name and para.style.name.startswith('List Number'):
                    # 简化处理，所有编号列表都使用1. 作为前缀
                    markdown_content.append(f"1. {para.text}")
                
                # 处理引用
                elif para.style and para.style.name and para.style.name.startswith('Quote'):
                    markdown_content.append(f"> {para.text}")
                
                # 处理代码块（这里简化处理，实际docx中可能没有直接的代码块样式）
                elif para.style and para.style.name and 'code' in para.style.name.lower():
                    # 检查是否已经有代码块开始标记
                    if markdown_content and not markdown_content[-1].startswith('```'):
                        markdown_content.append('```')
                    markdown_content.append(para.text)
                    # 代码块结束（后续可能需要更复杂的逻辑来检测代码块结束）
                    markdown_content.append('```')
                
                # 普通段落
                else:
                    markdown_content.append(para.text)
            except Exception:
                # 任何异常都作为普通段落处理
                markdown_content.append(para.text)
        
        # 处理表格
        for table in doc.tables:
            # 添加一个空行分隔表格和前后内容
            markdown_content.append('')
            
            # 处理表头
            headers = [cell.text.strip() for cell in table.rows[0].cells]
            markdown_content.append('| ' + ' | '.join(headers) + ' |')
            
            # 添加分隔线
            separators = ['---'] * len(headers)
            markdown_content.append('| ' + ' | '.join(separators) + ' |')
            
            # 处理表格内容
            for row in table.rows[1:]:
                cells = [cell.text.strip() for cell in row.cells]
                markdown_content.append('| ' + ' | '.join(cells) + ' |')
            
            # 添加一个空行
            markdown_content.append('')
        
        # 合并所有内容并写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(markdown_content))
        
        print(f"成功将 '{input_file}' 转换为 '{output_file}'")
        return output_file
    
    except Exception as e:
        print(f"转换过程中发生错误: {str(e)}")
        sys.exit(1)


def show_help():
    """显示帮助信息"""
    print("文档格式转换工具：将DOCX文件转换为Markdown格式")
    print("\n使用方法:")
    print("    python docx_to_markdown.py 输入文件.docx [输出文件.md]")
    print("\n选项:")
    print("    -h, --help    显示此帮助信息")


if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) < 2 or len(sys.argv) > 3 or sys.argv[1] in ['-h', '--help']:
        show_help()
        sys.exit(0)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) == 3 else None
    
    # 执行转换
    convert_docx_to_markdown(input_file, output_file)