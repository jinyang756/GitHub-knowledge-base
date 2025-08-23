import os
import sys
# 将docs/技术目录添加到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), "docs", "技术"))
# 导入KnowledgeBaseTools类
from knowledge_base_utils import KnowledgeBaseTools

"""
自动更新docsify知识库的alias配置脚本

使用方法:
    python update_alias_config.py [目录路径]

示例:
    python update_alias_config.py 技术/热门指标公式集
    python update_alias_config.py 行业
    python update_alias_config.py 政策

如果不提供目录路径，将默认更新'技术/热门指标公式集'目录的alias配置
"""

def main():
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 获取用户提供的目录路径，如果没有提供则使用默认目录
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "技术/热门指标公式集"
    
    # 构建docs目录路径和目标物理路径
    docs_dir = os.path.join(script_dir, "docs")
    index_html_path = os.path.join(docs_dir, "index.html")
    
    # 构建物理路径（将URL路径转换为本地文件系统路径）
    physical_path = os.path.join(docs_dir, *target_dir.split("/"))
    
    # 检查目录是否存在
    if not os.path.exists(physical_path):
        print(f"错误: 目录 '{physical_path}' 不存在！")
        sys.exit(1)
    
    # 检查index.html文件是否存在
    if not os.path.exists(index_html_path):
        print(f"错误: index.html文件 '{index_html_path}' 不存在！")
        sys.exit(1)
    
    print(f"开始更新'{target_dir}'目录的alias配置...")
    print(f"物理路径: {physical_path}")
    print(f"index.html路径: {index_html_path}")
    
    # 初始化工具类并更新alias配置
    kb_tools = KnowledgeBaseTools()
    update_result = kb_tools.updateIndexHtmlAlias(index_html_path, target_dir, physical_path=physical_path)
    
    if update_result:
        print(f"\n🎉 成功！'{target_dir}'目录的alias配置已更新到index.html文件中。")
        print("提示: 更新完成后，建议重启docsify服务器以确保配置生效。")
    else:
        print("\n❌ 失败！无法更新alias配置，请查看错误信息。")

if __name__ == "__main__":
    print("======= docsify alias配置自动更新工具 =======")
    main()
    print("=========================================")