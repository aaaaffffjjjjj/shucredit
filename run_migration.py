#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行数据库迁移脚本
"""

import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '24567@Zzy',
    'database': 'student_system',
    'charset': 'utf8mb4'
}

def run_migration():
    print("="*70)
    print("🏗️  运行数据库迁移")
    print("="*70)
    
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 读取迁移文件
        with open('migrations/001_add_college_support.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
        
        # 分割并执行 SQL 语句（按分号）
        # 注意：这个简单的分割不适合复杂的 SQL，但这个迁移文件没问题
        statements = []
        current = []
        in_comment = False
        
        for line in sql.split('\n'):
            line = line.strip()
            
            # 跳过注释
            if line.startswith('--') or line.startswith('#'):
                continue
            
            if not line:
                continue
            
            current.append(line)
            
            if line.endswith(';'):
                statements.append(' '.join(current))
                current = []
        
        if current:
            statements.append(' '.join(current))
        
        print(f"\n📝 找到 {len(statements)} 条 SQL 语句\n")
        
        for i, stmt in enumerate(statements, 1):
            try:
                print(f"  [{i}/{len(statements)}] 执行...")
                cursor.execute(stmt)
                conn.commit()
                print(f"  ✅ 成功")
            except Exception as e:
                # 有些语句可能已经执行过（如 ALTER TABLE），所以忽略错误继续
                print(f"  ⚠️  警告: {e}")
                conn.rollback()
        
        print("\n" + "="*70)
        print("🎉 迁移执行完成！")
        print("="*70)
        
        # 验证
        print("\n📊 验证结果：")
        
        cursor.execute("SHOW TABLES")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"  表: {', '.join(tables)}")
        
        if 'college' in tables:
            cursor.execute("SELECT COUNT(*) FROM college")
            count = cursor.fetchone()[0]
            print(f"  学院数: {count}")
        
        if 'module' in tables:
            cursor.execute("SHOW COLUMNS FROM module LIKE 'college_id'")
            if cursor.fetchone():
                print(f"  ✅ module 表有 college_id 列")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    run_migration()
