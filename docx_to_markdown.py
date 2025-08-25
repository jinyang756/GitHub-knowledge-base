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
from docx.shared import Inches
import shutil
import uuid
from datetime import datetime


def convert_docx_to_markdown(input_file, output_file=None):
    """
    将DOCX文件转换为Markdown格式，并自动适配项目文档规范
    
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
    
    # 创建图片目录
    output_dir = os.path.dirname(output_file)
    if not output_dir:
        output_dir = os.getcwd()
    
    images_dir = os.path.join(output_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    # 初始化脚注存储
    footnotes = {}
    
    try:
        # 读取DOCX文件
        doc = Document(input_file)
        
        # 创建Markdown内容
        markdown_content = []
        
        # 标记是否在代码块内
        in_code_block = False
        
        for para in doc.paragraphs:
            # 跳过空段落
            if not para.text.strip():
                markdown_content.append('')
                continue
            
            try:
                # 获取段落文本，检查是否包含脚注引用
                para_text = para.text
                
                # 检查并提取脚注（简化处理，实际可能需要更复杂的解析）
                # 这里假设脚注格式为 [^数字]
                if '[' in para_text and ']' in para_text:
                    footnotes_refs = re.findall(r'\[\^(\d+)\]', para_text)
                    for ref in footnotes_refs:
                        if ref not in footnotes:
                            # 生成一个简单的脚注内容（实际应该从文档中提取）
                            footnotes[ref] = f"脚注{ref}：请参考原始文档获取详细注释"
            except Exception:
                para_text = para.text
            
            try:
                # 处理标题
                if para.style and para.style.name and para.style.name.startswith('Heading'):
                    # 提取标题级别（1-9）
                    try:
                        level = int(para.style.name.replace('Heading ', ''))
                        if 1 <= level <= 6:  # Markdown最多支持6级标题
                            # 处理标题文本，添加data-number标记
                            titled_text = add_data_number_markers(para_text)
                            markdown_content.append(f"{'#' * level} {titled_text}")
                        else:
                            # 级别超过6的标题，使用普通段落并添加data-number标记
                            markdown_content.append(add_data_number_markers(para_text))
                    except ValueError:
                        # 无法解析标题级别，作为普通段落处理并添加data-number标记
                        markdown_content.append(add_data_number_markers(para_text))
                
                # 处理列表（项目符号和编号）
                elif para.style and para.style.name and para.style.name.startswith('List Bullet'):
                    # 处理列表项文本，添加data-number标记
                    list_text = add_data_number_markers(para_text)
                    markdown_content.append(f"* {list_text}")
                elif para.style and para.style.name and para.style.name.startswith('List Number'):
                    # 简化处理，所有编号列表都使用1. 作为前缀
                    # 处理列表项文本，添加data-number标记
                    list_text = add_data_number_markers(para_text)
                    markdown_content.append(f"1. {list_text}")
                
                # 处理引用
                elif para.style and para.style.name and para.style.name.startswith('Quote'):
                    # 处理引用文本，添加data-number标记
                    quote_text = add_data_number_markers(para_text)
                    markdown_content.append(f"> {quote_text}")
                
                # 处理代码块
                elif para.style and para.style.name and 'code' in para.style.name.lower():
                    if not in_code_block:
                        markdown_content.append('```')
                        in_code_block = True
                    # 代码块中的内容不添加data-number标记
                    markdown_content.append(para_text)
                
                # 普通段落
                else:
                    # 如果之前在代码块内，现在应该结束代码块
                    if in_code_block:
                        markdown_content.append('```')
                        in_code_block = False
                    
                    # 处理普通段落文本，添加data-number标记
                    para_text_with_markers = add_data_number_markers(para_text)
                    markdown_content.append(para_text_with_markers)
            except Exception as e:
                # 任何异常都作为普通段落处理，并添加错误信息
                error_msg = f"[转换警告：段落处理出错 - {str(e)}]"
                markdown_content.append(add_data_number_markers(para.text) + error_msg)
        
        # 如果最后还在代码块内，添加结束标记
        if in_code_block:
            markdown_content.append('```')
        
        # 处理表格 - 增强版
        for table_idx, table in enumerate(doc.tables):
            try:
                # 添加一个空行分隔表格和前后内容
                markdown_content.append('')
                
                # 为复杂表格添加注释
                if len(table.rows) > 10 or len(table.columns) > 5:
                    markdown_content.append(f"<!-- 复杂表格{table_idx+1}：可能需要手动调整格式 -->")
                
                # 处理表头
                headers = []
                for cell in table.rows[0].cells:
                    # 处理表头单元格文本，添加data-number标记
                    header_text = add_data_number_markers(cell.text.strip())
                    headers.append(header_text)
                markdown_content.append('| ' + ' | '.join(headers) + ' |')
                
                # 添加分隔线
                separators = ['---'] * len(headers)
                markdown_content.append('| ' + ' | '.join(separators) + ' |')
                
                # 处理表格内容
                for row in table.rows[1:]:
                    cells = []
                    for cell in row.cells:
                        # 处理表格单元格文本，添加data-number标记
                        cell_text = add_data_number_markers(cell.text.strip())
                        cells.append(cell_text)
                    markdown_content.append('| ' + ' | '.join(cells) + ' |')
                
                # 添加一个空行
                markdown_content.append('')
            except Exception as e:
                # 表格处理出错时添加错误信息
                error_msg = f"[转换警告：表格{table_idx+1}处理出错 - {str(e)}]"
                markdown_content.append(error_msg)
        
        # 处理图片
        image_count = 0
        for rel in doc.part.rels.values():
            if "image" in rel.target_ref:
                try:
                    # 获取图片数据
                    image_part = rel.target_part
                    image_bytes = image_part._blob
                    
                    # 确定图片格式
                    content_type = image_part.content_type
                    if content_type == 'image/png':
                        ext = '.png'
                    elif content_type == 'image/jpeg':
                        ext = '.jpg'
                    elif content_type == 'image/gif':
                        ext = '.gif'
                    else:
                        ext = '.png'  # 默认使用PNG格式
                    
                    # 生成唯一的图片文件名
                    image_name = f"image_{uuid.uuid4().hex[:8]}{ext}"
                    image_path = os.path.join(images_dir, image_name)
                    
                    # 保存图片
                    with open(image_path, 'wb') as f:
                        f.write(image_bytes)
                    
                    # 在Markdown中添加图片引用
                    rel_path = os.path.relpath(image_path, output_dir)
                    markdown_content.append(f"![图片{image_count+1}]({rel_path})\n")
                    image_count += 1
                except Exception as e:
                    # 图片处理出错时添加错误信息
                    error_msg = f"[转换警告：图片处理出错 - {str(e)}]"
                    markdown_content.append(error_msg)
        
        # 添加脚注
        if footnotes:
            markdown_content.append('')
            markdown_content.append('## 注释')
            for ref, content in sorted(footnotes.items(), key=lambda x: int(x[0])):
                markdown_content.append(f"[^ref{ref}]: {content}")
        
        # 添加文档元数据和规范说明
        markdown_content.insert(0, f"<!-- 文档转换自: {os.path.basename(input_file)} -->")
        markdown_content.insert(1, f"<!-- 转换时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -->")
        markdown_content.insert(2, "<!-- 提示: 文档中的关键数据已使用data-number类标记 -->")
        markdown_content.insert(3, '')
        
        # 合并所有内容并写入文件
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(markdown_content))
            
            print(f"成功将 '{input_file}' 转换为 '{output_file}'")
            if image_count > 0:
                print(f"  - 成功提取并保存了 {image_count} 张图片")
            if footnotes:
                print(f"  - 识别并处理了 {len(footnotes)} 个脚注引用")
            print("  - 已自动为关键数据添加 data-number 标记")
            return output_file
        except IOError as e:
            print(f"写入输出文件时发生错误: {str(e)}")
            sys.exit(1)
    
    except Exception as e:
        print(f"转换过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def add_data_number_markers(text):
    """
    为文本中的关键数据（数字、百分比等）添加data-number类标记
    
    Args:
        text (str): 输入文本
        
    Returns:
        str: 添加了data-number标记的文本
    """
    if not text:
        return text
    
    # 定义需要标记的模式：数字、百分比、货币金额等
    # 排除代码块中的内容和已经被标记的内容
    if '```' not in text and '<span class="data-number">' not in text:
        # 匹配：
        # 1. 整数或小数（可能带正负号）
        # 2. 百分比
        # 3. 带单位的数值
        patterns = [
            # 匹配数字：整数、小数、科学计数法，可能带正负号
            r'([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)',
            # 匹配百分比
            r'(\d+(?:\.\d+)?%)',
            # 匹配带常见单位的数值
            r'(\d+(?:\.\d+)?\s*(?:万元|亿元|亿美元|人民币|美元|欧元|日元|英镑|公斤|吨|米|公里|平方米|公顷))'
        ]
        
        # 合并所有模式
        combined_pattern = '|'.join(patterns)
        
        # 使用正则表达式替换，为匹配的数字添加data-number标记
        def replace_with_marker(match):
            # 获取匹配的内容
            matched_text = match.group(0)
            # 返回添加了标记的内容
            return f'<span class="data-number">{matched_text}</span>'
        
        # 应用替换，但避免重复标记
        result = re.sub(combined_pattern, replace_with_marker, text)
        return result
    
    return text


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