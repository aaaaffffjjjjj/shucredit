#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试改进版的PDF解析器
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shucredit_scripts.parsers.universal_pdf_parser import SHUPDFParser


print("="*80)
print("🧪 测试改进版的PDF解析器")
print("="*80)

# 测试通信工程
print("\n" + "="*80)
print("📄 测试1: 2025通信工程.pdf")
print("="*80)

pdf_path = r'e:\wodeaishiyan\2025通信工程.pdf'
parser = SHUPDFParser('通信与信息工程学院', '通信工程', 'TE001')

if parser.parse_pdf(pdf_path):
    parser.print_structure()
    choice = input("\n💡 导入数据库? (y/n): ").strip().lower()
    if choice == 'y':
        parser.import_to_database()

# 测试电子信息工程
print("\n" + "="*80)
print("📄 测试2: 2025电子信息工程.pdf")
print("="*80)

pdf_path = r'e:\wodeaishiyan\2025电子信息工程.pdf'
parser = SHUPDFParser('通信与信息工程学院', '电子信息工程', 'EIE001')

if parser.parse_pdf(pdf_path):
    parser.print_structure()
    choice = input("\n💡 导入数据库? (y/n): ").strip().lower()
    if choice == 'y':
        parser.import_to_database()

print("\n" + "="*80)
print("✅ 测试完成！")
print("="*80)
