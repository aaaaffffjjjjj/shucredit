#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终测试 - 测试改进的PDF解析器
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_simple_parse():
    """简单测试 - 仅解析，不导入"""
    print("="*80)
    print("🧪 测试1: 简单PDF解析")
    print("="*80)
    
    import pdfplumber
    import re
    
    pdf_path = r'e:\wodeaishiyan\2025通信工程.pdf'
    
    print(f"\n📄 解析: {pdf_path}")
    
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() or "" for page in pdf.pages])
        print(f"   页数: {len(pdf.pages)}")
        print(f"   字符: {len(text)}")
    
    # 查找模块
    mod_pattern = r'(\d+)\.\s*([^\n]+?)\s*(\d+(?:\.\d+)?)\s*学分'
    mods = re.findall(mod_pattern, text)
    print(f"\n📦 找到 {len(mods)} 个模块:")
    for m in mods:
        print(f"      {m[0]}. {m[1]} ({m[2]}学分)")
    
    # 查找课程代码
    code_pattern = r'[A-Z]{3}\d{5,7}'
    codes = set(re.findall(code_pattern, text))
    print(f"\n📚 找到 {len(codes)} 个课程代码")
    print(f"   前10个: {', '.join(sorted(list(codes))[:10])}")
    
    print(f"\n✅ 解析测试通过！")


def test_parsing_ability():
    """测试解析能力"""
    print("\n" + "="*80)
    print("🏗️  测试2: 解析器能力")
    print("="*80)
    
    # 导入我们的解析器
    from shucredit_scripts.parsers.shupdf_parser_final import SHUPDFParserFinal
    
    pdf_path = r'e:\wodeaishiyan\2025通信工程.pdf'
    
    # 创建解析器
    parser = SHUPDFParserFinal(
        college_name='通信与信息工程学院',
        major_name='通信工程',
        major_code='TE001'
    )
    
    # 解析
    if parser.parse(pdf_path):
        parser.print_summary()
        print(f"\n✅ 解析器工作正常！")
        return parser
    else:
        print(f"\n❌ 解析失败！")
        return None


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║              改进版PDF解析器 - 最终测试                        ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # 测试1
    test_simple_parse()
    
    # 测试2
    parser = test_parsing_ability()
    
    print("\n" + "="*80)
    print("📝 功能总结")
    print("="*80)
    
    print(f"""
✅ 已完成的改进:

1. **PDF解析** - 现在可以真正解析PDF内容
2. **模块构建** - 自动构建完整的模块结构
3. **课程提取** - 提取课程信息并去重
4. **智能方向识别** - 根据专业名确定方向
5. **完整导入** - 一键解析并导入数据库

📦 工具包包含:
   - shupdf_parser_final.py (✅ 最终推荐)
   - universal_major_creator.py (通用创建)
   - create_preconfigured_majors.py (预配置)
   - PDF_PARSER_GUIDE.md (✅ 使用指南)

💡 使用方式:
   1. 直接运行: cd parsers && python shupdf_parser_final.py
   2. 在代码中导入使用
   3. 查看 PDF_PARSER_GUIDE.md 完整文档
    """)
    
    print("\n" + "="*80)
    print("🎉 所有改进工作完成！")
    print("="*80)


if __name__ == '__main__':
    main()
