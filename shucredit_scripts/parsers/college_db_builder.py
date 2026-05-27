#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学院/专业数据库构建器
完全兼容源项目的数据库结构（支持 college_id）
"""

import pymysql
import sys

# ==========================================
# 数据库配置
# ==========================================
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '24567@Zzy',
    'database': 'student_system',
    'charset': 'utf8mb4'
}

# ==========================================
# 学院定义
# ==========================================
COLLEGES = {
    '通信工程': {
        'code': 'TE',
        'modules': [
            (1, '公共基础课程', 67.5, None),
            (2, '思政类', 18.5, 1),
            (3, '军体类', 9.0, 1),
            (4, '大学英语', 8.0, 1),
            (5, '人工智能类', 5.0, 1),
            (6, '国家安全教育', 1.0, 1),
            (7, '自然科学类', 26.0, 1),
            
            (8, '通识课程', 8.0, None),
            (15, '核心通识课', 2.0, 8),
            (16, '跨类通识课', 2.0, 8),
            (17, '其他通识课', 4.0, 8),
            
            (9, '专业基础课程', 52.0, None),
            (10, '专业必修课程', 18.5, None),
            (11, '专业选修课程', 4.0, None),
            (18, '专业选修子模块1', 2.0, 11),
            (19, '专业选修子模块2', 2.0, 11),
            
            (12, '个性化教育课程', 10.0, None),
            (13, '综合工程实践能力培养模块', 10.0, 12),
            
            (14, '专业方向模块', 10.0, None),
            (20, '通信方向', 4.0, 14),
            (21, '光通信方向', 4.0, 14),
            (22, 'AI方向', 2.0, 14),
        ],
        'courses': [
            (100, 'GBK2000001', '形势与政策', 1.0, 2),
            (101, 'GBK2000003', '思想道德与法治', 3.0, 2),
            (102, 'GBK2000004', '中国近现代史纲要', 3.0, 2),
            (103, 'GBK2000002', '形势与政策（实践）', 1.0, 2),
            (104, 'GBK2000005', '马克思主义基本原理', 3.0, 2),
            (105, 'GBK2000006', '毛泽东思想和中国特色社会主义理论体系概论', 3.0, 2),
            (106, 'GBK2000007', '习近平新时代中国特色社会主义思想概论', 3.0, 2),
            (107, 'GBK5100001', '军事技能', 2.0, 3),
            (108, 'GBK2000008', '军事理论', 2.0, 3),
            (109, 'GBK2800501', '体质健康促进（1）', 0.5, 3),
            (110, 'GBK2800701', '体质健康促进（2）', 0.5, 3),
            (111, 'GBK1200001', '程序设计(C语言)', 3.0, 5),
            (112, 'GBK1200005', '人工智能基础A', 2.0, 5),
            (113, 'GBK2000009', '国家安全教育', 1.0, 6),
            (114, 'GBK0101001', '高等数学A(1)', 5.0, 7),
            (115, 'GBK0101002', '高等数学A(2)', 5.0, 7),
            (116, 'GBK0103001', '大学物理A(1)', 4.0, 7),
            (117, 'GBK0103002', '大学物理A(2)', 4.0, 7),
            (118, 'GBK0103003', '大学物理实验A(1)', 1.0, 7),
            (119, 'GBK0103004', '大学物理实验A(2)', 1.0, 7),
            (120, 'GBK0104001', '大学化学', 2.0, 7),
            (121, 'GBK0104002', '大学化学实验', 1.0, 7),
            (122, 'GBK0101006', '线性代数', 3.0, 7),
        ]
    },
    '微电子科学与工程': {
        'code': 'ME',
        'modules': [
            (1, '公共基础课程', 67.5, None),
            (2, '思政类', 18.5, 1),
            (3, '军体类', 9.0, 1),
            (4, '大学英语', 8.0, 1),
            (5, '人工智能类', 5.0, 1),
            (6, '国家安全教育', 1.0, 1),
            (7, '自然科学类', 26.0, 1),
            
            (8, '通识课程', 8.0, None),
            (15, '核心通识课', 2.0, 8),
            (16, '跨类通识课', 2.0, 8),
            (17, '其他通识课', 4.0, 8),
            
            (9, '专业基础课程', 5.0, None),
            (10, '专业必修课程', 61.5, None),
            (11, '专业选修课程', 8.0, None),
            (18, '专业选修子模块1', 4.0, 11),
            (19, '专业选修子模块2', 4.0, 11),
            
            (14, '专业方向模块', 10.0, None),
            (20, '集成电路微纳电子学方向', 4.0, 14),
            (21, '集成电路制造工程方向', 4.0, 14),
            (22, '集成电路设计方向', 2.0, 14),
        ],
        'courses': [
            (100, 'GBK2000001', '形势与政策', 1.0, 2),
            (101, 'GBK2000003', '思想道德与法治', 3.0, 2),
            (102, 'GBK2000004', '中国近现代史纲要', 3.0, 2),
            (103, 'GBK2000002', '形势与政策（实践）', 1.0, 2),
            (104, 'GBK2000005', '马克思主义基本原理', 3.0, 2),
            (105, 'GBK2000006', '毛泽东思想和中国特色社会主义理论体系概论', 3.0, 2),
            (106, 'GBK2000007', '习近平新时代中国特色社会主义思想概论', 3.0, 2),
            (107, 'GBK5100001', '军事技能', 2.0, 3),
            (108, 'GBK2000008', '军事理论', 2.0, 3),
            (109, 'GBK2800501', '体质健康促进（1）', 0.5, 3),
            (110, 'GBK2800701', '体质健康促进（2）', 0.5, 3),
            (111, 'GBK1200001', '程序设计(C语言)', 3.0, 5),
            (112, 'GBK1200005', '人工智能基础A', 2.0, 5),
            (113, 'GBK2000009', '国家安全教育', 1.0, 6),
            (114, 'GBK0101001', '高等数学A(1)', 5.0, 7),
            (115, 'GBK0101002', '高等数学A(2)', 5.0, 7),
            (116, 'GBK0103001', '大学物理A(1)', 4.0, 7),
            (117, 'GBK0103002', '大学物理A(2)', 4.0, 7),
            (118, 'GBK0103003', '大学物理实验A(1)', 1.0, 7),
            (119, 'GBK0103004', '大学物理实验A(2)', 1.0, 7),
            (120, 'GBK0104001', '大学化学', 2.0, 7),
            (121, 'GBK0104002', '大学化学实验', 1.0, 7),
            (122, 'GBK0101006', '线性代数', 3.0, 7),
            (130, 'JBK1300001', '工程图学', 2.0, 9),
            (131, 'JBK5400003', '工程实践B', 3.0, 9),
            (150, 'BBK0206001', '集成电路前沿技术导论', 1.0, 10),
            (151, 'BBK0206002', '概率论与数理统计', 2.0, 10),
            (152, 'BBK0206003', '数学物理方法', 4.0, 10),
            (153, 'BBK0206004', '量子力学与固体物理基础', 4.0, 10),
            (154, 'BBK0206005', '电路与模拟电子技术', 4.0, 10),
            (155, 'BBK0206006', '电子技术实验(1)', 0.5, 10),
            (156, 'BBK0206007', '电磁场与电磁波', 2.0, 10),
            (157, 'BBK0206008', '半导体物理与器件实验', 0.5, 10),
            (158, 'BBK0206009', '半导体物理', 4.0, 10),
            (159, 'BBK0206010', '电子技术实验(2)', 1.0, 10),
            (160, 'BBK0206011', '信号与系统基础', 2.5, 10),
            (161, 'BBK0206012', '计算机实习', 1.0, 10),
            (162, 'BBK0206013', '认识实习', 1.0, 10),
            (163, 'BBK0206014', '电子实习', 1.0, 10),
            (164, 'BBK0206015', '数字集成电路设计实验', 1.0, 10),
            (165, 'BBK0206016', '数字集成电路芯片设计', 3.0, 10),
            (166, 'BBK0206017', '半导体器件物理', 3.0, 10),
            (167, 'BBK0206018', '集成电路与微纳制造基础', 2.5, 10),
            (168, 'BBK0206019', '集成电路器件与工艺仿真', 1.0, 10),
            (169, 'BBK0206020', '模拟集成电路设计实验', 1.0, 10),
            (200, 'XBK0206001', '材料力学', 2.0, 11),
            (201, 'XBK0206002', '集成电路和半导体知识产权', 1.0, 11),
            (202, 'XBK0206003', '生物芯片创业思路与实践', 1.0, 11),
            (203, 'XBK0206004', '未来显示技术', 1.0, 11),
            (204, 'XBK0206005', '微电子专业英语', 2.0, 11),
            (205, 'XBK0206006', '无线通信概论', 2.0, 11),
            (206, 'XBK0206007', '嵌入式系统与结构', 2.0, 11),
            (207, 'XBK0206008', '半导体材料表征基础', 2.0, 11),
            (208, 'XBK0206009', '人工智能算法与系统', 2.5, 11),
            (209, 'XBK0206010', '机器学习概论', 2.0, 11),
        ]
    }
}

class CollegeDBBuilder:
    """学院数据库构建器"""
    
    def __init__(self, config=None):
        self.config = config or DB_CONFIG
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """连接数据库"""
        self.connection = pymysql.connect(**self.config)
        self.cursor = self.connection.cursor()
        return self
    
    def disconnect(self):
        """断开连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def clear_database(self):
        """清空数据库（保留学院）"""
        print("\n📋 正在清空现有数据...")
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        self.cursor.execute("DELETE FROM enrollment")
        self.cursor.execute("DELETE FROM course")
        self.cursor.execute("DELETE FROM module")
        self.connection.commit()
        print("✅ 清空完成")
    
    def ensure_college(self, college_name, college_code):
        """确保学院存在，返回学院ID"""
        self.cursor.execute("SELECT id FROM college WHERE name = %s", (college_name,))
        result = self.cursor.fetchone()
        
        if result:
            college_id = result[0]
            print(f"📚 学院已存在：{college_name} (ID: {college_id})")
        else:
            self.cursor.execute("INSERT INTO college (name, code) VALUES (%s, %s)", 
                              (college_name, college_code))
            self.connection.commit()
            college_id = self.cursor.lastrowid
            print(f"📚 创建学院：{college_name} (ID: {college_id}, 代码: {college_code})")
        
        return college_id
    
    def insert_modules(self, modules, college_id):
        """插入模块（支持college_id）"""
        print("\n📦 正在插入模块...")
        
        for module in modules:
            module_id, name, required_credits, parent_id = module
            parent_id_value = 'NULL' if parent_id is None else parent_id
            
            self.cursor.execute("""
                INSERT INTO module (id, name, required_credits, parent_id, college_id) 
                VALUES (%s, %s, %s, %s, %s)
            """, (module_id, name, required_credits, parent_id, college_id))
        
        self.connection.commit()
        print(f"✅ 插入了 {len(modules)} 个模块")
    
    def insert_courses(self, courses):
        """插入课程"""
        print("\n📚 正在插入课程...")
        
        for course in courses:
            course_id, course_code, name, credit, module_id = course
            
            self.cursor.execute("""
                INSERT INTO course (id, course_code, name, credit, module_id) 
                VALUES (%s, %s, %s, %s, %s)
            """, (course_id, course_code, name, credit, module_id))
        
        self.connection.commit()
        print(f"✅ 插入了 {len(courses)} 门课程")
    
    def verify_data(self):
        """验证数据"""
        print("\n" + "="*70)
        print("📊 数据验证")
        print("="*70)
        
        # 学院统计
        self.cursor.execute("SELECT COUNT(*), GROUP_CONCAT(name) FROM college")
        college_count, college_names = self.cursor.fetchone()
        print(f"\n🏛️  学院：{college_count} 个 ({college_names})")
        
        # 模块统计
        self.cursor.execute("""
            SELECT c.name, COUNT(m.id) 
            FROM college c 
            LEFT JOIN module m ON c.id = m.college_id 
            GROUP BY c.id, c.name
        """)
        print("\n📦 各学院模块数：")
        for college_name, count in self.cursor.fetchall():
            print(f"  - {college_name}: {count} 个")
        
        # 课程统计
        self.cursor.execute("""
            SELECT c.name, COUNT(crs.id) 
            FROM college c 
            LEFT JOIN module m ON c.id = m.college_id 
            LEFT JOIN course crs ON m.id = crs.module_id 
            GROUP BY c.id, c.name
        """)
        print("\n📚 各学院课程数：")
        for college_name, count in self.cursor.fetchall():
            print(f"  - {college_name}: {count} 门")
        
        # 模块树展示
        print("\n📁 模块树（按学院）：")
        self.cursor.execute("SELECT id, name FROM college ORDER BY id")
        colleges = self.cursor.fetchall()
        
        for college_id, college_name in colleges:
            print(f"\n🏛️  {college_name}:")
            self.cursor.execute("""
                SELECT id, name, required_credits, parent_id 
                FROM module 
                WHERE college_id = %s 
                ORDER BY id
            """, (college_id,))
            
            for m in self.cursor.fetchall():
                indent = "    " if m[3] is not None else "  "
                print(f"{indent}{m[0]}. {m[1]} ({m[2]}学分)")
    
    def build_college(self, college_name):
        """构建单个学院的数据库"""
        if college_name not in COLLEGES:
            print(f"❌ 学院 '{college_name}' 未定义")
            print(f"可用学院：{', '.join(COLLEGES.keys())}")
            return False
        
        college_data = COLLEGES[college_name]
        
        print("="*70)
        print(f"🏗️  构建学院：{college_name}")
        print("="*70)
        
        try:
            self.connect()
            
            # 1. 确保学院存在
            college_id = self.ensure_college(college_name, college_data['code'])
            
            # 2. 清空该学院的模块和课程
            print("\n📋 清空该学院数据...")
            self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            self.cursor.execute("""
                DELETE crs FROM course crs 
                JOIN module m ON crs.module_id = m.id 
                WHERE m.college_id = %s
            """, (college_id,))
            self.cursor.execute("DELETE FROM module WHERE college_id = %s", (college_id,))
            self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            self.connection.commit()
            
            # 3. 插入模块
            self.insert_modules(college_data['modules'], college_id)
            
            # 4. 插入课程
            self.insert_courses(college_data['courses'])
            
            # 5. 验证
            self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            self.connection.commit()
            
            print("\n" + "="*70)
            print(f"🎉 {college_name} 构建完成！")
            print("="*70)
            
            # 简单统计
            self.cursor.execute("SELECT COUNT(*) FROM module WHERE college_id = %s", (college_id,))
            m_count = self.cursor.fetchone()[0]
            self.cursor.execute("""
                SELECT COUNT(*) FROM course crs 
                JOIN module m ON crs.module_id = m.id 
                WHERE m.college_id = %s
            """, (college_id,))
            c_count = self.cursor.fetchone()[0]
            
            print(f"\n📊 当前数据：")
            print(f"  - 模块数：{m_count}")
            print(f"  - 课程数：{c_count}")
            
            self.disconnect()
            return True
            
        except Exception as e:
            print(f"\n❌ 错误：{e}")
            import traceback
            traceback.print_exc()
            return False
    
    def build_all(self):
        """构建所有学院"""
        print("="*70)
        print("🏗️  构建所有学院的数据库")
        print("="*70)
        
        try:
            self.connect()
            
            self.clear_database()
            
            for college_name in COLLEGES.keys():
                college_data = COLLEGES[college_name]
                
                # 确保学院存在
                college_id = self.ensure_college(college_name, college_data['code'])
                
                # 插入模块
                self.insert_modules(college_data['modules'], college_id)
                
                # 插入课程
                self.insert_courses(college_data['courses'])
            
            self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            self.connection.commit()
            
            self.verify_data()
            
            print("\n" + "="*70)
            print("🎉 所有学院构建完成！")
            print("="*70)
            
            self.disconnect()
            return True
            
        except Exception as e:
            print(f"\n❌ 错误：{e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                    学院数据库构建器                             ║
║          完全兼容源项目 API 和 college_id 支持                  ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    if len(sys.argv) > 1:
        college_name = sys.argv[1]
        builder = CollegeDBBuilder()
        success = builder.build_college(college_name)
        sys.exit(0 if success else 1)
    else:
        print("""
用法：
  python college_db_builder.py                    # 构建所有学院
  python college_db_builder.py "通信工程"        # 只构建通信工程
  python college_db_builder.py "微电子科学与工程"  # 只构建微电子

可用学院：
  - 通信工程
  - 微电子科学与工程
        """)
        
        choice = input("\n选择操作 [1=全部, 2=通信工程, 3=微电子]: ").strip()
        
        builder = CollegeDBBuilder()
        
        if choice == '1':
            builder.build_all()
        elif choice == '2':
            builder.build_college('通信工程')
        elif choice == '3':
            builder.build_college('微电子科学与工程')
        else:
            print("无效选择")

if __name__ == '__main__':
    main()
