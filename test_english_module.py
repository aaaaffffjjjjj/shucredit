"""
测试全英文课程模块提取
"""
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app'))

from app import SmartExcelParser

excel_path = os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app', 'uploads', 'sydney_business_25.xlsx')

print("="*100)
print("测试全英文课程模块提取")
print("="*100)

parser = SmartExcelParser()
parser.parse(excel_path, '信管课程25级', 'sydney_business_25.xlsx')
result = parser.get_result()

print("\n所有模块:")
for mod in result['modules']:
    print(f"  {mod['id']}. {mod['name']}")

# 检查是否有全英文课程模块
has_english = any("全英文" in mod['name'] for mod in result['modules'])
print(f"\n是否有全英文课程模块: {has_english}")

print("\n课程列表（查找全英文模块的课程）:")
module_id_to_name = {mod['id']: mod['name'] for mod in result['modules']}
for course in result['courses']:
    if "全英文" in module_id_to_name.get(course['module_id'], ''):
        print(f"  {course['name']} -> {module_id_to_name[course['module_id']]}")

print("\n所有课程与模块对应（前30个）:")
for course in result['courses'][:30]:
    print(f"  {course['name']} -> {module_id_to_name.get(course['module_id'], '未知')}")
