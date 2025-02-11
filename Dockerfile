# 使用 Ubuntu 作为基础镜像
FROM ubuntu:latest

# 设置工作目录
WORKDIR /app

# 安装 Python 和依赖工具
RUN apt update && apt install -y python3 python3-pip ffmpeg && \
    python3 -m pip install --upgrade pip setuptools wheel

# 复制项目文件
COPY downloadvideo.py /app/downloadvideo.py

# 安装 Python 依赖
RUN pip3 install --no-cache-dir flask flask-cors yt-dlp

# 暴露 Flask 运行端口
EXPOSE 5000

# 运行 Flask 应用
CMD ["python3", "/app/downloadvideo.py"]
