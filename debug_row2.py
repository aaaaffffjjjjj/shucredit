"""
调试行2的模块识别
"""
import os
import sys
import pandas as pd
import re

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app'))

excel_path = os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app', 'uploads', 'sydney_business_25.xlsx')

print("="*100)
print("调试行2的模块识别")
print("="*100)

excel_file = pd.ExcelFile(excel_path)
df = pd.read_excel(excel_path, sheet_name='信管课程25级', header=None)

invalid_phrases = ["未必能完全", "注意", "推测", "简称建议", "选双学位", "各总计", "大一", "大二", "大三", "大四", "前半学期", "后半学期", "夏"]

i = 2
row = df.iloc[i].values

print(f"\n行{i}:")
for j, cell in enumerate(row):
    if pd.notna(cell):
        print(f"  列{j}: {cell}")

# 测试模块识别
cell_content = str(row[5]) if len(row) > 5 and pd.notna(row[5]) else ""
print(f"\n测试内容: '{cell_content}'")

# 检查是否被过滤
is_invalid = False
for phrase in invalid_phrases:
    if phrase in cell_content:
        print(f"  被过滤: 包含 '{phrase}'")
        is_invalid = True
        break
print(f"  是否无效: {is_invalid}")

# 检查模块判断条件
conditions = [
    "模块" in cell_content,
    ("课" in cell_content and "分" in cell_content),
    "必" in cell_content,
    "选修" in cell_content,
    "个性化" in cell_content,
    "创新创业" in cell_content,
    "劳动" in cell_content,
    "Canvas" in cell_content
]
print(f"\n条件检查:")
for i, cond in enumerate(conditions):
    print(f"  条件{i}: {cond}")
print(f"  任一条件满足: {any(conditions)}")
