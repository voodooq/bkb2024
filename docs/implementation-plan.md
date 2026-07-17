# Implementation Plan: Docker CPU 占用过高修复

## 阶段一: P0 — 紧急修复 (预计效果: CPU 降低 30~50%)

### 步骤 1.1: 修复 Docker Compose 配置
- **文件**: `bkb2024.yml`
- **操作**:
  - 移除 `privileged: true`
  - 移除 `stdin_open: true`
  - 移除 `tty: true`
  - 添加日志轮转配置 `max-size: 10m, max-file: 3`
  - 添加资源限制 `cpus: 2.0, memory: 2G`

### 步骤 1.2: 清理无效数据源配置
- **文件**: `config.py`
- **操作**:
  - 注释或移除 `femolocal` 数据源（`127.0.0.1:1433` 在容器内不可达）
  - 确认其他数据源在容器网络内的可达性

### 步骤 1.3: 清理容器内冗余文件
- **操作**:
  - 删除 `core.570`（145MB core dump 文件）
  - 清理 `nohup.out` 或限制其增长

---

## 阶段二: P1 — 核心优化 (预计效果: CPU 再降低 20~30%)

### 步骤 2.1: 修复连接池 ping 策略
- **文件**: `pluginDB.py`, `pluginMssql.py`, `pluginMysql.py`
- **操作**: 将所有 `ping=1` 修改为 `ping=4`（仅在执行 SQL 时检测）

### 步骤 2.2: 降低 pluginMssql 连接池预分配
- **文件**: `pluginMssql.py`
- **操作**: `mincached` 从 10 改为 0，`maxcached` 从 15 改为 5，`maxconnections` 从 100 改为 20

### 步骤 2.3: 替换 print 为 logging
- **文件**: 所有 Python 文件
- **操作**: 引入 `logging` 模块，替换所有 `print()` 调用，生产环境设置为 `WARNING` 级别

---

## 阶段三: P2 — 性能增强

### 步骤 3.1: 优化 pluginBkSignup 锁粒度
- **文件**: `pluginBkSignup.py`
- **操作**:
  - `session_updateUserData` 中将 OSS 写入移到 `dataLock` 锁外
  - `getUserData` 中的数据遍历添加索引缓存

### 步骤 3.2: 优化 dbBuffer 消费者线程
- **文件**: `pluginBkSignup.py`
- **操作**:
  - 将 `dbBuffer.get(timeout=0.5)` 改为 `dbBuffer.get()`（阻塞式等待）
  - 添加异常退避机制 `time.sleep(1)` 防止疯狂重试

---

## 阶段四: P3 — 长期治理

### 步骤 4.1: 消除重复连接池
- **分析**: `pluginMssql` 和 `pluginDB` 对同一数据源各自维护独立连接池，建议统一使用 `pluginDB` 管理

### 步骤 4.2: uvicorn worker 配置
- **文件**: `pyapisvr.py`
- **操作**: 添加 `workers` 参数，根据 CPU 核心数合理配置工作进程数
