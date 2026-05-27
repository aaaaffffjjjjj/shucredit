#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用源项目 ORM 模型填充学院数据
完全兼容源项目 API
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, College, Module, Course

# ==========================================
# 学院数据定义
# ==========================================
COLLEGE_DATA = {
    '通信工程': {
        'code': 'TE',
        'modules': [
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
            
            ('专业基础课程', 52.0, None),
            ('专业必修课程', 18.5, None),
            ('专业选修课程', 4.0, None),
            ('专业选修子模块1', 2.0, '专业选修课程'),
            ('专业选修子模块2', 2.0, '专业选修课程'),
            
            ('个性化教育课程', 10.0, None),
            ('综合工程实践能力培养模块', 10.0, '个性化教育课程'),
            
            ('专业方向模块', 10.0, None),
            ('通信方向', 4.0, '专业方向模块'),
            ('光通信方向', 4.0, '专业方向模块'),
            ('AI方向', 2.0, '专业方向模块'),
        ],
        'courses': [
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
        ]
    },
    '微电子科学与工程': {
        'code': 'ME',
        'modules': [
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
        ],
        'courses': [
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
            ('JBK1300001', '工程图学', 2.0, '专业基础课程'),
            ('JBK5400003', '工程实践B', 3.0, '专业基础课程'),
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
            ('XBK0206001', '材料力学', 2.0, '专业选修课程'),
            ('XBK0206002', '集成电路和半导体知识产权', 1.0, '专业选修课程'),
            ('XBK0206003', '生物芯片创业思路与实践', 1.0, '专业选修课程'),
            ('XBK0206004', '未来显示技术', 1.0, '专业选修课程'),
            ('XBK0206005', '微电子专业英语', 2.0, '专业选修课程'),
            ('XBK0206006', '无线通信概论', 2.0, '专业选修课程'),
            ('XBK0206007', '嵌入式系统与结构', 2.0, '专业选修课程'),
            ('XBK0206008', '半导体材料表征基础', 2.0, '专业选修课程'),
            ('XBK0206009', '人工智能算法与系统', 2.5, '专业选修课程'),
            ('XBK0206010', '机器学习概论', 2.0, '专业选修课程'),
        ]
    }
}

class CollegePopulator:
    """学院数据填充器"""
    
    def __init__(self):
        self.module_map = {}  # 模块名 -> 模块ID
    
    def clear_college_data(self, college):
        """清除学院的模块和课程"""
        # 先删除该学院模块下的课程
        modules = Module.query.filter_by(college_id=college.id).all()
        module_ids = [m.id for m in modules]
        
        if module_ids:
            Course.query.filter(Course.module_id.in_(module_ids)).delete(synchronize_session=False)
        
        # 再删除该学院的模块
        Module.query.filter_by(college_id=college.id).delete(synchronize_session=False)
        
        db.session.commit()
        print(f"  ✅ 已清除学院 '{college.name}' 的旧数据")
    
    def populate_modules(self, college, modules_data):
        """填充模块"""
        print(f"\n📦 正在插入模块...")
        
        # 先插入所有根模块
        root_modules = [m for m in modules_data if m[2] is None]
        for name, credits, _ in root_modules:
            module = Module(
                name=name,
                required_credits=credits,
                parent_id=None,
                college_id=college.id
            )
            db.session.add(module)
            db.session.flush()  # 获取 ID
            self.module_map[name] = module.id
        
        # 再插入子模块
        child_modules = [m for m in modules_data if m[2] is not None]
        for name, credits, parent_name in child_modules:
            parent_id = self.module_map.get(parent_name)
            if parent_id is None:
                print(f"  ⚠️  找不到父模块 '{parent_name}', 跳过 '{name}'")
                continue
            
            module = Module(
                name=name,
                required_credits=credits,
                parent_id=parent_id,
                college_id=college.id
            )
            db.session.add(module)
            db.session.flush()
            self.module_map[name] = module.id
        
        db.session.commit()
        print(f"  ✅ 插入了 {len(modules_data)} 个模块")
    
    def populate_courses(self, college, courses_data):
        """填充课程"""
        print(f"\n📚 正在插入课程...")
        
        for course_code, name, credit, module_name in courses_data:
            module_id = self.module_map.get(module_name)
            if module_id is None:
                print(f"  ⚠️  找不到模块 '{module_name}', 跳过课程 '{name}'")
                continue
            
            # 检查课程是否已存在
            existing = Course.query.filter_by(course_code=course_code).first()
            if existing:
                # 更新课程
                existing.name = name
                existing.credit = credit
                existing.module_id = module_id
            else:
                # 创建新课程
                course = Course(
                    course_code=course_code,
                    name=name,
                    credit=credit,
                    module_id=module_id
                )
                db.session.add(course)
        
        db.session.commit()
        print(f"  ✅ 处理了 {len(courses_data)} 门课程")
    
    def populate_college(self, college_name):
        """填充单个学院"""
        if college_name not in COLLEGE_DATA:
            print(f"❌ 学院 '{college_name}' 未定义")
            print(f"可用学院：{', '.join(COLLEGE_DATA.keys())}")
            return False
        
        data = COLLEGE_DATA[college_name]
        
        print("="*70)
        print(f"🏗️  构建学院：{college_name}")
        print("="*70)
        
        try:
            with app.app_context():
                # 获取或创建学院
                college = College.query.filter_by(name=college_name).first()
                if not college:
                    college = College(name=college_name, code=data['code'])
                    db.session.add(college)
                    db.session.commit()
                    print(f"📚 创建学院：{college_name} (ID: {college.id}, 代码: {data['code']})")
                else:
                    print(f"📚 学院已存在：{college_name} (ID: {college.id})")
                    # 更新代码
                    if college.code != data['code']:
                        college.code = data['code']
                        db.session.commit()
                
                # 清除旧数据
                self.clear_college_data(college)
                
                # 填充模块
                self.module_map = {}
                self.populate_modules(college, data['modules'])
                
                # 填充课程
                self.populate_courses(college, data['courses'])
                
                # 验证
                print("\n" + "="*70)
                print(f"🎉 {college_name} 构建完成！")
                print("="*70)
                
                module_count = Module.query.filter_by(college_id=college.id).count()
                course_count = Course.query.join(Module).filter(Module.college_id == college.id).count()
                
                print(f"\n📊 当前数据：")
                print(f"  - 模块数：{module_count}")
                print(f"  - 课程数：{course_count}")
                
                # 显示模块树
                print(f"\n📁 模块树：")
                modules = Module.query.filter_by(college_id=college.id).order_by(Module.id).all()
                for m in modules:
                    indent = "  " if m.parent_id is not None else ""
                    print(f"{indent}{m.id}. {m.name} ({m.required_credits}学分)")
            
            return True
            
        except Exception as e:
            print(f"\n❌ 错误：{e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False
    
    def populate_all(self):
        """填充所有学院"""
        print("="*70)
        print("🏗️  构建所有学院的数据库")
        print("="*70)
        
        try:
            with app.app_context():
                for college_name in COLLEGE_DATA.keys():
                    self.module_map = {}
                    self.populate_college(college_name)
                
                # 验证所有数据
                print("\n" + "="*70)
                print("📊 数据验证")
                print("="*70)
                
                colleges = College.query.order_by(College.id).all()
                print(f"\n🏛️  学院：{len(colleges)} 个")
                
                for college in colleges:
                    module_count = Module.query.filter_by(college_id=college.id).count()
                    course_count = Course.query.join(Module).filter(Module.college_id == college.id).count()
                    print(f"\n📚 {college.name} (ID: {college.id}, 代码: {college.code}):")
                    print(f"  - 模块：{module_count} 个")
                    print(f"  - 课程：{course_count} 门")
                
                print("\n" + "="*70)
                print("🎉 所有学院构建完成！")
                print("="*70)
            
            return True
            
        except Exception as e:
            print(f"\n❌ 错误：{e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

def main():
    print("""
╔═══════════════════════════════════════════════════════════════╗
║              使用源项目 ORM 的学院数据填充器                     ║
║                  完全兼容源项目 API                              ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    populator = CollegePopulator()
    
    if len(sys.argv) > 1:
        college_name = sys.argv[1]
        success = populator.populate_college(college_name)
        sys.exit(0 if success else 1)
    else:
        print("""
用法：
  python populate_colleges.py                    # 构建所有学院
  python populate_colleges.py "通信工程"        # 只构建通信工程
  python populate_colleges.py "微电子科学与工程"  # 只构建微电子

可用学院：
  - 通信工程
  - 微电子科学与工程
        """)
        
        choice = input("\n选择操作 [1=全部, 2=通信工程, 3=微电子]: ").strip()
        
        if choice == '1':
            populator.populate_all()
        elif choice == '2':
            populator.populate_college('通信工程')
        elif choice == '3':
            populator.populate_college('微电子科学与工程')
        else:
            print("无效选择")

if __name__ == '__main__':
    main()
