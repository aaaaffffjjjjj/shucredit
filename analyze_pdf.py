#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析PDF文件格式
"""

import pdfplumber

pdf_path = r'e:\wodeaishiyan\2025通信工程.pdf'

print(f"📄 正在分析: {pdf_path}")
print("="*80)

try:
    with pdfplumber.open(pdf_path) as pdf:
        print(f"   总页数: {len(pdf.pages)}")
        
        # 查看前3页
        for page_num in range(min(3, len(pdf.pages))):
            page = pdf.pages[page_num]
            print(f"\n--- 第 {page_num+1} 页 ---")
            
            # 提取文本
            text = page.extract_text() or ""
            print(text[:500] if text else "无文本")
            
            # 查看表格
            tables = page.extract_tables()
            if tables:
                print(f"\n   表格数: {len(tables)}")
                for i, table in enumerate(tables[:2]):
                    print(f"\n   表格 {i+1} (前5行):")
                    for row in table[:5]:
                        print(f"      {row}")
                
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()
