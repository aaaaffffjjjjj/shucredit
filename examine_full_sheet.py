"""完整查看Excel文件的前100行"""
import os
import openpyxl

excel_path = os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app', 'uploads', 'sydney_business_25.xlsx')

print("="*150)
print("悉尼工商学院Excel完整查看")
print("="*150)

wb = openpyxl.load_workbook(excel_path, data_only=True)
sheet = wb['信管课程25级']

for row_idx in range(1, min(101, sheet.max_row + 1)):
    row = sheet[row_idx]
    values = []
    for col_idx, cell in enumerate(row, 1):
        if cell.value is not None and str(cell.value).strip() != "":
            val = str(cell.value).strip()
            # 获取填充颜色
            color_info = ""
            if cell.fill and cell.fill.fgColor and cell.fill.fgColor.rgb:
                color = cell.fill.fgColor.rgb
                if color == 'FFFFFF00':
                    color_info = " [黄]"
                elif color == 'FF00B050':
                    color_info = " [绿]"
                elif color == '00000000':
                    color_info = " [无]"
                else:
                    color_info = f" [{color}]"
            values.append(f"[{col_idx}]{val}{color_info}")
    if values:
        print(f"\n行{row_idx:2d}: " + " | ".join(values))
