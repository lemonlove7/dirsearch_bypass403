import sys
import os

# 打印当前 Python 解释器路径
print(f"当前 Python 解释器: {sys.executable}")

# 打印 Python 模块搜索路径
print("\nPython 模块搜索路径:")
for path in sys.path:
    print(f"  {path}")

# 检查 requests 模块是否能被导入
try:
    import requests
    print("\n✓ 成功导入 requests 模块")
    print(f"  requests 模块路径: {requests.__file__}")
    print(f"  requests 版本: {requests.__version__}")
except ImportError:
    print("\n✗ 无法导入 requests 模块")
    
# 检查是否有虚拟环境激活
env_path = os.environ.get('VIRTUAL_ENV')
if env_path:
    print(f"\n检测到激活的虚拟环境: {env_path}")
else:
    print("\n未检测到激活的虚拟环境")