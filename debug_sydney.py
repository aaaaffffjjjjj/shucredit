"""
调试悉尼工商学院解析器
"""
import os
import sys
import pandas as pd
import re

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app'))

excel_path = os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app', 'uploads', 'sydney_business_25.xlsx')

print("="*100)
print("调试悉尼工商学院解析器")
print("="*100)

# 读取文件
try:
    excel_file = pd.ExcelFile(excel_path)
    print("工作表列表:", excel_file.sheet_names)
    
    # 读取信管课程表
    df = pd.read_excel(excel_path, sheet_name='信管课程25级', header=None)
    print(f"\n课程表形状: {df.shape}")
    
    # 读取学分食用概况表
    credit_df = None
    for name in excel_file.sheet_names:
        if "信管" in name and "学分" in name:
            credit_df = pd.read_excel(excel_path, sheet_name=name, header=None)
            print(f"\n学分概况表: {name}, 形状: {credit_df.shape}")
            break
    
    # 测试提取课程与模块关系
    print("\n测试提取课程与模块关系:")
    print("-"*100)
    
    course_module_map = {}
    
    invalid_phrases = ["未必能完全", "注意", "推测", "简称建议", "选双学位", "各总计", "大一", "大二", "大三", "大四", "前半学期", "后半学期"]
    
    for i in range(min(20, len(df))):
        row = df.iloc[i].values
        
        row_courses = []
        for j in range(5):
            if j < len(row) and pd.notna(row[j]) and str(row[j]).strip():
                course_name = str(row[j]).strip()
                
                is_invalid = False
                for phrase in invalid_phrases:
                    if phrase in course_name:
                        is_invalid = True
                        break
                if is_invalid or len(course_name) < 2:
                    continue
                
                row_courses.append(course_name)
        
        row_modules = []
        for j in range(5, len(row)):
            if pd.notna(row[j]) and str(row[j]).strip():
                cell_content = str(row[j]).strip()
                
                is_invalid = False
                for phrase in invalid_phrases:
                    if phrase in cell_content:
                        is_invalid = True
                        break
                if is_invalid:
                    continue
                
                if ("模块" in cell_content or 
                    ("课" in cell_content and "分" in cell_content) or 
                    "必" in cell_content or
                    "选修" in cell_content or
                    "个性化" in cell_content or
                    "创新创业" in cell_content or
                    "劳动" in cell_content):
                    
                    module_name = cell_content
                    credits = 0.0
                    credit_match = re.search(r'(\d+(?:\.\d+)?)\s*分', module_name)
                    if credit_match:
                        credits = float(credit_match.group(1))
                        module_name = re.sub(r'\s*\d+(?:\.\d+)?\s*分', '', module_name).strip()
                    
                    module_name = re.sub(r'（[^）]*）', '', module_name).strip()
                    module_name = re.sub(r'\([^)]*\)', '', module_name).strip()
                    
                    if module_name:
                        row_modules.append((module_name, credits))
        
        if row_courses and row_modules:
            print(f"行{i:2d}: 课程={row_courses} -> 模块={row_modules}")
            for course_name in row_courses:
                if course_name not in course_module_map:
                    course_module_map[course_name] = []
                for module_name, credits in row_modules:
                    if module_name not in [m[0] for m in course_module_map[course_name]]:
                        course_module_map[course_name].append((module_name, credits))
    
    print("\n课程-模块映射:")
    print("-"*100)
    for course_name, modules in list(course_module_map.items())[:10]:
        print(f"  {course_name:40s} -> {modules}")
        
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
