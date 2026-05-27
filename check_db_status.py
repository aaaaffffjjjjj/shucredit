#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查数据库状态"""

import pymysql

config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '24567@Zzy',
    'database': 'student_system',
    'charset': 'utf8mb4'
}

try:
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    
    print("=" * 70)
    print("📊 数据库状态检查")
    print("=" * 70)
    
    # 检查 College
    cursor.execute("SELECT COUNT(*) FROM college")
    college_count = cursor.fetchone()[0]
    print(f"\n📚 College 表: {college_count} 条记录")
    if college_count > 0:
        cursor.execute("SELECT * FROM college")
        for row in cursor.fetchall():
            print(f"  - {row}")
    
    # 检查 Major
    cursor.execute("SELECT COUNT(*) FROM major")
    major_count = cursor.fetchone()[0]
    print(f"\n🎓 Major 表: {major_count} 条记录")
    if major_count > 0:
        cursor.execute("SELECT * FROM major")
        for row in cursor.fetchall():
            print(f"  - {row}")
    
    # 检查 Module
    cursor.execute("SELECT COUNT(*) FROM module")
    module_count = cursor.fetchone()[0]
    print(f"\n📁 Module 表: {module_count} 条记录")
    if module_count > 0:
        cursor.execute("SELECT id, name, college_id, major_id FROM module LIMIT 10")
        for row in cursor.fetchall():
            print(f"  - {row}")
    
    # 检查 Course
    cursor.execute("SELECT COUNT(*) FROM course")
    course_count = cursor.fetchone()[0]
    print(f"\n📖 Course 表: {course_count} 条记录")
    
    print("\n" + "=" * 70)
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()
