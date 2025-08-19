#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆包AI云盘同步脚本

该脚本用于将豆包AI云盘的内容同步到GitHub知识库的国泰海通证券目录。
当云盘内容更新时，运行此脚本可以自动更新本地目录内容，并可选地提交到Git仓库。

使用说明:
1. 安装必要的依赖: pip install requests
2. 配置脚本中的云盘API信息和本地路径
3. 运行脚本: python sync_doubao_cloud.py

可以将脚本设置为定时任务，实现定期自动同步。
"""

import os
import shutil
import requests
import json
import time
from datetime import datetime
import subprocess

# 配置参数
class Config:
    # 豆包AI云盘API配置
    # 注意：这里需要替换为实际的API URL和认证信息
    DOUBAO_API_URL = "https://api.doubao.com/cloud-drive"
    API_KEY = "YOUR_API_KEY_HERE"
    SECRET_KEY = "YOUR_SECRET_KEY_HERE"
    CLOUD_DIR_ID = "YOUR_CLOUD_DIRECTORY_ID"
    
    # 本地路径配置
    LOCAL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "国泰海通证券")
    
    # 日志文件
    LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sync_log.txt")
    
    # Git配置
    ENABLE_GIT_COMMIT = True  # 是否自动提交到Git
    GIT_REPO_PATH = os.path.dirname(os.path.abspath(__file__))

# 日志函数
def log(message):
    """记录日志信息"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}\n"
    
    print(log_message)
    with open(Config.LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_message)

# 获取豆包AI云盘内容
def get_cloud_files():
    """从豆包AI云盘获取文件列表"""
    try:
        headers = {
            "Authorization": f"Bearer {Config.API_KEY}",
            "Content-Type": "application/json"
        }
        
        params = {
            "dir_id": Config.CLOUD_DIR_ID,
            "recursive": True
        }
        
        response = requests.get(f"{Config.DOUBAO_API_URL}/files", headers=headers, params=params)
        response.raise_for_status()
        
        return response.json()
    except Exception as e:
        log(f"获取云盘文件失败: {str(e)}")
        return None

# 下载云盘文件到本地
def download_file(file_info):
    """下载单个文件到本地"""
    try:
        file_path = file_info["path"]
        file_name = os.path.basename(file_path)
        local_file_path = os.path.join(Config.LOCAL_DIR, file_name)
        
        # 确保本地目录存在
        os.makedirs(Config.LOCAL_DIR, exist_ok=True)
        
        # 检查文件是否需要更新
        # 这里简化处理，实际应用中可以比较文件大小、修改时间等
        
        # 下载文件
        headers = {
            "Authorization": f"Bearer {Config.API_KEY}"
        }
        
        response = requests.get(f"{Config.DOUBAO_API_URL}/download", 
                               headers=headers, 
                               params={"file_id": file_info["id"]}, 
                               stream=True)
        response.raise_for_status()
        
        with open(local_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        log(f"已下载文件: {file_name}")
        return True
    except Exception as e:
        log(f"下载文件失败: {str(e)}")
        return False

# 同步云盘内容到本地
def sync_cloud_to_local():
    """同步云盘内容到本地目录"""
    log("开始同步豆包AI云盘内容...")
    
    # 获取云盘文件列表
    cloud_files = get_cloud_files()
    if not cloud_files:
        log("同步失败: 无法获取云盘文件列表")
        return False
    
    # 下载所有文件
    success_count = 0
    fail_count = 0
    
    for file_info in cloud_files.get("files", []):
        if file_info["type"] == "file":  # 只下载文件，跳过目录
            if download_file(file_info):
                success_count += 1
            else:
                fail_count += 1
    
    log(f"同步完成: 成功 {success_count} 个文件, 失败 {fail_count} 个文件")
    return success_count > 0

# 提交更改到Git仓库
def commit_to_git():
    """将更改提交到Git仓库"""
    if not Config.ENABLE_GIT_COMMIT:
        log("Git自动提交已禁用")
        return True
    
    try:
        # 执行Git命令
        subprocess.run(["git", "add", Config.LOCAL_DIR], 
                      cwd=Config.GIT_REPO_PATH, 
                      check=True, 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
        
        # 检查是否有更改
        status_output = subprocess.run(["git", "status", "--porcelain"], 
                                      cwd=Config.GIT_REPO_PATH, 
                                      check=True, 
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE)
        
        if status_output.stdout:
            commit_message = f"自动同步豆包AI云盘内容 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(["git", "commit", "-m", commit_message], 
                          cwd=Config.GIT_REPO_PATH, 
                          check=True, 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
            
            subprocess.run(["git", "push", "origin", "main"], 
                          cwd=Config.GIT_REPO_PATH, 
                          check=True, 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
            
            log("已成功提交更改到Git仓库")
        else:
            log("没有检测到需要提交的更改")
        
        return True
    except Exception as e:
        log(f"Git操作失败: {str(e)}")
        return False

# 主函数
def main():
    """主函数"""
    try:
        # 同步云盘内容
        if sync_cloud_to_local():
            # 提交到Git
            commit_to_git()
        
        log("同步任务已完成")
    except Exception as e:
        log(f"同步任务异常: {str(e)}")

if __name__ == "__main__":
    main()