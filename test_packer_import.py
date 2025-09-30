#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import sys

# 打印当前执行路径和工作目录
print(f"当前脚本路径: {os.path.abspath(__file__)}")
print(f"当前工作目录: {os.getcwd()}")
print(f"当前 Python 解释器: {sys.executable}")

# 打印 Python 模块搜索路径
print("\nPython 模块搜索路径:")
for path in sys.path:
    print(f"  {path}")

# 尝试直接导入 requests
print("\n直接导入 requests 模块:")
try:
    import requests
    print("✓ 成功导入 requests 模块")
    print(f"  requests 模块路径: {requests.__file__}")
    print(f"  requests 版本: {requests.__version__}")
except ImportError as e:
    print(f"✗ 无法导入 requests 模块: {e}")

# 尝试从Packer-Fuzzer目录结构导入模块
print("\n从Packer-Fuzzer目录结构导入模块:")
try:
    # 添加Packer-Fuzzer目录到模块搜索路径
    packer_fuzzer_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Packer-Fuzzer'))
    if packer_fuzzer_path not in sys.path:
        sys.path.insert(0, packer_fuzzer_path)
        print(f"已添加到搜索路径: {packer_fuzzer_path}")
    
    # 尝试导入ParseJs模块
    from lib.ParseJs import ParseJs
    print("✓ 成功导入 ParseJs 模块")
except ImportError as e:
    print(f"✗ 无法导入 ParseJs 模块: {e}")

# 检查是否有多个Python版本
print("\n检查系统中的Python版本:")
try:
    import subprocess
    result = subprocess.run(['which', '-a', 'python'], capture_output=True, text=True)
    print(f"Python路径: {result.stdout.strip()}")
    result = subprocess.run(['which', '-a', 'python3'], capture_output=True, text=True)
    print(f"Python3路径: {result.stdout.strip()}")
except Exception as e:
    print(f"检查Python版本失败: {e}")