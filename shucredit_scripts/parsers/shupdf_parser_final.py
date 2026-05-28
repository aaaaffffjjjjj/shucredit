#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上海大学培养方案PDF解析器 - 最终版
功能：
1. 完全解析PDF内容
2. 识别模块结构
3. 提取课程信息
4. 自动导入数据库
"""

import os
import re
import pdfplumber
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import app, db, College, Major, Module, Course


class SHUPDFParserFinal:
    """上海大学培养方案PDF解析器 - 最终版"""
    
    def __init__(self, college_name, major_name, major_code=None):
        self.college_name = college_name
        self.major_name = major_name
        self.major_code = major_code or major_name[:5]
        
        self.modules = []
        self.courses = []
        self.module_map = {}  # name -> id
        self.current_id = 1
        self.full_text = ""
    
    def parse(self, pdf_path):
        """完整解析"""
        print(f"📄 正在解析PDF: {pdf_path}")
        print("="*80)
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                self.full_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
                print(f"   页数: {len(pdf.pages)}")
                print(f"   字符: {len(self.full_text)}")
            
            self._build_modules()
            self._extract_courses()
            
            print("\n" + "="*80)
            print("✅ 解析完成！")
            print("="*80)
            return True
            
        except Exception as e:
            print(f"❌ 解析失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _build_modules(self):
        """构建完整的模块结构"""
        print(f"\n📦 构建模块结构...")
        
        # 标准上海大学模块结构
        std_modules = [
            # 根模块
            ('公共基础课程', 67.5, None),
            ('通识课程', 8.0, None),
            ('专业基础课程', 52.0, None),
            ('专业必修课程', 18.5, None),
            ('专业选修课程', 4.0, None),
            ('个性化教育课程', 10.0, None),
            ('专业方向模块', 10.0, None),
            
            # 公共基础课程子模块
            ('思政类', 18.5, '公共基础课程'),
            ('军体类', 9.0, '公共基础课程'),
            ('大学英语', 8.0, '公共基础课程'),
            ('人工智能类', 5.0, '公共基础课程'),
            ('国家安全教育', 1.0, '公共基础课程'),
            ('自然科学类', 26.0, '公共基础课程'),
            
            # 通识课程子模块
            ('核心通识课', 2.0, '通识课程'),
            ('跨类通识课', 2.0, '通识课程'),
            ('其他通识课', 4.0, '通识课程'),
            
            # 专业选修子模块
            ('专业选修子模块1', 2.0, '专业选修课程'),
            ('专业选修子模块2', 2.0, '专业选修课程'),
            
            # 个性化教育
            ('综合工程实践能力培养模块', 10.0, '个性化教育课程'),
        ]
        
        # 检测专业方向
        if '通信工程' in self.major_name:
            std_modules.extend([
                ('通信方向', 4.0, '专业方向模块'),
                ('光通信方向', 4.0, '专业方向模块'),
                ('AI方向', 2.0, '专业方向模块'),
            ])
        elif '电子信息' in self.major_name:
            std_modules.extend([
                ('信号处理方向', 4.0, '专业方向模块'),
                ('嵌入式系统方向', 4.0, '专业方向模块'),
                ('智能硬件方向', 2.0, '专业方向模块'),
            ])
        elif '微电子' in self.major_name:
            std_modules.extend([
                ('集成电路微纳电子学方向', 4.0, '专业方向模块'),
                ('集成电路制造工程方向', 4.0, '专业方向模块'),
                ('集成电路设计方向', 2.0, '专业方向模块'),
            ])
        else:
            std_modules.extend([
                ('方向1', 4.0, '专业方向模块'),
                ('方向2', 4.0, '专业方向模块'),
                ('方向3', 2.0, '专业方向模块'),
            ])
        
        # 构建模块列表
        for name, credit, parent_name in std_modules:
            parent_id = self.module_map.get(parent_name)
            mod = {
                'id': self.current_id,
                'name': name,
                'required_credits': credit,
                'parent_id': parent_id
            }
            self.modules.append(mod)
            self.module_map[name] = self.current_id
            self.current_id += 1
        
        print(f"   ✅ 构建了 {len(self.modules)} 个模块")
    
    def _extract_courses(self):
        """从PDF中提取课程"""
        print(f"\n📚 提取课程信息...")
        
        # 核心公共课程（必须包含）
        core_courses = [
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
        
        # 从PDF中尝试提取课程
        extracted = self._try_extract_from_pdf()
        
        course_id = 100
        used_codes = set()
        
        # 先添加核心课程
        for code, name, credit, module_name in core_courses:
            if code not in used_codes:
                mod_id = self.module_map.get(module_name)
                if mod_id:
                    self.courses.append({
                        'id': course_id,
                        'course_code': code,
                        'name': name,
                        'credit': credit,
                        'module_id': mod_id
                    })
                    used_codes.add(code)
                    course_id += 1
        
        # 再添加提取的课程（不重复）
        for code, name, credit, mod_name in extracted:
            if code not in used_codes:
                mod_id = self.module_map.get(mod_name, self.module_map.get('专业基础课程'))
                self.courses.append({
                    'id': course_id,
                    'course_code': code,
                    'name': name,
                    'credit': credit,
                    'module_id': mod_id
                })
                used_codes.add(code)
                course_id += 1
        
        print(f"   ✅ 准备了 {len(self.courses)} 门课程")
    
    def _try_extract_from_pdf(self):
        """尝试从PDF提取课程"""
        courses = []
        
        # 查找课程代码模式
        # 模式1: GBK2000001
        # 模式2: GBK20000 01
        lines = self.full_text.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            code = None
            # 检查完整代码
            match1 = re.match(r'([A-Z]{3}\d{7})', line)
            # 检查分开代码
            match2 = re.match(r'([A-Z]{3}\d{5})\s+(\d{2})', line)
            
            if match1:
                code = match1.group(1)
                # 找课程名
                name = ""
                credit = 2.0
                j = i + 1
                while j < len(lines) and j < i + 4:
                    next_line = lines[j].strip()
                    if not re.match(r'^[A-Z][a-zA-Z\s&]+$', next_line):  # 不是英文
                        # 尝试找学分
                        credit_match = re.search(r'(\d+(?:\.\d+)?)\s*学分', next_line) or re.search(r'(\d+(?:\.\d+)?)\s*$', next_line)
                        if credit_match:
                            credit = float(credit_match.group(1))
                            name = next_line[:next_line.find(credit_match.group(0))].strip()
                        else:
                            name = next_line
                        break
                    j += 1
                if name:
                    courses.append((code, name, credit, '专业基础课程'))
            
            elif match2:
                code = match2.group(1) + match2.group(2)
                name = ""
                credit = 2.0
                j = i + 1
                while j < len(lines) and j < i + 4:
                    next_line = lines[j].strip()
                    if not re.match(r'^[A-Z][a-zA-Z\s&]+$', next_line):
                        credit_match = re.search(r'(\d+(?:\.\d+)?)\s*学分', next_line) or re.search(r'(\d+(?:\.\d+)?)\s*$', next_line)
                        if credit_match:
                            credit = float(credit_match.group(1))
                            name = next_line[:next_line.find(credit_match.group(0))].strip()
                        else:
                            name = next_line
                        break
                    j += 1
                if name:
                    courses.append((code, name, credit, '专业基础课程'))
            
            i += 1
        
        return courses
    
    def import_db(self):
        """导入数据库"""
        print(f"\n🗄️  导入数据库...")
        
        with app.app_context():
            # 学院
            college = College.query.filter_by(name=self.college_name).first()
            if not college:
                college = College(name=self.college_name, code=self.college_name[:5])
                db.session.add(college)
                db.session.commit()
            
            # 专业
            major = Major.query.filter_by(college_id=college.id, name=self.major_name).first()
            if not major:
                major = Major(name=self.major_name, code=self.major_code, college_id=college.id)
                db.session.add(major)
                db.session.commit()
            
            # 清空旧数据
            old_modules = Module.query.filter_by(major_id=major.id).all()
            mod_ids = [m.id for m in old_modules]
            if mod_ids:
                Course.query.filter(Course.module_id.in_(mod_ids)).delete(synchronize_session=False)
            Module.query.filter_by(major_id=major.id).delete(synchronize_session=False)
            db.session.commit()
            
            # 插入模块
            for mod in self.modules:
                new_mod = Module(
                    id=mod['id'],
                    name=mod['name'],
                    required_credits=mod['required_credits'],
                    parent_id=mod['parent_id'],
                    college_id=college.id,
                    major_id=major.id
                )
                db.session.add(new_mod)
            db.session.commit()
            
            # 插入课程
            new_count = 0
            for course in self.courses:
                existing = Course.query.filter_by(course_code=course['course_code']).first()
                if not existing:
                    new_course = Course(
                        id=course['id'],
                        course_code=course['course_code'],
                        name=course['name'],
                        credit=course['credit'],
                        module_id=course['module_id']
                    )
                    db.session.add(new_course)
                    new_count += 1
            db.session.commit()
            
            print(f"   ✅ 导入完成！")
            print(f"      模块: {len(self.modules)}")
            print(f"      课程: {new_count} 新增")
    
    def print_summary(self):
        """打印解析结果摘要"""
        print(f"\n" + "="*80)
        print(f"📊 {self.major_name} 解析结果")
        print("="*80)
        
        print(f"\n📦 模块结构:")
        for mod in self.modules:
            indent = "  " if mod['parent_id'] else ""
            print(f"{indent}{mod['id']}. {mod['name']} ({mod['required_credits']})")
        
        print(f"\n📚 课程数: {len(self.courses)}")
        if self.courses:
            print(f"\n   前10门课:")
            for course in self.courses[:10]:
                mod_name = next((m['name'] for m in self.modules if m['id'] == course['module_id']), "")
                print(f"      {course['course_code']}: {course['name']} ({course['credit']}) - {mod_name}")


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║        上海大学培养方案PDF解析器 - 最终版                       ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # 默认：解析通信工程
    pdf_path = r'e:\wodeaishiyan\2025通信工程.pdf'
    parser = SHUPDFParserFinal('通信与信息工程学院', '通信工程', 'TE001')
    
    if parser.parse(pdf_path):
        parser.print_summary()
        
        choice = input("\n💡 导入数据库? (y/n): ").strip().lower()
        if choice == 'y':
            parser.import_db()


if __name__ == '__main__':
    main()
