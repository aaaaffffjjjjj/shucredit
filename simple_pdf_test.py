#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的PDF解析测试 - 不导入数据库
"""

import os
import re
import pdfplumber


class SimplePDFParser:
    """简单的PDF解析器"""
    
    def __init__(self, college_name, major_name):
        self.college_name = college_name
        self.major_name = major_name
        self.full_text = ""
    
    def parse(self, pdf_path):
        """解析PDF"""
        print(f"📄 正在解析: {pdf_path}")
        print("="*80)
        
        with pdfplumber.open(pdf_path) as pdf:
            self.full_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
            print(f"   页数: {len(pdf.pages)}")
            print(f"   字符: {len(self.full_text)}")
        
        # 分析内容
        print(f"\n📊 内容分析:")
        
        # 查找模块
        module_pattern = r'(\d+)\.\s*([^\n]+?)\s*(\d+(?:\.\d+)?)\s*学分'
        modules = re.findall(module_pattern, self.full_text)
        
        print(f"\n   找到 {len(modules)} 个模块:")
        for mod in modules:
            print(f"      {mod[0]}. {mod[1]} ({mod[2]}学分)")
        
        # 查找课程代码（GBK开头）
        course_code_pattern = r'[A-Z]{3}\d{5,7}'
        codes = set(re.findall(course_code_pattern, self.full_text))
        
        print(f"\n   找到 {len(codes)} 个课程代码:")
        for code in sorted(list(codes))[:15]:  # 只看前15个
            print(f"      {code}")
        
        if len(codes) > 15:
            print(f"      ... (还有 {len(codes)-15} 个)")
        
        # 查找专业方向
        print(f"\n🎯 查找专业方向:")
        direction_keywords = ['方向', '模块']
        for keyword in direction_keywords:
            if keyword in self.full_text:
                print(f"   包含: {keyword}")
        
        # 尝试查找子模块
        print(f"\n📍 查找子模块:")
        sub_pattern = r'\(\d+\)\s*([^\n]+?)\s*(\d+(?:\.\d+)?)\s*学分'
        sub_modules = re.findall(sub_pattern, self.full_text)
        
        for sm in sub_modules[:10]:
            print(f"      {sm[0]} ({sm[1]}学分)")
        
        print(f"\n" + "="*80)
        print("✅ 解析完成！")
        print(f"\n💡 提示:")
        print(f"   - 此脚本仅做分析，不导入数据库")
        print(f"   - 如需完整功能，请使用 universal_pdf_parser.py")


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║           上海大学培养方案PDF解析测试                           ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # 测试通信工程
    pdf_path = r'e:\wodeaishiyan\2025通信工程.pdf'
    parser = SimplePDFParser('通信与信息工程学院', '通信工程')
    parser.parse(pdf_path)
    
    print(f"\n" + "="*80)
    print("📄 测试电子信息工程:")
    print("="*80)
    
    pdf_path2 = r'e:\wodeaishiyan\2025电子信息工程.pdf'
    parser2 = SimplePDFParser('通信与信息工程学院', '电子信息工程')
    parser2.parse(pdf_path2)


if __name__ == '__main__':
    main()
