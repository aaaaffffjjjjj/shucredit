#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具包准确性检验脚本
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, College, Major, Module, Course, User, Student


def reset_database():
    """重置数据库"""
    print("="*80)
    print("🧹 步骤 1/4: 重置数据库...")
    print("="*80)
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("✅ 数据库已重置")


def test_quick_start():
    """测试quick_start.py"""
    print("\n" + "="*80)
    print("🚀 步骤 2/4: 运行quick_start.py初始化...")
    print("="*80)
    
    # 导入并运行quick_start
    from shucredit_scripts.quick_start import init_all
    result = init_all()
    print(f"\nquick_start执行结果: {'✅ 成功' if result else '❌ 失败'}")
    
    return result


def verify_data():
    """验证数据准确性"""
    print("\n" + "="*80)
    print("🔍 步骤 3/4: 验证数据...")
    print("="*80)
    
    with app.app_context():
        results = {
            'colleges': College.query.count(),
            'majors': Major.query.count(),
            'modules': Module.query.count(),
            'courses': Course.query.count(),
            'students': Student.query.count(),
            'users': User.query.count(),
        }
        
        print("\n📊 数据统计:")
        for key, value in results.items():
            print(f"  {key}: {value}")
        
        # 验证学院
        print("\n📚 学院列表:")
        colleges = College.query.all()
        for college in colleges:
            major_count = len(college.majors)
            print(f"  ✅ {college.name} (代码: {college.code}, {major_count} 个专业)")
        
        # 验证通信工程专业模块
        print("\n📦 通信工程专业模块:")
        tx_college = College.query.filter_by(name='通信与信息工程学院').first()
        tx_major = Major.query.filter_by(college_id=tx_college.id, name='通信工程').first() if tx_college else None
        
        if tx_major:
            modules = Module.query.filter_by(major_id=tx_major.id).order_by(Module.id).all()
            print(f"  ✅ 共 {len(modules)} 个模块")
            
            module_tree = {}
            for mod in modules:
                if mod.parent_id is None:
                    module_tree[mod.id] = {
                        'name': mod.name,
                        'credits': mod.required_credits,
                        'children': []
                    }
            
            for mod in modules:
                if mod.parent_id is not None and mod.parent_id in module_tree:
                    module_tree[mod.parent_id]['children'].append({
                        'name': mod.name,
                        'credits': mod.required_credits
                    })
            
            print("\n  📁 模块树:")
            for mid, data in module_tree.items():
                print(f"    📦 {data['name']} ({data['credits']} 学分)")
                for child in data['children']:
                    print(f"        └── {child['name']} ({child['credits']} 学分)")
        
        return results


def generate_report(results):
    """生成检验报告"""
    print("\n" + "="*80)
    print("📋 步骤 4/4: 生成检验报告")
    print("="*80)
    
    report = []
    report.append("="*80)
    report.append("上海大学学分系统工具包检验报告")
    report.append("="*80)
    report.append("")
    
    # 检查要点
    checks = [
        ('学院数量', results['colleges'] > 0, results['colleges']),
        ('专业数量', results['majors'] > 0, results['majors']),
        ('模块数量', results['modules'] > 0, results['modules']),
        ('学生账户', results['students'] > 0, results['students']),
        ('用户账户', results['users'] > 0, results['users']),
    ]
    
    report.append("✅ 检查项目:")
    all_passed = True
    for name, passed, value in checks:
        status = "✅ 通过" if passed else "❌ 未通过"
        report.append(f"  {status}: {name} = {value}")
        if not passed:
            all_passed = False
    
    report.append("")
    report.append("✅ 通信工程专业模块检查:")
    with app.app_context():
        tx_college = College.query.filter_by(name='通信与信息工程学院').first()
        tx_major = Major.query.filter_by(college_id=tx_college.id, name='通信工程').first() if tx_college else None
        
        if tx_major:
            modules = Module.query.filter_by(major_id=tx_major.id).all()
            required_modules = ['公共基础课程', '通识课程', '专业基础课程', '专业必修课程', 
                               '专业选修课程', '个性化教育课程', '专业方向模块']
            
            module_names = [m.name for m in modules]
            missing = [name for name in required_modules if name not in module_names]
            
            if not missing:
                report.append("  ✅ 核心模块完整")
            else:
                report.append(f"  ❌ 缺失模块: {missing}")
    
    report.append("")
    report.append("="*80)
    if all_passed:
        report.append("🎉 检验通过！工具包可以正常使用！")
    else:
        report.append("⚠️  部分检验未通过，请检查相关配置")
    report.append("="*80)
    
    report_text = '\n'.join(report)
    print(report_text)
    
    # 保存报告
    with open('shucredit_scripts/检验报告.txt', 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(f"\n📄 报告已保存: shucredit_scripts/检验报告.txt")
    
    return all_passed


def main():
    print("="*80)
    print("🔍 工具包准确性检验")
    print("="*80)
    
    try:
        # 1. 重置数据库
        reset_database()
        
        # 2. 运行quick_start
        test_quick_start()
        
        # 3. 验证数据
        results = verify_data()
        
        # 4. 生成报告
        generate_report(results)
        
        print("\n" + "="*80)
        print("✅ 检验完成！")
        print("="*80)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
