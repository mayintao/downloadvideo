# 使用 Ubuntu 22.04 作为基础镜像
FROM ubuntu:22.04

# 设置工作目录
WORKDIR /app

# 更换 Ubuntu 软件源（提升安装速度，可选）
RUN sed -i 's|http://archive.ubuntu.com|http://mirrors.aliyun.com|g' /etc/apt/sources.list && apt update

# 更新软件包索引，并安装 Python3、pip 和 ffmpeg
RUN apt update && apt install -y --no-install-recommends \
    python3 python3-pip ffmpeg curl wget && \
    apt clean && rm -rf /var/lib/apt/lists/*

# 显示 Python 版本，确保 Python 可用（用于调试）
RUN python3 --version

# 确保 pip 可用，并升级到最新版本
RUN python3 -m pip install --upgrade pip setuptools wheel

# 复制 Python 文件到容器
COPY downloadvideo.py /app/downloadvideo.py

# 安装 Python 依赖
RUN pip install --no-cache-dir flask flask-cors yt-dlp

# 暴露 Flask 运行端口
EXPOSE 5000

# 运行 Flask 应用
CMD ["python3", "/app/downloadvideo.py"]
