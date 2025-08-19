module.exports = {
  title: 'VuePress 文档',
  description: '我的第一个 VuePress 网站',
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '技术', link: '/技术/' }
    ],
    sidebar: {
      '/技术/': [
        { title: 'Python', path: '/技术/Python.md' }
      ]
    }
  }
};