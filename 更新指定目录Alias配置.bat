@echo off

REM docsify知识库alias配置自动更新批处理文件（可指定目录）
REM 双击运行后可以输入要更新的目录路径

echo ======= docsify alias配置自动更新工具（可指定目录） =======
echo.
echo 请输入要更新alias配置的目录路径（相对于docs目录）
echo 例如：技术/热门指标公式集、行业、政策
 echo 直接按回车将默认更新'技术/热门指标公式集'目录

echo.
set /p target_dir="请输入目录路径: "

REM 如果用户没有输入，则使用默认目录
if "%target_dir%"=="" (
    set target_dir=技术/热门指标公式集
    echo 未输入目录路径，将使用默认目录: %target_dir%
)

echo.
echo 正在更新'%target_dir%'目录的alias配置...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python环境！
    echo 请先安装Python并将其添加到系统环境变量中。
    pause
    exit /b 1
)

REM 运行Python脚本并传递目录参数
python update_alias_config.py %target_dir%

REM 显示完成信息
if %errorlevel% equ 0 (
    echo.
    echo 配置更新完成！按任意键退出...
) else (
    echo.
    echo 配置更新失败！按任意键退出...
)
pause