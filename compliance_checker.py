#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文档合规性检查工具

用于检查Markdown文档是否符合项目规范要求，包括：
- 关键数据是否正确使用data-number类标记
- 标题层级是否规范
- 表格格式是否正确
- 代码块是否完整
- 其他文档格式要求

使用方法:
    python compliance_checker.py 文件路径.md
    python compliance_checker.py 目录路径  # 递归检查目录下所有.md文件
"""

import os
import sys
import re
import argparse
from datetime import datetime

# 定义合规性检查规则
class ComplianceRules:
    # 标题层级规则：允许1-6级标题，不允许跳跃层级
    MAX_HEADING_LEVEL = 6
    # 关键数据标记规则
    DATA_NUMBER_PATTERN = r'<span\s+class="data-number">.*?<\/span>'
    # 需要标记的数字模式
    NUMBER_PATTERN = r'([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)|(\d+(?:\.\d+)?%)|(\d+(?:\.\d+)?\s*(?:万元|亿元|亿美元|人民币|美元|欧元|日元|英镑|公斤|吨|米|公里|平方米|公顷))'
    # 排除的数字（在代码块、链接等中的数字不需要标记）
    EXCLUDE_PATTERNS = [
        r'`[^`]*?\d+[^`]*?`',  # 行内代码
        r'```[\s\S]*?```',      # 代码块
        r'!?\[.*?\]\(.*?\)',   # 链接和图片
        r'\d{1,2}\/\d{1,2}\/\d{2,4}',  # 日期格式
        r'\d{4}-\d{2}-\d{2}',  # ISO日期格式
        r'#[0-9a-fA-F]{6}',      # 颜色代码
        r'\b(?:19|20)\d{2}\b', # 年份
    ]
    # 表格格式规则
    TABLE_HEADER_PATTERN = r'^\|.*\|$'
    TABLE_SEPARATOR_PATTERN = r'^\|(?:\s*-+\s*\|)+$'

class ComplianceChecker:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.issues = []
        self.total_files = 0
        self.files_with_issues = 0
        
    def check_file(self, file_path):
        """检查单个文件的合规性"""
        if not os.path.exists(file_path):
            print(f"错误：找不到文件 '{file_path}'")
            return False
        
        if not file_path.lower().endswith('.md'):
            print(f"警告：'{file_path}' 不是Markdown文件，跳过检查")
            return False
        
        self.total_files += 1
        file_issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # 检查文档元数据
            if not content.startswith('<!-- 文档转换自:') and not content.startswith('<!-- 文档创建时间:'):
                file_issues.append("文档缺少元数据注释")
            
            # 检查关键数据标记
            self._check_data_number_markers(content, file_issues)
            
            # 检查标题层级
            self._check_heading_levels(lines, file_issues)
            
            # 检查表格格式
            self._check_table_format(lines, file_issues)
            
            # 检查代码块完整性
            self._check_code_blocks(content, file_issues)
            
            # 检查图片引用格式
            self._check_image_references(content, file_issues)
            
            # 检查链接格式
            self._check_links(content, file_issues)
            
            # 如果有问题，记录文件和问题
            if file_issues:
                self.files_with_issues += 1
                self.issues.append({
                    'file': file_path,
                    'issues': file_issues
                })
                
                if self.verbose:
                    print(f"文件 '{file_path}' 发现 {len(file_issues)} 个合规性问题：")
                    for i, issue in enumerate(file_issues, 1):
                        print(f"  {i}. {issue}")
            else:
                if self.verbose:
                    print(f"文件 '{file_path}' 符合所有合规性要求")
            
            return True
        except Exception as e:
            error_msg = f"读取文件 '{file_path}' 时发生错误: {str(e)}"
            file_issues.append(error_msg)
            self.issues.append({
                'file': file_path,
                'issues': file_issues
            })
            print(error_msg)
            return False
    
    def check_directory(self, dir_path):
        """递归检查目录下所有Markdown文件"""
        if not os.path.exists(dir_path):
            print(f"错误：找不到目录 '{dir_path}'")
            return False
        
        if not os.path.isdir(dir_path):
            print(f"错误：'{dir_path}' 不是目录")
            return False
        
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.lower().endswith('.md'):
                    file_path = os.path.join(root, file)
                    self.check_file(file_path)
        
        return True
    
    def _check_data_number_markers(self, content, issues):
        """检查关键数据是否正确标记"""
        # 提取所有需要检查的文本（排除代码块、链接等）
        text_to_check = content
        
        # 移除需要排除的内容
        for pattern in ComplianceRules.EXCLUDE_PATTERNS:
            text_to_check = re.sub(pattern, '', text_to_check, flags=re.DOTALL)
        
        # 查找所有需要标记的数字
        matches = re.finditer(ComplianceRules.NUMBER_PATTERN, text_to_check)
        
        # 检查这些数字是否已经被标记
        unmarked_numbers = []
        for match in matches:
            number = match.group(0)
            # 检查这个数字是否在data-number标记中
            if not re.search(rf'<span\s+class="data-number">.*?{re.escape(number)}.*?<\/span>', content):
                unmarked_numbers.append(number)
        
        if unmarked_numbers:
            # 只显示前5个未标记的数字作为示例
            sample_numbers = unmarked_numbers[:5]
            issues.append(f"发现 {len(unmarked_numbers)} 个未标记的关键数据（示例：{', '.join(sample_numbers)}{'...' if len(unmarked_numbers) > 5 else ''}）")
    
    def _check_heading_levels(self, lines, issues):
        """检查标题层级是否规范"""
        prev_level = 0
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line.startswith('#'):
                # 计算标题级别
                level = 0
                while level < len(line) and line[level] == '#':
                    level += 1
                
                # 检查级别是否超出范围
                if level > ComplianceRules.MAX_HEADING_LEVEL:
                    issues.append(f"第{i}行：标题级别 {level} 超过最大允许级别 {ComplianceRules.MAX_HEADING_LEVEL}")
                
                # 检查级别是否跳跃（最多允许增加1级）
                if prev_level > 0 and level > prev_level + 1:
                    issues.append(f"第{i}行：标题级别从 {prev_level} 跳跃到 {level}，最多允许增加1级")
                
                prev_level = level
    
    def _check_table_format(self, lines, issues):
        """检查表格格式是否正确"""
        in_table = False
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            if in_table:
                if not line or line.startswith('|'):
                    continue
                else:
                    in_table = False
            
            if line.startswith('|'):
                # 检查是否是表头行
                if re.match(ComplianceRules.TABLE_HEADER_PATTERN, line):
                    # 检查下一行是否是分隔线
                    if i < len(lines) and re.match(ComplianceRules.TABLE_SEPARATOR_PATTERN, lines[i].strip()):
                        in_table = True
                    else:
                        issues.append(f"第{i}行：表格缺少分隔线行")
                # 检查分隔线行
                elif re.match(ComplianceRules.TABLE_SEPARATOR_PATTERN, line):
                    # 检查上一行是否是表头
                    if i > 1 and not re.match(ComplianceRules.TABLE_HEADER_PATTERN, lines[i-2].strip()):
                        issues.append(f"第{i}行：表格分隔线缺少表头行")
    
    def _check_code_blocks(self, content, issues):
        """检查代码块是否完整"""
        code_blocks = re.finditer(r'```([\s\S]*?)```', content)
        
        for i, block in enumerate(code_blocks, 1):
            code_content = block.group(1)
            # 检查代码块内容是否为空
            if not code_content.strip():
                issues.append(f"代码块 #{i}：内容为空")
            
        # 检查未闭合的代码块
        open_blocks = content.count('```') % 2
        if open_blocks > 0:
            issues.append(f"发现 {open_blocks} 个未闭合的代码块")
    
    def _check_image_references(self, content, issues):
        """检查图片引用格式是否正确"""
        images = re.finditer(r'!\[(.*?)\]\((.*?)\)', content)
        
        for i, image in enumerate(images, 1):
            alt_text, src = image.groups()
            # 检查图片是否有替代文本
            if not alt_text.strip():
                issues.append(f"图片 #{i}：缺少替代文本")
            
            # 检查图片路径是否有效
            if not src.strip():
                issues.append(f"图片 #{i}：缺少图片路径")
    
    def _check_links(self, content, issues):
        """检查链接格式是否正确"""
        links = re.finditer(r'\[(.*?)\]\((.*?)\)', content)
        
        for i, link in enumerate(links, 1):
            link_text, href = link.groups()
            # 检查链接是否有文本
            if not link_text.strip():
                issues.append(f"链接 #{i}：缺少链接文本")
            
            # 检查链接URL是否有效
            if not href.strip():
                issues.append(f"链接 #{i}：缺少链接URL")
    
    def generate_report(self, output_file=None):
        """生成合规性检查报告"""
        report = []
        report.append(f"# 文档合规性检查报告")
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"检查文件总数: {self.total_files}")
        report.append(f"有问题的文件数: {self.files_with_issues}")
        report.append(f"问题总数: {sum(len(issue['issues']) for issue in self.issues)}")
        report.append("")
        
        if self.issues:
            report.append("## 问题详情")
            for file_issue in self.issues:
                report.append(f"### {file_issue['file']}")
                for issue in file_issue['issues']:
                    report.append(f"- {issue}")
                report.append("")
        else:
            report.append("## 检查结果")
            report.append("所有文件均符合合规性要求！")
        
        report.append("")
        report.append("## 合规性规范建议")
        report.append('1. 所有关键数据（数字、百分比、金额等）应使用 `<span class="data-number">关键数据</span>` 标记')
        report.append("2. 标题层级应规范，最多6级，且不应跳跃级别")
        report.append("3. 表格应包含表头和分隔线")
        report.append("4. 代码块应完整闭合")
        report.append("5. 图片应有替代文本和有效路径")
        
        report_content = '\n'.join(report)
        
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(report_content)
                print(f"\n合规性检查报告已保存至 '{output_file}'")
            except Exception as e:
                print(f"\n保存报告时发生错误: {str(e)}")
        
        # 输出摘要
        print(f"\n--- 合规性检查摘要 ---")
        print(f"检查文件总数: {self.total_files}")
        print(f"有问题的文件数: {self.files_with_issues}")
        print(f"问题总数: {sum(len(issue['issues']) for issue in self.issues)}")
        print("---")
        
        return report_content

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='文档合规性检查工具')
    parser.add_argument('path', help='要检查的文件或目录路径')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细信息')
    parser.add_argument('-o', '--output', help='输出报告文件路径')
    
    args = parser.parse_args()
    
    # 创建检查器
    checker = ComplianceChecker(verbose=args.verbose)
    
    # 根据路径类型执行检查
    if os.path.isfile(args.path):
        checker.check_file(args.path)
    elif os.path.isdir(args.path):
        checker.check_directory(args.path)
    else:
        print(f"错误：'{args.path}' 不是有效的文件或目录")
        sys.exit(1)
    
    # 生成报告
    checker.generate_report(args.output)
    
    # 如果有问题，返回非零退出码
    if checker.files_with_issues > 0:
        sys.exit(1)
    
if __name__ == '__main__':
    main()