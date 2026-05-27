#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查用户和学生数据"""

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
    print("📊 检查用户和学生数据")
    print("=" * 70)
    
    # 检查用户
    cursor.execute("SELECT id, username, student_id FROM user")
    users = cursor.fetchall()
    print(f"\n👤 用户数量: {len(users)}")
    for user in users:
        print(f"  - User {user[0]}: {user[1]}, Student ID: {user[2]}")
    
    # 检查学生
    cursor.execute("SELECT id, name, major, college_id, major_id FROM student")
    students = cursor.fetchall()
    print(f"\n🎓 学生数量: {len(students)}")
    for student in students:
        print(f"  - Student {student[0]}: {student[1]}, Major: {student[2]}")
        print(f"      college_id: {student[3]}, major_id: {student[4]}")
    
    # 检查当前模块
    print("\n" + "-" * 70)
    print("📁 当前模块状态:")
    cursor.execute("SELECT id, name, college_id, major_id FROM module WHERE id <= 22")
    for mod in cursor.fetchall():
        print(f"  - Module {mod[0]}: {mod[1]}")
        print(f"      college_id: {mod[2]}, major_id: {mod[3]}")
    
    print("\n" + "=" * 70)
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()
