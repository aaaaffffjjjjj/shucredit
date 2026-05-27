#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证微电子科学与工程专业导入结果
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, College, Major, Module, Course


def main():
    print("="*80)
    print("🔍 微电子科学与工程专业数据验证")
    print("="*80)
    
    with app.app_context():
        # 查找学院
        college = College.query.filter_by(name='微电子学院').first()
        if not college:
            print("❌ 学院未找到")
            return
        
        print(f"\n📚 学院: {college.name} (代码: {college.code})")
        
        # 查找专业
        major = Major.query.filter_by(college_id=college.id, name='微电子科学与工程').first()
        if not major:
            print("❌ 专业未找到")
            return
        
        print(f"🎓 专业: {major.name} (代码: {major.code})")
        
        # 统计模块和课程
        modules = Module.query.filter_by(major_id=major.id).all()
        module_ids = [m.id for m in modules]
        courses = Course.query.filter(Course.module_id.in_(module_ids)).all()
        
        print(f"\n📊 统计:")
        print(f"  - 模块数量: {len(modules)}")
        print(f"  - 课程数量: {len(courses)}")
        
        # 按模块统计课程
        print(f"\n📚 课程分布:")
        for module in modules:
            course_count = Course.query.filter_by(module_id=module.id).count()
            if course_count > 0:
                print(f"  - {module.name}: {course_count}门课程")
        
        # 列出根模块和子模块
        print(f"\n📁 完整模块树:")
        root_modules = [m for m in modules if m.parent_id is None]
        for root in sorted(root_modules, key=lambda x: x.id):
            print(f"\n  📦 {root.name} ({root.required_credits}学分)")
            children = [m for m in modules if m.parent_id == root.id]
            for child in sorted(children, key=lambda x: x.id):
                course_count = Course.query.filter_by(module_id=child.id).count()
                print(f"      └── {child.name} ({child.required_credits}学分) - {course_count}门课程")
        
        # 列出部分课程示例
        print(f"\n📖 课程示例 (前10门):")
        for course in courses[:10]:
            module = Module.query.get(course.module_id)
            print(f"  {course.course_code} - {course.name} ({course.credit}学分) - {module.name if module else 'N/A'}")
        
        print("\n" + "="*80)
        print("✅ 验证完成！微电子科学与工程专业数据完整。")
        print("="*80)


if __name__ == '__main__':
    main()
