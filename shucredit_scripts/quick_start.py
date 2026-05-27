#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上海大学学分系统 - 快速入门脚本
一键初始化完整的学院-专业-模块体系
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, College, Major, Module, Course, Student, User
from werkzeug.security import generate_password_hash


def init_all():
    """初始化所有数据"""
    print("="*80)
    print("🏗️  上海大学学分系统 - 一键初始化")
    print("="*80)
    
    try:
        with app.app_context():
            # 1. 创建表
            print("\n📋 步骤 1/4: 创建数据库表...")
            db.create_all()
            print("✅ 表创建完成")
            
            # 2. 创建管理员
            print("\n👤 步骤 2/4: 创建管理员账户...")
            if not User.query.filter_by(username='admin').first():
                admin_student = Student(name='管理员', major='系统管理')
                db.session.add(admin_student)
                db.session.flush()
                
                admin_user = User(
                    username='admin',
                    password_hash=generate_password_hash('admin'),
                    student_id=admin_student.id,
                )
                db.session.add(admin_user)
                db.session.commit()
                print("✅ 管理员已创建 (用户名: admin, 密码: admin)")
            else:
                print("ℹ️  管理员已存在")
            
            # 3. 导入学院和专业数据
            print("\n📚 步骤 3/4: 导入学院和专业数据...")
            
            # 完整的学院-专业数据
            COLLEGE_MAJOR_DATA = {
                '通信与信息工程学院': {
                    'code': 'communication',
                    'majors': [
                        ('通信工程', 'TX001'),
                        ('电子信息工程', 'DZ002'),
                        ('光电信息科学与工程', 'GD001'),
                        ('数据科学与大数据技术', 'SJ001'),
                    ]
                },
                '微电子学院': {
                    'code': 'microelectronics',
                    'majors': [
                        ('微电子科学与工程', 'WDZ001'),
                    ]
                },
                '计算机工程与科学学院': {
                    'code': 'cs',
                    'majors': [
                        ('计算机科学与技术', 'JSJ001'),
                        ('智能科学与技术', 'ZN001'),
                        ('网络空间安全', 'WL001'),
                        ('人工智能', 'RG001'),
                    ]
                },
            }
            
            for college_name, college_info in COLLEGE_MAJOR_DATA.items():
                college = College.query.filter_by(name=college_name).first()
                if not college:
                    college = College(name=college_name, code=college_info['code'])
                    db.session.add(college)
                    db.session.commit()
                    print(f"  📚 创建学院: {college_name}")
                
                for major_name, major_code in college_info['majors']:
                    major = Major.query.filter_by(college_id=college.id, name=major_name).first()
                    if not major:
                        major = Major(name=major_name, code=major_code, college_id=college.id)
                        db.session.add(major)
                        db.session.commit()
                        print(f"    🎓 创建专业: {major_name}")
            
            # 4. 为通信工程专业添加完整模块
            print("\n📦 步骤 4/4: 为通信工程专业添加模块...")
            
            tx_college = College.query.filter_by(name='通信与信息工程学院').first()
            tx_major = Major.query.filter_by(college_id=tx_college.id, name='通信工程').first() if tx_college else None
            
            if tx_major:
                # 检查是否已有模块
                existing_modules = Module.query.filter_by(major_id=tx_major.id).count()
                if existing_modules == 0:
                    # 完整模块结构
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
                        ('综合工程实践能力培养模块', 10.0, '个性化教育课程'),
                        ('通信方向', 4.0, '专业方向模块'),
                        ('光通信方向', 4.0, '专业方向模块'),
                        ('AI方向', 2.0, '专业方向模块'),
                    ]
                    
                    module_map = {}
                    for mod_name, credits, parent_name in modules:
                        parent_id = module_map.get(parent_name) if parent_name else None
                        module = Module(
                            name=mod_name,
                            required_credits=credits,
                            parent_id=parent_id,
                            college_id=tx_college.id,
                            major_id=tx_major.id
                        )
                        db.session.add(module)
                        db.session.flush()
                        module_map[mod_name] = module.id
                    
                    db.session.commit()
                    print(f"✅ 为通信工程专业添加了 {len(modules)} 个模块")
                else:
                    print(f"ℹ️  通信工程专业已有 {existing_modules} 个模块")
            
            # 统计结果
            print("\n" + "="*80)
            print("🎉 初始化完成！统计结果:")
            print("="*80)
            
            college_count = College.query.count()
            major_count = Major.query.count()
            module_count = Module.query.count()
            
            print(f"\n📊 统计:")
            print(f"  学院: {college_count} 个")
            print(f"  专业: {major_count} 个")
            print(f"  模块: {module_count} 个")
            
            print("\n" + "="*80)
            print("✅ 全部完成！")
            print("="*80)
            print("\n💡 下一步:")
            print("  1. 启动后端: python app.py")
            print("  2. 启动前端: npm run dev")
            print("  3. 访问 http://localhost:3000")
            print("  4. 登录: admin / admin")
            
            return True
            
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return False


if __name__ == '__main__':
    init_all()
