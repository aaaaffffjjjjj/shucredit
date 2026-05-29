import os
import pandas as pd

def analyze_excel_files():
    upload_dir = r'e:\nbainbshuda\shucredit-1\shucredit_scripts\pdf_app\uploads'
    
    print(f"正在检查目录: {upload_dir}\n")
    
    for filename in os.listdir(upload_dir):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(upload_dir, filename)
            print(f"=" * 60)
            print(f"文件: {filename}")
            print(f"路径: {file_path}")
            print("=" * 60)
            
            try:
                excel_file = pd.ExcelFile(file_path)
                print(f"工作表列表: {excel_file.sheet_names}")
                print()
                
                for sheet_name in excel_file.sheet_names:
                    print(f"--- 工作表: {sheet_name} ---")
                    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
                    print(f"形状: {df.shape}")
                    print()
                    
                    # 显示前20行
                    print("前20行内容:")
                    for i in range(min(20, len(df))):
                        row = df.iloc[i].values
                        row_str = " | ".join(str(cell).strip() if pd.notna(cell) else "" for cell in row)
                        print(f"  行{i}: {row_str}")
                    print()
                    
            except Exception as e:
                print(f"读取文件时出错: {e}")
                print()

if __name__ == "__main__":
    analyze_excel_files()
