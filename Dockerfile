# 使用 Ubuntu 作为基础镜像（比 Alpine 更兼容）
FROM ubuntu:latest

# 进入 /app 目录
WORKDIR /app

# 复制可执行文件
COPY downloadvideo /app/downloadvideo

# 给予执行权限
RUN chmod +x /app/downloadvideo

# 安装必要的运行库（如果需要）
RUN apt update && apt install -y libstdc++6

# 运行可执行文件
CMD ["/app/downloadvideo"]


