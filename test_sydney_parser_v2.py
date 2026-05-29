"""
测试改进后的悉尼工商学院Excel解析器 - 课程与模块对应关系
"""
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app'))

from app import SmartExcelParser

# 测试文件路径
excel_path = os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app', 'uploads', 'sydney_business_25.xlsx')

print("="*100)
print("测试改进后的悉尼工商学院Excel解析器 - 课程与模块对应关系")
print("="*100)
print(f"文件路径: {excel_path}")
print()

# 测试信管专业
print("-"*100)
print("测试1: 解析信管课程25级")
print("-"*100)
parser = SmartExcelParser()
try:
    parser.parse(excel_path, '信管课程25级', 'sydney_business_25.xlsx')
    result = parser.get_result()
    
    print(f"\n学院: {result['college_name']}")
    print(f"专业: {result['major_name']}")
    print(f"\n模块数: {len(result['modules'])}")
    print("模块列表:")
    for mod in result['modules']:
        print(f"  {mod['id']:2d}. {mod['name']} (学分: {mod['required_credits']})")
    
    print(f"\n课程数: {len(result['courses'])}")
    print("\n课程与模块对应关系 (前20个):")
    print("-"*100)
    
    # 创建模块ID到名称的映射
    module_id_to_name = {mod['id']: mod['name'] for mod in result['modules']}
    
    for course in result['courses'][:20]:
        module_name = module_id_to_name.get(course['module_id'], '未知模块')
        print(f"  {course['id']:3d}. {course['name']:40s} -> {module_name} (学分: {course['credits']})")
    
    # 显示几个典型的课程
    print("\n典型课程示例:")
    print("-"*100)
    typical_courses = ["形势与政策", "高等数学B(1)", "学术英语(1)", "体育(1)", "创新创业类"]
    for course in result['courses']:
        if course['name'] in typical_courses:
            module_name = module_id_to_name.get(course['module_id'], '未知模块')
            print(f"  {course['name']:40s} -> {module_name}")
    
except Exception as e:
    print(f"解析失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*100)
print("测试完成")
print("="*100)
