import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, College, Major, Module, Course

with app.app_context():
    college = College.query.filter_by(name="通信与信息工程学院").first()
    if not college:
        print("ERROR: 找不到通信与信息工程学院")
        exit()

    major = Major.query.filter_by(name="电子信息工程", college_id=college.id).first()
    if not major:
        print("ERROR: 找不到电子信息工程专业")
        exit()

    print(f"学院: {college.name} (ID: {college.id})")
    print(f"专业: {major.name} (ID: {major.id})")
    print()

    # 获取该专业的所有模块
    modules = Module.query.filter_by(major_id=major.id).all()
    print(f"=== 专业基础课程模块 ===")
    professional_base = Module.query.filter_by(name="专业基础课程", major_id=major.id).first()
    if professional_base:
        print(f"模块ID: {professional_base.id}, 名称: {professional_base.name}")
        courses = Course.query.filter_by(module_id=professional_base.id).all()
        print(f"课程数量: {len(courses)}")
        for c in courses[:10]:
            print(f"  - {c.course_code} {c.name} ({c.credit}学分) -> module_id={c.module_id}")
        if len(courses) > 10:
            print(f"  ... 还有 {len(courses) - 10} 门课程")
    else:
        print("未找到专业基础课程模块")

    print()
    print(f"=== 专业选修课程模块 ===")
    elective = Module.query.filter_by(name="专业选修课程", major_id=major.id).first()
    if elective:
        print(f"模块ID: {elective.id}, 名称: {elective.name}")
        courses = Course.query.filter_by(module_id=elective.id).all()
        print(f"课程数量: {len(courses)}")
        for c in courses:
            print(f"  - {c.course_code} {c.name} ({c.credit}学分)")
    else:
        print("未找到专业选修课程模块")

    print()
    print("=== 专业选修子模块1 ===")
    sub1 = Module.query.filter_by(name="专业选修子模块1（任选一门）", major_id=major.id).first()
    if sub1:
        print(f"模块ID: {sub1.id}, 名称: {sub1.name}")
        courses = Course.query.filter_by(module_id=sub1.id).all()
        print(f"课程数量: {len(courses)}")
        for c in courses:
            print(f"  - {c.course_code} {c.name} ({c.credit}学分)")
    else:
        print("未找到专业选修子模块1")

    print()
    print("=== 所有顶级模块 ===")
    for m in modules:
        if m.parent_id is None:
            print(f"ID:{m.id} {m.name}")