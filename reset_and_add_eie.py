#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重置并添加电子信息工程专业
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, College, Major, Module, Course


def main():
    print("="*80)
    print("🏗️  重置并添加电子信息工程专业")
    print("="*80)
    
    with app.app_context():
        # 清空并重建
        db.drop_all()
        db.create_all()
        
        # 运行快速初始化
        from shucredit_scripts.quick_start import init_all
        init_all()
        
        # 查找学院和专业
        college = College.query.filter_by(name='通信与信息工程学院').first()
        major = Major.query.filter_by(college_id=college.id, name='电子信息工程').first()
        
        # 先删除该专业的模块
        Module.query.filter_by(major_id=major.id).delete(synchronize_session=False)
        db.session.commit()
        
        # 插入模块
        modules = [
            ('公共基础课程', 67.5, None),
            ('通识课程', 8.0, None),
            ('专业基础课程', 52.0, None),
            ('专业必修课程', 18.5, None),
            ('专业选修课程', 4.0, None),
            ('个性化教育课程', 10.0, None),
            ('专业方向模块', 10.0, None),
            ('思政类', 18.5, '公共基础课程'),
            ('军体类', 9.0, '公共基础课程'),
            ('大学英语', 8.0, '公共基础课程'),
            ('人工智能类', 5.0, '公共基础课程'),
            ('国家安全教育', 1.0, '公共基础课程'),
            ('自然科学类', 26.0, '公共基础课程'),
            ('核心通识课', 2.0, '通识课程'),
            ('跨类通识课', 2.0, '通识课程'),
            ('其他通识课', 4.0, '通识课程'),
            ('专业选修子模块1', 2.0, '专业选修课程'),
            ('专业选修子模块2', 2.0, '专业选修课程'),
            ('综合工程实践能力培养模块', 10.0, '个性化教育课程'),
            ('信号处理方向', 4.0, '专业方向模块'),
            ('嵌入式系统方向', 4.0, '专业方向模块'),
            ('智能硬件方向', 2.0, '专业方向模块'),
        ]
        
        module_map = {}
        for mod_name, credits, parent_name in modules:
            parent_id = module_map.get(parent_name) if parent_name else None
            module = Module(
                name=mod_name,
                required_credits=credits,
                parent_id=parent_id,
                college_id=college.id,
                major_id=major.id
            )
            db.session.add(module)
            db.session.flush()
            module_map[mod_name] = module.id
        
        db.session.commit()
        
        # 统计
        print("\n" + "="*80)
        print("✅ 电子信息工程专业已添加！")
        print("="*80)
        
        m_count = Module.query.filter_by(major_id=major.id).count()
        print(f"\n📊 数据统计：")
        print(f"  - 模块数：{m_count}")


if __name__ == '__main__':
    main()
