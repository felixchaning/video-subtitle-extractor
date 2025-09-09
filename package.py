import importlib.metadata
import argparse
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--file', required=True, help='Your file name, e.g. main.py.')
args = parser.parse_args()

main_file = args.file

# 已安装的依赖
user_deps = [dist.metadata["Name"] for dist in importlib.metadata.distributions()]

# 你关心的依赖
deps_need = [
    "scipy",
    "protobuf",
    "numpy",
    "ftfy",
    "regex",
    "tiktoken",
]

# 基础 PyInstaller 命令
cmd = [
    sys.executable, "-m", "PyInstaller", main_file,
    "--collect-binaries", "paddle",
]

# 根据已安装依赖添加 metadata
for dep in deps_need:
    if dep in user_deps:
        cmd += ["--copy-metadata", dep]

# 处理 Paddle 的特殊 hidden import
cmd += ["--hidden-import", "scipy._lib.messagestream"]

print("PyInstaller command:", " ".join(cmd))

try:
    subprocess.run(cmd, check=True)
except subprocess.CalledProcessError as e:
    print("Build failed:", e)
    sys.exit(1)
