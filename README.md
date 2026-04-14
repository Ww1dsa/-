# -
一个网页版的虚假新闻检测

## pyweb - 暗流哨卫 Python 重做版

### 功能模块
- 首页检测：文本检测 + 图片/视频鉴别（演示规则）
- 举报投稿：表单提交并写入 SQLite
- 论坛：发帖与列表展示（SQLite 持久化）
- 知识库：套路、渠道、法规、鉴谣方法

### 运行方式
1. 创建虚拟环境（可选）
2. 安装依赖
   pip install -r requirements.txt
3. 启动服务
   uvicorn app.main:app --reload
4. 浏览器访问
   http://127.0.0.1:8000

### 一键部署到云端（Render）
1. 打开一键部署链接
   https://render.com/deploy?repo=https://github.com/Ww1dsa/-.git
2. 登录 Render，确认服务名后点击 Create Web Service。
3. 等待构建完成后，会得到公网地址，可直接分享给别人访问。

说明：当前默认使用 SQLite，免费实例重启可能导致数据丢失；要长期保存数据建议后续换 PostgreSQL。

### 目录说明
- app/main.py：路由与页面入口
- app/models.py：数据库模型
- app/services.py：检测与上传逻辑
- app/templates/：页面模板
- app/static/site.css：样式
