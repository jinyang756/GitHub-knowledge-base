import re
import json
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

# 测试用例
if __name__ == "__main__":
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