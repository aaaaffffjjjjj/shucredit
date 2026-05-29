"""
深入分析悉尼工商学院Excel文件中课程与模块的对应关系
"""
import pandas as pd

file_path = r'e:\nbainbshuda\shucredit-1\shucredit_scripts\pdf_app\uploads\sydney_business_25.xlsx'

print("="*100)
print("深入分析悉尼工商学院Excel - 课程与模块的对应关系")
print("="*100)

excel_file = pd.ExcelFile(file_path)

for sheet_name in excel_file.sheet_names:
    if "课程" in sheet_name and "学分" not in sheet_name:
        print(f"\n{'='*100}")
        print(f"工作表: {sheet_name}")
        print('='*100)
        
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        
        # 打印完整内容，显示行索引和列索引
        print(f"\n完整内容 (前50行):")
        print("-"*100)
        for i in range(min(50, len(df))):
            row = df.iloc[i].values
            cells = []
            for j, cell in enumerate(row):
                if pd.notna(cell) and str(cell).strip():
                    cells.append(f"[{j}] {str(cell).strip()[:40]}")
            if cells:
                print(f"行{i:2d}: {' | '.join(cells)}")
        
        print(f"\n{'='*100}")
        print("分析模块区域和课程区域的对应关系")
        print('='*100)
        
        # 分析每一行的右侧是否有模块信息
        print("\n逐行分析:")
        for i in range(min(30, len(df))):
            row = df.iloc[i].values
            
            # 提取左侧课程（前5列）
            left_cells = []
            for j in range(5):
                if pd.notna(row[j]) and str(row[j]).strip():
                    cell_val = str(row[j]).strip()
                    if "大一" not in cell_val and "大二" not in cell_val and "大三" not in cell_val and "大四" not in cell_val:
                        left_cells.append(cell_val)
            
            # 提取右侧模块（列5及以后）
            right_cells = []
            for j in range(5, len(row)):
                if pd.notna(row[j]) and str(row[j]).strip():
                    right_cells.append(f"[{j}] {str(row[j]).strip()[:50]}")
            
            if left_cells or right_cells:
                print(f"\n行{i:2d}:")
                if left_cells:
                    print(f"  课程: {', '.join(left_cells)}")
                if right_cells:
                    print(f"  模块: {', '.join(right_cells)}")
