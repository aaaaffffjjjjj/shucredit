import os
import pandas as pd

file_path = r'e:\nbainbshuda\shucredit-1\text_classifier_app\static\uploads\25.xlsx'

print(f"正在分析文件: {file_path}")
print()

try:
    excel_file = pd.ExcelFile(file_path)
    print(f"工作表列表: {excel_file.sheet_names}")
    print()
    
    for sheet_name in excel_file.sheet_names:
        print(f"--- 工作表: {sheet_name} ---")
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        print(f"形状: {df.shape}")
        print()
        
        # 显示前30行
        print("前30行内容:")
        for i in range(min(30, len(df))):
            row = df.iloc[i].values
            row_str = " | ".join(str(cell).strip() if pd.notna(cell) else "" for cell in row)
            print(f"  行{i}: {row_str}")
        print()
        
except Exception as e:
    print(f"读取文件时出错: {e}")
    import traceback
    traceback.print_exc()
