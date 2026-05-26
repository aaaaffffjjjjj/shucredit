#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复版培养方案导入脚本（支持模块父子关系 + 多学院参数）
功能：
- 自动重建 module, course, enrollment 表（保留学生和用户表）
- 根据数字序号点号数量建立模块层级
- 导入课程并正确归属到叶子模块
- 支持 --college 参数指定学院（名称或 ID）

用法：
  python import_curriculum.py                                          # 默认导入到通信学院
  python import_curriculum.py --college "计算机工程与科学学院"         # 按名称指定学院
  python import_curriculum.py --college_id 13                          # 按 ID 指定学院
  python import_curriculum.py --no-rebuild                             # 不重建表（增量导入）
"""

import argparse
import pdfplumber
import re
from sqlalchemy import text
from app import app, db, Module, Course, Enrollment, College

DEBUG = True


def rebuild_module_tables():
    """删除并重建 module, course, enrollment 表（保留 student 和 user）"""
    print("重建 module, course, enrollment 表...")
    try:
        # 使用 text() 包装原始 SQL
        db.session.execute(text('SET FOREIGN_KEY_CHECKS = 0'))
        db.session.execute(text('DROP TABLE IF EXISTS enrollment'))
        db.session.execute(text('DROP TABLE IF EXISTS course'))
        db.session.execute(text('DROP TABLE IF EXISTS module'))
        db.session.execute(text('SET FOREIGN_KEY_CHECKS = 1'))
        db.session.commit()
        print("旧表已删除")
        # 重新创建所有表（会根据最新模型定义创建）
        db.create_all()
        print("新表已创建")
    except Exception as e:
        print(f"重建表失败: {e}")
        db.session.rollback()
        raise


def get_level_from_number(num_str):
    """
    根据数字序号中的点号数量确定层级
    例如：
        "1"      -> 1
        "1.1"    -> 2
        "1.1.1"  -> 3
    """
    if not num_str:
        return 1
    return num_str.count('.') + 1


def parse_curriculum(pdf_path):
    """
    解析培养方案 PDF，返回：
        modules: list of (name, required_credits, parent_name, number_str)
        courses: list of (code, name, credit, module_name)
    """
    modules = []  # (name, credits, parent_name, number_str)
    courses = []  # (code, name, credit, module_name)
    stack = []  # 元素为 (level, name, number_str)
    current_module = None

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                continue
            if DEBUG:
                print(f"\n===== 第 {page_num} 页（前800字符）=====\n{text[:800]}\n")

            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # ---------- 1. 识别模块标题 ----------
                # 匹配格式：
                #   ## 1. 公共基础课程（67.5学分）
                #   ### 1.1 思政类（18.5学分）
                #   #### 6.1综合工程实践能力培养模块（10学分）
                #   子模块1（任选一门，2学分）   # 没有数字序号，特殊处理
                #   7.1通信方向（任选两门，4学分）  # 无 # 号
                match = re.match(r'^(#*)\s*(\d+(?:\.\d+)*|子模块\d+)\s*(.+?)（(\d+\.?\d*)学分）', line)
                if match:
                    number_str = match.group(2)  # 数字序号 或 "子模块1"
                    name = match.group(3).strip()
                    credits = float(match.group(4))

                    # 清理名称：去除可能残留的前导数字和点（例如 "1.1 " 已经在前面的 group 中分离了，这里一般没有）
                    # 但有时名称中可能包含数字，保留原样

                    # 确定层级
                    if number_str.startswith('子模块'):
                        # 子模块视为第 4 级（最深层）
                        level = 4
                    else:
                        level = get_level_from_number(number_str)

                    # 维护栈：弹出比当前层级高或相等的模块
                    while stack and stack[-1][0] >= level:
                        stack.pop()
                    # 父模块是栈顶模块（如果存在）
                    parent_name = stack[-1][1] if stack else None
                    # 记录模块
                    modules.append((name, credits, parent_name, number_str))
                    # 当前模块入栈
                    stack.append((level, name, number_str))
                    current_module = name
                    if DEBUG:
                        print(f"[模块] {name} 要求 {credits} 学分，层级 {level}，父模块: {parent_name}")
                    continue

                # ---------- 2. 匹配课程行（无竖线） ----------
                course_match = re.match(r'([A-Z]{2,5}\d{6,})\s+([\u4e00-\u9fa5A-Za-z0-9（）·\-]+)\s+(\d+\.?\d*)', line)
                if course_match and current_module:
                    code = course_match.group(1)
                    name = course_match.group(2)
                    credit = float(course_match.group(3))
                    courses.append((code, name, credit, current_module))
                    if DEBUG:
                        print(f"  [课程] {code} {name} {credit} -> {current_module}")
                    continue

                # ---------- 3. 处理带竖线的表格行 ----------
                if '|' in line and current_module:
                    parts = [p.strip() for p in line.split('|') if p.strip()]
                    if len(parts) >= 3:
                        code_candidate = parts[0]
                        name_candidate = parts[1]
                        credit_candidate = parts[2]
                        if re.match(r'[A-Z]{2,5}\d{6,}', code_candidate):
                            credit_match = re.search(r'\d+\.?\d*', credit_candidate)
                            if credit_match:
                                code = code_candidate
                                name = name_candidate
                                credit = float(credit_match.group())
                                courses.append((code, name, credit, current_module))
                                if DEBUG:
                                    print(f"  [课程-竖线] {code} {name} {credit} -> {current_module}")
                                continue

    # 去重课程
    unique_courses = []
    seen = set()
    for c in courses:
        if c[0] not in seen:
            seen.add(c[0])
            unique_courses.append(c)
    return modules, unique_courses


def import_curriculum(pdf_path, college_id=None):
    print("解析培养方案 PDF...")
    modules, courses = parse_curriculum(pdf_path)

    if college_id is None:
        college = College.query.filter_by(code='communication').first()
        if college:
            college_id = college.id
        else:
            print("警告：未找到通信学院，使用 college_id=1")
            college_id = 1

    college_obj = db.session.get(College, college_id)
    college_name = college_obj.name if college_obj else f'ID:{college_id}'
    print(f"导入到学院: {college_name} (ID: {college_id})")

    module_map = {}
    for name, credits, parent_name, number_str in modules:
        mod = Module(
            name=name,
            required_credits=credits,
            parent_id=None,
            college_id=college_id,
        )
        db.session.add(mod)
        module_map[name] = mod
    db.session.commit()
    print(f"创建了 {len(modules)} 个模块")

    # 第二步：更新 parent_id 关系
    for name, credits, parent_name, number_str in modules:
        if parent_name:
            parent = module_map.get(parent_name)
            if parent:
                module_map[name].parent_id = parent.id
            else:
                print(f"警告：找不到父模块 {parent_name}，模块 {name} 将保持无父模块")
    db.session.commit()
    print("模块父子关系已建立")

    # 第三步：插入课程
    course_count = 0
    for code, name, credit, mod_name in courses:
        mod = module_map.get(mod_name)
        if not mod:
            print(f"警告：课程 {code} 所属模块 {mod_name} 不存在，跳过")
            continue
        if not Course.query.filter_by(course_code=code).first():
            db.session.add(Course(course_code=code, name=name, credit=credit, module_id=mod.id))
            course_count += 1
            if DEBUG:
                print(f"新增课程: {code} {name} {credit} -> {mod_name}")
        else:
            print(f"课程已存在: {code}（跳过）")
    db.session.commit()
    print(f"共新增 {course_count} 门课程")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='导入培养方案 PDF')
    parser.add_argument(
        '--college', type=str, default=None,
        help='学院名称（如 "计算机工程与科学学院"）',
    )
    parser.add_argument(
        '--college_id', type=int, default=None,
        help='学院 ID（如 13）',
    )
    parser.add_argument(
        '--no-rebuild', action='store_true',
        help='不重建表（增量导入）',
    )
    parser.add_argument(
        '--pdf', type=str, default=None,
        help='PDF 文件路径（可选，默认使用通信工程 PDF）',
    )
    args = parser.parse_args()

    pdf_file = args.pdf or r'D:\Dev\studentsystem\通信工程专业学分结构最终版 含课程编号.pdf'

    with app.app_context():
        if not args.no_rebuild:
            rebuild_module_tables()

        if args.college_id:
            college_id = args.college_id
        elif args.college:
            college = College.query.filter_by(name=args.college).first()
            if college:
                college_id = college.id
            else:
                print(f"错误：未找到学院 '{args.college}'")
                print("可用的学院列表：")
                for c in College.query.order_by(College.id).all():
                    print(f"  {c.id}: {c.name} ({c.code})")
                exit(1)
        else:
            college_id = None

        import_curriculum(pdf_file, college_id=college_id)
        print("导入完成！")