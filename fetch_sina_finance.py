#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import requests
from datetime import datetime

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("sina_finance_fetch.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SinaFinanceFetcher:
    def __init__(self):
        # 设置请求头信息，模拟浏览器行为以避免被反爬
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://finance.sina.com.cn/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        # 设置代理（如果需要）
        self.proxies = None  # 可以配置代理，如 {"http": "http://proxy.example.com", "https": "https://proxy.example.com"}
    
    def fetch_stock_data(self, stock_code):
        """获取股票实时数据"""
        try:
            # 根据股票代码构建URL
            if stock_code.startswith('6'):
                # 沪市股票
                url = f"https://hq.sinajs.cn/list=sh{stock_code}"
            else:
                # 深市股票
                url = f"https://hq.sinajs.cn/list=sz{stock_code}"
            
            logger.info(f"正在获取股票 {stock_code} 数据，URL: {url}")
            
            # 添加完整请求头进行请求
            response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=10)
            
            # 检查响应状态
            if response.status_code == 200:
                logger.info(f"成功获取股票 {stock_code} 数据")
                return response.text
            else:
                logger.error(f"请求失败，状态码：{response.status_code}")
                logger.error(f"响应内容：{response.text}")
                return None
        except Exception as e:
            logger.error(f"获取股票数据异常: {str(e)}")
            return None
    
    def fetch_index_data(self, index_code):
        """获取指数实时数据"""
        try:
            # 构建指数数据URL
            url = f"https://hq.sinajs.cn/list={index_code}"
            
            logger.info(f"正在获取指数 {index_code} 数据，URL: {url}")
            
            # 添加完整请求头进行请求
            response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=10)
            
            # 检查响应状态
            if response.status_code == 200:
                logger.info(f"成功获取指数 {index_code} 数据")
                return response.text
            else:
                logger.error(f"请求失败，状态码：{response.status_code}")
                logger.error(f"响应内容：{response.text}")
                return None
        except Exception as e:
            logger.error(f"获取指数数据异常: {str(e)}")
            return None
    
    def fetch_market_overview(self):
        """获取市场概览数据"""
        try:
            # 获取主要指数数据
            indices = ['sh000001', 'sz399001', 'sz399006']  # 上证指数、深证成指、创业板指
            index_data = {}
            
            for index_code in indices:
                data = self.fetch_index_data(index_code)
                if data:
                    index_data[index_code] = data
            
            # 获取热门板块数据
            hot_sectors = self.fetch_hot_sectors()
            
            # 构建市场概览结果
            market_overview = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'indices': index_data,
                'hot_sectors': hot_sectors
            }
            
            return market_overview
        except Exception as e:
            logger.error(f"获取市场概览异常: {str(e)}")
            return None
    
    def fetch_hot_sectors(self):
        """获取热门板块数据"""
        try:
            url = "https://vip.stock.finance.sina.com.cn/mkt/#hs_a"
            
            logger.info(f"正在获取热门板块数据，URL: {url}")
            
            # 添加完整请求头进行请求
            response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=10)
            
            # 检查响应状态
            if response.status_code == 200:
                logger.info(f"成功获取热门板块数据")
                # 这里返回原始HTML，实际应用中需要解析HTML提取结构化数据
                return response.text
            else:
                logger.error(f"请求失败，状态码：{response.status_code}")
                logger.error(f"响应内容：{response.text}")
                return None
        except Exception as e:
            logger.error(f"获取热门板块数据异常: {str(e)}")
            return None
    
    def parse_stock_data(self, raw_data):
        """解析股票数据"""
        try:
            if not raw_data:
                return None
            
            # 新浪股票数据格式：var hq_str_sh600000="浦发银行,10.18,10.19,10.14,10.24,10.13,10.14,10.15,11155521,113223565.00,1112600,10.14,1337100,10.13,924800,10.12,1595400,10.11,1560200,10.10,1602400,10.15,1576900,10.16,1306800,10.17,1102100,10.18,1376900,10.19,2024-01-04,15:00:00,00";"
            
            # 提取数据部分
            data_str = raw_data.split('"')[1]
            data_list = data_str.split(',')
            
            # 解析数据
            stock_info = {
                'name': data_list[0],
                'open': float(data_list[1]) if data_list[1] else 0.0,
                'prev_close': float(data_list[2]) if data_list[2] else 0.0,
                'current': float(data_list[3]) if data_list[3] else 0.0,
                'high': float(data_list[4]) if data_list[4] else 0.0,
                'low': float(data_list[5]) if data_list[5] else 0.0,
                'buy1': float(data_list[6]) if data_list[6] else 0.0,
                'sell1': float(data_list[7]) if data_list[7] else 0.0,
                'volume': int(data_list[8]) if data_list[8] else 0,
                'amount': float(data_list[9]) if data_list[9] else 0.0,
                'date': data_list[30] if len(data_list) > 30 else '',
                'time': data_list[31] if len(data_list) > 31 else ''
            }
            
            # 计算涨跌幅
            if stock_info['prev_close'] > 0:
                stock_info['change'] = stock_info['current'] - stock_info['prev_close']
                stock_info['change_percent'] = (stock_info['change'] / stock_info['prev_close']) * 100
            else:
                stock_info['change'] = 0.0
                stock_info['change_percent'] = 0.0
            
            return stock_info
        except Exception as e:
            logger.error(f"解析股票数据异常: {str(e)}")
            return None
    
    def save_to_file(self, data, filename):
        """保存数据到文件"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # 写入文件
            with open(filename, 'w', encoding='utf-8') as f:
                if isinstance(data, dict):
                    import json
                    json.dump(data, f, ensure_ascii=False, indent=2)
                else:
                    f.write(str(data))
            
            logger.info(f"数据已保存到文件: {filename}")
            return True
        except Exception as e:
            logger.error(f"保存文件异常: {str(e)}")
            return False

def main():
    """主函数"""
    fetcher = SinaFinanceFetcher()
    
    # 示例：获取上证指数数据
    index_data = fetcher.fetch_index_data('sh000001')
    if index_data:
        print(f"上证指数数据: {index_data}")
        
    # 示例：获取股票数据
    stock_data = fetcher.fetch_stock_data('600000')  # 浦发银行
    if stock_data:
        parsed_data = fetcher.parse_stock_data(stock_data)
        if parsed_data:
            print(f"解析后的股票数据: {parsed_data}")
            
            # 保存数据到文件
            today_str = datetime.now().strftime('%Y%m%d')
            filename = f"data/sina_finance/stock_600000_{today_str}.json"
            fetcher.save_to_file(parsed_data, filename)
    
    # 示例：获取市场概览
    market_overview = fetcher.fetch_market_overview()
    if market_overview:
        print("获取市场概览成功")
        
        # 保存市场概览到文件
        today_str = datetime.now().strftime('%Y%m%d')
        filename = f"data/sina_finance/market_overview_{today_str}.json"
        fetcher.save_to_file(market_overview, filename)

if __name__ == "__main__":
    main()