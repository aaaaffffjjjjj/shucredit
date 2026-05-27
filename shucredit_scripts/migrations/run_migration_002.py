#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行专业支持迁移脚本
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
    print("🏗️  运行专业支持迁移")
    print("="*70)
    
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 读取迁移文件
        with open('migrations/002_add_major_support.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
        
        # 执行
        statements = []
        current = []
        
        for line in sql.split('\n'):
            line = line.strip()
            
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
        
        if 'major' in tables:
            print(f"  ✅ major 表已创建")
        
        if 'module' in tables:
            cursor.execute("SHOW COLUMNS FROM module LIKE 'major_id'")
            if cursor.fetchone():
                print(f"  ✅ module 表有 major_id 列")
        
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
