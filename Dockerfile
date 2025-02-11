# 使用 Alpine 作为基础镜像
FROM alpine:latest

# 进入 /app 目录
WORKDIR /app

# 复制可执行文件到容器
COPY downloadvideo /app/downloadvideo

# 给予执行权限
RUN chmod +x /app/downloadvideo

# 运行可执行文件
CMD ["/app/downloadvideo"]

