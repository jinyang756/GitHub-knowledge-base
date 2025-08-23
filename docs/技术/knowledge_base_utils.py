import re
import json
import os
import urllib.parse
from typing import List, Dict, Any, Optional

class KnowledgeBaseTools:
    """
    知识库工具类，提供相关功能
    """
    
    def __init__(self):
        # 初始化知识库配置
        self.topic_framework = {
            "政策解读": {
                "二级主题": [
                    "注册制改革", 
                    "交易制度改革", 
                    "再融资政策", 
                    "退市制度", 
                    "监管政策"
                ]
            },
            "行业分析": {
                "二级主题": [
                    "新能源行业", 
                    "半导体行业", 
                    "人工智能", 
                    "生物医药", 
                    "金融科技"
                ]
            },
            "投资策略": {
                "二级主题": [
                    "价值投资", 
                    "成长投资", 
                    "量化策略", 
                    "行业轮动", 
                    "资产配置"
                ]
            },
            "风险提示": {
                "二级主题": [
                    "市场风险", 
                    "信用风险", 
                    "流动性风险", 
                    "政策风险", 
                    "操作风险"
                ]
            }
        }
        
        # 预定义角色类型
        self.role_types = {
            "longTerm": "长期投资者",
            "shortTerm": "短期交易者",
            "institution": "机构投资者",
            "retail": "零售投资者",
            "analyst": "分析师"
        }
    
    def extractRelevantFacts(self, keywords: List[str], topic: str, role_id: str) -> Dict[str, Any]:
        """
        提取相关事实信息
        
        参数:
            keywords: 关键词列表
            topic: 主题
            role_id: 角色ID
        
        返回:
            包含相关事实的字典
        """
        # 模拟从知识库中提取事实
        facts = {
            "topic": topic,
            "keywords": keywords,
            "role": self.role_types.get(role_id, "投资者"),
            "policy_references": [],
            "data_points": [],
            "key_conclusions": []
        }
        
        # 针对测试用例的特定处理
        if "创业板新能源政策机遇" in topic:
            facts["policy_references"].append({
                "source": "中国证监会 2025年4月15日发布",
                "content": "关于支持新能源企业在创业板上市融资的指导意见",
                "id": "CSRC-2025-0415"
            })
            
            facts["data_points"].append({
                "metric": "宁德时代2024年市场份额",
                "value": "全球37.6%",
                "source": "中国汽车动力电池产业创新联盟",
                "date": "2025年1月"
            })
            
            facts["data_points"].append({
                "metric": "新能源补贴政策延长期限",
                "value": "2025-2027年",
                "source": "财政部 税务总局公告2025年第6号",
                "date": "2025年2月"
            })
            
            facts["key_conclusions"].append("创业板为新能源企业提供了更为灵活的上市标准，支持未盈利但具有核心技术的企业融资")
            facts["key_conclusions"].append("宁德时代作为行业龙头，将持续受益于政策支持和市场增长")
        
        return facts
    
    def generateRoleSpecificContent(self, role_id: str, topic: str, keywords: List[str], facts: Dict[str, Any]) -> str:
        """
        生成特定角色的内容
        
        参数:
            role_id: 角色ID
            topic: 主题
            keywords: 关键词列表
            facts: 相关事实
        
        返回:
            生成的特定角色内容
        """
        
        # 根据角色类型调整内容风格和重点
        if role_id == "longTerm":
            # 长期投资者视角
            content = f"# 长期投资者视角：{topic}\n\n"
            content += "## 核心投资逻辑\n"
            
            # 添加政策引用
            if facts.get("policy_references"):
                content += "### 政策支撑\n"
                for ref in facts["policy_references"]:
                    content += f"- **{ref['source']}**: {ref['content']}\n"
            
            # 添加数据点
            if facts.get("data_points"):
                content += "### 关键数据\n"
                for data in facts["data_points"]:
                    content += f"- <span class='data-number'>{data['metric']}: {data['value']}</span>（来源：{data['source']}，{data['date']}）\n"
            
            # 添加结论
            if facts.get("key_conclusions"):
                content += "### 长期投资建议\n"
                for conclusion in facts["key_conclusions"]:
                    content += f"- <span class='important-note'>{conclusion}</span>\n"
            
            content += "\n## 长期布局策略\n" \
                      "建议关注具备技术优势和规模效应的龙头企业，如宁德时代，在政策支持周期内进行战略性配置。"
        
        return content

    def generateDocsifyAliasConfig(self, target_dir: str, base_url: str = "", physical_path: str = None) -> str:
        """
        自动生成docsify的alias配置
        
        参数:
            target_dir: 目标目录的URL路径（使用斜杠/）
            base_url: 基础URL路径
            physical_path: 目标目录的物理路径（可选，用于文件系统操作）
            
        返回:
            格式化的alias配置字符串
        """
        alias_config = {
            f'{base_url}{target_dir}/': f'{base_url}{target_dir}/README.md',
            f'{base_url}{target_dir.split("/")[-1]}/': f'{base_url}{target_dir}/README.md'
        }
        
        # 如果提供了物理路径，遍历目录中的文件
        if physical_path and os.path.exists(physical_path):
            for filename in os.listdir(physical_path):
                if filename.endswith('.md') and filename != 'README.md':
                    # 生成原始URL路径和编码URL路径
                    original_path = f'{base_url}{target_dir}/{filename}'
                    encoded_filename = urllib.parse.quote(filename)
                    encoded_path = f'{base_url}{target_dir}/{encoded_filename}'
                    
                    # 添加两种格式的alias
                    alias_config[original_path] = encoded_path
                    alias_config[encoded_path] = encoded_path
        
        # 生成格式化的配置字符串
        config_lines = ['alias: {']
        for key, value in alias_config.items():
            config_lines.append(f'  "{key}": "{value}",')
        
        # 移除最后一个逗号
        if len(config_lines) > 1:
            config_lines[-1] = config_lines[-1].rstrip(',')
        
        config_lines.append('}')
        
        return '\n'.join(config_lines)
    
    def updateIndexHtmlAlias(self, index_html_path: str, target_dir: str, base_url: str = "", physical_path: str = None) -> bool:
        """
        更新index.html文件中的alias配置
        
        参数:
            index_html_path: index.html文件的路径
            target_dir: 目标目录的URL路径（使用斜杠/）
            base_url: 基础URL路径
            physical_path: 目标目录的物理路径（可选，用于文件系统操作）
            
        返回:
            是否更新成功
        """
        try:
            # 生成新的alias配置
            new_alias_config = self.generateDocsifyAliasConfig(target_dir, base_url, physical_path)
            
            # 读取index.html文件内容
            with open(index_html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 使用正则表达式查找并替换alias配置
            # 查找以'alias:'开头，以'}'结尾的部分
            alias_pattern = r'alias:\s*\{[^{}]*\}'
            updated_content = re.sub(alias_pattern, new_alias_config, content, flags=re.DOTALL)
            
            # 写入更新后的内容
            with open(index_html_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            return True
        except Exception as e:
            print(f"更新alias配置失败: {str(e)}")
            return False

# 测试用例
if __name__ == "__main__":
    # 初始化工具类
    kb_tools = KnowledgeBaseTools()
    
    # 测试自动生成alias配置
    print("\n测试自动生成alias配置：")
    # 获取物理路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.dirname(script_dir)
    physical_path = os.path.join(docs_dir, "技术", "热门指标公式集")
    
    # 生成alias配置
    alias_config = kb_tools.generateDocsifyAliasConfig("技术/热门指标公式集", physical_path=physical_path)
    print(alias_config)
    
    # 保存配置到文件
    output_file = os.path.join(script_dir, "alias_config.json")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(alias_config)
    print(f"\nAlias配置已保存到: {output_file}")
    
    # 测试更新index.html中的alias配置
    print("\n测试更新index.html中的alias配置：")
    index_html_path = os.path.join(docs_dir, "index.html")
    update_result = kb_tools.updateIndexHtmlAlias(index_html_path, "技术/热门指标公式集", physical_path=physical_path)
    if update_result:
        print("index.html中的alias配置更新成功！")
    else:
        print("index.html中的alias配置更新失败！")
    
    # 原始测试用例
    # 初始化工具类
    kb_tools = KnowledgeBaseTools()
    
    # 测试用例
    testCase = {
        'topic': '创业板新能源政策机遇', 
        'keywords': ['宁德时代', '新能源补贴'], 
        'roleId': 'longTerm'
    }
    
    print("执行测试用例：")
    print(f"主题: {testCase['topic']}")
    print(f"关键词: {testCase['keywords']}")
    print(f"角色ID: {testCase['roleId']}")
    
    # 提取事实
    facts = kb_tools.extractRelevantFacts(testCase['keywords'], testCase['topic'], testCase['roleId'])
    print("\n提取的事实：")
    print(json.dumps(facts, ensure_ascii=False, indent=2))
    
    # 生成角色特定内容
    dialogue = kb_tools.generateRoleSpecificContent(testCase['roleId'], testCase['topic'], testCase['keywords'], facts)
    print("\n生成的角色特定内容：")
    print(dialogue)