import os
import pandas as pd

file_path = r'e:\nbainbshuda\shucredit-1\text_classifier_app\static\uploads\25.xlsx'

print(f"正在深度分析文件: {file_path}")
print()

try:
    excel_file = pd.ExcelFile(file_path)
    print(f"工作表列表: {excel_file.sheet_names}")
    print()
    
    # 重点分析"信管25级学年规划"工作表
    sheet_name = "信管25级学年规划"
    print(f"--- 深度分析工作表: {sheet_name} ---")
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    print(f"形状: {df.shape}")
    print()
    
    # 显示完整的50行
    print("完整的前50行内容:")
    for i in range(min(50, len(df))):
        row = df.iloc[i].values
        row_str = " | ".join(f"[{j}]{str(cell).strip()[:30] if pd.notna(cell) else ''}" 
                            for j, cell in enumerate(row[:10]))
        print(f"行{i:2d}: {row_str}")
    print()
    
    # 也查看一下是否有其他可能的课程设置表
    for sheet_name in excel_file.sheet_names:
        if "信管" not in sheet_name and "港环" not in sheet_name:
            print(f"--- 查看工作表: {sheet_name} ---")
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
            print(f"形状: {df.shape}")
            for i in range(min(10, len(df))):
                row = df.iloc[i].values
                row_str = " | ".join(str(cell).strip()[:30] if pd.notna(cell) else "" for cell in row[:10])
                print(f"行{i:2d}: {row_str}")
            print()
            
except Exception as e:
    print(f"读取文件时出错: {e}")
    import traceback
    traceback.print_exc()
