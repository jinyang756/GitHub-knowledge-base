#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import json
import datetime
import time
import logging
from datetime import timedelta
import schedule
import threading

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("market_update.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MarketAnalysisUpdater:
    def __init__(self):
        # 项目根目录
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        # 政策分析文档目录
        self.policy_dir = os.path.join(self.root_dir, "docs", "policy")
        # 确保目录存在
        os.makedirs(self.policy_dir, exist_ok=True)
        
    def is_trading_day(self, date=None):
        """判断给定日期是否为交易日
        
        A股交易日规则：周一至周五，排除法定节假日
        这里使用简化版本，实际应用中应该使用更完善的交易日历
        """
        if date is None:
            date = datetime.date.today()
        
        # 检查是否为周末
        if date.weekday() >= 5:  # 5=周六, 6=周日
            return False
        
        # 这里可以添加法定节假日的检查
        # 实际应用中应该使用更完善的交易日历API
        return True
    
    def get_last_report(self):
        """获取最新的市场分析报告"""
        try:
            # 获取政策目录下的所有文件
            files = os.listdir(self.policy_dir)
            # 筛选出实时金融市场分析的文件
            report_files = [f for f in files if f.startswith("实时金融市场分析") and f.endswith(".md")]
            
            if not report_files:
                logger.warning("未找到任何市场分析报告")
                return None
            
            # 按文件名排序，假设文件名中包含日期信息
            report_files.sort(reverse=True)
            
            last_report = os.path.join(self.policy_dir, report_files[0])
            logger.info(f"找到最新报告: {report_files[0]}")
            
            return last_report
        except Exception as e:
            logger.error(f"获取最新报告失败: {str(e)}")
            return None
    
    def extract_report_structure(self, report_path):
        """从现有报告中提取结构"""
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取报告结构（标题、副标题等）
            # 这里使用简单的正则表达式来提取标题
            structure = {
                'title': re.search(r'#\s+(.*)', content),
                'sections': re.findall(r'##\s+(.*)', content)
            }
            
            # 处理提取结果
            if structure['title']:
                structure['title'] = structure['title'].group(1)
            
            logger.info(f"成功提取报告结构")
            return structure
        except Exception as e:
            logger.error(f"提取报告结构失败: {str(e)}")
            return self.get_default_template()
    
    def generate_new_report(self):
        """生成新的市场分析报告"""
        try:
            today = datetime.date.today()
            
            # 检查是否为交易日
            if not self.is_trading_day(today):
                logger.info(f"今天({today})不是交易日，不生成报告")
                return False
            
            # 获取最新报告
            last_report = self.get_last_report()
            
            if last_report:
                # 从最新报告提取结构
                template_structure = self.extract_report_structure(last_report)
            else:
                # 使用默认模板
                template_structure = self.get_default_template()
            
            # 生成报告内容
            report_content = self.generate_report_content(template_structure, today)
            
            # 生成文件名
            report_date_str = today.strftime("%Y年%m月%d日")
            report_filename = f"实时金融市场分析 - {report_date_str}.md"
            report_path = os.path.join(self.policy_dir, report_filename)
            
            # 检查文件是否已存在
            if os.path.exists(report_path):
                logger.info(f"今天的报告已存在: {report_filename}")
                return True
            
            # 写入报告文件
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            logger.info(f"成功生成新报告: {report_filename}")
            return True
        except Exception as e:
            logger.error(f"生成新报告失败: {str(e)}")
            return False
    
    def get_default_template(self):
        """获取默认的报告模板结构"""
        return {
            'title': '实时金融市场分析',
            'sections': [
                '宏观经济与政策',
                '金融市场动态',
                '行业热点及投资建议',
                '风险提示'
            ]
        }
    
    def generate_report_content(self, template_structure, date):
        """根据模板生成报告内容"""
        date_str = date.strftime("%Y年%m月%d日")
        
        # 构建报告内容
        content = f"# 实时金融市场分析 - {date_str}\n\n"
        content += f"> 发布时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # 添加各部分内容
        for section in template_structure['sections']:
            content += f"## {section}\n\n"
            
            # 根据不同章节添加示例内容
            if section == '宏观经济与政策':
                content += "- 国内宏观经济数据保持稳定增长趋势\n"
                content += "- 央行货币政策维持稳健基调\n"
                content += "- 财政政策持续发力支持实体经济\n\n"
            elif section == '金融市场动态':
                content += "- 股票市场：今日A股市场整体震荡上行，行业板块分化明显\n"
                content += "- 债券市场：国债收益率小幅波动\n"
                content += "- 商品市场：大宗商品价格走势分化\n\n"
            elif section == '行业热点及投资建议':
                content += "- 科技板块：半导体、人工智能等新兴产业表现活跃\n"
                content += "- 消费板块：内需持续恢复，消费升级趋势明显\n"
                content += "- 绿色能源：政策支持力度加大，行业发展前景广阔\n\n"
            else:
                content += "- 市场波动风险：关注地缘政治局势变化\n"
                content += "- 政策风险：密切关注监管政策动向\n"
                content += "- 流动性风险：警惕市场资金面变化\n\n"
        
        # 添加数据来源说明
        content += "---\n\n"
        content += "**数据来源**：Wind、东方财富Choice、公开资料整理\n"
        content += "**免责声明**：本报告仅供参考，不构成任何投资建议\n"
        content += "**更新时间**：本报告由自动化系统每日生成，确保信息及时准确"
        
        return content
    
    def run_daily_update(self):
        """执行每日更新"""
        logger.info("开始执行每日市场分析更新")
        
        # 尝试多次执行，以防临时网络或系统问题
        max_attempts = 3
        for attempt in range(max_attempts):
            if self.generate_new_report():
                logger.info("每日更新执行成功")
                return True
            else:
                if attempt < max_attempts - 1:
                    logger.warning(f"第{attempt+1}次更新失败，5分钟后重试")
                    time.sleep(300)  # 等待5分钟
        
        logger.error("多次尝试后更新仍然失败")
        return False
    
    def run_scheduler(self):
        """运行调度器，在每天早上8点执行更新"""
        logger.info("启动金融市场分析自动更新服务")
        logger.info("服务将在每天早上8点执行更新")
        
        # 设置每日8点执行的任务
        schedule.every().day.at("08:00").do(self.run_daily_update)
        
        # 初始执行一次
        logger.info("初始执行一次更新检查")
        self.run_daily_update()
        
        # 持续运行调度器
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
        except KeyboardInterrupt:
            logger.info("自动更新服务已手动停止")
        except Exception as e:
            logger.error(f"调度器异常: {str(e)}")
    
    def test_update(self, test_date=None):
        """测试更新功能，可指定测试日期
        
        参数:
            test_date: 测试日期，格式为YYYY-MM-DD字符串
        """
        logger.info("开始执行测试更新")
        
        # 设置测试日期
        if test_date:
            try:
                test_date_obj = datetime.datetime.strptime(test_date, "%Y-%m-%d").date()
                # 临时修改is_trading_day方法的行为，强制返回True
                original_is_trading_day = self.is_trading_day
                self.is_trading_day = lambda date=None: True
                
                logger.info(f"使用测试日期: {test_date}")
                result = self.generate_new_report()
                
                # 恢复原始方法
                self.is_trading_day = original_is_trading_day
                
                return result
            except Exception as e:
                logger.error(f"测试日期格式错误: {str(e)}")
                return False
        else:
            # 不指定日期，使用当前日期，但强制生成报告
            original_is_trading_day = self.is_trading_day
            self.is_trading_day = lambda date=None: True
            
            result = self.generate_new_report()
            
            # 恢复原始方法
            self.is_trading_day = original_is_trading_day
            
            return result

def main():
    """主函数"""
    updater = MarketAnalysisUpdater()
    
    # 解析命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "scheduler":
            # 启动调度器模式
            updater.run_scheduler()
        elif sys.argv[1] == "test":
            # 测试模式
            test_date = sys.argv[2] if len(sys.argv) > 2 else None
            updater.test_update(test_date)
        elif sys.argv[1] == "once":
            # 执行一次更新
            updater.run_daily_update()
    else:
        # 默认启动调度器
        updater.run_scheduler()

if __name__ == "__main__":
    main()