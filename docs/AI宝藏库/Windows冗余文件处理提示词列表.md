# Windows 冗余文件处理提示词列表（无关/重复/沉淀文件+无效日志）

以下按文件类型整理Windows系统（含原生工具、命令行、开发场景）的典型提示信息，覆盖删除确认、权限限制、自动清理等核心场景：

## 一、无关文件处理提示
<div class="prompt-table">
| 场景                | 提示内容                                                                 | 触发条件                                                                 | 
|---------------------|--------------------------------------------------------------------------|--------------------------------------------------------------------------| 
| 普通无关文件删除    | <div class="prompt-item"><code>「确定要将"xxx.xxx"移到回收站吗？」</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 右键删除与项目无关的文件（如旧安装包、临时下载的测试文件）                | 
| 系统临时文件清理    | <div class="prompt-item"><code>「存储感知发现可删除的临时文件，是否立即清理以释放空间？」</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 开启存储感知后，系统检测到超过阈值的临时文件（如`%temp%`目录下的缓存文件） | 
| 下载目录冗余文件提示 | <div class="prompt-item"><code>「下载文件夹中有30天未访问的文件，是否移至回收站？」</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 存储感知配置中启用"删除下载文件夹中30天未更改的文件"选项时触发        | 
| 管理员权限文件删除  | <div class="prompt-item"><code>「你要允许此应用对你的设备进行更改吗？」</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 删除位于`C:\Program Files`等系统目录下的无关开发工具残留文件时             | 
</div>

## 二、重复文件处理提示
<div class="prompt-table">
| 场景                | 提示内容                                                                 | 触发条件                                                                 | 
|---------------------|--------------------------------------------------------------------------|--------------------------------------------------------------------------| 
| 跨分区复制重名文件  | <div class="prompt-item"><code>「已存在名为"xxx.xxx"的文件。是否要替换它？(是/否/全部)」</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 从C盘复制文件到D盘时，目标目录存在同名文件（如重复的`utils.js`副本）  | 
| 同分区重复文件处理  | <div class="prompt-item"><code>（无提示，自动重命名）</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 同一分区内复制文件时，系统自动生成"xxx - 副本.xxx"命名（如`config - 副本.json`） | 
| 覆盖系统文件警告    | <div class="prompt-item"><code>「替换文件可能会导致程序无法正常工作。此文件来自更高级别的系统版本」</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 尝试用旧版本开发库文件覆盖`System32`或`SysWOW64`目录下的同名系统文件时     | 
| 批量复制冲突提示    | <div class="prompt-item"><code>「有12个文件与目标位置的文件重名。是否要替换所有文件？」</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 使用资源管理器批量复制文件夹时，存在多个同名文件冲突                       | 
</div>

## 三、沉淀文件处理提示
<div class="prompt-table">
| 场景                | 提示内容                                                                 | 触发条件                                                                 | 
|---------------------|--------------------------------------------------------------------------|--------------------------------------------------------------------------| 
| 长期未访问文件提示  | <div class="prompt-item"><code>「这些文件已超过90天未访问，是否将其移至云存储以释放空间？」</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 存储感知检测到本地大量长期未使用的开发归档文件（如旧版本项目备份）   | 
| 回收站沉淀文件清理  | <div class="prompt-item"><code>「回收站中有已存放30天以上的文件，是否永久删除？」</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 存储感知定期清理时，检测到过期回收站文件（含误删的开发中间产物）      | 
| 大型沉淀文件夹删除  | <div class="prompt-item"><code>「"archive_2023"文件夹已超过180天未修改，删除后将无法恢复，确定继续？」</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 右键删除包含历史项目的大型归档文件夹时，系统通过最后修改时间判断为沉淀文件 | 
| 云同步沉淀文件提示  | <div class="prompt-item"><code>「OneDrive中这些文件已30天未打开，将仅保留联机版本以释放空间」</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 开启OneDrive文件按需下载后，检测到长期未访问的开发文档               | 
</div>

## 四、开发无效日志处理提示
<div class="prompt-table">
| 场景                | 提示内容                                                                 | 触发条件                                                                 | 
|---------------------|--------------------------------------------------------------------------|--------------------------------------------------------------------------| 
| 普通日志文件删除    | <div class="prompt-item"><code>「确定要将"debug.log"移到回收站吗？」</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 右键删除开发调试日志、构建输出日志等非系统日志文件                       | 
| 日志文件被占用提示  | <div class="prompt-item"><code>「操作无法完成，因为文件已在"VS Code"中打开。关闭该文件并重试。」</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 尝试删除正在被IDE或服务进程占用的日志文件（如运行中的Node.js服务日志） | 
| PowerShell删除日志权限不足 | <div class="prompt-item"><code>「访问被拒绝」或「需要管理员权限才能执行此操作」</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 非管理员身份在PowerShell中执行`Remove-Item *.log`删除系统日志时     | 
| 系统日志满警告      | <div class="prompt-item"><code>「安全日志已满，需要登录系统管理员进行清理」</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 开发环境的Windows安全日志达到大小限制（如调试时频繁触发的权限审核日志） | 
| 事件日志删除确认    | <div class="prompt-item"><code>「确定要删除"Application"日志吗？这可能导致应用程序问题排查困难」</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 使用`Remove-EventLog -LogName Application`删除系统应用程序日志时    | 
| 批量日志清理提示    | <div class="prompt-item"><code>「即将删除1000+个日志文件，此操作不可撤销。是否继续？」</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 通过脚本批量删除`logs/`目录下的开发无效日志时（如加`-Confirm`参数的PowerShell命令） | 
</div>

## 五、核心处理工具提示差异
<div class="prompt-table">
| 工具/场景           | 典型提示特点                                                             | 适用场景                                                                 | 
|---------------------|--------------------------------------------------------------------------|--------------------------------------------------------------------------| 
| 资源管理器图形界面  | <div class="prompt-item"><code>强调"移至回收站""可恢复"，提示温和</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 手动删除单个或少量冗余文件、日志                                         | 
| 磁盘清理工具        | <div class="prompt-item"><code>列出分类大小（如"日志文件：2.5GB"），提示"删除后释放空间"</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 系统级清理无效日志、临时文件                                             | 
| PowerShell命令行    | <div class="prompt-item"><code>无提示（默认）或需显式确认（加`-Confirm`），权限不足提示明确</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 批量删除开发日志、自动化清理脚本                                         | 
| 存储感知自动清理    | <div class="prompt-item"><code>侧重"空间释放""自动执行"，提示频率低</code><button class="copy-btn" onclick="copyToClipboard(this)">复制</button></div> | 定期清理沉淀文件、长期未用的开发缓存                                     | 
</div>

## 关键注意事项
<div class="important-notes">

### 1. 可恢复性区分：
- 移至回收站的文件（如普通日志、无关文档）可临时恢复；
- 用`rm -rf`或磁盘清理删除的文件（如系统日志、大型沉淀文件）通常不可恢复，提示中会强调"永久删除"。

### 2. 权限边界：
- 开发日志（如`node_modules/.cache`）可普通权限删除；
- 系统日志（如事件查看器日志）需管理员权限，删除前会触发UAC确认提示。

### 3. 进程占用防护：
被开发工具（VS Code、数据库服务）占用的日志文件删除时，会明确提示占用进程名称，需关闭对应程序后操作。

</div>

可根据具体开发场景（如前端日志清理、后端系统日志管理）进一步细化提示词内容。

<script>
function copyToClipboard(button) {
    const codeElement = button.parentNode.querySelector('code');
    if (codeElement) {
        const textToCopy = codeElement.textContent;
        navigator.clipboard.writeText(textToCopy).then(() => {
            const originalText = button.textContent;
            button.textContent = '已复制！';
            button.classList.add('copied');
            setTimeout(() => {
                button.textContent = originalText;
                button.classList.remove('copied');
            }, 2000);
        }).catch(err => {
            console.error('复制失败:', err);
        });
    }
}
</script>

<style>
.prompt-table {
    margin-bottom: 20px;
}

.prompt-item {
    position: relative;
    display: inline-block;
    width: [投资比例建议];
}

.prompt-item code {
    background-color: #f5f5f5;
    padding: 5px 10px;
    border-radius: 4px;
    display: inline-block;
    width: calc([投资比例建议] - 80px);
    word-wrap: break-word;
}

.copy-btn {
    position: absolute;
    right: 0;
    top: [投资比例建议];
    transform: translateY(-[投资比例建议]);
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
    width: 70px;
}

.copy-btn:hover {
    background-color: #45a049;
}

.copy-btn.copied {
    background-color: #2196F3;
}

.important-notes {
    background-color: #f9f9f9;
    padding: 15px;
    border-left: 4px solid #2196F3;
    margin-top: 20px;
    border-radius: 4px;
}
</style>