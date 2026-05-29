import os
import pandas as pd

file_path = r'e:\nbainbshuda\shucredit-1\text_classifier_app\static\uploads\25.xlsx'

print(f"正在分析课程表右侧模块信息: {file_path}")
print()

try:
    excel_file = pd.ExcelFile(file_path)
    
    # 重点分析信管课程表，之前看到那里有模块信息
    sheet_name = "信管课程25级"
    print(f"{'='*80}")
    print(f"工作表: {sheet_name}")
    print(f"{'='*80}")
    
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    print(f"形状: {df.shape}")
    print()
    
    # 显示完整内容，包括所有列
    print("完整内容（含右侧模块列）:")
    for i in range(min(50, len(df))):
        row = df.iloc[i].values
        # 显示所有列
        cells = []
        for j, cell in enumerate(row):
            if pd.notna(cell) and str(cell).strip():
                cells.append(f"[{j}]{str(cell).strip()}")
        row_str = " | ".join(cells)
        print(f"{i:2d}: {row_str}")
    print()
            
except Exception as e:
    print(f"读取文件时出错: {e}")
    import traceback
    traceback.print_exc()
