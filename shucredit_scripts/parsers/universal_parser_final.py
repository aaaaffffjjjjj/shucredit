#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用专业培养方案解析器 - 最终版
特点：
1. 默认包含完整的通信工程专业模块和课程
2. 支持解析PDF扩展
3. 可用于其他专业
"""

import os
import pdfplumber


class ProfessionalProgramParser:
    """专业培养方案解析器"""
    
    # 默认完整模块结构（通信工程专业模板）
    DEFAULT_MODULES = [
        (1, '公共基础课程', 67.5, None),
        (8, '通识课程', 8.0, None),
        (9, '专业基础课程', 52.0, None),
        (10, '专业必修课程', 18.5, None),
        (11, '专业选修课程', 4.0, None),
        (12, '个性化教育课程', 10.0, None),
        (14, '专业方向模块', 10.0, None),
        (2, '思政类', 18.5, 1),
        (3, '军体类', 9.0, 1),
        (4, '大学英语', 8.0, 1),
        (5, '人工智能类', 5.0, 1),
        (6, '国家安全教育', 1.0, 1),
        (7, '自然科学类', 26.0, 1),
        (15, '核心通识课', 2.0, 8),
        (16, '跨类通识课', 2.0, 8),
        (17, '其他通识课', 4.0, 8),
        (18, '专业选修子模块1', 2.0, 11),
        (19, '专业选修子模块2', 2.0, 11),
        (13, '综合工程实践能力培养模块', 10.0, 12),
        (20, '通信方向', 4.0, 14),
        (21, '光通信方向', 4.0, 14),
        (22, 'AI方向', 2.0, 14),
    ]
    
    DEFAULT_COURSES = [
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
        (111, 'GBK1200001', '程序设计（C语言）', 3.0, 5),
        (112, 'GBK1200005', '人工智能基础A', 2.0, 5),
        (113, 'GBK2000009', '国家安全教育', 1.0, 6),
        (114, 'GBK0101001', '高等数学A（1）', 5.0, 7),
        (115, 'GBK0101002', '高等数学A（2）', 5.0, 7),
        (116, 'GBK0103001', '大学物理A（1）', 4.0, 7),
        (117, 'GBK0103002', '大学物理A（2）', 4.0, 7),
        (118, 'GBK0103003', '大学物理实验A（1）', 1.0, 7),
        (119, 'GBK0103004', '大学物理实验A（2）', 1.0, 7),
        (120, 'GBK0104001', '大学化学', 2.0, 7),
        (121, 'GBK0104002', '大学化学实验', 1.0, 7),
        (122, 'GBK0101006', '线性代数', 3.0, 7),
        (123, 'JBK1300001', '工程图学', 2.0, 9),
        (124, 'JBK5400003', '工程实践B', 3.0, 9),
        (125, 'JBK1131001', '复变函数与积分变换', 2.5, 9),
        (126, 'JBK1131002', '电路与电子线路基础（1）', 3.0, 9),
        (127, 'JBK1131003', '电路与电子线路基础（2）', 3.0, 9),
        (128, 'JBK1131004', '电路与电子线路基础实验（1）', 0.5, 9),
        (129, 'JBK1131005', '电路与电子线路基础实验（2）', 0.5, 9),
        (130, 'JBK1131006', '信号与系统（1）', 2.0, 9),
        (131, 'JBK1131007', '信号与系统（2）', 2.0, 9),
        (132, 'JBK1131008', '信号与系统实验', 0.5, 9),
        (133, 'JBK1131012', '数字逻辑电路分析与设计', 4.0, 9),
        (134, 'JBK1131013', '数字逻辑电路分析与设计实验', 0.5, 9),
        (135, 'JBK1131009', '面向对象程序设计', 2.5, 9),
        (136, 'JBK1131011', '概率论与随机过程', 2.5, 9),
        (137, 'JBK1131010', '微机原理', 2.5, 9),
        (138, 'JBK1131015', '数字信号处理', 2.5, 9),
        (139, 'JBK1131016', '数据结构与算法基础', 3.0, 9),
        (140, 'JBK1131017', '电磁场理论', 3.0, 9),
        (141, 'JBK1131018', '通信原理A', 3.0, 9),
        (142, 'JBK1131020', '通信原理实验', 0.5, 9),
        (143, 'JBK1131021', '计算机网络', 2.5, 9),
        (144, 'JBK1131022', '信息论与编码', 2.5, 9),
        (145, 'JBK1131023', '通信电子线路', 2.5, 9),
        (146, 'JBK1131024', '通信电子线路实验', 0.5, 9),
        (147, 'JBK1131014', '工程经济学与IT项目管理', 1.0, 9),
        (148, 'JBK1231001', '模拟电子线路A', 3.5, 9),
        (149, 'JBK1231002', '模拟电子线路实验A', 0.5, 9),
        (150, 'JBK1231003', '数字电子线路A', 3.0, 9),
        (151, 'JBK1231004', '数字电子线路实验A', 0.5, 9),
        (152, 'JBK1231005', '高频电子线路', 3.0, 9),
        (153, 'JBK1231006', '高频电子线路实验', 0.5, 9),
        (154, 'JBK1300004', '计算机导论', 1.0, 9),
        (155, 'JBK1300005', '计算机实验', 1.0, 9),
        (156, 'BBK1131001', '认识实习', 0.5, 10),
        (157, 'BBK1131003', '工程教育', 2.0, 10),
        (158, 'BBK1131004', '综合工程设计', 3.0, 10),
        (159, 'BBK1131002', '生产实习', 5.0, 10),
        (160, 'BBK1131005', '毕业论文（设计）', 8.0, 10),
    ]
    
    def __init__(self, program_name='通信工程', modules=None, courses=None):
        self.program_name = program_name
        self.modules = modules if modules is not None else self.DEFAULT_MODULES.copy()
        self.courses = courses if courses is not None else self.DEFAULT_COURSES.copy()
    
    def load_pdf(self, pdf_path):
        """解析PDF文件（可选，用于扩展）"""
        print(f"📄 正在解析PDF: {pdf_path}")
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = "\n".join([page.extract_text() or "" for page in pdf.pages])
                print(f"   共 {len(pdf.pages)} 页")
                return text
        except Exception as e:
            print(f"⚠️  解析PDF失败: {e}")
            return None
    
    def generate_sql_script(self, output_path):
        """生成SQL脚本"""
        print(f"💾 正在生成SQL脚本: {output_path}")
        
        sql_lines = []
        sql_lines.append("-- ==============================================")
        sql_lines.append(f"-- {self.program_name} 专业培养方案数据库")
        sql_lines.append("-- ==============================================")
        sql_lines.append("")
        sql_lines.append("SET NAMES utf8mb4;")
        sql_lines.append("SET FOREIGN_KEY_CHECKS = 0;")
        sql_lines.append("")
        sql_lines.append("DELETE FROM enrollment;")
        sql_lines.append("DELETE FROM course;")
        sql_lines.append("DELETE FROM module;")
        sql_lines.append("")
        sql_lines.append("-- ==============================================")
        sql_lines.append("-- 插入模块")
        sql_lines.append("-- ==============================================")
        sql_lines.append("")
        
        for mod in self.modules:
            parent_str = f"NULL" if mod[3] is None else str(mod[3])
            sql_lines.append(f"INSERT INTO module (id, name, required_credits, parent_id) VALUES")
            sql_lines.append(f"  ({mod[0]}, '{mod[1]}', {mod[2]}, {parent_str});")
        sql_lines.append("")
        
        sql_lines.append("-- ==============================================")
        sql_lines.append("-- 插入课程")
        sql_lines.append("-- ==============================================")
        sql_lines.append("")
        
        for course in self.courses:
            name_escaped = course[2].replace("'", "\\'")
            sql_lines.append(f"INSERT INTO course (id, course_code, name, credit, module_id) VALUES")
            sql_lines.append(f"  ({course[0]}, '{course[1]}', '{name_escaped}', {course[3]}, {course[4]});")
        sql_lines.append("")
        
        sql_lines.append("SET FOREIGN_KEY_CHECKS = 1;")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sql_lines))
        
        print(f"✅ SQL脚本已生成，共 {len(self.modules)} 模块，{len(self.courses)} 课程")
    
    def generate_python_reset(self, output_path):
        """生成Python重置脚本"""
        print(f"💾 正在生成Python重置脚本: {output_path}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
{self.program_name} 专业培养方案数据库重置脚本
\"\"\"

import sys
import os

sys.path.insert(0, r'e:\\nbainbshuda\\shucredit-1')

from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.sqlalchemy_uri()
db = SQLAlchemy(app)

with app.app_context():
    class Module(db.Model):
        __tablename__ = 'module'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        required_credits = db.Column(db.Float, nullable=False)
        parent_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=True)
    
    class Course(db.Model):
        __tablename__ = 'course'
        id = db.Column(db.Integer, primary_key=True)
        course_code = db.Column(db.String(50), unique=True, nullable=False)
        name = db.Column(db.String(150), nullable=False)
        credit = db.Column(db.Float, nullable=False)
        module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    
    print("="*60)
    print(f"🗑️  重置 {self.program_name} 专业数据库")
    print("="*60)
    
    print("\\n📋 正在清空...")
    db.session.execute("SET FOREIGN_KEY_CHECKS = 0")
    db.session.execute("DELETE FROM enrollment")
    db.session.execute("DELETE FROM course")
    db.session.execute("DELETE FROM module")
    db.session.commit()
    print("✅ 清空完成")
    
    print("\\n📦 正在插入模块...")
    modules_data = {repr(self.modules)}
    for mod in modules_data:
        m = Module(
            id=mod[0],
            name=mod[1],
            required_credits=mod[2],
            parent_id=mod[3]
        )
        db.session.add(m)
    db.session.commit()
    print(f"✅ 插入了 {{len(modules_data)}} 个模块")
    
    print("\\n📚 正在插入课程...")
    courses_data = {repr(self.courses)}
    for course in courses_data:
        c = Course(
            id=course[0],
            course_code=course[1],
            name=course[2],
            credit=course[3],
            module_id=course[4]
        )
        db.session.add(c)
    db.session.commit()
    print(f"✅ 插入了 {{len(courses_data)}} 门课程")
    
    db.session.execute("SET FOREIGN_KEY_CHECKS = 1")
    
    print("\\n" + "="*60)
    print("🎉 重置成功！")
    print("="*60)
""")
    
    def print_structure(self):
        """打印结构预览"""
        print("\n" + "="*70)
        print(f"📊 {self.program_name} 专业培养方案结构")
        print("="*70)
        
        print(f"\n📦 模块树:")
        for mod in self.modules:
            indent = "  " if mod[3] is not None else ""
            print(f"{indent}{mod[0]}. {mod[1]} ({mod[2]} 学分)")
        
        print(f"\n📚 课程统计:")
        module_course_count = {}
        for course in self.courses:
            mid = course[4]
            if mid not in module_course_count:
                module_course_count[mid] = 0
            module_course_count[mid] += 1
        
        for mid, count in sorted(module_course_count.items()):
            module_name = next(m[1] for m in self.modules if m[0] == mid)
            print(f"   {mid}. {module_name}: {count} 门课")
        
        print(f"\n✅ 总计: {len(self.modules)} 个模块，{len(self.courses)} 门课程")


def main():
    print("="*70)
    print("🎯 通用专业培养方案解析器 - 最终版")
    print("="*70)
    
    parser = ProfessionalProgramParser(program_name='通信工程')
    
    print(f"\n✅ 已加载: {parser.program_name} 专业默认数据")
    
    parser.print_structure()
    
    print("\n" + "-"*70)
    print("📝 正在生成脚本...")
    
    parser.generate_sql_script(r'e:\wodeaishiyan\communication_program.sql')
    parser.generate_python_reset(r'e:\wodeaishiyan\reset_communication_program.py')
    
    print("\n" + "="*70)
    print("🎉 完成！")
    print("="*70)
    print(f"  📄 SQL脚本: communication_program.sql")
    print(f"  🐍 Python脚本: reset_communication_program.py")
    print("\n💡 使用方法:")
    print("  - 对于其他专业，修改 DEFAULT_MODULES 和 DEFAULT_COURSES 即可")
    print("  - 或继承 ProfessionalProgramParser 类")


if __name__ == '__main__':
    main()
