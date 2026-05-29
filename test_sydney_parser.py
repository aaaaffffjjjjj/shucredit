"""
测试悉尼工商学院Excel解析器
"""
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app'))

from app import SmartExcelParser

# 测试文件路径
excel_path = os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app', 'uploads', 'sydney_business_25.xlsx')

print("="*80)
print("测试悉尼工商学院Excel解析器")
print("="*80)
print(f"文件路径: {excel_path}")
print()

# 测试信管专业
print("-"*80)
print("测试1: 解析信管课程25级")
print("-"*80)
parser = SmartExcelParser()
try:
    parser.parse(excel_path, '信管课程25级', 'sydney_business_25.xlsx')
    result = parser.get_result()
    
    print(f"\n学院: {result['college_name']}")
    print(f"专业: {result['major_name']}")
    print(f"\n模块数: {len(result['modules'])}")
    print("模块列表:")
    for mod in result['modules']:
        print(f"  - {mod['name']} (学分: {mod['required_credits']})")
    
    print(f"\n课程数: {len(result['courses'])}")
    print("前20个课程:")
    for course in result['courses'][:20]:
        print(f"  - {course['name']} (学分: {course['credits']})")
        
except Exception as e:
    print(f"解析失败: {e}")
    import traceback
    traceback.print_exc()

# 测试金融专业
print("\n" + "-"*80)
print("测试2: 解析金融课程25级")
print("-"*80)
parser2 = SmartExcelParser()
try:
    parser2.parse(excel_path, '金融课程25级', 'sydney_business_25.xlsx')
    result2 = parser2.get_result()
    
    print(f"\n模块数: {len(result2['modules'])}")
    print("模块列表:")
    for mod in result2['modules']:
        print(f"  - {mod['name']} (学分: {mod['required_credits']})")
    
    print(f"\n课程数: {len(result2['courses'])}")
        
except Exception as e:
    print(f"解析失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("测试完成")
print("="*80)
