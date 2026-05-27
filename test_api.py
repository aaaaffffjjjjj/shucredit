#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试 API 数据生成"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from app import build_progress_api_payload

# 在测试环境中运行
with app.app_context():
    from app import Student
    
    print("=" * 70)
    print("🧪 测试 API 数据生成")
    print("=" * 70)
    
    # 获取学生
    student = Student.query.filter_by(name='cissiao').first()
    if not student:
        print("❌ 未找到学生 cissiao")
        exit(1)
    
    print(f"\n👤 学生: {student.name}")
    print(f"   college_id: {student.college_id}")
    print(f"   major_id: {student.major_id}")
    
    # 测试构建数据
    print("\n" + "-" * 70)
    print("📡 构建 API payload...")
    
    try:
        payload = build_progress_api_payload(
            student.id, 
            use_cache=False,
            college_id=student.college_id,
            major_id=student.major_id
        )
        
        print(f"\n✅ 成功生成 payload")
        print(f"   - modules: {len(payload.get('modules', []))}")
        if 'sun' in payload:
            print(f"   - sun: {payload['sun']}")
        
        print(f"\n" + "-" * 70)
        print("📋 模块列表:")
        for i, mod in enumerate(payload.get('modules', [])):
            print(f"   {i+1}. {mod.get('name')} ({mod.get('required')}学分)")
        
        print("\n" + "=" * 70)
        print("🎉 API 测试通过！数据可以正常生成")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
