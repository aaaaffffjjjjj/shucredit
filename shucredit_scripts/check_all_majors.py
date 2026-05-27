#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查看所有学院和专业的数据
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, College, Major, Module, Course


def main():
    with app.app_context():
        print("="*80)
        print("📊 完整学院-专业-模块结构")
        print("="*80)
        
        for college in College.query.order_by(College.id).all():
            print(f"\n📚 学院：{college.name}")
            for major in college.majors:
                module_count = Module.query.filter_by(major_id=major.id).count()
                module_ids = [m.id for m in Module.query.filter_by(major_id=major.id).all()]
                course_count = Course.query.filter(Course.module_id.in_(module_ids)).count()
                print(f"  🎓 专业：{major.name} (模块：{module_count}, 课程：{course_count})")
                
                if module_count > 0:
                    modules = Module.query.filter_by(major_id=major.id).order_by(Module.id).all()
                    module_dict = {m.id: m for m in modules}
                    
                    print(f"    📁 模块树：")
                    for m in modules:
                        indent = "      " if m.parent_id is not None else "    "
                        print(f"{indent}{m.id}. {m.name} ({m.required_credits}学分)")
        
        print("\n" + "="*80)
        print("✅ 查看完成！")
        print("="*80)


if __name__ == '__main__':
    main()
