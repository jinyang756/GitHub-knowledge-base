/**
 * 高视觉盛宴冲击感渲染方案 - JavaScript动态效果
 * 证券行业知识库适配版
 */

// 等待DOM加载完成后执行
window.addEventListener('DOMContentLoaded', function() {
  // ===== 星空背景生成器 =====
  function createStarField() {
    const container = document.createElement('div');
    container.className = 'stars-container';
    document.body.appendChild(container);
    
    const starCount = window.innerWidth > 768 ? 200 : 100;
    
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
  }
  
  // ===== 粒子系统 =====
  function createParticleSystem() {
    // 检查是否支持Canvas
    if (!document.createElement('canvas').getContext) return;
    
    const container = document.createElement('div');
    container.className = 'particle-container';
    document.body.appendChild(container);
    
    const canvas = document.createElement('canvas');
    container.appendChild(canvas);
    const ctx = canvas.getContext('2d');
    
    // 设置Canvas尺寸
    function setCanvasSize() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    
    setCanvasSize();
    window.addEventListener('resize', setCanvasSize);
    
    // 粒子数组
    const particles = [];
    const particleCount = window.innerWidth > 768 ? 100 : 50;
    
    // 创建粒子
    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        size: Math.random() * 2 + 1,
        speedX: (Math.random() - 0.5) * 0.5,
        speedY: (Math.random() - 0.5) * 0.5,
        color: `rgba(${Math.floor(Math.random() * 6)}, ${Math.floor(Math.random() * 182) + 30}, ${Math.floor(Math.random() * 212) + 43}, ${Math.random() * 0.5 + 0.2})`,
        opacity: Math.random() * 0.5 + 0.2
      });
    }
    
    // 动画循环
    function animateParticles() {
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
        
        // 绘制粒子连线（可选，低性能设备可能需要禁用）
        if (window.innerWidth > 768) {
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
      
      requestAnimationFrame(animateParticles);
    }
    
    animateParticles();
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
    
    const regex = /([+-]?\d+(?:\.\d+)?)([%]?)/g;
    const textNodes = [];
    
    // 收集所有文本节点
    function collectTextNodes(node) {
      if (node.nodeType === Node.TEXT_NODE) {
        textNodes.push(node);
      } else {
        node.childNodes.forEach(collectTextNodes);
      }
    }
    
    collectTextNodes(content);
    
    // 处理文本节点中的数字
    textNodes.forEach(node => {
      if (node.parentElement.tagName === 'CODE' || node.parentElement.tagName === 'PRE') return;
      
      const parent = node.parentNode;
      const newParent = document.createElement('span');
      let text = node.textContent;
      
      // 替换数字为高亮元素
      let match;
      let lastIndex = 0;
      
      while ((match = regex.exec(text)) !== null) {
        // 添加匹配前的文本
        if (match.index > lastIndex) {
          newParent.appendChild(document.createTextNode(text.slice(lastIndex, match.index)));
        }
        
        const number = parseFloat(match[1]);
        const suffix = match[2];
        const span = document.createElement('span');
        
        // 根据数字正负应用不同样式
        if (number > 0 && !text.substring(match.index - 5, match.index).includes('下跌')) {
          span.className = 'data-highlight price-up';
        } else if (number < 0) {
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
      
      // 替换节点
      if (newParent.childNodes.length > 0) {
        parent.replaceChild(newParent, node);
      }
    });
  }
  
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
    let pressTimer;
    
    document.addEventListener('mousedown', function(e) {
      // 仅在数据元素上触发
      if (e.target.classList.contains('data-highlight')) {
        pressTimer = setTimeout(function() {
          createDataExplosion(e.target);
        }, 800);
      }
    });
    
    document.addEventListener('mouseup', function() {
      clearTimeout(pressTimer);
    });
    
    document.addEventListener('mouseleave', function() {
      clearTimeout(pressTimer);
    });
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
    // 检测系统暗黑模式偏好
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // 确保应用暗黑模式样式（我们的主题默认就是暗黑科技风）
    document.documentElement.classList.add('dark-mode');
    
    // 添加平滑过渡
    document.documentElement.style.transition = 'background-color 0.5s ease, color 0.5s ease';
  }
  
  // ===== 初始化所有视觉效果 =====
  function initVisualEffects() {
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
  
  // 检测性能
  const isLowPerformance = (function() {
    // 使用简单的性能检测
    const start = performance.now();
    let sum = 0;
    for (let i = 0; i < 10000; i++) {
      sum += Math.sqrt(i);
    }
    const end = performance.now();
    
    // 如果计算时间超过50ms，认为是低性能设备
    return (end - start) > 50;
  })();
  
  // 为低性能设备应用降级策略
  if (isMobile || isLowPerformance) {
    console.log('应用低性能设备视觉降级策略');
    
    // 添加低性能类标记
    document.documentElement.classList.add('low-performance');
    
    // 减少粒子数量
    const style = document.createElement('style');
    style.textContent = `
      .particle-container canvas {
        display: none;
      }
      
      .stars-container .star {
        display: none;
      }
      
      .stars-container .star:nth-child(1n+50) {
        display: block;
      }
    `;
    document.head.appendChild(style);
  }
}

// 初始化设备检测
window.addEventListener('load', detectDeviceAndOptimize);