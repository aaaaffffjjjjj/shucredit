#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查看PDF内容
"""

import pdfplumber

pdf_path = r'e:\nbainbshuda\shucredit-1\2025光电信息科学与工程.pdf'

with pdfplumber.open(pdf_path) as pdf:
    print("="*60)
    print("PDF内容 - 前3页")
    print("="*60)
    
    for i, page in enumerate(pdf.pages[:3]):
        text = page.extract_text() or ""
        print(f"\n第 {i+1} 页:")
        print("-"*40)
        # 打印前20行
        lines = text.split('\n')[:50]
        for j, line in enumerate(lines):
            print(f"{j+1:2d}. {repr(line)}")
