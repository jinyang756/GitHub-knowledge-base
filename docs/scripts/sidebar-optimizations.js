// 侧边栏优化脚本
window.addEventListener('DOMContentLoaded', function() {
  // 等待docsify完全加载后执行
  const observer = new MutationObserver(function(mutations) {
    if (document.querySelector('.sidebar-nav')) {
      observer.disconnect();
      optimizeSidebar();
    }
  });
  
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
});

function optimizeSidebar() {
  // 1. 自动折叠所有二级菜单，只保持一级菜单展开
  const sidebarItems = document.querySelectorAll('.sidebar-nav li');
  sidebarItems.forEach(item => {
    if (item.querySelector('ul')) {
      item.classList.add('collapse');
    }
  });
  
  // 2. 点击一级菜单项时，只展开/折叠当前项的子菜单
  const parentItems = document.querySelectorAll('.sidebar-nav > ul > li > a');
  parentItems.forEach(item => {
    item.addEventListener('click', function(e) {
      const parentLi = this.parentElement;
      const childUl = parentLi.querySelector('ul');
      
      if (childUl) {
        // 切换当前菜单的折叠状态
        parentLi.classList.toggle('collapse');
        
        // 阻止事件冒泡，防止触发其他菜单的折叠
        e.stopPropagation();
      }
    });
  });
  
  // 3. 点击文档链接时，保持侧边栏简洁，不自动展开所有相关菜单
  const docLinks = document.querySelectorAll('.sidebar-nav a');
  docLinks.forEach(link => {
    link.addEventListener('click', function() {
      setTimeout(() => {
        // 点击链接后再次折叠所有不相关的菜单
        const sidebarItems = document.querySelectorAll('.sidebar-nav li');
        sidebarItems.forEach(item => {
          if (item.querySelector('ul') && !item.classList.contains('active')) {
            item.classList.add('collapse');
          }
        });
      }, 100);
    });
  });
  
  // 4. 优化移动端侧边栏体验
  const sidebarToggle = document.querySelector('.sidebar-toggle');
  if (sidebarToggle) {
    sidebarToggle.addEventListener('click', function() {
      setTimeout(() => {
        optimizeSidebarDisplay();
      }, 300);
    });
  }
  
  // 5. 窗口大小变化时调整侧边栏显示
  window.addEventListener('resize', optimizeSidebarDisplay);
  
  // 初始优化显示
  optimizeSidebarDisplay();
}

function optimizeSidebarDisplay() {
  const sidebar = document.querySelector('.sidebar');
  const content = document.querySelector('.content');
  const windowWidth = window.innerWidth;
  
  // 根据窗口大小调整侧边栏和内容区域的布局
  if (windowWidth < 768) {
    // 移动端：确保侧边栏可以完全收起
    if (sidebar) {
      sidebar.style.width = '280px';
    }
  } else {
    // 桌面端：优化侧边栏与内容区域的比例
    if (sidebar) {
      sidebar.style.width = '300px';
    }
    if (content) {
      content.style.paddingLeft = '300px';
    }
  }
}

// 6. 添加侧边栏记忆功能，记住用户上次的展开/折叠状态
window.addEventListener('beforeunload', function() {
  const expandedItems = [];
  const sidebarItems = document.querySelectorAll('.sidebar-nav li');
  
  sidebarItems.forEach((item, index) => {
    if (!item.classList.contains('collapse')) {
      expandedItems.push(index);
    }
  });
  
  localStorage.setItem('sidebarExpandedItems', JSON.stringify(expandedItems));
});

// 7. 页面加载时恢复上次的侧边栏状态
window.addEventListener('DOMContentLoaded', function() {
  setTimeout(() => {
    const savedExpandedItems = localStorage.getItem('sidebarExpandedItems');
    if (savedExpandedItems) {
      const expandedItems = JSON.parse(savedExpandedItems);
      const sidebarItems = document.querySelectorAll('.sidebar-nav li');
      
      expandedItems.forEach(index => {
        if (sidebarItems[index]) {
          sidebarItems[index].classList.remove('collapse');
        }
      });
    }
  }, 500);
});