#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国泰海通证券知识库 - 合规性检查工具
用于识别知识库中的潜在合规风险和敏感信息
"""

import os
import re
import sys
from typing import List, Dict, Set, Tuple

class ComplianceChecker:
    def __init__(self, root_dir: str):
        """初始化合规检查器"""
        self.root_dir = root_dir
        self.risk_patterns = {
            # 证券代码模式
            'stock_code': re.compile(r'(\d{6})\s*[股票股份中体]'),
            # 价格模式
            'price': re.compile(r'([\d.]+)\s*元'),
            # 仓位建议模式
            'position': re.compile(r'(\d+成|\d+%|\d+资金|\d+仓位|金字塔建仓|分批次介入)'),
            # 投资引导性语言
            'investment_guidance': re.compile(r'(抄底牛股|获利\d+%|牛股|买入信号|金叉|买入|卖出|建仓|目标价位|止盈|止损)'),
            # 真实人物姓名模式
            'real_names': re.compile(r'(吕平波|但斌)'),
            # 机构名称模式
            'institution_name': re.compile(r'(国泰海通证券|国泰君安|海通证券)')
        }
        self.sensitive_files = []
        self.server_js_file = os.path.join(root_dir, 'docs', 'server.js')
        self.identified_issues = []

    def scan_files(self) -> None:
        """扫描知识库文件，识别潜在合规风险"""
        print(f"开始扫描知识库文件，根目录: {self.root_dir}")
        
        # 扫描docs目录下的所有文件
        for root, dirs, files in os.walk(os.path.join(self.root_dir, 'docs')):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    self._check_file(file_path)
        
        # 检查server.js的安全配置
        self._check_server_config()
        
        # 检查README.md中的目录一致性
        self._check_readme_consistency()
        
        # 生成报告
        self._generate_report()

    def _check_file(self, file_path: str) -> None:
        """检查单个文件中的合规风险"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.identified_issues.append({
                'type': '文件访问错误',
                'severity': '高',
                'file_path': file_path,
                'description': f'无法读取文件: {str(e)}'
            })
            return
        
        # 记录风险
        has_risk = False
        risk_details = {}
        
        for risk_type, pattern in self.risk_patterns.items():
            matches = pattern.findall(content)
            if matches:
                has_risk = True
                risk_details[risk_type] = list(set(matches))  # 去重
        
        if has_risk:
            relative_path = os.path.relpath(file_path, self.root_dir)
            self.sensitive_files.append(relative_path)
            
            issue_type = '证券投资咨询合规问题' if ('stock_code' in risk_details or 'price' in risk_details or 'position' in risk_details or 'investment_guidance' in risk_details) else '敏感信息'
            severity = '高' if issue_type == '证券投资咨询合规问题' else '中'
            
            self.identified_issues.append({
                'type': issue_type,
                'severity': severity,
                'file_path': relative_path,
                'description': f'包含以下类型的风险内容: {", ".join(risk_details.keys())}',
                'details': risk_details
            })

    def _check_server_config(self) -> None:
        """检查server.js的安全配置"""
        if not os.path.exists(self.server_js_file):
            self.identified_issues.append({
                'type': '配置文件缺失',
                'severity': '中',
                'file_path': os.path.relpath(self.server_js_file, self.root_dir),
                'description': 'server.js文件不存在'
            })
            return
        
        try:
            with open(self.server_js_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 检查Access-Control-Allow-Origin配置
            if 'Access-Control-Allow-Origin: *' in content:
                self.identified_issues.append({
                    'type': '跨域安全配置不当',
                    'severity': '高',
                    'file_path': os.path.relpath(self.server_js_file, self.root_dir),
                    'description': 'server.js中设置了Access-Control-Allow-Origin: *，存在安全风险'
                })
        except Exception as e:
            self.identified_issues.append({
                'type': '文件访问错误',
                'severity': '中',
                'file_path': os.path.relpath(self.server_js_file, self.root_dir),
                'description': f'无法读取server.js文件: {str(e)}'
            })

    def _check_readme_consistency(self) -> None:
        """检查README.md中的目录一致性"""
        readme_path = os.path.join(self.root_dir, 'README.md')
        if not os.path.exists(readme_path):
            self.identified_issues.append({
                'type': '文档缺失',
                'severity': '低',
                'file_path': 'README.md',
                'description': 'README.md文件不存在'
            })
            return
        
        # 这里可以添加更详细的目录一致性检查逻辑
        # 例如检查README中提到的文件是否实际存在

    def _generate_report(self) -> None:
        """生成合规性检查报告"""
        report_path = os.path.join(self.root_dir, '合规性检查报告.md')
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('# 国泰海通证券知识库 - 合规性检查报告\n\n')
            f.write('## 概述\n')
            f.write(f'本次检查共扫描了 {len(self.sensitive_files)} 个敏感文件，发现了 {len(self.identified_issues)} 个潜在问题。\n\n')
            
            # 按严重程度分组
            high_severity = [issue for issue in self.identified_issues if issue['severity'] == '高']
            medium_severity = [issue for issue in self.identified_issues if issue['severity'] == '中']
            low_severity = [issue for issue in self.identified_issues if issue['severity'] == '低']
            
            # 输出高风险问题
            if high_severity:
                f.write('## 高风险问题\n')
                for issue in high_severity:
                    f.write(f'- **{issue["type"]}**: {issue["file_path"]}\n')
                    f.write(f'  - 描述: {issue["description"]}\n')
                    if 'details' in issue:
                        f.write(f'  - 详情: {issue["details"]}\n')
            
            # 输出中风险问题
            if medium_severity:
                f.write('\n## 中风险问题\n')
                for issue in medium_severity:
                    f.write(f'- **{issue["type"]}**: {issue["file_path"]}\n')
                    f.write(f'  - 描述: {issue["description"]}\n')
            
            # 输出低风险问题
            if low_severity:
                f.write('\n## 低风险问题\n')
                for issue in low_severity:
                    f.write(f'- **{issue["type"]}**: {issue["file_path"]}\n')
                    f.write(f'  - 描述: {issue["description"]}\n')
            
            # 输出整改建议
            f.write('\n## 整改建议\n')
            f.write('1. **立即移除违规投资咨询内容**：删除所有具体股票推荐、买卖点位、仓位指导等内容\n')
            f.write('2. **核查机构名称授权**：确认"国泰海通证券"相关内容的使用合法性\n')
            f.write('3. **清理个人敏感信息**：删除或匿名化涉及真实个人的隐私内容\n')
            f.write('4. **修复安全配置**：将server.js中的Access-Control-Allow-Origin限制为指定域名\n')
            f.write('5. **规范文档与分支管理**：同步目录结构描述，定期执行分支清理\n')
            
        print(f"合规性检查报告已生成: {report_path}")
        print(f"发现 {len(high_severity)} 个高风险问题，{len(medium_severity)} 个中风险问题，{len(low_severity)} 个低风险问题")

if __name__ == '__main__':
    # 获取知识库根目录
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 创建合规检查器并运行
    checker = ComplianceChecker(root_dir)
    checker.scan_files()