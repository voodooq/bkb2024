FROM registry.cn-hangzhou.aliyuncs.com/hhuc/python:3.7-bkb2

# 设置环境变量，防止 Python 生成 pyc 缓存文件，及强制标准输出不缓冲（方便 docker logs 实时查看）
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 设置工作目录
WORKDIR /pyvueapps/svr/pyApiSvr

# 拷贝代码到镜像内部（生产环境推荐，如果是调试可通过 docker-compose volumes 覆盖）
COPY ./pyvueapps /pyvueapps

# 安装项目运行所需的额外依赖（利用阿里云镜像源加速）
RUN pip install alibabacloud_dysmsapi20170525 alibabacloud_tea_openapi alibabacloud_tea_util DBUtils==1.3 pymysql pymssql fastapi uvicorn -i https://mirrors.aliyun.com/pypi/simple/

# 暴露端口 (如果有需要外部访问，与 docker-compose.yml 中的 ports 映射对应)
EXPOSE 8010
EXPOSE 31503

# 启动服务
CMD ["python", "pyapisvr.py"]
