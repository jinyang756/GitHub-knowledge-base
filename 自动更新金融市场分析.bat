@echo off

REM 金融市场分析自动更新服务启动脚本
REM 此脚本将在每天早上8点自动生成新的市场分析报告

echo ======= 金融市场分析自动更新服务 =======
echo.
echo 此服务将在每天早上8点（A股交易日）自动生成新的金融市场分析报告
echo 服务启动后将持续运行，请勿关闭此窗口
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python环境！
    echo 请先安装Python并将其添加到系统环境变量中。
    pause
    exit /b 1
)

REM 检查是否以管理员权限运行（可选，但推荐）
NET SESSION >nul 2>&1
if %errorLevel% neq 0 (
    echo 警告: 建议以管理员权限运行此脚本，以便更好地管理系统资源
    echo.
)

REM 启动自动更新服务
echo 正在启动金融市场分析自动更新服务...
echo 日志输出将显示在此窗口和market_update.log文件中
echo. 

python automatic_market_update.py scheduler

REM 如果服务意外退出，显示错误信息
if %errorlevel% neq 0 (
    echo.
    echo 错误: 金融市场分析自动更新服务意外退出！
    echo 请查看market_update.log文件获取详细错误信息
    pause
    exit /b 1
)

pause