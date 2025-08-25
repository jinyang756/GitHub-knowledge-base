/**
 * 高视觉盛宴冲击感渲染方案 - 画面优化增强模块
 * 证券行业知识库适配版
 */

// 等待DOM加载完成后执行
window.addEventListener('DOMContentLoaded', function() {
  // ===== 1. 高级性能监控与自适应渲染 =====
  function initPerformanceMonitor() {
    // 性能监控配置
    const perfConfig = {
      // 性能模式切换阈值（包含缓冲区域以避免频繁切换）
      highToMediumThreshold: 45, // 从高性能降到中性能的阈值
      mediumToHighThreshold: 55, // 从中性能升到高性能的阈值
      mediumToLowThreshold: 25,  // 从中性能降到低性能的阈值
      lowToMediumThreshold: 35   // 从低性能升到中性能的阈值
    };
    
    // 性能监控器 - 增强版
    const perfMonitor = {
      frameCount: 0,
      lastTime: performance.now(),
      currentFps: 60,
      smoothedFps: 60, // 平滑后的FPS值
      fpsHistory: [],  // 存储最近的FPS值
      historyLength: 5, // 历史记录长度
      lastMode: 'high', // 上一次的性能模式
      interactionDetected: false, // 是否检测到用户交互
      interactionTimeout: null, // 交互超时定时器
      
      // 记录用户交互
      recordInteraction() {
        this.interactionDetected = true;
        
        // 清除之前的超时
        if (this.interactionTimeout) {
          clearTimeout(this.interactionTimeout);
        }
        
        // 3秒后重置交互标记
        this.interactionTimeout = setTimeout(() => {
          this.interactionDetected = false;
        }, 3000);
      },
      
      update() {
        const now = performance.now();
        this.frameCount++;
        
        // 每秒计算一次FPS
        if (now - this.lastTime >= 1000) {
          this.currentFps = this.frameCount;
          this.frameCount = 0;
          this.lastTime = now;
          
          // 添加到历史记录并保持固定长度
          this.fpsHistory.push(this.currentFps);
          if (this.fpsHistory.length > this.historyLength) {
            this.fpsHistory.shift();
          }
          
          // 计算平滑FPS（排除最高和最低值后的平均值）
          this.calculateSmoothedFps();
          
          // 根据平滑后的FPS调整效果
          this.adjustEffectsBasedOnPerformance();
        }
      },
      
      // 计算平滑后的FPS值（排除极端值）
      calculateSmoothedFps() {
        if (this.fpsHistory.length === 0) return;
        
        // 创建副本并排序
        const sortedHistory = [...this.fpsHistory].sort((a, b) => a - b);
        
        // 排除最高和最低值（如果有足够的数据点）
        let trimmedHistory = sortedHistory;
        if (sortedHistory.length > 3) {
          trimmedHistory = sortedHistory.slice(1, -1);
        }
        
        // 计算平均值
        const sum = trimmedHistory.reduce((acc, val) => acc + val, 0);
        this.smoothedFps = Math.round(sum / trimmedHistory.length);
      },
      
      adjustEffectsBasedOnPerformance() {
        // 在用户交互期间不进行模式切换
        if (this.interactionDetected) {
          return;
        }
        
        const body = document.body;
        let newMode = this.lastMode;
        
        // 根据平滑后的FPS和当前模式决定新模式（加入滞后效应避免频繁切换）
        if (this.lastMode === 'high' && this.smoothedFps <= perfConfig.highToMediumThreshold) {
          newMode = 'medium';
        } else if (this.lastMode === 'medium' && this.smoothedFps >= perfConfig.mediumToHighThreshold) {
          newMode = 'high';
        } else if (this.lastMode === 'medium' && this.smoothedFps <= perfConfig.mediumToLowThreshold) {
          newMode = 'low';
        } else if (this.lastMode === 'low' && this.smoothedFps >= perfConfig.lowToMediumThreshold) {
          newMode = 'medium';
        }
        
        // 只有当模式发生变化时才更新
        if (newMode !== this.lastMode) {
          // 移除所有模式类
          body.classList.remove('high-performance', 'medium-performance', 'low-performance');
          
          // 添加新模式类
          if (newMode === 'high') {
            body.classList.add('high-performance');
          } else if (newMode === 'medium') {
            body.classList.add('medium-performance');
          } else if (newMode === 'low') {
            body.classList.add('low-performance');
          }
          
          this.lastMode = newMode;
        }
      }
    };
    
    // 添加用户交互监听
    ['mousedown', 'mousemove', 'keydown', 'touchstart', 'wheel'].forEach(eventType => {
      window.addEventListener(eventType, () => {
        perfMonitor.recordInteraction();
      }, { passive: true });
    });
    
    // 将性能监控集成到动画循环 - 使用requestAnimationFrame的时间戳
    function monitorLoop(timestamp) {
      perfMonitor.update();
      requestAnimationFrame(monitorLoop);
    }
    
    // 启动性能监控
    requestAnimationFrame(monitorLoop);
    window.perfMonitor = perfMonitor;
  }
  
  // ===== 2. 增强型粒子系统 =====
  function enhanceParticleSystem() {
    // 检查是否已存在粒子系统容器
    const existingContainer = document.querySelector('.particle-container');
    if (!existingContainer) return;
    
    const canvas = existingContainer.querySelector('canvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // 保存原始粒子系统引用
    const originalAnimateParticles = window.originalAnimateParticles || function() {};
    window.originalAnimateParticles = originalAnimateParticles;
    
    // 创建增强的粒子系统
    const enhancedParticles = [];
    const enhancedParticleCount = Math.floor(window.innerWidth / 100);
    
    // 初始化增强粒子
    for (let i = 0; i < enhancedParticleCount; i++) {
      enhancedParticles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        size: Math.random() * 3 + 2,
        speedX: (Math.random() - 0.5) * 0.3,
        speedY: (Math.random() - 0.5) * 0.3,
        color: `rgba(6, 182, 212, ${Math.random() * 0.3 + 0.1})`,
        opacity: Math.random() * 0.3 + 0.1,
        pulseRate: Math.random() * 2 + 1
      });
    }
    
    // 增强的粒子动画循环
    function enhancedAnimateParticles() {
      // 仅在高性能模式下运行增强粒子系统
      if (document.body.classList.contains('high-performance') || document.body.classList.contains('medium-performance')) {
        enhancedParticles.forEach((particle, index) => {
          // 更新位置
          particle.x += particle.speedX;
          particle.y += particle.speedY;
          
          // 边界检查与循环
          if (particle.x < 0) particle.x = canvas.width;
          else if (particle.x > canvas.width) particle.x = 0;
          
          if (particle.y < 0) particle.y = canvas.height;
          else if (particle.y > canvas.height) particle.y = 0;
          
          // 脉冲效果
          const pulseFactor = (Math.sin(Date.now() * 0.001 * particle.pulseRate) + 1) * 0.5;
          const currentSize = particle.size * (0.8 + pulseFactor * 0.4);
          const currentOpacity = particle.opacity * (0.6 + pulseFactor * 0.4);
          
          // 绘制粒子光晕
          ctx.beginPath();
          ctx.arc(particle.x, particle.y, currentSize * 3, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(6, 182, 212, ${currentOpacity * 0.1})`;
          ctx.fill();
          
          // 绘制粒子核心
          ctx.beginPath();
          ctx.arc(particle.x, particle.y, currentSize, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(6, 182, 212, ${currentOpacity})`;
          ctx.fill();
        });
      }
      
      requestAnimationFrame(enhancedAnimateParticles);
    }
    
    enhancedAnimateParticles();
  }
  
  // ===== 3. 动态背景元素 =====
  function createDynamicBackgroundElements() {
    // 创建大型背景光晕
    function createBackgroundGlows() {
      const container = document.createElement('div');
      container.className = 'background-glows';
      document.body.appendChild(container);
      
      const glowCount = 3;
      const colors = [
        'rgba(37, 99, 235, 0.1)',  // 深蓝色
        'rgba(6, 182, 212, 0.08)', // 青色
        'rgba(52, 211, 153, 0.05)'  // 绿色
      ];
      
      for (let i = 0; i < glowCount; i++) {
        const glow = document.createElement('div');
        glow.className = 'background-glow';
        
        const size = 400 + Math.random() * 300;
        const x = Math.random() * 100;
        const y = Math.random() * 100;
        const duration = 20 + Math.random() * 30;
        
        Object.assign(glow.style, {
          width: `${size}px`,
          height: `${size}px`,
          left: `${x}%`,
          top: `${y}%`,
          backgroundColor: colors[i % colors.length],
          '--duration': `${duration}s`,
          animationDelay: `${Math.random() * 5}s`
        });
        
        container.appendChild(glow);
      }
    }
    
    createBackgroundGlows();
  }
  
  // ===== 4. 内容区域光效增强 =====
  function enhanceContentLighting() {
    const content = document.querySelector('.content');
    if (!content) return;
    
    // 添加全局光源效果
    function createContentGlow() {
      const glow = document.createElement('div');
      glow.className = 'content-glow';
      content.parentNode.insertBefore(glow, content.nextSibling);
    }
    
    createContentGlow();
    
    // 为卡片添加动态边缘照明
    function addDynamicEdgeLighting() {
      const cards = document.querySelectorAll('.holo-card');
      
      cards.forEach(card => {
        // 添加左边缘光
        const leftEdge = document.createElement('div');
        leftEdge.className = 'dynamic-edge left-edge';
        card.appendChild(leftEdge);
        
        // 添加右边缘光
        const rightEdge = document.createElement('div');
        rightEdge.className = 'dynamic-edge right-edge';
        card.appendChild(rightEdge);
        
        // 添加鼠标跟踪效果
        card.addEventListener('mousemove', function(e) {
          const rect = card.getBoundingClientRect();
          const x = e.clientX - rect.left;
          const y = e.clientY - rect.top;
          const xPercent = x / rect.width;
          const yPercent = y / rect.height;
          
          // 根据鼠标位置调整边缘光强度
          leftEdge.style.opacity = (1 - xPercent) * 0.5;
          rightEdge.style.opacity = xPercent * 0.5;
        });
        
        // 鼠标离开时重置
        card.addEventListener('mouseleave', function() {
          leftEdge.style.opacity = '0';
          rightEdge.style.opacity = '0';
        });
      });
    }
    
    addDynamicEdgeLighting();
  }
  
  // ===== 5. 文字深度与锐度增强 =====
  function enhanceTextRendering() {
    // 添加字体平滑与文本阴影增强
    const style = document.createElement('style');
    style.textContent = `
      body {
        text-rendering: optimizeLegibility;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
      }
      
      .markdown-section p,
      .markdown-section li {
        text-shadow: 0 0 1px rgba(226, 232, 240, 0.2);
      }
    `;
    document.head.appendChild(style);
  }
  
  // ===== 6. 高级视差滚动系统 =====
  function createAdvancedParallax() {
    // 收集所有视差元素
    const parallaxLayers = [
      { element: '.stars-container', speed: 0.03 },
      { element: '.particle-container', speed: 0.07 },
      { element: '.background-glows', speed: 0.02 },
      { element: '.content', speed: 0.01 }
    ];
    
    // 视差滚动处理函数
    function handleParallax() {
      const scrollY = window.pageYOffset;
      
      parallaxLayers.forEach(layer => {
        const element = document.querySelector(layer.element);
        if (element) {
          const translateY = scrollY * layer.speed;
          element.style.transform = `translateY(${translateY}px)`;
        }
      });
    }
    
    // 添加滚动事件监听
    window.addEventListener('scroll', handleParallax);
    
    // 初始调用
    handleParallax();
  }
  
  // ===== 7. 交互式数据可视化增强 =====
  function enhanceDataVisualization() {
    // 为数据表格添加悬停效果
    function enhanceTables() {
      const tables = document.querySelectorAll('.markdown-section table');
      
      tables.forEach(table => {
        const rows = table.querySelectorAll('tr');
        
        rows.forEach(row => {
          const cells = row.querySelectorAll('td, th');
          
          row.addEventListener('mouseenter', function() {
            cells.forEach(cell => {
              if (cell.textContent.match(/[+-]?\d+(?:\.\d+)?[%]?/)) {
                cell.classList.add('data-hover');
              }
            });
          });
          
          row.addEventListener('mouseleave', function() {
            cells.forEach(cell => {
              cell.classList.remove('data-hover');
            });
          });
        });
      });
    }
    
    enhanceTables();
    
    // 为代码块添加复制按钮效果
    function enhanceCodeBlocks() {
      const codeBlocks = document.querySelectorAll('.markdown-section pre');
      
      codeBlocks.forEach(block => {
        block.addEventListener('mouseenter', function() {
          this.classList.add('code-block-hover');
        });
        
        block.addEventListener('mouseleave', function() {
          this.classList.remove('code-block-hover');
        });
      });
    }
    
    enhanceCodeBlocks();
  }
  
  // ===== 8. 初始化所有优化效果 =====
  function initVisualEnhancements() {
    // 初始化性能监控
    initPerformanceMonitor();
    
    // 增强粒子系统
    enhanceParticleSystem();
    
    // 创建动态背景元素
    createDynamicBackgroundElements();
    
    // 增强内容区域光效
    enhanceContentLighting();
    
    // 增强文字渲染
    enhanceTextRendering();
    
    // 创建高级视差滚动
    createAdvancedParallax();
    
    // 增强数据可视化
    enhanceDataVisualization();
  }
  
  // 启动视觉优化增强
  initVisualEnhancements();
});