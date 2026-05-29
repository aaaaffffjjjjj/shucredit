"""
直接测试悉尼工商学院解析器的内部方法
"""
import os
import sys
import pandas as pd

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app'))

from app import SmartExcelParser

excel_path = os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app', 'uploads', 'sydney_business_25.xlsx')

print("="*100)
print("直接测试悉尼工商学院解析器内部方法")
print("="*100)

parser = SmartExcelParser()

# 读取文件
excel_file = pd.ExcelFile(excel_path)
df = pd.read_excel(excel_path, sheet_name='信管课程25级', header=None)

# 读取学分概况表
credit_df = None
for name in excel_file.sheet_names:
    if "信管" in name and "学分" in name:
        credit_df = pd.read_excel(excel_path, sheet_name=name, header=None)
        break

print("\n1. 测试 _extract_credit_map")
try:
    credit_map = parser._extract_credit_map(credit_df)
    print(f"   提取到 {len(credit_map)} 个课程学分映射")
    for course_name, credits in list(credit_map.items())[:5]:
        print(f"     {course_name}: {credits}")
except Exception as e:
    print(f"   错误: {e}")
    import traceback
    traceback.print_exc()

print("\n2. 测试 _extract_course_module_relationships")
try:
    course_module_map = parser._extract_course_module_relationships(df, credit_map)
    print(f"   提取到 {len(course_module_map)} 个课程")
    for course_name, modules in list(course_module_map.items())[:10]:
        print(f"     {course_name:40s} -> {modules}")
except Exception as e:
    print(f"   错误: {e}")
    import traceback
    traceback.print_exc()

print("\n3. 测试 _build_modules_and_courses_from_map")
try:
    modules, courses = parser._build_modules_and_courses_from_map(course_module_map, credit_map)
    print(f"   构建了 {len(modules)} 个模块")
    for mod in modules:
        print(f"     {mod['order']:2d}. {mod['name']}")
    print(f"\n   构建了 {len(courses)} 个课程")
    for course in courses[:10]:
        print(f"     {course['id']:3d}. {course['name']:40s} -> 模块{course['module_id']}")
except Exception as e:
    print(f"   错误: {e}")
    import traceback
    traceback.print_exc()

print("\n4. 测试完整解析流程")
try:
    parser._parse_sydney_format(df, credit_df)
    result = parser.get_result()
    print(f"   模块数: {len(result['modules'])}")
    print(f"   课程数: {len(result['courses'])}")
except Exception as e:
    print(f"   错误: {e}")
    import traceback
    traceback.print_exc()
