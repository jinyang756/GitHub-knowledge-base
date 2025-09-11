// 侧边栏优化脚本
(function() {
  // 防止多次初始化的标志
  let initialized = false;
  
  // 初始化函数
  function initSidebarOptimizations() {
    if (initialized) return;
    initialized = true;
    
    // 等待docsify完全加载后执行
    const observer = new MutationObserver(function(mutations) {
      const sidebarNav = document.querySelector('.sidebar-nav');
      if (sidebarNav) {
        observer.disconnect();
        optimizeSidebar(sidebarNav);
        // 尝试恢复侧边栏状态
        restoreSidebarState();
      }
    });
    
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
    
    // 优化移动端侧边栏体验
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    if (sidebarToggle) {
      sidebarToggle.addEventListener('click', function() {
        setTimeout(() => {
          optimizeSidebarDisplay();
        }, 300);
      });
    }
    
    // 窗口大小变化时调整侧边栏显示
    window.addEventListener('resize', optimizeSidebarDisplay);
    
    // 页面切换时重新优化侧边栏
    window.addEventListener('DOMNodeInserted', function(e) {
      if (e.target.className && e.target.className.includes('markdown-section')) {
        setTimeout(() => {
          const sidebarNav = document.querySelector('.sidebar-nav');
          if (sidebarNav) {
            optimizeSidebarDisplay();
          }
        }, 100);
      }
    });
    
    // 监听页面卸载事件，保存侧边栏状态
    window.addEventListener('beforeunload', saveSidebarState);
  }
  
  // 优化侧边栏功能
  function optimizeSidebar(sidebarNav) {
    // 1. 自动折叠所有二级菜单，只保持一级菜单展开
    const sidebarItems = sidebarNav.querySelectorAll('li');
    sidebarItems.forEach(item => {
      if (item.querySelector('ul') && !item.classList.contains('active')) {
        item.classList.add('collapse');
      }
    });
    
    // 2. 点击一级菜单项时，只展开/折叠当前项的子菜单
    const parentItems = sidebarNav.querySelectorAll('> ul > li > a');
    parentItems.forEach(item => {
      item.addEventListener('click', function(e) {
        const parentLi = this.parentElement;
        const childUl = parentLi.querySelector('ul');
        
        if (childUl) {
          // 切换当前菜单的折叠状态
          parentLi.classList.toggle('collapse');
          
          // 阻止事件冒泡，防止触发其他菜单的折叠
          e.stopPropagation();
          
          // 保存状态
          saveSidebarState();
        }
      });
    });
    
    // 3. 点击文档链接时，保持侧边栏简洁，不自动展开所有相关菜单
    const docLinks = sidebarNav.querySelectorAll('a');
    docLinks.forEach(link => {
      link.addEventListener('click', function() {
        setTimeout(() => {
          // 点击链接后再次折叠所有不相关的菜单
          const sidebarItems = sidebarNav.querySelectorAll('li');
          sidebarItems.forEach(item => {
            if (item.querySelector('ul') && !item.classList.contains('active')) {
              item.classList.add('collapse');
            }
          });
          
          // 保存状态
          saveSidebarState();
        }, 100);
      });
    });
    
    // 初始优化显示
    optimizeSidebarDisplay();
  }
  
  // 优化侧边栏显示
  function optimizeSidebarDisplay() {
    const sidebar = document.querySelector('.sidebar');
    const content = document.querySelector('.content');
    const windowWidth = window.innerWidth;
    
    // 确保元素存在
    if (!sidebar || !content) return;
    
    // 根据窗口大小调整侧边栏和内容区域的布局
    if (windowWidth < 768) {
      // 移动端：确保侧边栏可以完全收起
      sidebar.style.width = '280px';
    } else {
      // 桌面端：优化侧边栏与内容区域的比例
      sidebar.style.width = '300px';
      content.style.paddingLeft = '300px';
    }
  }
  
  // 保存侧边栏状态
  function saveSidebarState() {
    try {
      const sidebarNav = document.querySelector('.sidebar-nav');
      if (!sidebarNav) return;
      
      // 使用更可靠的标识方式：使用链接文本而不是索引
      const expandedItems = [];
      const sidebarItems = sidebarNav.querySelectorAll('li');
      
      sidebarItems.forEach((item, index) => {
        if (item.querySelector('a') && !item.classList.contains('collapse')) {
          const linkText = item.querySelector('a').textContent.trim();
          expandedItems.push(linkText);
        }
      });
      
      localStorage.setItem('sidebarExpandedItems', JSON.stringify(expandedItems));
    } catch (error) {
      console.warn('Failed to save sidebar state:', error);
    }
  }
  
  // 恢复侧边栏状态
  function restoreSidebarState() {
    try {
      const savedExpandedItems = localStorage.getItem('sidebarExpandedItems');
      if (!savedExpandedItems) return;
      
      const expandedItems = JSON.parse(savedExpandedItems);
      const sidebarNav = document.querySelector('.sidebar-nav');
      if (!sidebarNav) return;
      
      // 遍历所有链接，找到匹配的文本并展开
      const sidebarLinks = sidebarNav.querySelectorAll('li > a');
      sidebarLinks.forEach(link => {
        const linkText = link.textContent.trim();
        if (expandedItems.includes(linkText)) {
          const parentLi = link.parentElement;
          if (parentLi && parentLi.classList.contains('collapse')) {
            parentLi.classList.remove('collapse');
          }
        }
      });
    } catch (error) {
      console.warn('Failed to restore sidebar state:', error);
      // 出现错误时清除存储的数据
      localStorage.removeItem('sidebarExpandedItems');
    }
  }
  
  // 等待DOM加载完成后初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSidebarOptimizations);
  } else {
    initSidebarOptimizations();
  }
  
  // 导出全局方法，方便调试和扩展
  window.SidebarOptimizations = {
    init: initSidebarOptimizations,
    saveState: saveSidebarState,
    restoreState: restoreSidebarState
  };
})();