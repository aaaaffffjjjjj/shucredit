"""测试多模块功能"""
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app'))

from app import SmartExcelParser

excel_path = os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app', 'uploads', 'sydney_business_25.xlsx')

print("="*100)
print("测试多模块功能")
print("="*100)

parser = SmartExcelParser()
parser.parse(excel_path, '信管课程25级', 'sydney_business_25.xlsx')
result = parser.get_result()

print(f"\n学院: {result['college_name']}")
print(f"专业: {result['major_name']}")
print(f"\n模块数: {len(result['modules'])}")
print("\n模块列表:")
for mod in result['modules']:
    print(f"  {mod['id']:2d}. {mod['name']}")

print(f"\n课程数: {len(result['courses'])}")
print("\n课程与模块对应关系（前30个）:")
print("-"*100)
for course in result['courses'][:30]:
    module_names = course.get('module_names', [])
    module_str = ', '.join(module_names) if module_names else '-'
    print(f"  {course['id']:3d}. {course['name']:40s} -> {module_str}")

print("\n" + "="*100)
print("查找有多模块的课程:")
print("="*100)
for course in result['courses']:
    module_names = course.get('module_names', [])
    if len(module_names) > 1:
        print(f"\n{course['name']}:")
        for name in module_names:
            print(f"  - {name}")
