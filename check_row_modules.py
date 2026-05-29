"""
检查每行右侧的模块信息
"""
import os
import pandas as pd

excel_path = os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app', 'uploads', 'sydney_business_25.xlsx')

print("="*100)
print("检查每行右侧的模块信息")
print("="*100)

excel_file = pd.ExcelFile(excel_path)
df = pd.read_excel(excel_path, sheet_name='信管课程25级', header=None)

invalid_phrases = ["未必能完全", "注意", "推测", "简称建议", "选双学位", "各总计", "大一", "大二", "大三", "大四", "前半学期", "后半学期"]

for i in range(len(df)):
    row = df.iloc[i].values
    
    # 提取课程
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
    
    # 提取右侧所有内容
    right_content = []
    for j in range(5, len(row)):
        if pd.notna(row[j]) and str(row[j]).strip():
            right_content.append(str(row[j]).strip())
    
    if row_courses or right_content:
        print(f"\n行{i:2d}:")
        if row_courses:
            print(f"  课程: {row_courses}")
        if right_content:
            print(f"  右侧: {right_content}")
