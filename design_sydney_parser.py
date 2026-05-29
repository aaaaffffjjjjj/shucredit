"""
悉尼工商学院Excel文件格式分析与解析器设计

文件特点：
1. 有多个专业的工作表，如"国贸课程25级"、"工管课程25级"、"金融课程25级"、"信管课程25级"
2. 每个课程表的结构：
   - 左侧：按学期排列的课程（大一上、大一下、大一夏、大二上、大二下、大二夏、大三上、大三下、大三夏、大四上、大四下、大四夏）
   - 右侧：模块信息（从列5开始），包含模块名和学分要求
3. 还有对应的"学分食用概况"表，按学分大小分类课程
4. 有一个"课程交叉情况"表，列出课程与各专业的关系

需要解析的模块（以信管为例）：
- 必修
- 必修且Canvas（大三为单双学位必修）
- 双学位必修单学位选修
- 选修课（10分）
- 个性化课（15分）
- 拔尖人才培养模块——优化决策与数智运营模块（15分）
- 专业方向模块——管理实践与创新发展模块（15分）
- 专业方向模块——数字技术与智能前沿模块（15分）
- 创新创业类
- 劳动类
- 全英文课程
"""

import os
import pandas as pd
import re

file_path = r'e:\nbainbshuda\shucredit-1\text_classifier_app\static\uploads\25.xlsx'

print("开始分析悉尼工商学院Excel文件格式...")
print()

try:
    excel_file = pd.ExcelFile(file_path)
    
    # 先查看所有专业的课程表，确认结构
    print("="*80)
    print("检查各专业课程表结构")
    print("="*80)
    for sheet_name in excel_file.sheet_names:
        if "课程" in sheet_name and "学分" not in sheet_name:
            print(f"\n--- 检查: {sheet_name} ---")
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
            
            # 查看前20行，找模块信息
            for i in range(min(20, len(df))):
                row = df.iloc[i].values
                # 查找包含模块信息的单元格
                for j, cell in enumerate(row):
                    if pd.notna(cell) and ("模块" in str(cell) or "课" in str(cell) and "分" in str(cell)):
                        print(f"行{i}, 列{j}: {str(cell)[:60]}")
    
    print("\n" + "="*80)
    print("设计解析策略")
    print("="*80)
    
    # 分析信管课程表，尝试提取模块和课程
    print("\n--- 尝试解析信管课程表 ---")
    sheet_name = "信管课程25级"
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    
    # 先提取课程列表
    courses = []
    for i in range(len(df)):
        row = df.iloc[i].values
        for j in range(5):  # 前5列是学期列
            if pd.notna(row[j]) and str(row[j]).strip() and "大一" not in str(row[j]) and "大二" not in str(row[j]) and "大三" not in str(row[j]) and "大四" not in str(row[j]):
                course_name = str(row[j]).strip()
                if course_name:
                    courses.append(course_name)
    
    print(f"找到课程: {len(courses)}")
    print(f"前10个课程: {courses[:10]}")
    
    # 提取模块信息
    print("\n提取模块信息:")
    modules = []
    for i in range(len(df)):
        row = df.iloc[i].values
        # 从列5开始查找模块信息
        for j in range(5, len(row)):
            if pd.notna(row[j]) and str(row[j]).strip():
                cell_content = str(row[j]).strip()
                # 判断是否是模块信息
                if "模块" in cell_content or "课" in cell_content or "分" in cell_content or "必" in cell_content:
                    print(f"行{i}, 列{j}: {cell_content}")
                    modules.append((i, j, cell_content))
    
    print("\n" + "="*80)
    print("解析策略设计完成")
    print("="*80)
    print("""
解析策略：
1. 检测文件是否是悉尼工商学院格式
2. 提取所有专业工作表名
3. 对每个专业课程表：
   a. 提取课程与学期的映射
   b. 提取右侧的模块信息
   c. 尝试建立课程与模块的关联
4. 从"学分食用概况"表提取学分信息
5. 构建与PDF/标准Excel格式兼容的模块树结构
    """)
            
except Exception as e:
    print(f"出错: {e}")
    import traceback
    traceback.print_exc()
