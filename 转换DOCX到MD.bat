@echo off
REM DOCX到Markdown转换工具批处理脚本

REM 检查Python是否已安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python。请先安装Python并添加到系统PATH中。
    pause
    exit /b 1
)

REM 检查python-docx库是否已安装
python -c "import docx" >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装python-docx库...
    pip install python-docx
    if %errorlevel% neq 0 (
        echo 错误: 安装python-docx库失败。
        pause
        exit /b 1
    )
)

REM 提示用户输入DOCX文件路径
set /p input_file=请输入DOCX文件路径（例如：C:\文档\报告.docx）: 

REM 检查文件是否存在
if not exist "%input_file%" (
    echo 错误: 找不到文件 "%input_file%"
    pause
    exit /b 1
)

REM 提示用户输入输出文件路径，默认为同目录同名MD文件
set /p output_file=请输入输出MD文件路径（留空使用默认路径）: 

REM 执行转换脚本
if defined output_file (
    python "%~dp0docx_to_markdown.py" "%input_file%" "%output_file%"
) else (
    python "%~dp0docx_to_markdown.py" "%input_file%"
)

REM 检查转换是否成功
if %errorlevel% equ 0 (
    echo 转换成功！
) else (
    echo 转换失败！
)

pause