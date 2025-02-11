# 使用 Ubuntu 作为基础镜像
FROM ubuntu:latest

# 设置环境变量，避免 apt 交互模式导致安装失败
ENV DEBIAN_FRONTEND=noninteractive

# 设置工作目录
WORKDIR /app

# 更新 apt 包索引，并安装 Python 及必要工具
RUN apt update && apt install -y --no-install-recommends \
    python3 python3-pip python3-venv ffmpeg curl wget ca-certificates && \
    apt clean && rm -rf /var/lib/apt/lists/*

# 检查 Python 和 curl 版本（用于调试）
RUN python3 --version && curl --version

# 手动下载安装 pip
RUN wget https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py && python3 /tmp/get-pip.py

# 确保 pip 可用，并升级到最新版本
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel

# 复制项目文件
COPY downloadvideo.py /app/downloadvideo.py

# 安装 Python 依赖
RUN pip3 install --no-cache-dir flask flask-cors yt-dlp

# 暴露 Flask 运行端口
EXPOSE 5000

# 运行 Flask 应用
CMD ["python3", "/app/downloadvideo.py"]
