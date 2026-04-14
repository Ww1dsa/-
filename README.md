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

### 国内云函数部署（阿里云函数计算 FC）
1. 安装并登录 Serverless Devs 工具
   npm i -g @serverless-devs/s
   s config add
2. 构建并推送镜像到阿里云容器镜像服务 ACR
   docker build -t pyweb-fc:latest .
   docker tag pyweb-fc:latest <你的ACR镜像地址>
   docker push <你的ACR镜像地址>
3. 在当前目录设置镜像环境变量
   Windows PowerShell:
   $env:IMAGE_URI="<你的ACR镜像地址>"
4. 部署到函数计算
   s deploy -t s.yaml
5. 部署完成后，工具会输出公网 HTTP 触发器地址，直接访问即可。

说明：
- 你要把 s.yaml 中的 region 改成你实际开通的地域。
- 当前默认 SQLite，函数实例重启会导致数据不稳定，生产建议换 RDS PostgreSQL/MySQL。

### 目录说明
- app/main.py：路由与页面入口
- app/models.py：数据库模型
- app/services.py：检测与上传逻辑
- app/templates/：页面模板
- app/static/site.css：样式
- s.yaml：阿里云函数计算部署模板
- Dockerfile：函数计算自定义容器镜像构建文件
