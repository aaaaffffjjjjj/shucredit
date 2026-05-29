#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试PDF模块解析
"""

import pdfplumber
import re

pdf_path = r'e:\nbainbshuda\shucredit-1\2025光电信息科学与工程.pdf'

with pdfplumber.open(pdf_path) as pdf:
    full_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    
    print("="*60)
    print("直接测试PDF模块解析")
    print("="*60)
    
    lines = full_text.split('\n')
    modules = []
    current_root_order = 0
    
    for line in lines:
        # 匹配根模块：1. 模块名 学分 或 1、模块名 学分
        root_match = re.match(r'^(\d+)[\.、]\s*([^\n]+?)\s*(\d+(?:\.\d+)?)\s*学分', line.strip())
        if root_match:
            current_root_order = int(root_match.group(1))
            modules.append({
                'order': current_root_order,
                'sub_order': None,  # 根模块
                'name': root_match.group(2).strip(),
                'credits': float(root_match.group(3)),
                'parent_order': None
            })
            continue
        
        # 匹配子模块：（1）模块名 学分 或 (1) 模块名 学分
        sub_match = re.match(r'^[（(](\d+)[）)]\s*([^\n]+?)\s*(\d+(?:\.\d+)?)\s*学分', line.strip())
        if sub_match and current_root_order > 0:
            modules.append({
                'order': current_root_order,
                'sub_order': int(sub_match.group(1)),
                'name': sub_match.group(2).strip(),
                'credits': float(sub_match.group(3)),
                'parent_order': current_root_order
            })
            continue
    
    print(f"\n找到的模块 ({len(modules)}个):")
    for mod in modules:
        parent_str = f' (父: {mod["parent_order"]})' if mod["parent_order"] else ''
        print(f'  Order={mod["order"]}, SubOrder={mod["sub_order"]}: {mod["name"]} ({mod["credits"]}学分){parent_str}')
    
    print("\n" + "="*60)
    print("✓ 测试完成！")
    print("="*60)
