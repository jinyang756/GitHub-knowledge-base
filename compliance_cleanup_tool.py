#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国泰海通证券知识库 - 合规内容清理工具
用于自动清理知识库中的潜在合规风险和敏感信息
"""

import os
import re
import argparse
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime

class ComplianceCleanupTool:
    def __init__(self, root_dir: str, dry_run: bool = False):
        """初始化合规内容清理工具"""
        self.root_dir = root_dir
        self.dry_run = dry_run  # 模拟运行模式，不实际修改文件
        self.cleanup_count = 0
        self.processed_files = 0
        self.ignored_files = []
        
        # 定义清理规则
        self.cleanup_rules = {
            # 股票代码清理规则
            'stock_code': {
                'pattern': re.compile(r'(\d{6})\s*[股票股份中体]'),
                'replacement': 'XXX $1',  # 替换为XXX + 部分代码
                'description': '股票代码'
            },
            # 价格信息清理规则
            'price': {
                'pattern': re.compile(r'([\d.]+)\s*元'),
                'replacement': '[价格信息]',
                'description': '价格信息'
            },
            # 仓位建议清理规则
            'position': {
                'pattern': re.compile(r'(\d+成|\d+%|\d+资金|\d+仓位|金字塔建仓|分批次介入)'),
                'replacement': '[投资比例建议]',
                'description': '仓位建议'
            },
            # 投资引导性语言清理规则
            'investment_guidance': {
                'pattern': re.compile(r'(抄底牛股|获利\d+%|牛股|买入信号|金叉|买入|卖出|建仓|目标价位|止盈|止损)'),
                'replacement': lambda m: f'[{m.group(1)}]',
                'description': '投资引导性语言'
            },
            # 真实人物姓名清理规则
            'real_names': {
                'pattern': re.compile(r'(吕平波|但斌)'),
                'replacement': '[分析师]',
                'description': '真实人物姓名'
            },
            # 机构名称规范化规则
            'institution_name': {
                'pattern': re.compile(r'(国泰海通证券|国泰君安|海通证券)'),
                'replacement': '[金融机构]',  # 或者保留原始名称，如果有授权
                'description': '机构名称'
            }
        }
        
        # 清理日志
        self.cleanup_log = {
            'timestamp': datetime.now().isoformat(),
            'root_dir': root_dir,
            'dry_run': dry_run,
            'processed_files': [],
            'cleanup_summary': {}
        }
    
    def run(self) -> None:
        """运行合规内容清理工具"""
        print(f"开始清理知识库内容，根目录: {self.root_dir}")
        print(f"运行模式: {'模拟运行(不实际修改文件)' if self.dry_run else '实际运行(将修改文件)'}")
        
        # 扫描docs目录下的所有文件
        for root, dirs, files in os.walk(os.path.join(self.root_dir, 'docs')):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    self._process_file(file_path)
        
        # 生成清理报告
        self._generate_report()
        
        print(f"\n清理完成！")
        print(f"总共处理文件数: {self.processed_files}")
        print(f"清理文件数: {self.cleanup_count}")
        if self.ignored_files:
            print(f"忽略文件数: {len(self.ignored_files)}")
            for file in self.ignored_files:
                print(f"  - {file}")
    
    def _process_file(self, file_path: str) -> None:
        """处理单个文件，清理其中的合规风险内容"""
        relative_path = os.path.relpath(file_path, self.root_dir)
        self.processed_files += 1
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.ignored_files.append(f"{relative_path} (读取错误: {str(e)})")
            return
        
        # 记录原始内容哈希值，用于检查是否有修改
        original_content = content
        file_log = {
            'file_path': relative_path,
            'changes': {}
        }
        
        # 应用清理规则
        for rule_name, rule_info in self.cleanup_rules.items():
            pattern = rule_info['pattern']
            replacement = rule_info['replacement']
            description = rule_info['description']
            
            # 查找所有匹配
            matches = pattern.findall(content)
            if not matches:
                continue
            
            # 记录匹配数量
            match_count = len(set(matches))  # 去重
            file_log['changes'][rule_name] = {
                'description': description,
                'match_count': match_count,
                'unique_matches': list(set(matches))
            }
            
            # 应用替换
            if callable(replacement):
                content = pattern.sub(replacement, content)
            else:
                content = pattern.sub(replacement, content)
        
        # 检查内容是否发生变化
        if content != original_content:
            self.cleanup_count += 1
            
            # 更新日志
            self.cleanup_log['processed_files'].append(file_log)
            
            # 更新清理摘要
            for rule_name in file_log['changes']:
                if rule_name not in self.cleanup_log['cleanup_summary']:
                    self.cleanup_log['cleanup_summary'][rule_name] = 0
                self.cleanup_log['cleanup_summary'][rule_name] += 1
            
            # 输出清理信息
            print(f"清理文件: {relative_path}")
            for rule_name, rule_info in file_log['changes'].items():
                print(f"  - {rule_info['description']}: 发现{rule_info['match_count']}个匹配项")
            
            # 保存修改后的内容（如果不是模拟运行）
            if not self.dry_run:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                except Exception as e:
                    print(f"  保存文件失败: {str(e)}")
    
    def _generate_report(self) -> None:
        """生成清理报告"""
        # 生成日志文件
        log_file_path = os.path.join(self.root_dir, '合规内容清理日志.json')
        with open(log_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.cleanup_log, f, ensure_ascii=False, indent=2)
        
        # 生成可读报告
        report_path = os.path.join(self.root_dir, '合规内容清理报告.md')
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('# 国泰海通证券知识库 - 合规内容清理报告\n\n')
            f.write(f'## 清理概况\n')
            f.write(f'- 清理时间: {self.cleanup_log["timestamp"]}\n')
            f.write(f'- 根目录: {self.cleanup_log["root_dir"]}\n')
            f.write(f'- 运行模式: {'模拟运行(不实际修改文件)' if self.cleanup_log['dry_run'] else '实际运行(已修改文件)'}\n')
            f.write(f'- 总共处理文件数: {self.processed_files}\n')
            f.write(f'- 清理文件数: {self.cleanup_count}\n')
            if self.ignored_files:
                f.write(f'- 忽略文件数: {len(self.ignored_files)}\n\n')
            
            # 清理摘要
            f.write('\n## 清理摘要\n')
            for rule_name, count in self.cleanup_log['cleanup_summary'].items():
                if rule_name in self.cleanup_rules:
                    f.write(f'- {self.cleanup_rules[rule_name]["description"]}: 清理了{count}个文件\n')
            
            # 详细清理信息
            if self.cleanup_log['processed_files']:
                f.write('\n## 详细清理信息\n')
                for file_log in self.cleanup_log['processed_files']:
                    f.write(f'\n### {file_log["file_path"]}\n')
                    for rule_name, rule_info in file_log['changes'].items():
                        f.write(f'- {rule_info["description"]}: 发现{rule_info["match_count"]}个匹配项\n')
            
            # 整改建议
            f.write('\n## 后续整改建议\n')
            f.write('1. **审核清理结果**: 请人工审核清理后的文件，确保清理效果符合预期\n')
            f.write('2. **建立内容审核机制**: 制定知识库内容发布前的合规审核流程\n')
            f.write('3. **定期合规检查**: 定期运行compliance_checker.py进行合规性检查\n')
            f.write('4. **确认机构名称授权**: 如要使用"国泰海通证券"等机构名称，请确保已获得授权\n')
            f.write('5. **培训内容贡献者**: 向内容贡献者提供合规培训，避免在未来的内容中引入类似风险\n')
    
    def create_backup(self) -> None:
        """为知识库创建备份（可选功能）"""
        # 这个功能可以根据需要实现，用于在清理前创建知识库的备份
        pass

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='国泰海通证券知识库 - 合规内容清理工具')
    parser.add_argument('--root-dir', type=str, default=os.path.dirname(os.path.abspath(__file__)),
                        help='知识库根目录路径')
    parser.add_argument('--dry-run', action='store_true', default=False,
                        help='模拟运行模式，不实际修改文件')
    
    args = parser.parse_args()
    
    # 创建清理工具并运行
    cleanup_tool = ComplianceCleanupTool(args.root_dir, args.dry_run)
    cleanup_tool.run()

if __name__ == '__main__':
    main()