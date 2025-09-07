#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import time
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def test_trading_analysis():
    """测试实盘解析自动化脚本的功能"""
    try:
        # 项目根目录
        root_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 检查实盘解析自动化脚本是否存在
        trading_analysis_script = os.path.join(root_dir, "automatic_trading_analysis.py")
        if not os.path.exists(trading_analysis_script):
            logger.error("实盘解析自动化脚本不存在: %s", trading_analysis_script)
            return False
        
        logger.info("开始测试实盘解析自动化脚本...")
        
        # 生成测试日期（使用今天或下一个交易日）
        today = datetime.date.today()
        test_date = today.strftime("%Y-%m-%d")
        
        # 执行测试命令
        logger.info(f"使用测试日期: {test_date}")
        
        # 调用实盘解析自动化脚本的测试模式
        command = f"python {trading_analysis_script} test {test_date}"
        logger.info(f"执行命令: {command}")
        
        # 执行命令
        exit_code = os.system(command)
        
        if exit_code != 0:
            logger.error("实盘解析自动化脚本测试失败，退出代码: %d", exit_code)
            return False
        
        # 检查是否生成了测试报告
        report_dir = os.path.join(root_dir, "docs", "policy", "实盘")
        report_filename = f"{today.strftime('%Y年%m月%d日')}实盘解析.md"
        report_path = os.path.join(report_dir, report_filename)
        
        if not os.path.exists(report_path):
            logger.error("测试报告未生成: %s", report_path)
            return False
        
        logger.info(f"测试报告已生成: {report_path}")
        
        # 读取并检查报告内容
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查报告基本结构
        required_sections = [
            "# " + today.strftime("%Y年%m月%d日") + "实盘解析",
            "发布时间",
        ]
        
        for section in required_sections:
            if section not in content:
                logger.error(f"报告中缺少必要部分: {section}")
                return False
        
        logger.info("实盘解析自动化脚本测试通过！")
        return True
    
    except Exception as e:
        logger.error(f"测试过程中发生错误: {str(e)}")
        return False

def main():
    """主函数"""
    success = test_trading_analysis()
    
    if success:
        print("\n测试总结：")
        print("1. 实盘解析自动化脚本已成功创建")
        print("2. 测试报告已成功生成")
        print("3. 启动批处理文件已创建，可通过双击start_trading_analysis.bat启动服务")
        print("\n使用说明：")
        print("- 在交易日，系统会自动在9:00生成开盘问候")
        print("- 在9:30开始实盘解析")
        print("- 每隔半小时自动生成一句总结")
        print("- 在15:00生成收盘总结")
        print("- 所有内容将保存在当天的实盘解析报告中")
        sys.exit(0)
    else:
        print("\n测试失败，请检查日志输出以获取详细信息。")
        sys.exit(1)

if __name__ == "__main__":
    main()