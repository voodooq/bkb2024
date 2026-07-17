# Task List: Docker CPU 占用过高修复与安全加固

## P0 — 紧急修复

- [x] **Task 1.1**: 修改 `bkb2024.yml`，移除 `privileged/stdin_open/tty`，添加日志轮转和资源限制
- [x] **Task 1.2**: 修改 `config.py`，配置全部提取至环境变量（`.env`）
- [ ] **Task 1.3**: 删除 `core.570` 文件，清理 `nohup.out`（需在服务器上手动操作）

## P1 — 核心优化与安全

- [x] **Task 2.1**: 修改 `pluginDB.py` / `pluginMssql.py` / `pluginMysql.py`，`ping=1` → `ping=4` 并添加连接超时控制
- [x] **Task 2.2**: 修复 `pluginMssql.py` 游标可能泄漏的问题（移至 finally 块关闭），降低预分配参数
- [x] **Task 2.3**: `pyapisvr.py` 和各插件中 `print()` 彻底替换为 `logging` 模块
- [x] **Task 2.4**: 修复 `pluginDB.py` SQL 注入漏洞（白名单校验标识符）
- [x] **Task 2.5**: 修复 `pluginBkSignup.py` 短信限频、测试后门和会话过期（TTL）
- [x] **Task 2.6**: 修复 `plugOssLive.py` AK/SK 硬编码问题

## P2 — 性能增强

- [x] **Task 3.1**: 优化 `pluginBkSignup.py` 中 `dbBuffer` 消费者线程：由 `time.sleep` 改为阻塞式 `queue.get()`
- [x] **Task 3.2**: 优化 `pluginBkSignup.py` 中 `dataLock` 锁粒度（将 OSS JSON 序列化与网络写入移到锁外）
- [x] **Task 3.3**: 优化 `pluginBkSignup.py` `getUserData` 中的数据遍历（引入 `_user_teams_idx` 等字典索引，避免 O(N) 遍历）

## P3 — 长期治理

- [x] **Task 4.1**: 统一 `pluginMssql`/`pluginMysql`/`pluginDB` 重复连接池管理（已删除多余插件，统一归口至 pluginDB 并作向后兼容）
- [ ] **Task 4.2**: 配置 uvicorn workers 参数（可结合机器核数调整）
