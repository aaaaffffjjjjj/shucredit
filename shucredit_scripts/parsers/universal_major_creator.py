#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用专业数据生成脚本
适用于所有专业，只需配置专业信息即可
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import app, db, College, Major, Module, Course


# 通用模块模板（适用于大多数工科专业）
GENERAL_MODULE_TEMPLATE = [
    # --- 根模块 ---
    ('公共基础课程', 67.5, None),
    ('通识课程', 8.0, None),
    ('专业基础课程', 52.0, None),
    ('专业必修课程', 18.5, None),
    ('专业选修课程', 4.0, None),
    ('个性化教育课程', 10.0, None),
    ('专业方向模块', 10.0, None),
    
    # --- 公共基础课程的子模块 ---
    ('思政类', 18.5, '公共基础课程'),
    ('军体类', 9.0, '公共基础课程'),
    ('大学英语', 8.0, '公共基础课程'),
    ('人工智能类', 5.0, '公共基础课程'),
    ('国家安全教育', 1.0, '公共基础课程'),
    ('自然科学类', 26.0, '公共基础课程'),
    
    # --- 通识课程的子模块 ---
    ('核心通识课', 2.0, '通识课程'),
    ('跨类通识课', 2.0, '通识课程'),
    ('其他通识课', 4.0, '通识课程'),
    
    # --- 专业选修课程的子模块 ---
    ('专业选修子模块1', 2.0, '专业选修课程'),
    ('专业选修子模块2', 2.0, '专业选修课程'),
    
    # --- 个性化教育课程的子模块 ---
    ('综合工程实践能力培养模块', 10.0, '个性化教育课程'),
]


# 公共基础课程模板（大多数专业通用）
GENERAL_COURSE_TEMPLATE = [
    # --- 思政类 ---
    ('GBK2000001', '形势与政策', 1.0, '思政类'),
    ('GBK2000003', '思想道德与法治', 3.0, '思政类'),
    ('GBK2000004', '中国近现代史纲要', 3.0, '思政类'),
    ('GBK2000002', '形势与政策（实践）', 1.0, '思政类'),
    ('GBK2000005', '马克思主义基本原理', 3.0, '思政类'),
    ('GBK2000006', '毛泽东思想和中国特色社会主义理论体系概论', 3.0, '思政类'),
    ('GBK2000007', '习近平新时代中国特色社会主义思想概论', 3.0, '思政类'),
    
    # --- 军体类 ---
    ('GBK5100001', '军事技能', 2.0, '军体类'),
    ('GBK2000008', '军事理论', 2.0, '军体类'),
    ('GBK2800501', '体质健康促进（1）', 0.5, '军体类'),
    ('GBK2800701', '体质健康促进（2）', 0.5, '军体类'),
    
    # --- 人工智能类 ---
    ('GBK1200001', '程序设计(C语言)', 3.0, '人工智能类'),
    ('GBK1200005', '人工智能基础A', 2.0, '人工智能类'),
    
    # --- 国家安全教育 ---
    ('GBK2000009', '国家安全教育', 1.0, '国家安全教育'),
    
    # --- 自然科学类 ---
    ('GBK0101001', '高等数学A(1)', 5.0, '自然科学类'),
    ('GBK0101002', '高等数学A(2)', 5.0, '自然科学类'),
    ('GBK0103001', '大学物理A(1)', 4.0, '自然科学类'),
    ('GBK0103002', '大学物理A(2)', 4.0, '自然科学类'),
    ('GBK0103003', '大学物理实验A(1)', 1.0, '自然科学类'),
    ('GBK0103004', '大学物理实验A(2)', 1.0, '自然科学类'),
    ('GBK0104001', '大学化学', 2.0, '自然科学类'),
    ('GBK0104002', '大学化学实验', 1.0, '自然科学类'),
    ('GBK0101006', '线性代数', 3.0, '自然科学类'),
]


def create_major_data(major_config, use_template=True):
    """
    创建专业数据的通用函数
    
    Args:
        major_config (dict): 专业配置，包含：
            - college_name (str): 学院名称
            - major_name (str): 专业名称
            - major_code (str): 专业代码
            - modules (list, optional): 自定义模块列表
            - courses (list, optional): 自定义课程列表
            - direction_modules (list, optional): 专业方向模块列表
        
        use_template (bool): 是否使用通用模板
    """
    print("="*80)
    print(f"🏗️  创建专业：{major_config['major_name']}")
    print("="*80)
    
    with app.app_context():
        # 查找或创建学院
        college = College.query.filter_by(name=major_config['college_name']).first()
        if not college:
            college = College(
                name=major_config['college_name'],
                code=major_config.get('college_code', major_config['college_name'][:5])
            )
            db.session.add(college)
            db.session.commit()
            print(f"  📚 创建新学院：{major_config['college_name']}")
        else:
            print(f"  📚 找到学院：{major_config['college_name']}")
        
        # 查找或创建专业
        major = Major.query.filter_by(college_id=college.id, name=major_config['major_name']).first()
        if not major:
            major = Major(
                name=major_config['major_name'],
                code=major_config.get('major_code', major_config['major_name'][:5]),
                college_id=college.id
            )
            db.session.add(major)
            db.session.commit()
            print(f"  🎓 创建新专业：{major_config['major_name']}")
        else:
            print(f"  🎓 找到专业：{major_config['major_name']}")
        
        # 删除该专业的现有模块
        print(f"\n  🧹 清理现有数据...")
        existing_modules = Module.query.filter_by(major_id=major.id).all()
        module_ids = [m.id for m in existing_modules]
        
        if module_ids:
            Course.query.filter(Course.module_id.in_(module_ids)).delete(synchronize_session=False)
        
        Module.query.filter_by(major_id=major.id).delete(synchronize_session=False)
        db.session.commit()
        print(f"  ✅ 已清理 {len(existing_modules)} 个模块")
        
        # 构建模块列表
        modules = []
        
        if use_template:
            modules.extend(GENERAL_MODULE_TEMPLATE)
        
        # 添加专业方向模块
        if 'direction_modules' in major_config:
            modules.extend(major_config['direction_modules'])
        
        # 添加自定义模块
        if 'modules' in major_config:
            modules.extend(major_config['modules'])
        
        # 插入模块
        print(f"\n  📦 正在插入模块...")
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
        print(f"  ✅ 插入了 {len(modules)} 个模块")
        
        # 插入课程
        courses = []
        
        if use_template:
            courses.extend(GENERAL_COURSE_TEMPLATE)
        
        if 'courses' in major_config:
            courses.extend(major_config['courses'])
        
        if courses:
            print(f"\n  📚 正在插入课程...")
            inserted_count = 0
            for course_code, name, credit, module_name in courses:
                module_id = module_map.get(module_name)
                if module_id:
                    # 检查课程是否已存在
                    existing = Course.query.filter_by(course_code=course_code).first()
                    if not existing:
                        course = Course(
                            course_code=course_code,
                            name=name,
                            credit=credit,
                            module_id=module_id
                        )
                        db.session.add(course)
                        inserted_count += 1
            
            db.session.commit()
            print(f"  ✅ 插入了 {inserted_count} 门新课程 (跳过了 {len(courses) - inserted_count} 个重复课程)")
        
        # 显示结果
        print("\n" + "="*80)
        print(f"🎉 {major_config['major_name']} 专业数据创建完成！")
        print("="*80)
        
        module_count = Module.query.filter_by(major_id=major.id).count()
        module_ids = [m.id for m in Module.query.filter_by(major_id=major.id).all()]
        course_count = Course.query.filter(Course.module_id.in_(module_ids)).count()
        
        print(f"\n📊 数据统计：")
        print(f"  - 模块数：{module_count}")
        print(f"  - 课程数：{course_count}")
        
        print(f"\n📁 模块树：")
        modules = Module.query.filter_by(major_id=major.id).order_by(Module.id).all()
        
        for m in modules:
            indent = "  " if m.parent_id is not None else ""
            print(f"{indent}{m.id}. {m.name} ({m.required_credits}学分)")
        
        print("\n" + "="*80)
        print("✅ 完成！")
        print("="*80)


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║        通用专业数据生成器 - 使用说明                          ║
╠══════════════════════════════════════════════════════════════╣
║  方式1：在脚本中配置专业参数                                  ║
║  方式2：导入此模块并调用 create_major_data() 函数            ║
╠══════════════════════════════════════════════════════════════╣
║  示例配置：                                                    ║
║  major_config = {                                             ║
║      'college_name': '计算机工程与科学学院',                  ║
║      'major_name': '计算机科学与技术',                        ║
║      'major_code': 'CS001',                                   ║
║      'direction_modules': [                                   ║
║          ('软件工程方向', 4.0, '专业方向模块'),              ║
║          ('人工智能方向', 4.0, '专业方向模块'),              ║
║          ('网络安全方向', 2.0, '专业方向模块'),              ║
║      ],                                                       ║
║  }                                                            ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # 默认示例：创建计算机科学与技术专业
    example_config = {
        'college_name': '计算机工程与科学学院',
        'major_name': '计算机科学与技术',
        'major_code': 'CS001',
        'direction_modules': [
            ('软件工程方向', 4.0, '专业方向模块'),
            ('人工智能方向', 4.0, '专业方向模块'),
            ('网络安全方向', 2.0, '专业方向模块'),
        ],
    }
    
    print(f"\n🎯 运行示例：创建 {example_config['major_name']} 专业\n")
    
    # 询问是否运行示例
    choice = input("是否运行示例？(y/n): ").strip().lower()
    
    if choice == 'y' or choice == 'yes':
        create_major_data(example_config)
    else:
        print("\n📖 请编辑此脚本或导入此模块以使用自定义配置！")


if __name__ == '__main__':
    main()
