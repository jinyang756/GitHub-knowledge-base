@echo off

REM 启动实盘解析自动化工作流
cd /d "%~dp0"
echo 正在启动实盘解析自动更新服务...

REM 使用Python启动自动化脚本
python automatic_trading_analysis.py scheduler

REM 如果脚本意外退出，显示错误信息
if %errorlevel% neq 0 (
echo 实盘解析自动更新服务启动失败！
pause
exit /b %errorlevel%
)

REM 等待用户按键退出
echo 实盘解析自动更新服务已启动成功！
echo 按任意键退出命令窗口（服务将在后台继续运行）...
pause >nul