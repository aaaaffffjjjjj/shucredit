import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, College, Major, Module, Course

with app.app_context():
    # 检查通信原理B这门课在哪些模块里
    print("=== 查找 '通信原理B' 课程 ===")
    courses = Course.query.filter_by(name="通信原理B").all()
    for c in courses:
        mod = db.session.get(Module, c.module_id)
        if mod:
            major = db.session.get(Major, mod.major_id) if mod.major_id else None
            major_name = major.name if major else "无专业"
            college = db.session.get(College, mod.college_id) if mod.college_id else None
            college_name = college.name if college else "无学院"
            print(f"  课程ID:{c.id} course_code:{c.course_code} 模块ID:{c.module_id} 模块名:{mod.name} 专业:{major_name} 学院:{college_name}")

    print()
    print("=== 查找 JBK1131019 课程号 ===")
    courses = Course.query.filter_by(course_code="JBK1131019").all()
    for c in courses:
        mod = db.session.get(Module, c.module_id)
        if mod:
            major = db.session.get(Major, mod.major_id) if mod.major_id else None
            major_name = major.name if major else "无专业"
            print(f"  课程ID:{c.id} name:{c.name} 模块名:{mod.name} 专业:{major_name}")

    print()
    print("=== 专业选修子模块1的课程（在其他模块中）===")
    sub1_name = "专业选修子模块1（任选一门）"
    courses = Course.query.filter(Course.name.in_([
        "智能信息感知与识别", "电生理技术的应用", "科技写作与交流"
    ])).all()
    for c in courses:
        mod = db.session.get(Module, c.module_id)
        if mod:
            major = db.session.get(Major, mod.major_id) if mod.major_id else None
            major_name = major.name if major else "无专业"
            print(f"  {c.name} -> 模块:{mod.name} 专业:{major_name} course_code:{c.course_code}")