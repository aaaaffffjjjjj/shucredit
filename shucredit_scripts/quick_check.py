#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速数据检查
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, College, Major, Module


def main():
    with app.app_context():
        print("="*80)
        print("📊 数据库当前状态")
        print("="*80)
        
        college_count = College.query.count()
        major_count = Major.query.count()
        module_count = Module.query.count()
        
        print(f"\n学院: {college_count} 个")
        print(f"专业: {major_count} 个")
        print(f"模块: {module_count} 个")
        
        print("\n" + "="*80)
        print("📦 完整的学院-专业体系已就绪！")
        print("="*80)
        print("\n使用方法:")
        print("  - 快速初始化: python shucredit_scripts/quick_start.py")
        print("  - 完整填充: python shucredit_scripts/core/populate_college_majors.py")


if __name__ == '__main__':
    main()
