@echo off

REM 启动服务监控程序
cd /d "%~dp0"
echo 正在启动服务监控程序...

REM 使用Python启动监控脚本
python service_monitor.py

REM 如果脚本意外退出，显示错误信息
if %errorlevel% neq 0 (
echo 服务监控程序启动失败！
pause
exit /b %errorlevel%
)

REM 等待用户按键退出
pause >nul