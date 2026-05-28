#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试独立版PDF解析器
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shucredit_scripts', 'parsers'))
from standalone_pdf_parser import StandalonePDFParser


print("""
╔══════════════════════════════════════════════════════════════╗
║           独立版PDF解析器 - 完整测试                           ║
╚══════════════════════════════════════════════════════════════╝
""")

# === 测试1: 通信工程 ===
print("="*80)
print("📄 测试1: 2025通信工程")
print("="*80)

pdf_path = r'e:\wodeaishiyan\2025通信工程.pdf'
parser = StandalonePDFParser('通信与信息工程学院', '通信工程', 'TE001')
if parser.parse(pdf_path):
    parser.print_summary()

# === 测试2: 电子信息工程 ===
print("\n" + "="*80)
print("📄 测试2: 2025电子信息工程")
print("="*80)

pdf_path2 = r'e:\wodeaishiyan\2025电子信息工程.pdf'
parser2 = StandalonePDFParser('通信与信息工程学院', '电子信息工程', 'EIE001')
if parser2.parse(pdf_path2):
    parser2.print_summary()

print("\n" + "="*80)
print("""
✅ 测试完成！

📦 现在你有：
   - standalone_pdf_parser.py (✅ 独立版 - 推荐)
   - shupdf_parser_final.py (完整版 - 需先修复app.py)
   - PDF_PARSER_GUIDE.md (完整文档)

💡 下一步：
   1. 使用 standalone_pdf_parser.py 导入数据
   2. 查看 PDF_PARSER_GUIDE.md 完整文档
   3. 修复 app.py 的git冲突（可选）
""")
print("="*80)
