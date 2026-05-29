#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试PDF解析
"""

import sys
import os

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app'))

from app import SmartPDFParser

# 找一个培养方案的PDF文件
pdf_files = [
    r'e:\nbainbshuda\shucredit-1\2025光电信息科学与工程.pdf',
    r'e:\nbainbshuda\shucredit-1\通信工程专业学分结构最终版 含课程编号.pdf',
]

pdf_path = None
for path in pdf_files:
    if os.path.exists(path):
        pdf_path = path
        break

if pdf_path:
    print("="*60)
    print("测试PDF解析器")
    print("="*60)
    print(f"解析文件: {pdf_path}")
    
    parser = SmartPDFParser()
    parser.parse(pdf_path, os.path.basename(pdf_path))
    
    result = parser.get_result()
    
    # 打印学院和专业
    print(f"\n学院: {result['college_name']}")
    print(f"专业: {result['major_name']}")
    
    # 打印解析结果
    print(f'\n解析到的模块 ({len(result["modules"])}个):')
    for module in result['modules']:
        parent_str = f' (父: {module["parent_id"]})' if module['parent_id'] else ''
        print(f'  {module["id"]}. {module["name"]} ({module["required_credits"]}学分){parent_str}')
    
    print("\n" + "="*60)
    print("✓ 测试完成！")
    print("="*60)
else:
    print("找不到测试PDF文件！")
