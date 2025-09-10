import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # 尝试直接从本地导入模块
    from ai_services import __version__
    print(f"直接从本地导入成功! 版本: {__version__}")
except ImportError:
    print("直接从本地导入失败")
    
    # 打印Python路径，查看问题所在
    print("Python路径:")
    for path in sys.path:
        print(f"  {path}")