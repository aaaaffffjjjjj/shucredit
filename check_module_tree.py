#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查模块的树形结构"""

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
    print("🌳 检查模块树形结构")
    print("=" * 70)
    
    # 读取所有模块
    cursor.execute("SELECT id, name, parent_id, required_credits FROM module WHERE id <= 22 ORDER BY id")
    modules = cursor.fetchall()
    
    # 构建映射
    module_dict = {}
    for mod in modules:
        module_dict[mod[0]] = {
            'id': mod[0],
            'name': mod[1],
            'parent_id': mod[2],
            'required_credits': mod[3],
            'children': []
        }
    
    # 构建树
    roots = []
    for mod in modules:
        mod_info = module_dict[mod[0]]
        if mod_info['parent_id'] is None:
            roots.append(mod_info)
        elif mod_info['parent_id'] in module_dict:
            module_dict[mod_info['parent_id']]['children'].append(mod_info)
    
    # 打印树
    print(f"\n📁 模块数量: {len(modules)}")
    print(f"🌿 根模块数量: {len(roots)}")
    
    def print_tree(node, level=0):
        indent = '  ' * level
        status = '✅' if level == 0 else '📦'
        print(f"{indent}{status} {node['id']}. {node['name']} ({node['required_credits']}学分)")
        for child in node['children']:
            print_tree(child, level + 1)
    
    print("\n" + "-" * 70)
    print("📋 模块树:")
    for root in roots:
        print_tree(root)
    
    # 检查孤立模块
    print("\n" + "-" * 70)
    print("🔍 孤立模块检查:")
    all_ids = set(module_dict.keys())
    child_ids = set()
    for mod in modules:
        if mod[2] is not None:
            child_ids.add(mod[0])
    orphan_ids = all_ids - child_ids - set(r['id'] for r in roots)
    if orphan_ids:
        print(f"❌ 发现孤立模块: {list(orphan_ids)}")
    else:
        print("✅ 没有孤立模块")
    
    print("\n" + "=" * 70)
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()
