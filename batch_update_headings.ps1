# 批量修改指标文件中的一级标题为二级标题

$targetDir = "c:\Users\Administrator\Desktop\GitHub知识库\docs\技术\热门指标公式集"
$files = Get-ChildItem -Path $targetDir -Filter "*.md" | Where-Object { $_.Name -match '^\d+\. ' }

foreach ($file in $files) {
    Write-Host "处理文件: $($file.FullName)"
    
    # 读取文件内容
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    
    # 使用正则表达式替换一级标题为二级标题
    $updatedContent = $content -replace '^# (.*)', '## $1'
    
    # 保存修改后的内容
    Set-Content -Path $file.FullName -Value $updatedContent -Encoding UTF8
    
    Write-Host "已更新文件: $($file.FullName)"
}

Write-Host "所有文件处理完成！共处理 $($files.Count) 个文件。"