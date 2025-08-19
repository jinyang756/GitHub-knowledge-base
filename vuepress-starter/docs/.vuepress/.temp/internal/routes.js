export const redirects = JSON.parse("{}")

export const routes = Object.fromEntries([
  ["/", { loader: () => import(/* webpackChunkName: "index.html" */"C:/Users/Administrator/Desktop/GitHub知识库/vuepress-starter/docs/.vuepress/.temp/pages/index.html.js"), meta: {} }],
  ["/%E6%8A%80%E6%9C%AF/Python.html", { loader: () => import(/* webpackChunkName: "技术_Python.html" */"C:/Users/Administrator/Desktop/GitHub知识库/vuepress-starter/docs/.vuepress/.temp/pages/技术/Python.html.js"), meta: {} }],
  ["/404.html", { loader: () => import(/* webpackChunkName: "404.html" */"C:/Users/Administrator/Desktop/GitHub知识库/vuepress-starter/docs/.vuepress/.temp/pages/404.html.js"), meta: {} }],
]);
