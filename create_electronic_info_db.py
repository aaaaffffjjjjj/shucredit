#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建电子信息工程专业的数据库
使用工具包的ORM模型
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, College, Major, Module, Course


def create_electronic_info_db():
    print("="*80)
    print("🏗️  创建电子信息工程专业数据库")
    print("="*80)
    
    try:
        with app.app_context():
            # 查找学院和专业
            print("\n📚 查找学院和专业...")
            college = College.query.filter_by(name='通信与信息工程学院').first()
            major = Major.query.filter_by(college_id=college.id, name='电子信息工程').first() if college else None
            
            if not college:
                print("❌ 未找到通信与信息工程学院，请先运行quick_start.py")
                return
            
            if not major:
                print("❌ 未找到电子信息工程专业，请先运行quick_start.py")
                return
            
            print(f"✅ 找到: {college.name} -> {major.name}")
            
            # 删除该专业的现有模块和课程
            print("\n🧹 清理现有数据...")
            existing_modules = Module.query.filter_by(major_id=major.id).all()
            module_ids = [m.id for m in existing_modules]
            
            if module_ids:
                Course.query.filter(Course.module_id.in_(module_ids)).delete(synchronize_session=False)
            
            Module.query.filter_by(major_id=major.id).delete(synchronize_session=False)
            db.session.commit()
            print(f"✅ 已清理 {len(existing_modules)} 个模块")
            
            # 插入模块（与通信工程类似，调整专业方向模块）
            print("\n📦 正在插入模块...")
            
            modules = [
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
                
                # --- 专业方向模块（电子信息工程特色方向） ---
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
            print(f"✅ 插入了 {len(modules)} 个模块")
            
            # 插入课程（公共基础部分与通信工程相同，专业部分使用电子信息工程的课程）
            print("\n📚 正在插入课程...")
            
            courses = [
                # --- 公共基础课程（与通信工程相同） ---
                ('GBK2000001', '形势与政策', 1.0, '思政类'),
                ('GBK2000003', '思想道德与法治', 3.0, '思政类'),
                ('GBK2000004', '中国近现代史纲要', 3.0, '思政类'),
                ('GBK2000002', '形势与政策（实践）', 1.0, '思政类'),
                ('GBK2000005', '马克思主义基本原理', 3.0, '思政类'),
                ('GBK2000006', '毛泽东思想和中国特色社会主义理论体系概论', 3.0, '思政类'),
                ('GBK2000007', '习近平新时代中国特色社会主义思想概论', 3.0, '思政类'),
                
                ('GBK5100001', '军事技能', 2.0, '军体类'),
                ('GBK2000008', '军事理论', 2.0, '军体类'),
                ('GBK2800501', '体质健康促进（1）', 0.5, '军体类'),
                ('GBK2800701', '体质健康促进（2）', 0.5, '军体类'),
                
                ('GBK1200001', '程序设计(C语言)', 3.0, '人工智能类'),
                ('GBK1200005', '人工智能基础A', 2.0, '人工智能类'),
                
                ('GBK2000009', '国家安全教育', 1.0, '国家安全教育'),
                
                ('GBK0101001', '高等数学A(1)', 5.0, '自然科学类'),
                ('GBK0101002', '高等数学A(2)', 5.0, '自然科学类'),
                ('GBK0103001', '大学物理A(1)', 4.0, '自然科学类'),
                ('GBK0103002', '大学物理A(2)', 4.0, '自然科学类'),
                ('GBK0103003', '大学物理实验A(1)', 1.0, '自然科学类'),
                ('GBK0103004', '大学物理实验A(2)', 1.0, '自然科学类'),
                ('GBK0104001', '大学化学', 2.0, '自然科学类'),
                ('GBK0104002', '大学化学实验', 1.0, '自然科学类'),
                ('GBK0101006', '线性代数', 3.0, '自然科学类'),
                
                # --- 专业基础课程（电子信息工程特色） ---
                ('JBK0205001', '电路分析', 4.0, '专业基础课程'),
                ('JBK0205002', '模拟电子技术', 4.0, '专业基础课程'),
                ('JBK0205003', '数字电子技术', 4.0, '专业基础课程'),
                ('JBK0205004', '信号与系统', 4.0, '专业基础课程'),
                ('JBK0205005', '电磁场与电磁波', 3.0, '专业基础课程'),
                ('JBK0205006', '通信原理', 4.0, '专业基础课程'),
                ('JBK0205007', '电子技术实验(1)', 0.5, '专业基础课程'),
                ('JBK0205008', '电子技术实验(2)', 1.0, '专业基础课程'),
                ('JBK0205009', '数字信号处理', 3.0, '专业基础课程'),
                ('JBK0205010', '单片机原理', 3.0, '专业基础课程'),
                
                # --- 专业必修课程 ---
                ('BBK0205001', '高频电子线路', 3.0, '专业必修课程'),
                ('BBK0205002', '数字通信原理', 3.0, '专业必修课程'),
                ('BBK0205003', '微机原理与接口技术', 4.0, '专业必修课程'),
                ('BBK0205004', 'EDA技术', 2.0, '专业必修课程'),
                ('BBK0205005', 'DSP技术', 2.0, '专业必修课程'),
                ('BBK0205006', '认识实习', 1.0, '专业必修课程'),
                ('BBK0205007', '电子实习', 1.0, '专业必修课程'),
                ('BBK0205008', '计算机实习', 1.0, '专业必修课程'),
                
                # --- 专业选修课程 ---
                ('XBK0205001', '现代交换原理', 2.0, '专业选修子模块1'),
                ('XBK0205002', '光纤通信', 2.0, '专业选修子模块1'),
                ('XBK0205003', '移动通信', 2.0, '专业选修子模块1'),
                ('XBK0205004', '信息论与编码', 2.0, '专业选修子模块2'),
                ('XBK0205005', '通信网络基础', 2.0, '专业选修子模块2'),
                ('XBK0205006', '数字图像处理', 2.0, '专业选修子模块2'),
                ('XBK0205007', '嵌入式系统设计', 2.0, '专业选修子模块2'),
                ('XBK0205008', '电子设计自动化', 2.0, '专业选修子模块2'),
                
                # --- 专业方向模块 ---
                ('XBK0205009', '数字信号处理与MATLAB', 2.0, '信号处理方向'),
                ('XBK0205010', '自适应信号处理', 2.0, '信号处理方向'),
                ('XBK0205011', '嵌入式操作系统', 2.0, '嵌入式系统方向'),
                ('XBK0205012', 'ARM体系结构', 2.0, '嵌入式系统方向'),
                ('XBK0205013', 'FPGA开发与应用', 2.0, '智能硬件方向'),
            ]
            
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
            print(f"✅ 插入了 {inserted_count} 门新课程 (跳过了 {len(courses) - inserted_count} 个重复课程)")
            
            print("\n" + "="*80)
            print("🎉 电子信息工程专业数据库创建完成！")
            print("="*80)
            
            # 验证
            module_count = Module.query.filter_by(major_id=major.id).count()
            module_ids = [m.id for m in Module.query.filter_by(major_id=major.id).all()]
            course_count = Course.query.filter(Course.module_id.in_(module_ids)).count()
            
            print(f"\n📊 数据统计：")
            print(f"  - 模块数：{module_count}")
            print(f"  - 课程数：{course_count}")
            
            print("\n📁 模块树：")
            modules = Module.query.filter_by(major_id=major.id).order_by(Module.id).all()
            module_dict = {m.id: m for m in modules}
            
            for m in modules:
                indent = "  " if m.parent_id is not None else ""
                print(f"{indent}{m.id}. {m.name} ({m.required_credits}学分)")
            
            print("\n" + "="*80)
            print("✅ 完成！")
            print("="*80)
            
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        with app.app_context():
            db.session.rollback()


if __name__ == '__main__':
    create_electronic_info_db()
