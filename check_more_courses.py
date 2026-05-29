"""
检查Excel中是否还有更多课程可以提取
"""
import os
import pandas as pd

excel_path = os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app', 'uploads', 'sydney_business_25.xlsx')

print("="*100)
print("检查Excel中所有课程")
print("="*100)

excel_file = pd.ExcelFile(excel_path)
df = pd.read_excel(excel_path, sheet_name='信管课程25级', header=None)

print(f"Excel形状: {df.shape}")
print("\n所有前5列的内容:")
print("-"*100)

all_courses = []
invalid_phrases = ["大一", "大二", "大三", "大四", "前半学期", "后半学期", "夏"]

for i in range(len(df)):
    row = df.iloc[i].values
    for j in range(5):
        if j < len(row) and pd.notna(row[j]) and str(row[j]).strip():
            course_name = str(row[j]).strip()
            
            # 检查是否是无效内容
            is_invalid = False
            for phrase in invalid_phrases:
                if phrase in course_name:
                    is_invalid = True
                    break
            if len(course_name) < 2:
                is_invalid = True
            
            if not is_invalid:
                all_courses.append((i, j, course_name))

print(f"\n找到 {len(all_courses)} 个可能的课程:")
print("-"*100)
for i, j, course_name in all_courses:
    print(f"  行{i:2d} 列{j}: {course_name}")

print(f"\n去重后有 {len(set(c for i,j,c in all_courses))} 个唯一课程")
