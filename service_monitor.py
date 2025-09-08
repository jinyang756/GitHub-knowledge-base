#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import subprocess
import datetime
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("service_monitor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ServiceMonitor:
    def __init__(self):
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.market_service_bat = os.path.join(self.root_dir, "自动更新金融市场分析.bat")
        self.trading_service_bat = os.path.join(self.root_dir, "start_trading_analysis.bat")
        
    def is_service_running(self, service_name):
        """检查服务是否在运行"""
        try:
            # 使用tasklist命令检查Python进程
            result = subprocess.check_output(
                ['tasklist', '/FI', 'IMAGENAME eq python.exe', '/V'],
                universal_newlines=True
            )
            
            # 检查进程列表中是否包含特定的服务名称
            return service_name in result
        except Exception as e:
            logger.error(f"检查服务运行状态失败: {str(e)}")
            return False
            
    def start_service(self, bat_file):
        """启动服务"""
        try:
            logger.info(f"正在启动服务: {bat_file}")
            # 使用START命令在新窗口中启动批处理文件
            subprocess.Popen(
                ['cmd.exe', '/c', 'start', '', bat_file],
                cwd=os.path.dirname(bat_file)
            )
            logger.info(f"服务启动成功")
            return True
        except Exception as e:
            logger.error(f"服务启动失败: {str(e)}")
            return False
            
    def run_monitor(self):
        """运行监控"""
        logger.info("服务监控程序已启动")
        
        while True:
            # 检查是否为交易日
            today = datetime.date.today()
            is_trading_day = today.weekday() < 5  # 周一至周五
            
            # 检查并启动金融市场分析服务
            if not self.is_service_running("automatic_market_update.py"):
                logger.warning("金融市场分析服务未运行，正在重启...")
                self.start_service(self.market_service_bat)
            
            # 检查并启动实盘解析服务（仅在交易日）
            if is_trading_day and not self.is_service_running("automatic_trading_analysis.py"):
                logger.warning("实盘解析服务未运行，正在重启...")
                self.start_service(self.trading_service_bat)
            
            # 每30分钟检查一次
            time.sleep(1800)

def main():
    monitor = ServiceMonitor()
    monitor.run_monitor()

if __name__ == "__main__":
    main()