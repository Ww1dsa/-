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

### 目录说明
- app/main.py：路由与页面入口
- app/models.py：数据库模型
- app/services.py：检测与上传逻辑
- app/templates/：页面模板
- app/static/site.css：样式
