// 暗域访问控制脚本

/**
 * 检查是否已通过暗域验证
 * @returns {boolean} 是否已验证
 */
function isDarkDomainVerified() {
  return localStorage.getItem('darkDomainVerified') === 'true';
}

/**
 * 验证暗域访问密码
 * @param {string} password 用户输入的密码
 * @returns {Object} 验证结果
 */
function verifyDarkDomainPassword(password) {
  password = password.trim().toLowerCase();
  
  // 验证暗号
  if (password === '金阳' || password === 'jinyang') {
    // 验证成功
    localStorage.setItem('darkDomainVerified', 'true');
    
    return {
      success: true,
      message: '验证成功'
    };
  } else {
    // 验证失败，只做简单提示
    return {
      success: false,
      message: '验证失败，请重试'
    };
  }
}

/**
 * 创建暗域访问界面
 * @param {string} containerId 容器ID
 * @param {Function} onVerifySuccess 验证成功回调
 */
function createDarkDomainAccess(containerId, onVerifySuccess) {
  const container = document.getElementById(containerId);
  if (!container) return;
  
  // 检查是否已验证
  if (isDarkDomainVerified()) {
    onVerifySuccess();
    return;
  }
  
  // 创建锁界面
  const lockHtml = `
    <div id="${containerId}-lock" style="text-align: center; padding: 50px 20px;">
      <h3 style="color: #9ca3af;">访问受限区域</h3>
      <p style="color: #d1d5db; margin: 20px 0;">请输入访问暗号以继续</p>
      <input type="password" id="${containerId}-password" placeholder="请输入暗号" style="
        padding: 10px 15px;
        width: 250px;
        border: 1px solid #374151;
        border-radius: 6px;
        background-color: #1f2937;
        color: #e5e7eb;
        font-size: 16px;
        margin: 20px 0;
      ">
      <div style="color: #ef4444; margin-top: 10px; display: none;" id="${containerId}-error"></div>
      <button onclick="handleDarkDomainVerify('${containerId}', ${onVerifySuccess.toString()})" style="
        padding: 10px 25px;
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 16px;
        margin-top: 10px;
      ">验证</button>
    </div>
  `;
  
  container.innerHTML = lockHtml;
  
  // 监听回车键
  document.getElementById(`${containerId}-password`).addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      handleDarkDomainVerify(containerId, onVerifySuccess);
    }
  });
}

/**
 * 处理暗域验证
 * @param {string} containerId 容器ID
 * @param {Function} onVerifySuccess 验证成功回调
 */
function handleDarkDomainVerify(containerId, onVerifySuccess) {
  const passwordInput = document.getElementById(`${containerId}-password`);
  const errorElement = document.getElementById(`${containerId}-error`);
  const password = passwordInput.value;
  
  const result = verifyDarkDomainPassword(password);
  
  if (result.success) {
    // 验证成功
    document.getElementById(`${containerId}-lock`).style.display = 'none';
    onVerifySuccess();
  } else {
    // 验证失败
    errorElement.textContent = result.message;
    errorElement.style.display = 'block';
    passwordInput.value = '';
  }
}

/**
 * 初始化暗域访问控制
 */
function initDarkDomainAccess() {
  // 暴露全局方法
  window.isDarkDomainVerified = isDarkDomainVerified;
  window.verifyDarkDomainPassword = verifyDarkDomainPassword;
  window.createDarkDomainAccess = createDarkDomainAccess;
  window.handleDarkDomainVerify = handleDarkDomainVerify;
}

// 当DOM加载完成后初始化
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initDarkDomainAccess);
} else {
  initDarkDomainAccess();
}