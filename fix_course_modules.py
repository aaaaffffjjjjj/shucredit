#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修复微电子学院课程的模块关联问题"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from app import Module, Course

def fix_microelectronics_courses():
    with app.app_context():
        print("修复微电子学院课程的模块关联...")
        
        # 获取微电子学院的专业基础课程模块
        micro_major = None
        from app import Major
        majors = Major.query.all()
        for m in majors:
            if '微电子' in m.name:
                micro_major = m
                break
        
        if not micro_major:
            print("错误：未找到微电子相关专业")
            return
        
        print(f"找到专业: {micro_major.name} (ID: {micro_major.id})")
        
        # 获取该专业的专业基础课程模块
        micro_module = Module.query.filter_by(
            name='专业基础课程', 
            major_id=micro_major.id
        ).first()
        
        if not micro_module:
            print("错误：未找到微电子学院的专业基础课程模块")
            return
        
        print(f"微电子学院专业基础课程模块 ID: {micro_module.id}")
        
        # 需要修复的课程
        courses_to_fix = [
            ('JBK1300001', '工程图学'),
            ('JBK5400003', '工程实践B'),
        ]
        
        fixed_count = 0
        for course_code, course_name in courses_to_fix:
            course = Course.query.filter_by(course_code=course_code).first()
            if course:
                old_module = Module.query.get(course.module_id)
                old_college_name = "Unknown"
                if old_module:
                    from app import College
                    old_college = College.query.get(old_module.college_id)
                    old_college_name = old_college.name if old_college else "Unknown"
                
                print(f"\n修复课程: {course_code} - {course_name}")
                print(f"  原模块ID: {course.module_id}")
                print(f"  目标模块ID: {micro_module.id}")
                
                course.module_id = micro_module.id
                fixed_count += 1
            else:
                print(f"\n警告：未找到课程 {course_code} - {course_name}")
        
        db.session.commit()
        print(f"\n修复完成！共修复 {fixed_count} 门课程")

if __name__ == "__main__":
    fix_microelectronics_courses()
