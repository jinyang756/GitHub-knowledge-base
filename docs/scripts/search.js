// 搜索功能实现脚本

// 使用立即执行函数表达式(IIFE)避免全局命名空间污染
(function() {
  // 配置常量
  const CONFIG = {
    MIN_SEARCH_LENGTH: 2,
    DEBOUNCE_DELAY: 300,
    INITIALIZATION_DELAY: 300,
    NO_RESULTS_TIMEOUT: 3000,
    HIGHLIGHT_CLASS: 'search-highlight',
    SUGGESTION_CLASS: 'suggestion-item'
  };
  
  // 搜索历史记录
  let searchHistory = [];
  const MAX_HISTORY_SIZE = 10;
  
  // 防抖函数
  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }
  
  // DOM加载完成后执行初始化
  function init() {
    // 等待DOM加载完成
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initializeSearch);
    } else {
      // 如果DOM已经加载完成，直接初始化
      initializeSearch();
    }
    
    // 监听docsify页面切换事件
    window.addEventListener('hashchange', handlePageChange);
    
    // 监听DOM节点插入事件，确保在动态内容加载后重新初始化
    document.addEventListener('DOMNodeInserted', function(e) {
      // 当检测到section内容加载完成时，重新初始化
      if (e.target.className && e.target.className.includes('markdown-section')) {
        setTimeout(initializeSearch, 100);
      }
    });
  }
  
  // 初始化搜索功能
  function initializeSearch() {
    try {
      // 获取搜索相关元素（使用与现有代码兼容的选择器）
      const searchInput = document.getElementById('header-search-input');
      const searchButton = document.getElementById('header-search-btn');
      const searchSuggestions = document.getElementById('search-suggestions');
      
      if (!searchInput || !searchButton || !searchSuggestions) {
        console.warn('搜索相关元素未找到');
        return;
      }
      
      // 从localStorage加载搜索历史
      loadSearchHistory();
      
      // 为搜索框添加事件监听
      searchInput.addEventListener('input', debounce(handleSearchInput, CONFIG.DEBOUNCE_DELAY));
      searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          executeSearch();
        }
      });
      
      // 添加搜索框焦点和失焦事件
      searchInput.addEventListener('focus', function() {
        searchSuggestions.classList.add('active');
        showSearchSuggestions(); // 显示搜索历史或热门搜索
      });
      
      searchInput.addEventListener('blur', function() {
        setTimeout(() => {
          searchSuggestions.classList.remove('active');
        }, 200);
      });
      
      // 添加搜索按钮点击事件
      searchButton.addEventListener('click', executeSearch);
      
      // 确保搜索建议容器有正确的样式
      ensureSuggestionsContainerStyle();
      
    } catch (error) {
      console.error('初始化搜索功能失败:', error);
    }
  }
  
  // 处理搜索输入
  function handleSearchInput(e) {
    const searchTerm = e.target.value.trim().toLowerCase();
    
    if (searchTerm.length >= CONFIG.MIN_SEARCH_LENGTH) {
      showSearchSuggestions(searchTerm);
    } else if (searchTerm.length === 0) {
      // 显示搜索历史
      showSearchHistory();
    } else {
      clearSuggestions();
    }
  }
  
  // 确保搜索建议容器有正确的样式
  function ensureSuggestionsContainerStyle() {
    try {
      const searchSuggestions = document.getElementById('search-suggestions');
      if (searchSuggestions && !searchSuggestions.style.position) {
        Object.assign(searchSuggestions.style, {
          position: 'absolute',
          backgroundColor: 'white',
          border: '1px solid #e0e0e0',
          borderRadius: '8px',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
          maxHeight: '300px',
          overflowY: 'auto',
          zIndex: '1000',
          display: 'none',
          marginTop: '4px',
          left: '0',
          right: '0'
        });
      }
    } catch (error) {
      console.error('设置搜索建议容器样式失败:', error);
    }
  }
  
  // 显示搜索建议
  function showSearchSuggestions(searchTerm = '') {
    try {
      const searchSuggestions = document.getElementById('search-suggestions');
      const searchInput = document.getElementById('header-search-input');
      
      if (!searchSuggestions || !searchInput) {
        return;
      }
      
      // 获取当前输入的搜索词
      const currentSearchTerm = searchTerm || searchInput.value.trim().toLowerCase();
      
      // 清空容器
      clearSuggestions();
      
      // 首先显示搜索历史（如果有）
      if (searchHistory.length > 0 && currentSearchTerm.length === 0) {
        showSearchHistory();
      } else if (currentSearchTerm.length >= CONFIG.MIN_SEARCH_LENGTH) {
        // 模拟搜索建议
        const suggestions = generateSearchSuggestions(currentSearchTerm);
        
        if (suggestions.length > 0) {
          suggestions.forEach(suggestion => {
            const li = document.createElement('div');
            li.className = CONFIG.SUGGESTION_CLASS;
            li.innerHTML = highlightSearchTerm(suggestion.text || suggestion, currentSearchTerm);
            
            // 添加样式
            Object.assign(li.style, {
              padding: '0.75rem 1rem',
              cursor: 'pointer',
              borderBottom: '1px solid var(--border-color, #eee)',
              transition: 'background-color 0.2s ease'
            });
            
            // 添加悬停效果
            li.addEventListener('mouseenter', function() {
              this.style.backgroundColor = 'rgba(37, 99, 235, 0.1)';
            });
            
            li.addEventListener('mouseleave', function() {
              this.style.backgroundColor = '';
            });
            
            // 添加点击事件
            li.addEventListener('click', function() {
              searchInput.value = this.textContent;
              executeSearch();
            });
            
            searchSuggestions.appendChild(li);
          });
        } else {
          // 没有找到匹配的建议
          const li = document.createElement('div');
          li.className = CONFIG.SUGGESTION_CLASS;
          li.style.color = '#999';
          li.style.textAlign = 'center';
          li.style.fontStyle = 'italic';
          li.textContent = '没有找到相关建议';
          li.style.cursor = 'default';
          li.style.padding = '0.75rem 1rem';
          searchSuggestions.appendChild(li);
        }
      }
      
      // 显示搜索建议容器
      searchSuggestions.style.display = 'block';
      searchSuggestions.classList.add('active');
      
    } catch (error) {
      console.error('显示搜索建议失败:', error);
    }
  }
  
  // 显示搜索历史
  function showSearchHistory() {
    try {
      const searchSuggestions = document.getElementById('search-suggestions');
      const searchInput = document.getElementById('header-search-input');
      
      if (!searchSuggestions || !searchInput) {
        return;
      }
      
      // 清空容器
      clearSuggestions();
      
      // 添加历史记录标题
      if (searchHistory.length > 0) {
        const historyHeader = document.createElement('div');
        historyHeader.className = 'search-history-header';
        historyHeader.textContent = '搜索历史';
        
        // 添加清除历史按钮
        const clearButton = document.createElement('span');
        clearButton.className = 'search-history-clear';
        clearButton.innerHTML = '<i class="fas fa-trash-alt"></i> 清除';
        clearButton.style.float = 'right';
        clearButton.style.cursor = 'pointer';
        clearButton.style.color = '#999';
        
        clearButton.addEventListener('click', function(e) {
          e.stopPropagation();
          clearSearchHistory();
          clearSuggestions();
          
          // 显示默认提示
          const defaultText = document.createElement('div');
          defaultText.className = CONFIG.SUGGESTION_CLASS;
          defaultText.textContent = '输入关键词进行搜索...';
          defaultText.style.padding = '0.75rem 1rem';
          defaultText.style.color = 'var(--secondary-text, #999)';
          defaultText.style.fontStyle = 'italic';
          
          searchSuggestions.appendChild(defaultText);
        });
        
        clearButton.addEventListener('mouseenter', function() {
          this.style.color = '#666';
        });
        
        historyHeader.appendChild(clearButton);
        historyHeader.style.padding = '8px 1rem';
        historyHeader.style.fontSize = '0.85rem';
        historyHeader.style.color = '#666';
        historyHeader.style.borderBottom = '1px solid #eee';
        historyHeader.style.fontWeight = '600';
        
        searchSuggestions.appendChild(historyHeader);
        
        // 添加历史记录项
        searchHistory.forEach(item => {
          const li = document.createElement('div');
          li.className = CONFIG.SUGGESTION_CLASS;
          li.innerHTML = `<i class="fas fa-history"></i> ${item}`;
          
          // 添加样式
          Object.assign(li.style, {
            padding: '0.75rem 1rem',
            cursor: 'pointer',
            borderBottom: '1px solid var(--border-color, #eee)',
            transition: 'background-color 0.2s ease'
          });
          
          // 添加悬停效果
          li.addEventListener('mouseenter', function() {
            this.style.backgroundColor = 'rgba(37, 99, 235, 0.1)';
          });
          
          li.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
          });
          
          // 添加点击事件
          li.addEventListener('click', function() {
            searchInput.value = item;
            executeSearch();
          });
          
          searchSuggestions.appendChild(li);
        });
      } else {
        // 显示默认提示
        const defaultText = document.createElement('div');
        defaultText.className = CONFIG.SUGGESTION_CLASS;
        defaultText.textContent = '输入关键词进行搜索...';
        defaultText.style.padding = '0.75rem 1rem';
        defaultText.style.color = 'var(--secondary-text, #999)';
        defaultText.style.fontStyle = 'italic';
        
        searchSuggestions.appendChild(defaultText);
      }
      
      // 显示搜索建议容器
      searchSuggestions.style.display = 'block';
      searchSuggestions.classList.add('active');
    } catch (error) {
      console.error('显示搜索历史失败:', error);
    }
  }
  
  // 清空搜索建议
  function clearSuggestions() {
    try {
      const searchSuggestions = document.getElementById('search-suggestions');
      if (searchSuggestions) {
        searchSuggestions.innerHTML = '';
      }
    } catch (error) {
      console.error('清空搜索建议失败:', error);
    }
  }
  
  // 高亮搜索词
  function highlightSearchTerm(text, searchTerm) {
    if (!searchTerm) return text;
    
    const regex = new RegExp(`(${escapeRegExp(searchTerm)})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
  }
  
  // 转义正则表达式特殊字符
  function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // $& 表示整个匹配的字符串
  }
  
  // 执行搜索
  function executeSearch() {
    try {
      const searchInput = document.getElementById('header-search-input');
      if (!searchInput) {
        return;
      }
      
      const searchTerm = searchInput.value.trim();
      if (searchTerm === '') {
        return;
      }
      
      // 添加到搜索历史
      addToSearchHistory(searchTerm);
      
      // 隐藏搜索建议
      const searchSuggestions = document.getElementById('search-suggestions');
      if (searchSuggestions) {
        searchSuggestions.style.display = 'none';
        searchSuggestions.classList.remove('active');
      }
      
      // 清空之前的高亮
      clearSearchHighlights();
      
      // 如果docsify的搜索插件可用，使用它执行搜索
      if (window.$docsify && window.$docsify.search && typeof window.$docsify.search.val === 'function') {
        // 触发docsify搜索
        window.$docsify.search.val(searchTerm);
        // 滚动到搜索结果区域
        const searchContainer = document.querySelector('.sidebar-nav');
        if (searchContainer) {
          searchContainer.scrollIntoView({ behavior: 'smooth' });
        }
      } else {
        // 自定义搜索实现
        performCustomSearch(searchTerm);
      }
    } catch (error) {
      console.error('执行搜索失败:', error);
      showSearchError('搜索过程中出现错误，请重试');
    }
  }
  
  // 自定义搜索实现
  function performCustomSearch(searchTerm) {
    try {
      // 在当前页面中搜索
      const markdownSection = document.querySelector('.markdown-section');
      if (!markdownSection) {
        showSearchNoResults();
        return;
      }
      
      // 获取页面文本内容
      const pageText = markdownSection.textContent.toLowerCase();
      const searchTermLower = searchTerm.toLowerCase();
      
      // 检查是否包含搜索词
      if (pageText.includes(searchTermLower)) {
        // 高亮匹配的文本
        highlightMatchingText(markdownSection, searchTermLower);
        
        // 滚动到第一个匹配项
        const firstMatch = document.querySelector(`.${CONFIG.HIGHLIGHT_CLASS}`);
        if (firstMatch) {
          firstMatch.scrollIntoView({ behavior: 'smooth', block: 'center' });
          // 为第一个匹配项添加动画效果
          firstMatch.style.animation = 'pulse 1s ease-in-out';
        }
      } else {
        // 没有找到匹配项
        showSearchNoResults();
      }
    } catch (error) {
      console.error('自定义搜索失败:', error);
      showSearchError('搜索过程中出现错误，请重试');
    }
  }
  
  // 高亮匹配的文本
  function highlightMatchingText(element, searchTerm) {
    try {
      const treeWalker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT, null, false);
      const textNodes = [];
      
      // 收集所有文本节点，但排除script和style标签
      while (treeWalker.nextNode()) {
        const parent = treeWalker.currentNode.parentNode;
        if (!parent || (!parent.closest('script') && !parent.closest('style'))) {
          textNodes.push(treeWalker.currentNode);
        }
      }
      
      // 遍历文本节点并高亮匹配的文本
      textNodes.forEach(node => {
        const text = node.textContent;
        const regex = new RegExp(`(${escapeRegExp(searchTerm)})`, 'gi');
        
        if (regex.test(text)) {
          const span = document.createElement('span');
          span.className = CONFIG.HIGHLIGHT_CLASS;
          span.innerHTML = text.replace(regex, '<mark>$1</mark>');
          node.parentNode.replaceChild(span, node);
        }
      });
    } catch (error) {
      console.error('高亮文本失败:', error);
    }
  }
  
  // 清空搜索高亮
  function clearSearchHighlights() {
    try {
      const highlights = document.querySelectorAll(`.${CONFIG.HIGHLIGHT_CLASS}`);
      highlights.forEach(highlight => {
        // 恢复原始文本
        const parent = highlight.parentNode;
        while (highlight.firstChild) {
          parent.insertBefore(highlight.firstChild, highlight);
        }
        parent.removeChild(highlight);
      });
    } catch (error) {
      console.error('清空高亮失败:', error);
    }
  }
  
  // 显示搜索无结果
  function showSearchNoResults() {
    try {
      // 检查是否已存在无结果提示
      let noResultsElement = document.querySelector('.search-no-results');
      
      if (!noResultsElement) {
        // 创建无结果提示
        noResultsElement = document.createElement('div');
        noResultsElement.className = 'search-no-results';
        noResultsElement.innerHTML = '<i class="fas fa-search"></i> 未找到相关内容，请尝试其他关键词';
        noResultsElement.style.cssText = `
          position: fixed;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          background-color: white;
          padding: 20px 30px;
          border-radius: 8px;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
          z-index: 2000;
          text-align: center;
          color: #666;
          font-size: 16px;
          display: none;
        `;
        
        // 添加到文档中
        document.body.appendChild(noResultsElement);
      }
      
      // 显示提示
      noResultsElement.style.display = 'block';
      
      // 3秒后隐藏提示
      setTimeout(() => {
        if (noResultsElement) {
          noResultsElement.style.display = 'none';
        }
      }, CONFIG.NO_RESULTS_TIMEOUT);
    } catch (error) {
      console.error('显示无结果提示失败:', error);
    }
  }
  
  // 显示搜索错误
  function showSearchError(message) {
    try {
      // 复用无结果提示元素，但更改内容
      let errorElement = document.querySelector('.search-no-results');
      
      if (!errorElement) {
        // 创建错误提示
        errorElement = document.createElement('div');
        errorElement.className = 'search-no-results';
        errorElement.style.cssText = `
          position: fixed;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          background-color: #ffebee;
          color: #c62828;
          padding: 20px 30px;
          border-radius: 8px;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
          z-index: 2000;
          text-align: center;
          font-size: 16px;
          display: none;
        `;
        
        // 添加到文档中
        document.body.appendChild(errorElement);
      }
      
      // 更新内容和样式
      errorElement.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
      errorElement.style.backgroundColor = '#ffebee';
      errorElement.style.color = '#c62828';
      
      // 显示提示
      errorElement.style.display = 'block';
      
      // 3秒后隐藏提示
      setTimeout(() => {
        if (errorElement) {
          errorElement.style.display = 'none';
        }
      }, CONFIG.NO_RESULTS_TIMEOUT);
    } catch (error) {
      console.error('显示错误提示失败:', error);
    }
  }
  
  // 生成搜索建议
  function generateSearchSuggestions(searchTerm) {
    try {
      // 模拟搜索建议数据
      const allSuggestions = [
        { text: '政策解读', category: '政策' },
        { text: '行业分析', category: '行业' },
        { text: '投资策略', category: '投资' },
        { text: '技术分析', category: '技术' },
        { text: 'AI宝藏库', category: 'AI' },
        { text: '宏观经济', category: '经济' },
        { text: '金融市场', category: '市场' },
        { text: '量化交易', category: '量化' },
        { text: '风险管理', category: '风险' },
        { text: '资产配置', category: '资产' },
        { text: '股票分析', category: '股票' },
        { text: '债券市场', category: '债券' },
        { text: '基金投资', category: '基金' },
        { text: '期货市场', category: '期货' },
        { text: '期权策略', category: '期权' },
        { text: '实时金融市场分析', category: '分析' },
        { text: '投资比例建议', category: '建议' },
        { text: '市场趋势预测', category: '预测' },
        { text: '交易策略回测', category: '回测' },
        { text: '资产负债管理', category: '管理' }
      ];
      
      // 过滤匹配的建议
      return allSuggestions.filter(suggestion => 
        suggestion.text.toLowerCase().includes(searchTerm.toLowerCase())
      );
    } catch (error) {
      console.error('生成搜索建议失败:', error);
      return [];
    }
  }
  
  // 添加到搜索历史
  function addToSearchHistory(searchTerm) {
    try {
      // 如果搜索词已存在于历史记录中，先移除它
      const index = searchHistory.indexOf(searchTerm);
      if (index > -1) {
        searchHistory.splice(index, 1);
      }
      
      // 将搜索词添加到历史记录的开头
      searchHistory.unshift(searchTerm);
      
      // 限制历史记录的大小
      if (searchHistory.length > MAX_HISTORY_SIZE) {
        searchHistory.pop();
      }
      
      // 保存到localStorage
      saveSearchHistory();
    } catch (error) {
      console.error('添加到搜索历史失败:', error);
    }
  }
  
  // 保存搜索历史到localStorage
  function saveSearchHistory() {
    try {
      localStorage.setItem('searchHistory', JSON.stringify(searchHistory));
    } catch (error) {
      console.warn('保存搜索历史失败:', error);
      // 静默失败，不影响用户体验
    }
  }
  
  // 从localStorage加载搜索历史
  function loadSearchHistory() {
    try {
      const savedHistory = localStorage.getItem('searchHistory');
      if (savedHistory) {
        searchHistory = JSON.parse(savedHistory);
        // 确保历史记录不超过最大大小
        if (searchHistory.length > MAX_HISTORY_SIZE) {
          searchHistory = searchHistory.slice(0, MAX_HISTORY_SIZE);
        }
      }
    } catch (error) {
      console.warn('加载搜索历史失败:', error);
      // 静默失败，使用空历史记录
      searchHistory = [];
    }
  }
  
  // 清除搜索历史
  function clearSearchHistory() {
    try {
      searchHistory = [];
      localStorage.removeItem('searchHistory');
    } catch (error) {
      console.error('清除搜索历史失败:', error);
    }
  }
  
  // 处理页面切换
  function handlePageChange() {
    // 延迟执行，确保页面内容已加载
    setTimeout(() => {
      try {
        // 重新初始化搜索功能以适应新页面
        initializeSearch();
        // 清空搜索高亮
        clearSearchHighlights();
        // 重置搜索输入框
        const searchInput = document.getElementById('header-search-input');
        if (searchInput) {
          searchInput.value = '';
        }
      } catch (error) {
        console.error('处理页面切换失败:', error);
      }
    }, CONFIG.INITIALIZATION_DELAY);
  }
  
  // 添加一些全局样式
  function addGlobalStyles() {
    try {
      // 检查是否已经添加了样式
      if (!document.getElementById('search-global-styles')) {
        const style = document.createElement('style');
        style.id = 'search-global-styles';
        style.textContent = `
          @keyframes pulse {
            0% {
              background-color: rgba(255, 235, 59, 0.3);
            }
            50% {
              background-color: rgba(255, 235, 59, 0.6);
            }
            100% {
              background-color: rgba(255, 235, 59, 0.3);
            }
          }
          
          .search-highlight {
            background-color: rgba(255, 235, 59, 0.3);
            border-radius: 3px;
          }
          
          .search-highlight mark {
            background-color: #ffeb3b;
            padding: 2px 4px;
            border-radius: 2px;
            font-weight: 600;
          }
          
          /* 确保搜索建议在移动端正常显示 */
          @media (max-width: 768px) {
            #search-suggestions {
              left: 50% !important;
              transform: translateX(-50%) !important;
              width: calc(100% - 40px) !important;
              max-width: 500px !important;
            }
          }
          
          /* 确保搜索区域的样式正确 */
          .search-section {
            position: relative;
          }
        `;
        document.head.appendChild(style);
      }
    } catch (error) {
      console.error('添加全局样式失败:', error);
    }
  }
  
  // 添加全局样式
  addGlobalStyles();
  
  // 初始化搜索功能
  init();
  
  // 导出全局方法，方便调试和扩展
  window.SearchFunctionality = {
    init: initializeSearch,
    performSearch: executeSearch,
    clearHighlights: clearSearchHighlights,
    clearHistory: clearSearchHistory,
    getHistory: () => [...searchHistory]
  };
})();