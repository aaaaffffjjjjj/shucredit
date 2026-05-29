"""调试颜色到模块的映射"""
import os
import openpyxl

excel_path = os.path.join(os.path.dirname(__file__), 'shucredit_scripts', 'pdf_app', 'uploads', 'sydney_business_25.xlsx')

wb = openpyxl.load_workbook(excel_path, data_only=True)
sheet = wb['信管课程25级']

print("="*100)
print("调试颜色到模块的映射")
print("="*100)

color_to_modules = {}
module_invalid_phrases = ["未必能完全", "注意", "推测", "简称建议", "选双学位", "各总计"]

# 收集模块和颜色
for row_idx in range(1, 20):
    row = sheet[row_idx]
    print(f"\n行 {row_idx}:")
    
    for col_idx in range(6, 15):
        if col_idx - 1 >= len(row):
            continue
        cell = row[col_idx - 1]
        if cell.value is None or str(cell.value).strip() == "":
            continue
        
        cell_content = str(cell.value).strip()
        
        # 获取颜色
        color_key = None
        if cell.fill and cell.fill.fgColor and cell.fill.fgColor.rgb:
            color_key = cell.fill.fgColor.rgb
        
        print(f"  列 {col_idx}: '{cell_content}', 颜色: {color_key}")
        
        # 清理模块名
        module_name = cell_content
        
        # 移除括号里的说明
        import re
        module_name = re.sub(r'（[^）]*）', '', module_name).strip()
        module_name = re.sub(r'\([^)]*\)', '', module_name).strip()
        
        # 检查清理后的模块名是否有效
        is_invalid = False
        for phrase in module_invalid_phrases:
            if phrase in module_name:
                is_invalid = True
                break
        if is_invalid:
            continue
        
        # 判断是否是模块信息
        if ("模块" in module_name or 
            ("课" in module_name and "分" in module_name) or 
            "必" in module_name or
            "选修" in module_name or
            "个性化" in module_name or
            "创新创业" in module_name or
            "劳动" in module_name or
            "Canvas" in module_name or
            "全英文" in module_name):
            
            if module_name:
                if color_key:
                    if color_key not in color_to_modules:
                        color_to_modules[color_key] = []
                    if module_name not in color_to_modules[color_key]:
                        color_to_modules[color_key].append(module_name)

print("\n" + "="*100)
print("颜色到模块的映射:")
print("="*100)
for color, modules in color_to_modules.items():
    print(f"\n颜色 {color}:")
    for module in modules:
        print(f"  - {module}")
