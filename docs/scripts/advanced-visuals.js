/**
 * 高视觉盛宴冲击感渲染方案 - JavaScript动态效果
 * 证券行业知识库适配版
 */

// 性能配置 - 可通过控制面板调整
let performanceConfig = {
  particleCount: window.innerWidth > 768 ? 100 : 50,
  particleSize: window.innerWidth > 768 ? 2 : 1,
  particleSpeed: window.innerWidth > 768 ? 0.5 : 0.3,
  starCount: window.innerWidth > 768 ? 200 : 100,
  showParticles: true,
  showStars: true,
  showConnections: window.innerWidth > 768,
  dataExplosion: true,
  performanceMode: 'balanced' // high, balanced, low
};

// 节流函数
function throttle(func, limit) {
  let inThrottle;
  return function() {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// 等待DOM加载完成后执行
window.addEventListener('DOMContentLoaded', function() {
  // ===== 星空背景生成器 =====
  function createStarField() {
    if (!performanceConfig.showStars) return;
    
    const container = document.createElement('div');
    container.className = 'stars-container';
    document.body.appendChild(container);
    
    const starCount = performanceConfig.starCount;
    
    for (let i = 0; i < starCount; i++) {
      const star = document.createElement('div');
      star.className = 'star';
      
      // 随机位置
      const x = Math.random() * 100;
      const y = Math.random() * 100;
      
      // 随机大小
      const size = Math.random() * 2 + 1;
      
      // 随机动画持续时间
      const duration = Math.random() * 5 + 3;
      
      // 随机延迟
      const delay = Math.random() * 5;
      
      // 应用样式
      Object.assign(star.style, {
        left: `${x}%`,
        top: `${y}%`,
        width: `${size}px`,
        height: `${size}px`,
        '--duration': `${duration}s`,
        animationDelay: `${delay}s`,
        opacity: Math.random() * 0.6 + 0.2
      });
      
      container.appendChild(star);
    }
    
    // 保存容器引用以便后续控制
    window.starsContainer = container;
  }
  
  // ===== 粒子系统 =====
  function createParticleSystem() {
    if (!performanceConfig.showParticles) return;
    
    // 检查是否支持Canvas
    if (!document.createElement('canvas').getContext) return;
    
    const container = document.createElement('div');
    container.className = 'particle-container';
    document.body.appendChild(container);
    
    const canvas = document.createElement('canvas');
    container.appendChild(canvas);
    const ctx = canvas.getContext('2d');
    
    // 设置Canvas尺寸
    const setCanvasSize = throttle(function() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }, 200);
    
    setCanvasSize();
    window.addEventListener('resize', setCanvasSize);
    
    // 粒子数组
    const particles = [];
    const particleCount = performanceConfig.particleCount;
    const particleSize = performanceConfig.particleSize;
    const particleSpeed = performanceConfig.particleSpeed;
    
    // 创建粒子
    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        size: Math.random() * particleSize + 0.5,
        speedX: (Math.random() - 0.5) * particleSpeed,
        speedY: (Math.random() - 0.5) * particleSpeed,
        color: `rgba(${Math.floor(Math.random() * 6)}, ${Math.floor(Math.random() * 182) + 30}, ${Math.floor(Math.random() * 212) + 43}, ${Math.random() * 0.5 + 0.2})`,
        opacity: Math.random() * 0.5 + 0.2
      });
    }
    
    // 动画循环
    let frameCount = 0;
    let lastTime = 0;
    let fps = 60;
    
    function animateParticles(timestamp) {
      // 根据性能模式调整帧率
      if (performanceConfig.performanceMode === 'low' && frameCount % 2 !== 0) {
        frameCount++;
        requestAnimationFrame(animateParticles);
        return;
      }
      
      // 计算FPS
      if (timestamp) {
        const deltaTime = timestamp - lastTime;
        fps = Math.round(1000 / deltaTime);
        lastTime = timestamp;
      }
      
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      particles.forEach(particle => {
        // 更新位置
        particle.x += particle.speedX;
        particle.y += particle.speedY;
        
        // 边界检查
        if (particle.x < 0 || particle.x > canvas.width) particle.speedX *= -1;
        if (particle.y < 0 || particle.y > canvas.height) particle.speedY *= -1;
        
        // 绘制粒子
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
        ctx.fillStyle = particle.color;
        ctx.fill();
        
        // 绘制粒子连线（根据配置决定是否启用）
        if (performanceConfig.showConnections) {
          particles.forEach(otherParticle => {
            const dx = particle.x - otherParticle.x;
            const dy = particle.y - otherParticle.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < 100) {
              ctx.beginPath();
              ctx.strokeStyle = `rgba(6, 182, 212, ${(100 - distance) / 1000})`;
              ctx.lineWidth = 0.5;
              ctx.moveTo(particle.x, particle.y);
              ctx.lineTo(otherParticle.x, otherParticle.y);
              ctx.stroke();
            }
          });
        }
      });
      
      frameCount++;
      requestAnimationFrame(animateParticles);
    }
    
    animateParticles();
    
    // 保存引用以便后续控制
    window.particleContainer = container;
    window.particles = particles;
    window.particleCanvas = canvas;
  }
  
  // ===== 视差滚动效果 =====
  function createParallaxEffect() {
    const starsContainer = document.querySelector('.stars-container');
    const particleContainer = document.querySelector('.particle-container');
    
    if (!starsContainer || !particleContainer) return;
    
    window.addEventListener('scroll', function() {
      const scrollY = window.pageYOffset;
      
      // 不同元素以不同速率移动，创建视差效果
      starsContainer.style.transform = `translateY(${scrollY * 0.05}px)`;
      particleContainer.style.transform = `translateY(${scrollY * 0.1}px)`;
    });
  }
  
  // ===== 动态数据高亮 =====
  function enhanceDataDisplay() {
    // 为数字和百分比添加动态高亮
    const content = document.querySelector('.content');
    if (!content) return;
    
    // 精确匹配数据数字的正则表达式，排除日期、页码等
    const regex = /([+-]?\d+(?:\.\d+)?)([%]?)/g;
    const textNodes = [];
    
    // 需要排除的元素类型
    const excludeTags = ['CODE', 'PRE', 'TIME', 'A', 'BUTTON', 'INPUT', 'SELECT', 'TEXTAREA'];
    const excludeClasses = ['no-highlight', 'pagination', 'date', 'time'];
    
    // 收集所有文本节点
    function collectTextNodes(node) {
      if (node.nodeType === Node.TEXT_NODE) {
        // 检查父元素是否需要排除
        let shouldExclude = false;
        let current = node.parentElement;
        
        while (current && current !== content) {
          if (excludeTags.includes(current.tagName)) {
            shouldExclude = true;
            break;
          }
          
          for (const cls of excludeClasses) {
            if (current.classList.contains(cls)) {
              shouldExclude = true;
              break;
            }
          }
          
          if (shouldExclude) break;
          current = current.parentElement;
        }
        
        if (!shouldExclude) {
          textNodes.push(node);
        }
      } else {
        node.childNodes.forEach(collectTextNodes);
      }
    }
    
    collectTextNodes(content);
    
    // 使用文档碎片提高性能
    const fragment = document.createDocumentFragment();
    
    // 处理文本节点中的数字
    textNodes.forEach(node => {
      const parent = node.parentNode;
      const newParent = document.createElement('span');
      let text = node.textContent;
      
      // 跳过空文本节点
      if (!text.trim()) return;
      
      // 替换数字为高亮元素
      let match;
      let lastIndex = 0;
      let hasMatches = false;
      
      while ((match = regex.exec(text)) !== null) {
        hasMatches = true;
        
        // 添加匹配前的文本
        if (match.index > lastIndex) {
          newParent.appendChild(document.createTextNode(text.slice(lastIndex, match.index)));
        }
        
        const number = parseFloat(match[1]);
        const suffix = match[2];
        const span = document.createElement('span');
        
        // 检查上下文，避免误判
        const context = text.substring(Math.max(0, match.index - 15), Math.min(text.length, match.index + 15)).toLowerCase();
        
        // 根据数字正负应用不同样式
        if (number > 0 && !context.includes('下跌') && !context.includes('减少') && !context.includes('降低')) {
          span.className = 'data-highlight price-up';
        } else if (number < 0 || context.includes('下跌') || context.includes('减少') || context.includes('降低')) {
          span.className = 'data-highlight price-down';
        } else {
          span.className = 'data-highlight';
        }
        
        span.textContent = match[0];
        newParent.appendChild(span);
        lastIndex = regex.lastIndex;
      }
      
      // 添加剩余文本
      if (lastIndex < text.length) {
        newParent.appendChild(document.createTextNode(text.slice(lastIndex)));
      }
      
      // 仅在有匹配项时替换节点
      if (hasMatches && newParent.childNodes.length > 0) {
        parent.replaceChild(newParent, node);
      }
    });
  }
  
  // 将函数暴露到全局以便其他地方调用
  window.enhanceDataDisplay = enhanceDataDisplay;
  
  // ===== 页面滚动动画 =====
  function animateOnScroll() {
    const elements = document.querySelectorAll('.holo-card, h1, h2, h3');
    
    function checkInView() {
      elements.forEach(element => {
        const bounding = element.getBoundingClientRect();
        const isVisible = bounding.top < window.innerHeight * 0.8 && bounding.bottom > 0;
        
        if (isVisible && !element.classList.contains('animate-in')) {
          element.classList.add('animate-in');
          element.style.opacity = '0';
          element.style.transform = 'translateY(20px)';
          element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
          
          // 使用setTimeout确保样式生效后再开始动画
          setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
          }, 10);
        }
      });
    }
    
    // 初始检查
    checkInView();
    
    // 滚动时检查
    window.addEventListener('scroll', checkInView);
  }
  
  // ===== 数据穿透交互（长按效果）=====
  function enableDataPenetration() {
    if (!performanceConfig.dataExplosion) return;
    
    let pressTimer;
    
    // 使用节流函数减少事件触发频率
    const handleMouseDown = throttle(function(e) {
      // 仅在数据元素上触发
      if (e.target.classList.contains('data-highlight')) {
        pressTimer = setTimeout(function() {
          createDataExplosion(e.target);
        }, 800);
      }
    }, 100);
    
    const handleMouseUp = function() {
      clearTimeout(pressTimer);
    };
    
    document.addEventListener('mousedown', handleMouseDown);
    document.addEventListener('mouseup', handleMouseUp);
    document.addEventListener('mouseleave', handleMouseUp);
  }
  
  // 创建数据爆炸效果
  function createDataExplosion(element) {
    if (!element) return;
    
    const rect = element.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    const explosion = document.createElement('div');
    explosion.className = 'data-explosion';
    
    Object.assign(explosion.style, {
      position: 'fixed',
      left: `${centerX}px`,
      top: `${centerY}px`,
      width: '0',
      height: '0',
      background: 'rgba(6, 182, 212, 0.3)',
      borderRadius: '50%',
      pointerEvents: 'none',
      zIndex: '1000'
    });
    
    document.body.appendChild(explosion);
    
    // 动画效果
    setTimeout(() => {
      Object.assign(explosion.style, {
        width: '100px',
        height: '100px',
        left: `${centerX - 50}px`,
        top: `${centerY - 50}px`,
        opacity: '0',
        transition: 'all 0.6s ease-out'
      });
    }, 10);
    
    // 移除元素
    setTimeout(() => {
      document.body.removeChild(explosion);
    }, 700);
  }
  
  // ===== 暗黑模式切换增强 =====
  function enhanceDarkModeTransition() {
    // 从localStorage读取用户偏好
    const savedMode = localStorage.getItem('darkMode');
    let isDarkMode;
    
    // 检测系统暗黑模式偏好
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // 决定初始模式
    if (savedMode !== null) {
      isDarkMode = savedMode === 'true';
    } else {
      isDarkMode = prefersDark;
    }
    
    // 应用初始模式
    if (isDarkMode) {
      document.documentElement.classList.add('dark-mode');
    } else {
      document.documentElement.classList.remove('dark-mode');
    }
    
    // 添加平滑过渡
    document.documentElement.style.transition = 'background-color 0.5s ease, color 0.5s ease';
    
    // 创建暗黑模式切换按钮
    createDarkModeToggle();
    
    // 监听系统模式变化
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
      if (localStorage.getItem('darkMode') === null) {
        // 只有在用户没有明确设置时才跟随系统变化
        if (e.matches) {
          document.documentElement.classList.add('dark-mode');
        } else {
          document.documentElement.classList.remove('dark-mode');
        }
      }
    });
  }
  
  // 创建暗黑模式切换按钮
  function createDarkModeToggle() {
    const toggle = document.createElement('button');
    toggle.className = 'dark-mode-toggle';
    toggle.title = '切换暗黑模式';
    toggle.innerHTML = document.documentElement.classList.contains('dark-mode') ? '🌞' : '🌙';
    
    // 添加样式
    Object.assign(toggle.style, {
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      width: '40px',
      height: '40px',
      borderRadius: '50%',
      background: 'rgba(6, 182, 212, 0.2)',
      border: '1px solid rgba(6, 182, 212, 0.5)',
      color: '#06b6d4',
      fontSize: '20px',
      cursor: 'pointer',
      zIndex: '1000',
      transition: 'all 0.3s ease'
    });
    
    // 添加悬停效果
    toggle.addEventListener('mouseenter', function() {
      this.style.background = 'rgba(6, 182, 212, 0.3)';
      this.style.transform = 'scale(1.1)';
    });
    
    toggle.addEventListener('mouseleave', function() {
      this.style.background = 'rgba(6, 182, 212, 0.2)';
      this.style.transform = 'scale(1)';
    });
    
    // 添加点击事件
    toggle.addEventListener('click', function() {
      const isDark = document.documentElement.classList.toggle('dark-mode');
      this.innerHTML = isDark ? '🌞' : '🌙';
      
      // 保存用户偏好
      localStorage.setItem('darkMode', isDark);
    });
    
    document.body.appendChild(toggle);
  }
  
  // ===== 创建视觉效果控制面板 =====
  function createVisualControlPanel() {
    const panel = document.createElement('div');
    panel.className = 'visual-control-panel';
    panel.style.display = 'none'; // 默认隐藏
    
    // 添加样式
    Object.assign(panel.style, {
      position: 'fixed',
      top: '20px',
      right: '20px',
      background: 'rgba(15, 23, 42, 0.95)',
      border: '1px solid rgba(6, 182, 212, 0.3)',
      borderRadius: '8px',
      padding: '15px',
      color: '#e2e8f0',
      fontSize: '14px',
      zIndex: '1001',
      boxShadow: '0 0 15px rgba(6, 182, 212, 0.1)',
      backdropFilter: 'blur(10px)',
      maxWidth: '300px'
    });
    
    // 添加标题
    const title = document.createElement('h3');
    title.textContent = '视觉效果控制';
    title.style.margin = '0 0 15px 0';
    title.style.color = '#06b6d4';
    title.style.fontSize = '16px';
    panel.appendChild(title);
    
    // 创建性能模式选择器
    const perfModeContainer = document.createElement('div');
    perfModeContainer.style.marginBottom = '15px';
    
    const perfModeLabel = document.createElement('label');
    perfModeLabel.textContent = '性能模式：';
    perfModeLabel.style.display = 'block';
    perfModeLabel.style.marginBottom = '5px';
    
    const perfModeSelect = document.createElement('select');
    perfModeSelect.value = performanceConfig.performanceMode;
    
    const modes = [
      { value: 'high', text: '高性能' },
      { value: 'balanced', text: '平衡' },
      { value: 'low', text: '低性能' }
    ];
    
    modes.forEach(mode => {
      const option = document.createElement('option');
      option.value = mode.value;
      option.textContent = mode.text;
      perfModeSelect.appendChild(option);
    });
    
    perfModeSelect.style.width = '100%';
    perfModeSelect.style.padding = '5px';
    perfModeSelect.style.background = 'rgba(30, 41, 59, 0.8)';
    perfModeSelect.style.border = '1px solid rgba(6, 182, 212, 0.3)';
    perfModeSelect.style.borderRadius = '4px';
    perfModeSelect.style.color = '#e2e8f0';
    
    perfModeSelect.addEventListener('change', function() {
      performanceConfig.performanceMode = this.value;
      applyPerformanceSettings();
    });
    
    perfModeContainer.appendChild(perfModeLabel);
    perfModeContainer.appendChild(perfModeSelect);
    panel.appendChild(perfModeContainer);
    
    // 创建开关选项
    const createToggle = function(labelText, property) {
      const container = document.createElement('div');
      container.style.marginBottom = '10px';
      container.style.display = 'flex';
      container.style.justifyContent = 'space-between';
      container.style.alignItems = 'center';
      
      const label = document.createElement('label');
      label.textContent = labelText;
      label.style.cursor = 'pointer';
      
      const toggle = document.createElement('input');
      toggle.type = 'checkbox';
      toggle.checked = performanceConfig[property];
      
      toggle.style.cursor = 'pointer';
      toggle.style.accentColor = '#06b6d4';
      
      toggle.addEventListener('change', function() {
        performanceConfig[property] = this.checked;
        applyVisualSettings();
      });
      
      container.appendChild(label);
      container.appendChild(toggle);
      return container;
    };
    
    panel.appendChild(createToggle('显示粒子系统', 'showParticles'));
    panel.appendChild(createToggle('显示星空背景', 'showStars'));
    panel.appendChild(createToggle('显示粒子连线', 'showConnections'));
    panel.appendChild(createToggle('数据爆炸效果', 'dataExplosion'));
    
    // 添加重置按钮
    const resetBtn = document.createElement('button');
    resetBtn.textContent = '重置为默认设置';
    resetBtn.style.width = '100%';
    resetBtn.style.marginTop = '10px';
    resetBtn.style.padding = '8px';
    resetBtn.style.background = 'rgba(6, 182, 212, 0.1)';
    resetBtn.style.border = '1px solid rgba(6, 182, 212, 0.3)';
    resetBtn.style.borderRadius = '4px';
    resetBtn.style.color = '#06b6d4';
    resetBtn.style.cursor = 'pointer';
    resetBtn.style.transition = 'all 0.3s ease';
    
    resetBtn.addEventListener('mouseenter', function() {
      this.style.background = 'rgba(6, 182, 212, 0.2)';
    });
    
    resetBtn.addEventListener('mouseleave', function() {
      this.style.background = 'rgba(6, 182, 212, 0.1)';
    });
    
    resetBtn.addEventListener('click', function() {
      performanceConfig = {
        particleCount: window.innerWidth > 768 ? 100 : 50,
        particleSize: window.innerWidth > 768 ? 2 : 1,
        particleSpeed: window.innerWidth > 768 ? 0.5 : 0.3,
        starCount: window.innerWidth > 768 ? 200 : 100,
        showParticles: true,
        showStars: true,
        showConnections: window.innerWidth > 768,
        dataExplosion: true,
        performanceMode: 'balanced'
      };
      
      // 重新渲染控制面板
      document.body.removeChild(panel);
      document.body.removeChild(controlBtn);
      createVisualControlPanel();
      
      // 应用设置
      applyVisualSettings();
      applyPerformanceSettings();
    });
    
    panel.appendChild(resetBtn);
    
    document.body.appendChild(panel);
    
    // 创建控制面板切换按钮
    const controlBtn = document.createElement('button');
    controlBtn.className = 'control-panel-toggle';
    controlBtn.title = '显示视觉效果控制面板';
    controlBtn.innerHTML = '🎛️';
    
    Object.assign(controlBtn.style, {
      position: 'fixed',
      top: '20px',
      right: '20px',
      width: '40px',
      height: '40px',
      borderRadius: '50%',
      background: 'rgba(6, 182, 212, 0.2)',
      border: '1px solid rgba(6, 182, 212, 0.5)',
      color: '#06b6d4',
      fontSize: '20px',
      cursor: 'pointer',
      zIndex: '1002',
      transition: 'all 0.3s ease'
    });
    
    controlBtn.addEventListener('mouseenter', function() {
      this.style.background = 'rgba(6, 182, 212, 0.3)';
      this.style.transform = 'scale(1.1)';
    });
    
    controlBtn.addEventListener('mouseleave', function() {
      this.style.background = 'rgba(6, 182, 212, 0.2)';
      this.style.transform = 'scale(1)';
    });
    
    controlBtn.addEventListener('click', function() {
      panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
    });
    
    document.body.appendChild(controlBtn);
  }
  
  // 应用视觉设置
  function applyVisualSettings() {
    // 控制星空显示
    if (window.starsContainer) {
      window.starsContainer.style.display = performanceConfig.showStars ? 'block' : 'none';
    }
    
    // 控制粒子系统显示
    if (window.particleContainer) {
      window.particleContainer.style.display = performanceConfig.showParticles ? 'block' : 'none';
    }
  }
  
  // 应用性能设置
  function applyPerformanceSettings() {
    // 根据性能模式调整配置
    switch (performanceConfig.performanceMode) {
      case 'high':
        performanceConfig.particleCount = window.innerWidth > 768 ? 150 : 75;
        performanceConfig.particleSize = 2;
        performanceConfig.particleSpeed = 0.6;
        performanceConfig.showConnections = true;
        break;
      case 'balanced':
        performanceConfig.particleCount = window.innerWidth > 768 ? 100 : 50;
        performanceConfig.particleSize = 1.5;
        performanceConfig.particleSpeed = 0.4;
        performanceConfig.showConnections = window.innerWidth > 768;
        break;
      case 'low':
        performanceConfig.particleCount = window.innerWidth > 768 ? 50 : 25;
        performanceConfig.particleSize = 1;
        performanceConfig.particleSpeed = 0.2;
        performanceConfig.showConnections = false;
        break;
    }
    
    // 如果已经初始化了粒子系统，可以考虑重建粒子
  }
  
  // ===== 初始化所有视觉效果 =====
  function initVisualEffects() {
    // 先进行设备检测和性能优化
    detectDeviceAndOptimize();
    
    // 创建星空背景
    createStarField();
    
    // 创建粒子系统
    createParticleSystem();
    
    // 创建视差滚动效果
    createParallaxEffect();
    
    // 增强数据显示
    enhanceDataDisplay();
    
    // 页面滚动动画
    animateOnScroll();
    
    // 数据穿透交互
    enableDataPenetration();
    
    // 暗黑模式过渡增强
    enhanceDarkModeTransition();
    
    // 创建视觉效果控制面板
    createVisualControlPanel();
    
    // 添加Orbitron字体（用于标题）
    const fontLink = document.createElement('link');
    fontLink.href = 'https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&display=swap';
    fontLink.rel = 'stylesheet';
    document.head.appendChild(fontLink);
  }
  
  // 启动视觉效果
  initVisualEffects();
});

// ===== 页面切换动画 =====
(function() {
  // 监听docsify的页面切换事件
  if (window.$docsify) {
    window.$docsify.plugins.push(function(hook) {
      // 页面加载前
      hook.beforeEach(function(html) {
        // 添加全息卡片样式到内容块
        html = html.replace(/<div class="content">/g, '<div class="content holo-card">');
        
        // 为标题添加轨道装饰
        html = html.replace(/<h1([^>]*)>/g, '<h1$1 class="track-decoration">');
        html = html.replace(/<h2([^>]*)>/g, '<h2$1 class="track-decoration">');
        
        return html;
      });
      
      // 页面加载完成后
      hook.afterEach(function(html) {
        // 增强数据显示
        setTimeout(() => {
          if (window.enhanceDataDisplay) {
            window.enhanceDataDisplay();
          }
        }, 100);
        
        return html;
      });
    });
  }
})();

// ===== 性能优化：设备检测与降级策略 =====
function detectDeviceAndOptimize() {
  // 检测移动设备
  const isMobile = window.innerWidth <= 768;
  
  // 检测性能 - 使用更准确的方法
  const isLowPerformance = (function() {
    try {
      // 使用更准确的性能检测
      const start = performance.now();
      let sum = 0;
      for (let i = 0; i < 10000; i++) {
        sum += Math.sqrt(i);
        sum = Math.sin(sum); // 增加计算复杂度
      }
      const end = performance.now();
      
      // 考虑设备类型调整阈值
      const threshold = isMobile ? 30 : 50;
      return (end - start) > threshold;
    } catch (e) {
      // 如果性能API不可用，默认认为是低性能设备
      return true;
    }
  })();
  
  // 为低性能设备应用降级策略
  if (isMobile || isLowPerformance) {
    console.log('应用低性能设备视觉降级策略');
    
    // 添加低性能类标记
    document.documentElement.classList.add('low-performance');
    
    // 自动调整性能配置
    performanceConfig.performanceMode = 'low';
    performanceConfig.particleCount = isMobile ? 25 : 50;
    performanceConfig.showConnections = false;
    
    // 减少视觉效果
    const style = document.createElement('style');
    style.textContent = `
      .low-performance .particle-container canvas {
        opacity: 0.5;
      }
      
      .low-performance .stars-container .star {
        opacity: 0.3;
      }
    `;
    document.head.appendChild(style);
  }
}

// 初始化设备检测
window.addEventListener('load', detectDeviceAndOptimize);