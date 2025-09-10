#!/bin/bash

# AI服务模块启动脚本

# 设置脚本为执行出错时立即退出
set -e

# 检查Python是否安装
if ! command -v python3 &> /dev/null
then
    echo "错误: Python3 未安装。请先安装Python 3.8或更高版本。"
    exit 1
fi

# 检查pip是否安装
if ! command -v pip3 &> /dev/null
then
    echo "错误: pip3 未安装。请先安装pip。"
    exit 1
fi

# 函数：显示帮助信息
show_help() {
    echo "AI服务模块启动脚本"
    echo "用法: ./start.sh [选项]"
    echo "选项:"
    echo "  --install      安装依赖包"
    echo "  --test         运行基本测试"
    echo "  --demo         运行示例应用"
    echo "  --install-gpu  安装带GPU支持的依赖包"
    echo "  --dev          安装开发依赖包"
    echo "  --help         显示帮助信息"
    echo ""
    echo "示例:"
    echo "  ./start.sh --install --test     # 安装依赖并运行测试"
    echo "  ./start.sh --demo               # 运行示例应用"
}

# 函数：安装基本依赖
install_dependencies() {
    echo "正在安装基本依赖..."
    pip3 install -r requirements.txt
    echo "基本依赖安装完成！"
}

# 函数：安装带GPU支持的依赖
install_gpu_dependencies() {
    echo "正在安装带GPU支持的依赖..."
    # 先卸载CPU版本
    pip3 uninstall -y faiss-cpu
    # 安装GPU版本
    pip3 install faiss-gpu>=1.7.3
    echo "GPU依赖安装完成！"
}

# 函数：安装开发依赖
install_dev_dependencies() {
    echo "正在安装开发依赖..."
    pip3 install pytest black isort
    echo "开发依赖安装完成！"
}

# 函数：运行基本测试
run_tests() {
    echo "正在运行基本测试..."
    python3 test_basic.py
    echo "测试完成！"
}

# 函数：运行示例应用
run_demo() {
    echo "正在运行示例应用..."
    python3 example_app.py
    echo "示例应用运行完成！"
}

# 如果没有提供参数，显示帮助信息
if [ $# -eq 0 ]
then
    show_help
    exit 0
fi

# 处理命令行参数
while [ $# -gt 0 ]
do
    case $1 in
        --install)
            install_dependencies
            shift
            ;;
        --install-gpu)
            install_gpu_dependencies
            shift
            ;;
        --dev)
            install_dev_dependencies
            shift
            ;;
        --test)
            run_tests
            shift
            ;;
        --demo)
            run_demo
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

echo "启动脚本执行完成！"