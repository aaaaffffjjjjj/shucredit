#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试导入脚本"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from app import College, Major, Module, Course

print("Start testing...")
with app.app_context():
    # 检查学院
    print("Checking colleges...")
    colleges = College.query.all()
    print("College count: %d" % len(colleges))
    for c in colleges:
        print("  - %s (ID: %d)" % (c.name, c.id))
    
    # 检查是否有微电子学院
    college = College.query.filter_by(name="微电子学院").first()
    if college:
        print("\nFound 微电子学院: ID=%d" % college.id)
    else:
        print("\nNot found 微电子学院")
        
    # 检查专业
    print("\nChecking majors...")
    majors = Major.query.all()
    print("Major count: %d" % len(majors))
    
    # 检查模块
    print("\nChecking modules...")
    modules = Module.query.all()
    print("Module count: %d" % len(modules))
    
    # 检查课程
    print("\nChecking courses...")
    courses = Course.query.all()
    print("Course count: %d" % len(courses))

print("\nTest completed")
