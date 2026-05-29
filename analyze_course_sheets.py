import os
import pandas as pd

file_path = r'e:\nbainbshuda\shucredit-1\text_classifier_app\static\uploads\25.xlsx'

print(f"正在分析课程表工作表: {file_path}")
print()

try:
    excel_file = pd.ExcelFile(file_path)
    
    # 分析课程相关的工作表
    for sheet_name in excel_file.sheet_names:
        if "课程" in sheet_name and "学分" not in sheet_name:
            print(f"{'='*60}")
            print(f"工作表: {sheet_name}")
            print(f"{'='*60}")
            
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
            print(f"形状: {df.shape}")
            print()
            
            # 显示所有行（最多100行）
            print("所有内容:")
            for i in range(min(100, len(df))):
                row = df.iloc[i].values
                row_str = " | ".join(f"{str(cell).strip()[:40]}" 
                                    if pd.notna(cell) else "" 
                                    for cell in row[:15])
                print(f"{i:3d}: {row_str}")
            print()
            
except Exception as e:
    print(f"读取文件时出错: {e}")
    import traceback
    traceback.print_exc()
