# 1. 选择合适的基础镜像（CPU 版本 PaddlePaddle）
FROM python:3.12-slim

# 2. 设置工作目录
WORKDIR /app

# 3. 安装依赖（系统库 + Python 库）
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libglib2.0-0 \
        libsm6 \
        libxrender1 \
        libxext6 \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 4. 复制 requirements.txt 并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir paddlepaddle

# 5. 复制项目代码（只拷贝 backend + gui.py 等必要文件）
COPY backend ./backend
COPY gui.py .
COPY requirements_directml.txt .
COPY LICENSE README.md README_en.md ./

# 6. 设置 Python 路径，保证能 import backend
ENV PYTHONPATH=/app

# 7. 默认入口点（让容器像命令行工具一样用）
ENTRYPOINT ["python", "backend/main.py"]