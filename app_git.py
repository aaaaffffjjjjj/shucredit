#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上海大学培养方案PDF解析器 - Web应用版
功能：上传PDF → 智能解析 → 预览编辑 → 导入数据库
新增功能：通过PDF文件名识别专业和学院归属
"""

import os
import re
import pdfplumber
import pymysql
import uuid
from flask import Flask, request, render_template, jsonify, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'supersecretkey'

# 确保目录存在
os.makedirs('uploads', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'shu_credit',
    'charset': 'utf8mb4'
}

# 全局状态（用于存储解析结果）
parsing_results = {}

# ==================== 学院-专业映射表 ====================
COLLEGE_MAJOR_MAP = {
    # 通信与信息工程学院
    '通信与信息工程学院': [
        '通信工程', '电子信息工程', '电子科学与技术', '信息安全',
        '通信工程(中外合作)', '电子信息工程(中外合作)'
    ],
    # 微电子学院
    '微电子学院': [
        '微电子科学与工程', '集成电路设计与集成系统', '微电子科学与工程(中外合作)'
    ],
    # 计算机工程与科学学院
    '计算机工程与科学学院': [
        '计算机科学与技术', '软件工程', '网络工程', '人工智能',
        '计算机科学与技术(中外合作)', '数据科学与大数据技术'
    ],
    # 机电工程与自动化学院
    '机电工程与自动化学院': [
        '机械工程', '机械设计制造及其自动化', '自动化', '测控技术与仪器',
        '工业工程', '机器人工程', '智能制造工程'
    ],
    # 材料科学与工程学院
    '材料科学与工程学院': [
        '材料科学与工程', '材料物理', '材料化学', '新能源材料与器件'
    ],
    # 环境与化学工程学院
    '环境与化学工程学院': [
        '环境工程', '化学工程与工艺', '应用化学', '生物工程', '制药工程'
    ],
    # 生命科学学院
    '生命科学学院': [
        '生物科学', '生物技术', '生物信息学', '食品科学与工程'
    ],
    # 理学院
    '理学院': [
        '数学与应用数学', '信息与计算科学', '物理学', '应用物理学',
        '统计学', '光电信息科学与工程'
    ],
    # 外国语学院
    '外国语学院': [
        '英语', '日语', '德语', '法语', '翻译'
    ],
    # 文学院
    '文学院': [
        '汉语言文学', '历史学', '哲学', '新闻学', '广播电视学', '广告学'
    ],
    # 法学院
    '法学院': [
        '法学', '知识产权'
    ],
    # 经济学院
    '经济学院': [
        '经济学', '国际经济与贸易', '金融学', '会计学', '工商管理',
        '市场营销', '信息管理与信息系统', '工程管理'
    ],
    # 管理学院
    '管理学院': [
        '工商管理', '公共管理', '信息管理与信息系统', '物流管理', '工业工程'
    ],
    # 悉尼工商学院
    '悉尼工商学院': [
        '国际经济与贸易', '工商管理', '会计学', '金融学', '信息管理与信息系统'
    ],
    # 中欧工程技术学院
    '中欧工程技术学院': [
        '机械工程', '电气工程及其自动化', '材料科学与工程', '生物工程'
    ],
    # 社会学院
    '社会学院': [
        '社会学', '社会工作', '公共事业管理'
    ],
    # 美术学院
    '美术学院': [
        '美术学', '绘画', '雕塑', '视觉传达设计', '环境设计', '产品设计'
    ],
    # 音乐学院
    '音乐学院': [
        '音乐表演', '音乐学', '作曲与作曲技术理论'
    ],
    # 体育学院
    '体育学院': [
        '体育教育', '运动训练', '社会体育指导与管理'
    ],
    # 影视学院
    '影视学院': [
        '戏剧影视文学', '广播电视编导', '表演', '动画', '数字媒体艺术'
    ],
    # 新闻传播学院
    '新闻传播学院': [
        '新闻学', '广播电视学', '广告学', '网络与新媒体', '传播学'
    ],
    # 马克思主义学院
    '马克思主义学院': [
        '思想政治教育'
    ],
    # 力学与工程科学学院
    '力学与工程科学学院': [
        '工程力学', '土木工程', '建筑环境与能源应用工程'
    ],
    # 土木工程系
    '土木工程系': [
        '土木工程', '建筑环境与能源应用工程', '给排水科学与工程'
    ],
    # 电气工程系
    '电气工程系': [
        '电气工程及其自动化', '自动化', '智能电网信息工程'
    ],
    # 化学系
    '化学系': [
        '化学', '应用化学', '材料化学'
    ],
    # 物理系
    '物理系': [
        '物理学', '应用物理学', '光电信息科学与工程'
    ],
    # 数学系
    '数学系': [
        '数学与应用数学', '信息与计算科学', '统计学'
    ],
    # 工程训练中心
    '工程训练中心': [
        '智能制造工程', '工业工程'
    ]
}

# 反向映射：专业名称 → 学院名称
MAJOR_COLLEGE_MAP = {}
for college, majors in COLLEGE_MAJOR_MAP.items():
    for major in majors:
        MAJOR_COLLEGE_MAP[major] = college

# 常见专业名称关键词
MAJOR_KEYWORDS = [
    '通信工程', '电子信息工程', '微电子', '计算机', '软件工程',
    '机械', '自动化', '材料', '环境', '化学', '生物',
    '数学', '物理', '英语', '日语', '法学', '经济', '金融',
    '会计', '管理', '土木', '电气', '建筑', '设计', '音乐',
    '体育', '新闻', '传播', '影视', '美术', '哲学', '历史'
]


def guess_college_and_major_from_filename(filename):
    """
    从PDF文件名智能识别学院和专业
    
    Args:
        filename: PDF文件名
        
    Returns:
        (college_name, major_name): 学院名称和专业名称
    """
    # 移除扩展名和常见前缀
    name = filename.replace('.pdf', '').replace('.PDF', '')
    name = re.sub(r'^(202[0-9]|培养方案|本科|专业)', '', name)
    
    # 查找专业关键词
    found_major = None
    for keyword in MAJOR_KEYWORDS:
        if keyword in name:
            found_major = keyword
            break
    
    # 如果找到专业关键词，尝试匹配学院
    if found_major:
        # 精确匹配
        for major, college in MAJOR_COLLEGE_MAP.items():
            if found_major in major:
                return college, major
        
        # 模糊匹配
        for major, college in MAJOR_COLLEGE_MAP.items():
            if found_major in major or major in found_major:
                return college, major
        
        return "未知学院", found_major
    
    return "未知学院", "未知专业"


def get_all_colleges():
    """获取所有学院列表"""
    return list(COLLEGE_MAJOR_MAP.keys())


def get_majors_by_college(college_name):
    """根据学院获取专业列表"""
    return COLLEGE_MAJOR_MAP.get(college_name, [])


# ==================== SmartPDFParser类 ====================
class SmartPDFParser:
    """智能PDF解析器"""
    
    def __init__(self):
        self.modules = []
        self.courses = []
        self.full_text = ""
        self.college_name = ""
        self.major_name = ""
        self.filename = ""
    
    def parse(self, pdf_path, filename=""):
        """解析PDF"""
        self.filename = filename
        
        # 1. 先从文件名识别学院和专业
        if filename:
            college_from_file, major_from_file = guess_college_and_major_from_filename(filename)
            self.college_name = college_from_file
            self.major_name = major_from_file
        
        # 2. 解析PDF内容
        with pdfplumber.open(pdf_path) as pdf:
            self.full_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
        
        # 3. 从PDF内容提取学院和专业（如果文件名没识别出来）
        self._extract_college_and_major()
        
        # 4. 解析模块（从PDF提取）
        self._parse_modules_from_pdf()
        
        # 5. 解析课程（从PDF提取）
        self._parse_courses_from_pdf()
        
        return True
    
    def _extract_college_and_major(self):
        """从PDF内容提取学院和专业名称"""
        # 如果文件名已经识别出学院和专业，优先级较低
        patterns = [
            r'(\S+学院)\s+(\S+专业)',
            r'(\S+专业)\s+培养方案',
            r'(\S+学院)',
            r'(\S+专业)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.full_text)
            if match:
                if len(match.groups()) >= 2:
                    pdf_college = match.group(1)
                    pdf_major = match.group(2)
                else:
                    pdf_major = match.group(1)
                    pdf_college = None
                
                # 更新学院和专业（优先使用PDF内容）
                if pdf_college and pdf_college != "未知学院":
                    self.college_name = pdf_college
                if pdf_major and pdf_major != "未知专业":
                    self.major_name = pdf_major
                break
    
    def _parse_modules_from_pdf(self):
        """从PDF解析模块"""
        pattern1 = r'(\d+)\.\s*([^\n]+?)\s*(\d+(?:\.\d+)?)\s*学分'
        pattern2 = r'（(\d+)）\s*([^\n]+?)\s*(\d+(?:\.\d+)?)\s*学分'
        pattern3 = r'([^\n]+?)\s*（(\d+(?:\.\d+)?)学分）'
        
        modules = []
        
        for pattern in [pattern1, pattern2, pattern3]:
            matches = re.findall(pattern, self.full_text)
            for match in matches:
                if len(match) == 3:
                    modules.append({
                        'order': int(match[0]),
                        'name': match[1].strip(),
                        'credits': float(match[2])
                    })
                elif len(match) == 2:
                    modules.append({
                        'order': len(modules) + 1,
                        'name': match[0].strip(),
                        'credits': float(match[1])
                    })
        
        seen = set()
        unique_modules = []
        for mod in modules:
            key = (mod['name'], mod['credits'])
            if key not in seen:
                seen.add(key)
                unique_modules.append(mod)
        
        unique_modules.sort(key=lambda x: x['order'])
        self._map_to_standard_structure(unique_modules)
    
    def _map_to_standard_structure(self, parsed_modules):
        """将解析的模块映射到标准结构"""
        standard_names = [
            '公共基础课程', '通识课程', '专业基础课程', 
            '专业必修课程', '专业选修课程', '个性化教育课程', '专业方向模块'
        ]
        
        std_modules = []
        module_id = 1
        
        for name in standard_names:
            found = False
            for parsed in parsed_modules:
                if name in parsed['name'] or parsed['name'] in name:
                    std_modules.append({
                        'id': module_id,
                        'name': name,
                        'required_credits': parsed['credits'],
                        'parent_id': None,
                        'source': 'pdf'
                    })
                    module_id += 1
                    found = True
                    break
            
            if not found:
                default_credits = {
                    '公共基础课程': 67.5,
                    '通识课程': 8.0,
                    '专业基础课程': 52.0,
                    '专业必修课程': 18.5,
                    '专业选修课程': 4.0,
                    '个性化教育课程': 10.0,
                    '专业方向模块': 10.0
                }
                std_modules.append({
                    'id': module_id,
                    'name': name,
                    'required_credits': default_credits.get(name, 10.0),
                    'parent_id': None,
                    'source': 'default'
                })
                module_id += 1
        
        sub_modules = [
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
        
        direction_credits = self._parse_direction_credits()
        if direction_credits:
            sub_modules.extend(direction_credits)
        else:
            sub_modules.extend([
                ('方向1', 4.0, '专业方向模块'),
                ('方向2', 4.0, '专业方向模块'),
                ('方向3', 2.0, '专业方向模块'),
            ])
        
        for name, credits, parent_name in sub_modules:
            parent_id = next((m['id'] for m in std_modules if m['name'] == parent_name), None)
            if parent_id:
                std_modules.append({
                    'id': module_id,
                    'name': name,
                    'required_credits': credits,
                    'parent_id': parent_id,
                    'source': 'default'
                })
                module_id += 1
        
        self.modules = std_modules
    
    def _parse_direction_credits(self):
        """尝试从PDF解析专业方向"""
        direction_section = re.search(r'专业方向.*?(?=\n\n|\Z)', self.full_text, re.DOTALL)
        if direction_section:
            text = direction_section.group()
            pattern = r'(\S+方向)\s*(\d+(?:\.\d+)?)学分'
            matches = re.findall(pattern, text)
            if matches:
                return [(m[0], float(m[1]), '专业方向模块') for m in matches]
        return None
    
    def _parse_courses_from_pdf(self):
        """从PDF解析课程"""
        courses = []
        lines = self.full_text.split('\n')
        course_id = 100
        
        for i, line in enumerate(lines):
            code_match = re.match(r'([A-Z]{3}\d{5,7})', line.strip())
            if code_match:
                code = code_match.group(1)
                name = ""
                credit = 2.0
                
                for j in range(i + 1, min(i + 5, len(lines))):
                    next_line = lines[j].strip()
                    if next_line and not re.match(r'[A-Z]{3}\d+', next_line):
                        credit_match = re.search(r'(\d+(?:\.\d+)?)\s*学分', next_line)
                        if credit_match:
                            credit = float(credit_match.group(1))
                            name = next_line[:next_line.find(credit_match.group(0))].strip()
                        else:
                            name = next_line
                        break
                
                if name:
                    courses.append({
                        'id': course_id,
                        'course_code': code,
                        'name': name,
                        'credit': credit,
                        'module_id': 3
                    })
                    course_id += 1
        
        self.courses = courses
    
    def get_result(self):
        """获取解析结果"""
        return {
            'college_name': self.college_name,
            'major_name': self.major_name,
            'filename': self.filename,
            'modules': self.modules,
            'courses': self.courses
        }


# ==================== Flask路由 ====================
@app.route('/', methods=['GET', 'POST'])
def index():
    """首页 - 上传PDF"""
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return render_template('index.html', error='请选择PDF文件')
        
        file = request.files['pdf_file']
        if file.filename == '':
            return render_template('index.html', error='请选择PDF文件')
        
        if file and file.filename.endswith('.pdf'):
            filename = str(uuid.uuid4()) + '.pdf'
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(pdf_path)
            
            # 解析PDF（传入原始文件名用于识别）
            parser = SmartPDFParser()
            try:
                parser.parse(pdf_path, file.filename)
                result = parser.get_result()
                
                session_id = os.path.splitext(filename)[0]
                parsing_results[session_id] = result
                
                return redirect(url_for('preview', session_id=session_id))
            except Exception as e:
                return render_template('index.html', error=f'解析失败: {str(e)}')
    
    # 获取所有学院列表供选择
    colleges = get_all_colleges()
    return render_template('index.html', colleges=colleges)


@app.route('/preview/<session_id>')
def preview(session_id):
    """预览页面"""
    if session_id not in parsing_results:
        return redirect(url_for('index'))
    
    result = parsing_results[session_id]
    
    # 获取所有学院和对应专业供选择
    colleges = get_all_colleges()
    majors = get_majors_by_college(result.get('college_name', ''))
    
    return render_template('preview.html', 
                           data=result, 
                           session_id=session_id,
                           colleges=colleges,
                           majors=majors)


@app.route('/get_majors/<college_name>')
def get_majors(college_name):
    """根据学院获取专业列表（AJAX接口）"""
    majors = get_majors_by_college(college_name)
    return jsonify({'success': True, 'majors': majors})


@app.route('/update', methods=['POST'])
def update():
    """更新解析结果"""
    session_id = request.form.get('session_id')
    if session_id not in parsing_results:
        return jsonify({'success': False, 'message': '会话不存在'})
    
    try:
        data = parsing_results[session_id]
        data['college_name'] = request.form.get('college_name', '')
        data['major_name'] = request.form.get('major_name', '')
        
        modules = []
        for key in request.form:
            if key.startswith('module_name_'):
                idx = int(key.split('_')[-1])
                modules.append({
                    'id': int(request.form.get(f'module_id_{idx}', idx)),
                    'name': request.form.get(f'module_name_{idx}', ''),
                    'required_credits': float(request.form.get(f'module_credits_{idx}', 0)),
                    'parent_id': int(request.form.get(f'module_parent_{idx}', 0)) or None
                })
        
        if modules:
            data['modules'] = modules
        
        courses = []
        for key in request.form:
            if key.startswith('course_code_'):
                idx = int(key.split('_')[-1])
                courses.append({
                    'id': int(request.form.get(f'course_id_{idx}', idx)),
                    'course_code': request.form.get(f'course_code_{idx}', ''),
                    'name': request.form.get(f'course_name_{idx}', ''),
                    'credit': float(request.form.get(f'course_credit_{idx}', 0)),
                    'module_id': int(request.form.get(f'course_module_{idx}', 0))
                })
        
        if courses:
            data['courses'] = courses
        
        parsing_results[session_id] = data
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/import/<session_id>')
def import_db(session_id):
    """导入数据库"""
    if session_id not in parsing_results:
        return jsonify({'success': False, 'message': '会话不存在'})
    
    data = parsing_results[session_id]
    
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM college WHERE name = %s", (data['college_name'],))
        college = cursor.fetchone()
        if not college:
            cursor.execute("INSERT INTO college (name, code) VALUES (%s, %s)", 
                          (data['college_name'], data['college_name'][:5]))
            conn.commit()
            college_id = cursor.lastrowid
        else:
            college_id = college[0]
        
        cursor.execute("SELECT id FROM major WHERE college_id = %s AND name = %s", 
                      (college_id, data['major_name']))
        major = cursor.fetchone()
        if not major:
            cursor.execute("INSERT INTO major (name, code, college_id) VALUES (%s, %s, %s)",
                          (data['major_name'], data['major_name'][:5], college_id))
            conn.commit()
            major_id = cursor.lastrowid
        else:
            major_id = major[0]
        
        cursor.execute("SELECT id FROM module WHERE major_id = %s", (major_id,))
        old_mods = [str(row[0]) for row in cursor.fetchall()]
        if old_mods:
            cursor.execute(f"DELETE FROM course WHERE module_id IN ({','.join(old_mods)})")
            cursor.execute("DELETE FROM module WHERE major_id = %s", (major_id,))
        conn.commit()
        
        for mod in data['modules']:
            cursor.execute("""
                INSERT INTO module (id, name, required_credits, parent_id, college_id, major_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (mod['id'], mod['name'], mod['required_credits'], mod['parent_id'], 
                  college_id, major_id))
        conn.commit()
        
        new_count = 0
        for course in data['courses']:
            cursor.execute("SELECT id FROM course WHERE course_code = %s", (course['course_code'],))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO course (id, course_code, name, credit, module_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (course['id'], course['course_code'], course['name'], 
                      course['credit'], course['module_id']))
                new_count += 1
        conn.commit()
        
        cursor.close()
        conn.close()
        
        del parsing_results[session_id]
        
        return jsonify({
            'success': True,
            'message': f'导入成功！模块: {len(data["modules"])}, 课程: {new_count}'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/preview/<session_id>')
def api_preview(session_id):
    """获取预览数据"""
    if session_id not in parsing_results:
        return jsonify({'success': False, 'message': '会话不存在'})
    
    return jsonify({'success': True, 'data': parsing_results[session_id]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
