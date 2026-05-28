import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, College, Major, Module, Course

with app.app_context():
    college = College.query.filter_by(name="通信与信息工程学院").first()
    if college:
        print(f"学院: {college.name} (ID: {college.id})")
        majors = Major.query.filter_by(college_id=college.id).all()
        print(f"该学院下的专业:")
        for m in majors:
            print(f"  ID:{m.id} {m.name}")
            modules = Module.query.filter_by(major_id=m.id).count()
            print(f"    模块数: {modules}")
    else:
        print("未找到通信与信息工程学院")

    print()
    # 检查XBK1130001等课程号在哪些专业
    print("=== 查找 XBK1130001 ===")
    courses = Course.query.filter_by(course_code="XBK1130001").all()
    for c in courses:
        mod = db.session.get(Module, c.module_id)
        if mod:
            major = db.session.get(Major, mod.major_id) if mod.major_id else None
            print(f"  课程:{c.name} course_code:{c.course_code} 模块:{mod.name} 专业:{major.name if major else 'N/A'}")

    print()
    print("=== 电子信息工程 vs 通信工程 ===")
    major1 = Major.query.filter_by(name="电子信息工程", college_id=11).first()
    major2 = Major.query.filter_by(name="通信工程", college_id=11).first()
    print(f"电子信息工程: ID={major1.id if major1 else 'N/A'}")
    print(f"通信工程: ID={major2.id if major2 else 'N/A'}")