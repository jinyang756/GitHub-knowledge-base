// div自由拉升功能实现
// 使用立即执行函数表达式(IIFE)避免全局命名空间污染
(function() {
  // 配置常量
  const CONFIG = {
    MIN_HEIGHT: 50,
    MIN_WIDTH: 100,
    INITIALIZATION_DELAY: 100,
    MARGIN_PADDING: 20
  };
  
  // 防止多次初始化的标志
  let initialized = false;

  // 初始化div自由拉升功能
  function initDivResizer() {
    try {
      // 1. 为搜索框添加自由拉升功能
      setupResizerForElement('.search-section', 'vertical');
      
      // 2. 为主要内容区域的卡片添加自由拉升功能
      setupResizerForClass('.markdown-section > div:not(.search-section):not(.quick-navigation)', 'vertical');
      
      // 3. 为快速导航区域添加自由拉升功能
      setupResizerForElement('.quick-navigation', 'vertical');
      
      // 4. 为section模块添加跟随功能
      setupSectionFollowing();
    } catch (error) {
      console.warn('Error initializing div resizer:', error);
    }
  }

  // 为指定元素添加拉升功能
  function setupResizerForElement(selector, direction) {
    try {
      const element = document.querySelector(selector);
      if (element && !element.querySelector('.resizer-handle')) {
        addResizer(element, direction);
      }
    } catch (error) {
      console.warn(`Error setting up resizer for element ${selector}:`, error);
    }
  }

  // 为指定类的所有元素添加拉升功能
  function setupResizerForClass(classSelector, direction) {
    try {
      const elements = document.querySelectorAll(classSelector);
      elements.forEach(element => {
        if (!element.querySelector('.resizer-handle')) {
          addResizer(element, direction);
        }
      });
    } catch (error) {
      console.warn(`Error setting up resizer for class ${classSelector}:`, error);
    }
  }

  // 添加拉升手柄
  function addResizer(element, direction) {
    try {
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
          if (newHeight > CONFIG.MIN_HEIGHT) {
            element.style.height = newHeight + 'px';
            element.style.minHeight = newHeight + 'px';
            // 通知section跟随调整
            notifySectionResize();
          }
        } else if (direction === 'horizontal') {
          const newWidth = startWidth + (e.clientX - startX);
          // 限制最小宽度
          if (newWidth > CONFIG.MIN_WIDTH) {
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
    } catch (error) {
      console.warn('Error adding resizer:', error);
    }
  }

  // 初始化拉升手柄的CSS样式
  function initResizerCSS() {
    try {
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
    } catch (error) {
      console.warn('Error initializing resizer CSS:', error);
    }
  }

  // 设置section跟随功能
  function setupSectionFollowing() {
    try {
      // 使用MutationObserver替代DOMNodeInserted
      const observer = new MutationObserver(mutations => {
        try {
          const hasRelevantChange = mutations.some(mutation => {
            return mutation.type === 'childList' || 
                  (mutation.type === 'attributes' && 
                   (mutation.target.classList?.contains('markdown-section') ||
                    mutation.target.classList?.contains('resizing')));
          });
          
          if (hasRelevantChange) {
            notifySectionResize();
          }
        } catch (observerError) {
          console.warn('Error in MutationObserver:', observerError);
        }
      });
      
      observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['style', 'class']
      });
    } catch (error) {
      console.warn('Error setting up section following:', error);
    }
  }

  // 通知section内容调整大小
  function notifySectionResize() {
    try {
      // 触发窗口大小调整事件，让docsify重新计算布局
      window.dispatchEvent(new Event('resize'));
      
      // 滚动到当前位置，确保视图正确
      if (window.scrollY > 0) {
        window.scrollTo(window.scrollX, window.scrollY);
      }
    } catch (error) {
      console.warn('Error notifying section resize:', error);
    }
  }

  // 初始化函数
  function initialize() {
    if (initialized) return;
    initialized = true;
    
    // 等待DOM加载完成
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function() {
        initDivResizer();
      });
    } else {
      // 如果DOM已经加载完成，直接初始化
      initDivResizer();
    }
    
    // 监听页面内容变化，docsify在切换页面时会重新渲染内容
    document.addEventListener('DOMNodeInserted', function(e) {
      try {
        // 当检测到section内容加载完成时，重新初始化
        if (e.target.className && e.target.className.includes('markdown-section')) {
          setTimeout(initDivResizer, CONFIG.INITIALIZATION_DELAY);
        }
      } catch (error) {
        console.warn('Error in DOMNodeInserted handler:', error);
      }
    });
    
    // 监听hash变化事件，docsify页面切换时触发
    window.addEventListener('hashchange', function() {
      try {
        setTimeout(initDivResizer, CONFIG.INITIALIZATION_DELAY);
      } catch (error) {
        console.warn('Error in hashchange handler:', error);
      }
    });
  }

  // 导出全局方法，方便调试和扩展
  window.DivResizer = {
    init: initDivResizer,
    addResizer: addResizer,
    initialize: initialize
  };
  
  // 自动初始化
  initialize();
})();