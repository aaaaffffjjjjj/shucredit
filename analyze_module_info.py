import os
import pandas as pd

file_path = r'e:\nbainbshuda\shucredit-1\text_classifier_app\static\uploads\25.xlsx'

print(f"正在分析模块信息: {file_path}")
print()

try:
    excel_file = pd.ExcelFile(file_path)
    
    # 分析各个专业的学分食用概况表，重点看右侧的模块信息
    for sheet_name in excel_file.sheet_names:
        if "学分食用概况" in sheet_name:
            print(f"{'='*70}")
            print(f"工作表: {sheet_name}")
            print(f"{'='*70}")
            
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
            print(f"形状: {df.shape}")
            print()
            
            # 显示所有行，包括右侧的列
            print("完整内容（含右侧模块列）:")
            for i in range(min(30, len(df))):
                row = df.iloc[i].values
                # 显示所有列，前面的是学分分类，后面的是模块信息
                row_str = " | ".join(f"{j}:{str(cell).strip()[:45]}" 
                                    if pd.notna(cell) else f"{j}:"
                                    for j, cell in enumerate(row))
                print(f"{i:2d}: {row_str}")
            print()
            
except Exception as e:
    print(f"读取文件时出错: {e}")
    import traceback
    traceback.print_exc()
