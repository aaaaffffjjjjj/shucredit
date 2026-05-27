#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2025微电子科学与工程专业导入脚本
兼容学院-专业-模块体系
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import app, db, College, Major, Module, Course


def import_microelectronics():
    print("="*80)
    print("🏗️  导入2025微电子科学与工程专业")
    print("="*80)
    
    try:
        with app.app_context():
            # 1. 确保学院和专业存在
            print("\n📚 步骤 1/4: 确保学院和专业...")
            college = College.query.filter_by(name='微电子学院').first()
            if not college:
                college = College(name='微电子学院', code='microelectronics')
                db.session.add(college)
                db.session.commit()
                print(f"  ✅ 创建学院: {college.name}")
            else:
                print(f"  ✅ 学院已存在: {college.name}")
            
            major = Major.query.filter_by(college_id=college.id, name='微电子科学与工程').first()
            if not major:
                major = Major(name='微电子科学与工程', code='WDZ001', college_id=college.id)
                db.session.add(major)
                db.session.commit()
                print(f"  ✅ 创建专业: {major.name}")
            else:
                print(f"  ✅ 专业已存在: {major.name}")
            
            # 2. 清理现有数据
            print("\n🧹 步骤 2/4: 清理现有数据...")
            existing_modules = Module.query.filter_by(major_id=major.id).all()
            module_ids = [m.id for m in existing_modules]
            Course.query.filter(Course.module_id.in_(module_ids)).delete(synchronize_session=False)
            Module.query.filter_by(major_id=major.id).delete(synchronize_session=False)
            db.session.commit()
            print(f"  ✅ 已清理 {len(module_ids)} 个模块及课程")
            
            # 3. 导入模块
            print("\n📦 步骤 3/4: 导入模块...")
            module_data = [
                ('公共基础课程', 67.5, None),
                ('思政类', 18.5, '公共基础课程'),
                ('军体类', 9.0, '公共基础课程'),
                ('大学英语', 8.0, '公共基础课程'),
                ('人工智能类', 5.0, '公共基础课程'),
                ('国家安全教育', 1.0, '公共基础课程'),
                ('自然科学类', 26.0, '公共基础课程'),
                
                ('通识课程', 8.0, None),
                ('核心通识课', 2.0, '通识课程'),
                ('跨类通识课', 2.0, '通识课程'),
                ('其他通识课', 4.0, '通识课程'),
                
                ('专业基础课程', 5.0, None),
                
                ('专业必修课程', 61.5, None),
                
                ('专业选修课程', 8.0, None),
                ('专业选修子模块1', 4.0, '专业选修课程'),
                ('专业选修子模块2', 4.0, '专业选修课程'),
                
                ('专业方向模块', 10.0, None),
                ('集成电路微纳电子学方向', 4.0, '专业方向模块'),
                ('集成电路制造工程方向', 4.0, '专业方向模块'),
                ('集成电路设计方向', 2.0, '专业方向模块'),
            ]
            
            module_map = {}
            for name, credits, parent_name in module_data:
                parent_id = module_map.get(parent_name) if parent_name else None
                module = Module(
                    name=name,
                    required_credits=credits,
                    parent_id=parent_id,
                    college_id=college.id,
                    major_id=major.id
                )
                db.session.add(module)
                db.session.flush()
                module_map[name] = module.id
            
            db.session.commit()
            print(f"  ✅ 导入了 {len(module_data)} 个模块")
            
            # 4. 导入课程
            print("\n📚 步骤 4/4: 导入课程...")
            course_data = [
                # --- 公共基础课程 ---
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
                
                # --- 专业基础课程 ---
                ('JBK1300001', '工程图学', 2.0, '专业基础课程'),
                ('JBK5400003', '工程实践B', 3.0, '专业基础课程'),
                
                # --- 专业必修课程 ---
                ('BBK0206001', '集成电路前沿技术导论', 1.0, '专业必修课程'),
                ('BBK0206002', '概率论与数理统计', 2.0, '专业必修课程'),
                ('BBK0206003', '数学物理方法', 4.0, '专业必修课程'),
                ('BBK0206004', '量子力学与固体物理基础', 4.0, '专业必修课程'),
                ('BBK0206005', '电路与模拟电子技术', 4.0, '专业必修课程'),
                ('BBK0206006', '电子技术实验(1)', 0.5, '专业必修课程'),
                ('BBK0206007', '电磁场与电磁波', 2.0, '专业必修课程'),
                ('BBK0206008', '半导体物理与器件实验', 0.5, '专业必修课程'),
                ('BBK0206009', '半导体物理', 4.0, '专业必修课程'),
                ('BBK0206010', '电子技术实验(2)', 1.0, '专业必修课程'),
                ('BBK0206011', '信号与系统基础', 2.5, '专业必修课程'),
                ('BBK0206012', '计算机实习', 1.0, '专业必修课程'),
                ('BBK0206013', '认识实习', 1.0, '专业必修课程'),
                ('BBK0206014', '电子实习', 1.0, '专业必修课程'),
                ('BBK0206015', '数字集成电路设计实验', 1.0, '专业必修课程'),
                ('BBK0206016', '数字集成电路芯片设计', 3.0, '专业必修课程'),
                ('BBK0206017', '半导体器件物理', 3.0, '专业必修课程'),
                ('BBK0206018', '集成电路与微纳制造基础', 2.5, '专业必修课程'),
                ('BBK0206019', '集成电路器件与工艺仿真', 1.0, '专业必修课程'),
                ('BBK0206020', '模拟集成电路设计实验', 1.0, '专业必修课程'),
                
                # --- 专业选修课程 ---
                ('XBK0206001', '材料力学', 2.0, '专业选修子模块1'),
                ('XBK0206002', '集成电路和半导体知识产权', 1.0, '专业选修子模块1'),
                ('XBK0206003', '生物芯片创业思路与实践', 1.0, '专业选修子模块1'),
                ('XBK0206004', '未来显示技术', 1.0, '专业选修子模块1'),
                ('XBK0206005', '微电子专业英语', 2.0, '专业选修子模块1'),
                ('XBK0206006', '无线通信概论', 2.0, '专业选修子模块2'),
                ('XBK0206007', '嵌入式系统与结构', 2.0, '专业选修子模块2'),
                ('XBK0206008', '半导体材料表征基础', 2.0, '专业选修子模块2'),
                ('XBK0206009', '人工智能算法与系统', 2.5, '专业选修子模块2'),
                ('XBK0206010', '机器学习概论', 2.0, '专业选修子模块2'),
                
                # --- 专业方向模块 ---
                ('XBK0206011', '硅基光电子器件', 1.0, '集成电路微纳电子学方向'),
                ('XBK0206012', '先进微纳光学技术', 2.0, '集成电路微纳电子学方向'),
                ('XBK0206013', '半导体光电材料与器件', 2.0, '集成电路微纳电子学方向'),
                ('XBK0206014', '集成光学与器件', 2.0, '集成电路微纳电子学方向'),
                ('XBK0206015', '生物传感芯片与系统', 2.0, '集成电路微纳电子学方向'),
                
                ('XBK0206016', '集成电路材料基础', 1.0, '集成电路制造工程方向'),
                ('XBK0206017', '半导体关键设备与技术', 2.0, '集成电路制造工程方向'),
                ('XBK0206018', '微电子封装技术概论', 2.0, '集成电路制造工程方向'),
                ('XBK0206019', '集成电路原子级工艺技术', 3.0, '集成电路制造工程方向'),
                ('XBK0206020', 'MEMS芯片加工与测试', 1.0, '集成电路制造工程方向'),
            ]
            
            for code, name, credit, module_name in course_data:
                module_id = module_map.get(module_name)
                if module_id:
                    course = Course(
                        course_code=code,
                        name=name,
                        credit=credit,
                        module_id=module_id
                    )
                    db.session.add(course)
            
            db.session.commit()
            print(f"  ✅ 导入了 {len(course_data)} 门课程")
            
            # 5. 验证结果
            print("\n" + "="*80)
            print("🎉 导入完成！验证结果")
            print("="*80)
            
            final_modules = Module.query.filter_by(major_id=major.id).count()
            final_courses = Course.query.filter(Course.module_id.in_(module_map.values())).count()
            
            print(f"\n📊 统计:")
            print(f"  - 学院: {college.name}")
            print(f"  - 专业: {major.name}")
            print(f"  - 模块: {final_modules}")
            print(f"  - 课程: {final_courses}")
            
            print(f"\n📁 模块树:")
            root_modules = Module.query.filter_by(major_id=major.id, parent_id=None).order_by(Module.id).all()
            for root in root_modules:
                print(f"  📦 {root.name} ({root.required_credits}学分)")
                children = Module.query.filter_by(major_id=major.id, parent_id=root.id).order_by(Module.id).all()
                for child in children:
                    print(f"      └── {child.name} ({child.required_credits}学分)")
            
            print("\n" + "="*80)
            print("✅ 微电子科学与工程专业导入成功！")
            print("="*80)
            
            return True
            
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return False


if __name__ == '__main__':
    import_microelectronics()
