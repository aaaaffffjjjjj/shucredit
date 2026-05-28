#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更详细的PDF分析
"""

import pdfplumber
import re

pdf_path = r'e:\wodeaishiyan\2025通信工程.pdf'

print(f"📄 正在分析: {pdf_path}")
print("="*80)

try:
    with pdfplumber.open(pdf_path) as pdf:
        full_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
        
        print(f"   总页数: {len(pdf.pages)}")
        print(f"   总字符: {len(full_text)}")
        
        # 查看完整文本
        print(f"\n--- 完整文本（前1500字符）---")
        print(full_text[:1500])
        
        # 查找模块标题
        print(f"\n--- 查找模块标题 ---")
        pattern = r'(\d+)\.\s*([^\n]+?)\s*(\d+(?:\.\d+)?)\s*学分'
        matches = re.findall(pattern, full_text)
        
        for match in matches:
            print(f"   模块 {match[0]}: {match[1]} ({match[2]}学分)")
        
        # 查找专业方向模块
        print(f"\n--- 查找专业方向 ---")
        dir_patterns = [
            r'专业方向模块',
            r'个性化教育课程'
        ]
        
        for pattern in dir_patterns:
            if pattern in full_text:
                print(f"   ✅ 找到: {pattern}")
                
                # 查找该部分的位置
                idx = full_text.find(pattern)
                snippet = full_text[idx:idx+500]
                print(f"\n   相关片段:\n{snippet}")

except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()
