#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动PDF解析器Web应用
"""

import os
import sys

# 设置工作目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 启动应用
from app import app

if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════╗
║           上海大学培养方案PDF解析器 - Web应用                 ║
╚══════════════════════════════════════════════════════════════╝
""")
    print("🚀 启动Web服务器...")
    print("📍 访问地址: http://localhost:5001")
    print("🔄 按 Ctrl+C 停止服务")
    print()
    
    app.run(host='0.0.0.0', port=5001, debug=True)
