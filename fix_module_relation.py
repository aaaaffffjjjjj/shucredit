#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复模块的 college_id 和 major_id 关联"""

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
    print("🔧 修复模块关联")
    print("=" * 70)
    
    college_id = 12  # 通信与信息工程学院
    major_id = 177   # 通信工程
    
    # 更新所有模块
    cursor.execute("""
        UPDATE module 
        SET college_id = %s, major_id = %s
        WHERE id BETWEEN 1 AND 22
    """, (college_id, major_id))
    
    connection.commit()
    
    print(f"\n✅ 已更新 {cursor.rowcount} 个模块")
    print(f"   college_id = {college_id} (通信与信息工程学院)")
    print(f"   major_id = {major_id} (通信工程)")
    
    # 验证
    print("\n" + "-" * 70)
    print("📊 验证更新结果:")
    
    cursor.execute("SELECT id, name, college_id, major_id FROM module LIMIT 10")
    for row in cursor.fetchall():
        print(f"  - {row}")
    
    print("\n" + "=" * 70)
    print("✅ 修复完成！")
    print("=" * 70)
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()
