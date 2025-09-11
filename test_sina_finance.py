#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import time
from fetch_sina_finance import SinaFinanceFetcher
from datetime import datetime

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_sina_finance.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def test_sina_finance_connection():
    """测试新浪财经数据连接是否正常"""
    logger.info("开始测试新浪财经数据连接...")
    
    # 创建数据目录
    os.makedirs("test_results", exist_ok=True)
    
    # 初始化fetcher
    fetcher = SinaFinanceFetcher()
    
    # 测试不同类型的数据请求
    test_cases = [
        ("上证指数", "sh000001", "index"),
        ("深证成指", "sz399001", "index"),
        ("创业板指", "sz399006", "index"),
        ("浦发银行", "600000", "stock"),
        ("贵州茅台", "600519", "stock"),
        ("宁德时代", "300750", "stock")
    ]
    
    # 记录测试结果
    test_results = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "success_count": 0,
        "fail_count": 0,
        "details": []
    }
    
    for name, code, type in test_cases:
        logger.info(f"测试获取 {name} ({code}) 数据...")
        
        try:
            start_time = time.time()
            
            if type == "index":
                data = fetcher.fetch_index_data(code)
            else:
                data = fetcher.fetch_stock_data(code)
                # 尝试解析股票数据
                if data:
                    parsed_data = fetcher.parse_stock_data(data)
                    if parsed_data:
                        logger.info(f"成功解析 {name} 数据: 当前价={parsed_data['current']}, 涨跌幅={parsed_data['change_percent']:.2f}%")
            
            end_time = time.time()
            
            if data:
                status = "成功"
                test_results["success_count"] += 1
                # 保存数据样本
                sample_filename = f"test_results/{code}_{type}_sample.txt"
                with open(sample_filename, 'w', encoding='utf-8') as f:
                    f.write(f"# {name} ({code})\n")
                    f.write(f"# 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"# 响应时间: {(end_time - start_time)*1000:.2f} ms\n")
                    f.write(f"# 数据长度: {len(data)} 字节\n")
                    f.write(f"\n{data[:1000]}..." if len(data) > 1000 else data)
            else:
                status = "失败"
                test_results["fail_count"] += 1
            
            test_results["details"].append({
                "name": name,
                "code": code,
                "type": type,
                "status": status,
                "response_time_ms": (end_time - start_time)*1000
            })
            
            logger.info(f"测试 {name} 结果: {status}, 响应时间: {(end_time - start_time)*1000:.2f} ms")
        except Exception as e:
            test_results["fail_count"] += 1
            test_results["details"].append({
                "name": name,
                "code": code,
                "type": type,
                "status": "异常",
                "error": str(e)
            })
            logger.error(f"测试 {name} 异常: {str(e)}")
        
        # 添加延迟，避免请求过于频繁
        time.sleep(2)
    
    # 测试市场概览
    try:
        logger.info("测试获取市场概览数据...")
        start_time = time.time()
        market_overview = fetcher.fetch_market_overview()
        end_time = time.time()
        
        if market_overview:
            test_results["details"].append({
                "name": "市场概览",
                "type": "overview",
                "status": "成功",
                "response_time_ms": (end_time - start_time)*1000
            })
            test_results["success_count"] += 1
            logger.info(f"成功获取市场概览数据，响应时间: {(end_time - start_time)*1000:.2f} ms")
            
            # 保存市场概览
            import json
            overview_filename = f"test_results/market_overview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(overview_filename, 'w', encoding='utf-8') as f:
                json.dump(market_overview, f, ensure_ascii=False, indent=2)
        else:
            test_results["details"].append({
                "name": "市场概览",
                "type": "overview",
                "status": "失败"
            })
            test_results["fail_count"] += 1
            logger.error("获取市场概览数据失败")
    except Exception as e:
        test_results["details"].append({
            "name": "市场概览",
            "type": "overview",
            "status": "异常",
            "error": str(e)
        })
        test_results["fail_count"] += 1
        logger.error(f"测试市场概览异常: {str(e)}")
    
    # 保存测试报告
    report_filename = f"test_results/test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    import json
    with open(report_filename, 'w', encoding='utf-8') as f:
        json.dump(test_results, f, ensure_ascii=False, indent=2)
    
    # 输出测试摘要
    logger.info(f"\n测试摘要:")
    logger.info(f"总测试用例: {test_results['success_count'] + test_results['fail_count']}")
    logger.info(f"成功: {test_results['success_count']}")
    logger.info(f"失败: {test_results['fail_count']}")
    logger.info(f"测试报告已保存到: {report_filename}")
    
    # 生成HTML测试报告（简单版）
    html_report = generate_html_report(test_results)
    html_filename = f"test_results/test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    logger.info(f"HTML测试报告已保存到: {html_filename}")
    
    # 如果有失败的测试用例，返回非零退出码
    return 0 if test_results['fail_count'] == 0 else 1

def generate_html_report(test_results):
    """生成简单的HTML测试报告"""
    html = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>新浪财经数据请求测试报告</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            .summary { margin: 20px 0; padding: 15px; background-color: #f5f5f5; border-radius: 5px; }
            .success { color: green; }
            .fail { color: red; }
            .details { margin-top: 20px; }
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
        </style>
    </head>
    <body>
        <h1>新浪财经数据请求测试报告</h1>
        <div class="summary">
            <p>测试时间: {timestamp}</p>
            <p>总测试用例: {total}</p>
            <p class="success">成功: {success}</p>
            <p class="fail">失败: {fail}</p>
        </div>
        <div class="details">
            <h2>测试详情</h2>
            <table>
                <tr>
                    <th>名称</th>
                    <th>代码</th>
                    <th>类型</th>
                    <th>状态</th>
                    <th>响应时间(ms)</th>
                    <th>错误信息</th>
                </tr>
    """
    
    # 格式化测试摘要
    html = html.format(
        timestamp=test_results['timestamp'],
        total=test_results['success_count'] + test_results['fail_count'],
        success=test_results['success_count'],
        fail=test_results['fail_count']
    )
    
    # 添加测试详情
    for detail in test_results['details']:
        status_class = "success" if detail['status'] == "成功" else "fail"
        response_time = f"{detail.get('response_time_ms', ''):.2f}" if detail.get('response_time_ms') else "-"
        error = detail.get('error', '')
        
        html += f"""
                <tr>
                    <td>{detail['name']}</td>
                    <td>{detail.get('code', '-')}</td>
                    <td>{detail['type']}</td>
                    <td class="{status_class}">{detail['status']}</td>
                    <td>{response_time}</td>
                    <td>{error}</td>
                </tr>
        """
    
    # 结束HTML
    html += """
            </table>
        </div>
    </body>
    </html>
    """
    
    return html

def main():
    """主函数"""
    logger.info("新浪财经数据请求测试工具")
    logger.info("此工具用于测试添加完整请求头后是否能够成功获取新浪财经数据")
    
    # 检查是否安装了requests库
    try:
        import requests
    except ImportError:
        logger.error("未找到requests库，请先安装: pip install requests")
        sys.exit(1)
    
    # 运行测试
    exit_code = test_sina_finance_connection()
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()