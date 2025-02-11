# 选择 Ubuntu 作为基础镜像
FROM ubuntu:latest

# 设置工作目录
WORKDIR /app

# 安装 Python 及所需组件
RUN apt update && apt install -y --no-install-recommends \
    python3 python3-pip python3-venv python3-dev \
    libffi-dev libssl-dev build-essential ffmpeg curl wget \
    && apt clean && rm -rf /var/lib/apt/lists/*

# 复制 Python 文件到容器
COPY downloadvideo.py /app/downloadvideo.py

# 确保 pip 可用，并升级到最新版本
RUN python3 -m pip install --upgrade pip setuptools wheel

# 安装 Flask 及所需的 Python 依赖
RUN pip3 install --no-cache-dir flask flask-cors yt-dlp

# 暴露 Flask 运行端口
EXPOSE 5000

# 运行 Python 脚本
CMD ["python3", "/app/downloadvideo.py"]
