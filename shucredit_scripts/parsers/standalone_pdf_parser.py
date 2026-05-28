#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
独立版PDF解析器 - 不依赖app.py
可立即使用，无需修复冲突
"""

import os
import re
import pdfplumber
import pymysql
from pymysql.cursors import DictCursor


class StandalonePDFParser:
    """独立的上海大学培养方案PDF解析器"""
    
    def __init__(self, college_name, major_name, major_code=None):
        self.college_name = college_name
        self.major_name = major_name
        self.major_code = major_code or major_name[:5]
        
        self.modules = []
        self.courses = []
        self.module_map = {}
        self.current_id = 1
        self.full_text = ""
        
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'shu_credit',
            'charset': 'utf8mb4'
        }
    
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
        
        std_modules = [
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
        ]
        
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
        
        extracted = self._try_extract_from_pdf()
        
        course_id = 100
        used_codes = set()
        
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
        lines = self.full_text.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            code = None
            match1 = re.match(r'([A-Z]{3}\d{7})', line)
            match2 = re.match(r'([A-Z]{3}\d{5})\s+(\d{2})', line)
            
            if match1:
                code = match1.group(1)
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
        """导入数据库（使用pymysql）"""
        print(f"\n🗄️  导入数据库...")
        
        conn = pymysql.connect(**self.db_config)
        cursor = conn.cursor(DictCursor)
        
        try:
            cursor.execute("SELECT id FROM college WHERE name = %s", (self.college_name,))
            college = cursor.fetchone()
            college_id = None
            if not college:
                cursor.execute("INSERT INTO college (name, code) VALUES (%s, %s)", 
                              (self.college_name, self.college_name[:5]))
                conn.commit()
                college_id = cursor.lastrowid
            else:
                college_id = college['id']
            
            cursor.execute("SELECT id FROM major WHERE college_id = %s AND name = %s", 
                          (college_id, self.major_name))
            major = cursor.fetchone()
            major_id = None
            if not major:
                cursor.execute("INSERT INTO major (name, code, college_id) VALUES (%s, %s, %s)",
                              (self.major_name, self.major_code, college_id))
                conn.commit()
                major_id = cursor.lastrowid
            else:
                major_id = major['id']
            
            cursor.execute("SELECT id FROM module WHERE major_id = %s", (major_id,))
            old_mods = [r['id'] for r in cursor.fetchall()]
            if old_mods:
                cursor.execute("DELETE FROM course WHERE module_id IN %s", (old_mods,))
                cursor.execute("DELETE FROM module WHERE major_id = %s", (major_id,))
            conn.commit()
            
            for mod in self.modules:
                cursor.execute("""
                    INSERT INTO module (id, name, required_credits, parent_id, college_id, major_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (mod['id'], mod['name'], mod['required_credits'], mod['parent_id'], 
                      college_id, major_id))
            conn.commit()
            
            new_count = 0
            for course in self.courses:
                cursor.execute("SELECT id FROM course WHERE course_code = %s", (course['course_code'],))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO course (id, course_code, name, credit, module_id)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (course['id'], course['course_code'], course['name'], 
                          course['credit'], course['module_id']))
                    new_count += 1
            conn.commit()
            
            print(f"   ✅ 导入完成！")
            print(f"      模块: {len(self.modules)}")
            print(f"      课程: {new_count} 新增")
            
        except Exception as e:
            print(f"   ❌ 导入失败: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
    
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
║      上海大学培养方案PDF解析器 - 独立版                          ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    pdf_path = r'e:\wodeaishiyan\2025通信工程.pdf'
    parser = StandalonePDFParser('通信与信息工程学院', '通信工程', 'TE001')
    
    if parser.parse(pdf_path):
        parser.print_summary()
        
        choice = input("\n💡 导入数据库? (y/n): ").strip().lower()
        if choice == 'y':
            parser.import_db()


if __name__ == '__main__':
    main()
