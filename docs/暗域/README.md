# 暗域

<script src="/scripts/dark-domain-access.js"></script>

<div id="dark-domain-content">
  <div id="dark-domain-access" style="display: none;">
    
    > 欢迎来到暗域，这里包含了特殊的知识内容。
    
    ## 暗域内容索引
    
    * [极客专用高效提示词与指令手册](极客专用高效提示词与指令手册.md)
    
  </div>
</div>

<script>
  // 验证成功后显示内容
  function onDarkDomainVerifySuccess() {
    const accessContent = document.getElementById('dark-domain-access');
    accessContent.style.display = 'block';
    
    // 更新侧边栏，确保极客手册链接可见
    setTimeout(() => {
      const app = window.$docsify || window.Docsify;
      if (app && app.router && app.router.refresh) {
        app.router.refresh();
      }
    }, 100);
  }
  
  // 初始化暗域访问控制
  document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('dark-domain-content');
    
    // 检查是否已验证
    if (window.isDarkDomainVerified && window.isDarkDomainVerified()) {
      onDarkDomainVerifySuccess();
    } else {
      // 创建验证界面
      window.createDarkDomainAccess('dark-domain-content', onDarkDomainVerifySuccess);
    }
  });
</script>