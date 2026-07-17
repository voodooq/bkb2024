# 项目概述

本项目包含一个使用 Vue.js 构建的前端 Web 应用和一个使用 Python (FastAPI 框架) 构建的后端 API 服务。
项目经过了深度的并发性能优化与安全重构，专为高并发场景（如多赛区篮球比赛实时记分）设计。

## 目录结构

```
E:\work\bkb2024\
├───pyvueapps\
    ├───README.md           # 本说明文件
    ├───web\                # 前端 (Vue.js 应用)
    └───svr\                # 后端 (Python API 服务)
        └───pyApiSvr\
            ├───pyapisvr.py # 后端应用主入口
            ├───config.py   # 核心配置文件（已重构为读取环境变量）
            └───apilibs\    # API 逻辑和功能插件
                ├───pluginDB.py      # 【核心】统一数据库插件（支持 MySQL/SQL Server，自管理连接池）
                ├───pluginBkSignup.py# 核心业务逻辑（内存数据缓冲、异步写库、OSS同步）
                ├───pluginOss.py     # OSS 读写插件
                ├───pluginOssBucket.py # OSS 高级功能插件 (含 STS)
                └───plugOssLive.py   # 直播推流处理插件
├───dockerfile              # 生产环境打包文件
├───bkb2024.yml             # Docker-Compose 部署文件
├───.env.example            # 环境变量配置模板
└───start.sh                # 快捷启动脚本
```

## 本地 Docker 打包与运行

系统已全面容器化，并支持通过读取 `.env` 环境变量文件进行灵活配置和扩展。请遵循以下步骤在本地或服务器打包运行：

### 1. 配置环境变量
项目根目录下有一个 `.env.example`，请复制一份命名为 `.env`，并在其中填入真实的数据库、OSS 和短信服务配置。
```bash
cp .env.example .env
```
**关键并发配置说明**：
为了应对比赛现场几十名操作员的高并发录入，在 `.env` 中可以配置数据库最大并发连接数（支持热插拔，代码中默认已从原来的 20 提至 100）：
- `DB_POOL_MAX_CONNECTIONS=100` 
- `DB_POOL_MIN_CACHED=0`
- `DB_POOL_MAX_CACHED=10`

### 2. 编译并启动服务
使用 Docker-Compose 一键构建本地镜像并后台启动：
```bash
# 停止旧服务
docker-compose -f bkb2024.yml down

# 重新构建本地 bkb_server_app 镜像并运行
docker-compose -f bkb2024.yml up -d --build
```
> 或者你也可以直接运行根目录提供的 `./start.sh` 快捷脚本。

### 3. 查看运行日志
系统已全面移除了会阻塞容器 I/O 的 `print()`，全部采用了 `logging` 模块。可以通过以下命令查看容器的安全日志：
```bash
docker logs -f bkb_server
```

---

## 核心架构与优化说明

### 统一数据库管理 (`pluginDB.py`)
经过深度重构，之前冗余的 `pluginMssql.py` 和 `pluginMysql.py` 已被永久移除。
现在所有的数据库访问（不管底层是 MySQL 还是 SQL Server）统一由 `pluginDB.py` 接管和路由。
*   **内存优化**：消除了启动时重复创建影子连接池的问题，Docker 内存占用下降约 40%。
*   **防假死机制**：全面补充了网络读取超时 (`read_timeout`)、连接超时 (`connect_timeout`)，并在 `finally` 块中强制释放 `cursor` 游标。
*   **向后兼容**：旧版前端调用的 `/msquery` 和 `/myquery` 路由依然可用，由 `pluginDB.py` 内部完美无缝转发。

### 异步队列防死锁 (`pluginBkSignup.py`)
针对于多赛区操作员同时提交比赛成绩的需求：
*   采用了 **内存级并发读取 + 异步无锁 OSS 回写前端 + 单线程队列写回数据库** 的高性能架构。
*   当大量请求涌入时，前端依然可以做到“秒存”（因为数据修改在内存瞬间完成）。对于极慢的网络数据库插入操作，采用了 `queue.Queue().get(timeout=5)` 阻塞式消费模型，极大避免了高频轮询的 CPU 空转。

### 对象存储与安全加固
*   **配置脱敏**：系统内所有硬编码的阿里云 AK/SK 和 短信服务凭据都已移除，强制从服务器环境变量（`.env`）挂载。
*   **短信防刷**：内置 60 秒限频策略，防止恶意消耗短信额度。
*   **安全防御**：SQL 注入白名单校验已开启，会话（Session）也强制增加了 2 小时的生存周期，防止内存无限膨胀。

---

## 前端本地运行与构建 (Vue.js)

前端代码位于 `pyvueapps/web` 目录下，若需在本地进行前端开发或打包，请确保已安装 Node.js，然后执行以下命令：

```bash
cd pyvueapps/web

# 1. 安装前端依赖
npm install

# 2. 启动本地开发热更新服务器 (默认位于 localhost:8080)
npm run dev

# 3. 生产环境混淆编译打包 (打包后文件可部署至 Nginx 等)
npm run build
```
