"""
检查全英文课程
"""
import os
import pandas as pd

excel_path = os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app', 'uploads', 'sydney_business_25.xlsx')

print("="*100)
print("检查全英文课程")
print("="*100)

excel_file = pd.ExcelFile(excel_path)
df = pd.read_excel(excel_path, sheet_name='信管课程25级', header=None)

print("\n行13内容:")
row = df.iloc[13].values
for j, cell in enumerate(row):
    if pd.notna(cell):
        print(f"  列{j}: {cell}")

print("\n检查哪些行有课程但可能没有被正确提取:")
for i in range(len(df)):
    row = df.iloc[i].values
    
    has_english_module = False
    for j in range(5, len(row)):
        if pd.notna(row[j]) and "全英文" in str(row[j]):
            has_english_module = True
            break
    
    if has_english_module:
        print(f"\n行{i}:")
        for j in range(5):
            if j < len(row) and pd.notna(row[j]) and str(row[j]).strip():
                print(f"  课程: {row[j]}")
        for j in range(5, len(row)):
            if pd.notna(row[j]) and str(row[j]).strip():
                print(f"  模块: {row[j]}")
