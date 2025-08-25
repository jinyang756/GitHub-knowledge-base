@echo off
REM DOCX/DOC到Markdown转换工具批处理脚本

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

REM 提示用户输入文件路径（支持.doc和.docx）
set /p input_file=请输入Word文件路径（支持.doc和.docx格式，例如：C:\文档\报告.doc）: 

REM 检查文件是否存在
if not exist "%input_file%" (
    echo 错误: 找不到文件 "%input_file%"
    pause
    exit /b 1
)

REM 获取用户输入文件的扩展名并转换为小写
for %%a in ("%input_file%") do set "file_ext=%%~xa"
set "file_ext=%file_ext:~1%"
set "file_ext=%file_ext:DOCX=docx%"
set "file_ext=%file_ext:DOC=doc%"

REM 如果是.doc文件，需要先转换为.docx
if "%file_ext%" equ "doc" (
    echo 检测到.doc文件，需要先转换为.docx格式...
    
    REM 检查pywin32库是否已安装
    python -c "import win32com.client" >nul 2>&1
    if %errorlevel% neq 0 (
        echo 正在安装pywin32库...
        pip install pywin32
        if %errorlevel% neq 0 (
            echo 错误: 安装pywin32库失败，无法转换.doc文件。
            pause
            exit /b 1
        )
    )
    
    REM 创建临时的DOCX文件路径
    set "temp_docx=%~dpn1_temp.docx"
    
    REM 使用PowerShell将DOC转换为DOCX
    powershell -Command "
    $word = New-Object -ComObject Word.Application;
    $word.Visible = $false;
    $word.DisplayAlerts = 0;
    try {
        $doc = $word.Documents.Open('"%input_file%"');
        $doc.SaveAs('"%temp_docx%"', 16);
        $doc.Close();
        Write-Host '成功将.doc文件转换为.docx格式';
    } catch {
        Write-Host '转换.doc到.docx时发生错误: ' $_ -ForegroundColor Red;
        exit 1;
    } finally {
        $word.Quit();
    }"
    
    if %errorlevel% neq 0 (
        echo 转换.doc到.docx失败！
        pause
        exit /b 1
    )
    
    REM 设置临时DOCX文件为输入文件
    set "input_file=%temp_docx%"
    set "cleanup_temp=1"
)

REM 提示用户输入输出文件路径，默认为同目录同名MD文件
set /p output_file=请输入输出MD文件路径（留空使用默认路径）: 

REM 如果未指定输出文件，则使用原始输入文件的名称，将扩展名改为.md
if not defined output_file (
    for %%a in ("%input_file%") do set "output_file=%%~dpna.md"
)

REM 执行转换脚本
if defined output_file (
    python "%~dp0docx_to_markdown.py" "%input_file%" "%output_file%"
) else (
    python "%~dp0docx_to_markdown.py" "%input_file%"
)

REM 检查转换是否成功
if %errorlevel% equ 0 (
    echo 转换成功！
    echo 生成的Markdown文件：%output_file%
) else (
    echo 转换失败！
)

REM 清理临时文件
if defined cleanup_temp (
    if exist "%temp_docx%" (
        del "%temp_docx%"
        echo 已清理临时文件
    )
)

pause