#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查其他PDF文件
"""

import pdfplumber
import re
import os

pdf_files = [
    r'e:\nbainbshuda\shucredit-1\通信工程专业学分结构最终版 含课程编号.pdf',
    r'e:\nbainbshuda\shucredit-1\shucredit_scripts\pdf_app\uploads\cc9f9d94-add4-442c-9ba7-c4bf05487224.pdf',
    r'e:\nbainbshuda\shucredit-1\shucredit_scripts\pdf_app\uploads\f394080f-13e2-4029-897b-fac47061edca.pdf',
]

for pdf_path in pdf_files:
    if os.path.exists(pdf_path):
        print(f"\n{'='*60}")
        print(f"文件: {pdf_path}")
        print('='*60)
        
        with pdfplumber.open(pdf_path) as pdf:
            full_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
            
            lines = full_text.split('\n')
            modules = []
            current_root_order = 0
            
            for line in lines:
                # 匹配根模块
                root_match = re.match(r'^(\d+)[\.、]\s*([^\n]+?)\s*(\d+(?:\.\d+)?)\s*学分', line.strip())
                if root_match:
                    current_root_order = int(root_match.group(1))
                    modules.append({
                        'order': current_root_order,
                        'sub_order': None,
                        'name': root_match.group(2).strip(),
                        'credits': float(root_match.group(3)),
                        'parent_order': None
                    })
                    continue
                
                # 匹配子模块
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
