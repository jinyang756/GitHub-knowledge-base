// div自由拉升功能实现
(function() {
  // 等待DOM加载完成
  document.addEventListener('DOMContentLoaded', function() {
    // 初始化自由拉升功能
    initDivResizer();
  });

  // 监听页面内容变化，docsify在切换页面时会重新渲染内容
  document.addEventListener('DOMNodeInserted', function(e) {
    // 当检测到section内容加载完成时，重新初始化
    if (e.target.className && e.target.className.includes('markdown-section')) {
      setTimeout(initDivResizer, 100);
    }
  });

  // 初始化div自由拉升功能
  function initDivResizer() {
    // 1. 为搜索框添加自由拉升功能
    setupResizerForElement('.search-section', 'vertical');
    
    // 2. 为主要内容区域的卡片添加自由拉升功能
    setupResizerForClass('.markdown-section > div:not(.search-section):not(.quick-navigation)', 'vertical');
    
    // 3. 为快速导航区域添加自由拉升功能
    setupResizerForElement('.quick-navigation', 'vertical');
    
    // 4. 为section模块添加跟随功能
    setupSectionFollowing();
  }

  // 为指定元素添加拉升功能
  function setupResizerForElement(selector, direction) {
    const element = document.querySelector(selector);
    if (element && !element.querySelector('.resizer-handle')) {
      addResizer(element, direction);
    }
  }

  // 为指定类的所有元素添加拉升功能
  function setupResizerForClass(classSelector, direction) {
    const elements = document.querySelectorAll(classSelector);
    elements.forEach(element => {
      if (!element.querySelector('.resizer-handle')) {
        addResizer(element, direction);
      }
    });
  }

  // 添加拉升手柄
  function addResizer(element, direction) {
    // 确保元素有相对定位
    if (getComputedStyle(element).position === 'static') {
      element.style.position = 'relative';
    }
    
    // 创建拉升手柄
    const resizer = document.createElement('div');
    resizer.className = 'resizer-handle';
    resizer.dataset.direction = direction;
    
    // 添加到元素中
    element.appendChild(resizer);
    
    // 初始化CSS样式
    initResizerCSS();
    
    // 添加事件监听
    let startX, startY, startWidth, startHeight;
    
    resizer.addEventListener('mousedown', function(e) {
      e.preventDefault();
      
      startX = e.clientX;
      startY = e.clientY;
      startWidth = element.offsetWidth;
      startHeight = element.offsetHeight;
      
      // 添加事件监听
      document.addEventListener('mousemove', resize);
      document.addEventListener('mouseup', stopResize);
      
      // 添加调整中样式
      resizer.classList.add('resizing');
      element.classList.add('resizing');
    });
    
    function resize(e) {
      if (direction === 'vertical') {
        const newHeight = startHeight + (e.clientY - startY);
        // 限制最小高度
        if (newHeight > 50) {
          element.style.height = newHeight + 'px';
          element.style.minHeight = newHeight + 'px';
          // 通知section跟随调整
          notifySectionResize();
        }
      } else if (direction === 'horizontal') {
        const newWidth = startWidth + (e.clientX - startX);
        // 限制最小宽度
        if (newWidth > 100) {
          element.style.width = newWidth + 'px';
          element.style.minWidth = newWidth + 'px';
          // 通知section跟随调整
          notifySectionResize();
        }
      }
    }
    
    function stopResize() {
      // 移除事件监听
      document.removeEventListener('mousemove', resize);
      document.removeEventListener('mouseup', stopResize);
      
      // 移除调整中样式
      resizer.classList.remove('resizing');
      element.classList.remove('resizing');
    }
  }

  // 初始化拉升手柄的CSS样式
  function initResizerCSS() {
    // 检查是否已经添加了样式
    if (!document.getElementById('resizer-css')) {
      const style = document.createElement('style');
      style.id = 'resizer-css';
      style.textContent = `
        .resizer-handle {
          position: absolute;
          right: 0;
          bottom: 0;
          width: 20px;
          height: 20px;
          background: linear-gradient(135deg, transparent 50%, var(--primary-color) 50%);
          cursor: se-resize;
          opacity: 0;
          transition: opacity 0.3s ease;
          z-index: 10;
        }
        
        .resizer-handle[data-direction="vertical"] {
          width: 100%;
          height: 10px;
          background: linear-gradient(180deg, transparent 50%, var(--primary-color) 50%);
          cursor: ns-resize;
        }
        
        .resizer-handle[data-direction="horizontal"] {
          width: 10px;
          height: 100%;
          background: linear-gradient(90deg, transparent 50%, var(--primary-color) 50%);
          cursor: ew-resize;
        }
        
        .resizer-handle:hover,
        .resizing .resizer-handle {
          opacity: 0.5;
        }
        
        .resizing {
          outline: 1px dashed var(--primary-color);
        }
        
        /* 确保内容区域有足够的空间 */
        .markdown-section {
          transition: all 0.3s ease;
        }
      `;
      document.head.appendChild(style);
    }
  }

  // 设置section跟随功能
  function setupSectionFollowing() {
    const sections = document.querySelectorAll('.markdown-section > section');
    sections.forEach(section => {
      const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
          if (mutation.type === 'childList' || mutation.type === 'attributes') {
            notifySectionResize();
          }
        });
      });
      
      observer.observe(section, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['style', 'class']
      });
    });
  }

  // 通知section内容调整大小
  function notifySectionResize() {
    // 触发窗口大小调整事件，让docsify重新计算布局
    window.dispatchEvent(new Event('resize'));
    
    // 滚动到当前位置，确保视图正确
    if (window.scrollY > 0) {
      window.scrollTo(window.scrollX, window.scrollY);
    }
  }

  // 导出全局方法，方便调试和扩展
  window.DivResizer = {
    init: initDivResizer,
    addResizer: addResizer
  };
})();