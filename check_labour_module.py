"""
检查劳动类模块
"""
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app'))

from app import SmartExcelParser

excel_path = os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app', 'uploads', 'sydney_business_25.xlsx')

print("="*100)
print("检查劳动类模块")
print("="*100)

parser = SmartExcelParser()
parser.parse(excel_path, '信管课程25级', 'sydney_business_25.xlsx')
result = parser.get_result()

print("\n所有模块:")
for mod in result['modules']:
    print(f"  {mod['id']}. {mod['name']}")

# 检查是否有劳动类模块
has_labour = any("劳动" in mod['name'] for mod in result['modules'])
print(f"\n是否有劳动类模块: {has_labour}")

if not has_labour:
    print("\n让我们看看原始解析过程:")
    import pandas as pd
    df = pd.read_excel(excel_path, sheet_name='信管课程25级', header=None)
    
    print(f"\n行11内容:")
    row = df.iloc[11].values
    for j, cell in enumerate(row):
        if pd.notna(cell):
            print(f"  列{j}: {cell}")
