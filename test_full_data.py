#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整学院-专业数据检验
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, College, Major, Module


def main():
    print("="*80)
    print("📚 完整学院-专业数据检验")
    print("="*80)
    
    with app.app_context():
        # 先重置
        db.drop_all()
        db.create_all()
        
        # 运行完整填充
        from shucredit_scripts.core.populate_college_majors import CollegeMajorPopulator
        populator = CollegeMajorPopulator()
        populator.populate_all(clear_first=False)
        
        print("\n" + "="*80)
        print("📊 完整数据统计")
        print("="*80)
        
        college_count = College.query.count()
        major_count = Major.query.count()
        module_count = Module.query.count()
        
        print(f"\n学院: {college_count} 个")
        print(f"专业: {major_count} 个")
        print(f"模块: {module_count} 个")
        
        # 检查关键学院
        print("\n🔍 检查关键学院:")
        key_colleges = ['通信与信息工程学院', '微电子学院', '计算机工程与科学学院']
        for name in key_colleges:
            college = College.query.filter_by(name=name).first()
            if college:
                major_count = len(college.majors)
                print(f"  ✅ {name}: {major_count} 个专业")
            else:
                print(f"  ❌ {name} 未找到")
        
        # 列出所有学院
        print("\n📋 完整学院列表:")
        all_colleges = College.query.order_by(College.id).all()
        for i, college in enumerate(all_colleges, 1):
            major_count = len(college.majors)
            print(f"  {i:2d}. {college.name} ({major_count} 个专业)")
        
        print("\n" + "="*80)
        print("✅ 完整数据检验完成！")
        print("="*80)


if __name__ == '__main__':
    main()
