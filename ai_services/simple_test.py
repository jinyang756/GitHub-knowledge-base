# 这是一个简单的测试脚本，尝试直接导入核心组件

print("尝试导入 TextProcessor 类...")
try:
    from nlp.text_processor import TextProcessor
    print("成功导入 TextProcessor 类!")
    
    # 测试基本功能
    processor = TextProcessor()
    text = "这是一段测试文本。"
    clean_text = processor.clean_text(text)
    print(f"清理后的文本: {clean_text}")
except Exception as e:
    print(f"导入失败: {e}")
    import traceback
    traceback.print_exc()