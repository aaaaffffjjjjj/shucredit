#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查找PDF中所有的模块
"""

import pdfplumber
import re

pdf_path = r'e:\nbainbshuda\shucredit-1\2025光电信息科学与工程.pdf'

with pdfplumber.open(pdf_path) as pdf:
    full_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    
    print("="*60)
    print("PDF中找到的所有模块")
    print("="*60)
    
    lines = full_text.split('\n')
    for line in lines:
        # 匹配根模块
        root_match = re.match(r'^(\d+)[\.、]\s*([^\n]+?)\s*(\d+(?:\.\d+)?)\s*学分', line.strip())
        if root_match:
            print(f"根模块: {line}")
        
        # 匹配子模块
        sub_match = re.match(r'^[（(](\d+)[）)]\s*([^\n]+?)\s*(\d+(?:\.\d+)?)\s*学分', line.strip())
        if sub_match:
            print(f"子模块: {line}")
