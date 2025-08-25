#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的DOC到DOCX转换工具
"""

import os
import sys
import win32com.client  # 需要安装pywin32库
import time


def convert_doc_to_docx(input_file, output_file=None):
    """
    将DOC文件转换为DOCX格式
    
    Args:
        input_file (str): 输入的DOC文件路径
        output_file (str, optional): 输出的DOCX文件路径
        
    Returns:
        str: 生成的DOCX文件路径
    """
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"错误：找不到输入文件 '{input_file}'")
        sys.exit(1)
    
    # 检查文件扩展名是否为doc
    if not input_file.lower().endswith('.doc'):
        print(f"错误：输入文件必须是.doc格式")
        sys.exit(1)
    
    # 如果未指定输出文件，则使用输入文件的名称，将扩展名改为.docx
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + '.docx'
    
    try:
        # 创建Word COM对象
        word = win32com.client.Dispatch('Word.Application')
        word.Visible = False
        word.DisplayAlerts = 0  # 不显示警告对话框
        
        # 打开DOC文件
        doc = word.Documents.Open(os.path.abspath(input_file))
        
        # 保存为DOCX格式
        # 16 = wdFormatXMLDocument (docx格式)
        doc.SaveAs(os.path.abspath(output_file), FileFormat=16)
        
        # 关闭文档和Word应用
        doc.Close()
        word.Quit()
        
        print(f"成功将 '{input_file}' 转换为 '{output_file}'")
        return output_file
    except Exception as e:
        print(f"转换过程中发生错误: {str(e)}")
        # 确保关闭Word应用
        try:
            word.Quit()
        except:
            pass
        sys.exit(1)


if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("使用方法:")
        print("    python convert_doc_to_docx.py 输入文件.doc [输出文件.docx]")
        sys.exit(0)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) == 3 else None
    
    # 执行转换
    convert_doc_to_docx(input_file, output_file)