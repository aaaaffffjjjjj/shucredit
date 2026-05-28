from functools import wraps
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from flask import (
    Flask, request, render_template, redirect, url_for, flash,
    jsonify, session,
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, login_required,
    logout_user, current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
import pdfplumber
import re
from datetime import datetime

import time
from config import Config

try:
    from flask_compress import Compress
except ImportError:
    Compress = None

from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.sqlalchemy_uri()
app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY', Config.SECRET_KEY,
)
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_PATH'] = '/'

db = SQLAlchemy(app)
if Compress is not None:
    Compress(app)

CORS(
    app,
    supports_credentials=True,
    origins=re.compile(r"https?://.*"),
    allow_headers=['Content-Type', 'Authorization'],
    methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录'


@login_manager.unauthorized_handler
def unauthorized():
    """API 请求未登录时返回 JSON 401，避免 302 重定向到 HTML 登录页。"""
    if request.path.startswith('/api/'):
        return jsonify({
            'error': '未登录',
            'authenticated': False,
        }), 401
    return redirect(url_for('login', next=request.url))

ADMIN_USERNAME = 'admin'

# 进度 API 内存缓存：student_id -> (timestamp, payload)
_progress_cache = {}
_PROGRESS_CACHE_TTL = 60
_module_rows_cache = {'ts': 0, 'rows': None}
_MODULE_ROWS_TTL = 3600


def invalidate_progress_cache(student_id=None):
    """选课/模块变更后清除进度缓存。"""
    if student_id is None:
        _progress_cache.clear()
    else:
        keys_to_remove = [
            k for k in _progress_cache
            if (isinstance(k, tuple) and k[0] == student_id) or k == student_id
        ]
        for key in keys_to_remove:
            _progress_cache.pop(key, None)


def invalidate_module_structure_cache():
    """管理员修改模块结构后清除模块表缓存。"""
    _module_rows_cache.clear()
    _progress_cache.clear()


def _get_all_module_rows(college_id=None, major_id=None):
    """缓存模块表行，减少重复全表查询。
    如果指定 major_id，则直接按专业过滤；否则按 college_id 过滤。
    """
    if major_id is not None:
        rows = Module.query.filter_by(major_id=major_id).all()
        return rows
    now = time.time()
    cache_key = f'all_{college_id}'
    if (
        _module_rows_cache.get(cache_key)
        and now - _module_rows_cache[cache_key]['ts'] < _MODULE_ROWS_TTL
    ):
        return _module_rows_cache[cache_key]['rows']
    q = Module.query
    if college_id is not None:
        q = q.filter_by(college_id=college_id)
    rows = q.all()
    _module_rows_cache[cache_key] = {'rows': rows, 'ts': now}
    return rows


# =========================
# 数据模型
# =========================
class College(db.Model):
    __tablename__ = 'college'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code = db.Column(db.String(50), nullable=False, unique=True)


class Major(db.Model):
    __tablename__ = 'major'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=False)
    college = db.relationship('College', backref='majors')


class Module(db.Model):
    __tablename__ = 'module'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    required_credits = db.Column(db.Float, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=True)
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=False, default=1)
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'), nullable=True)
    children = db.relationship(
        'Module', backref=db.backref('parent', remote_side=[id])
    )


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(50), index=True)
    name = db.Column(db.String(150))
    credit = db.Column(db.Float, default=0)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), index=True)
    module = db.relationship('Module', backref='courses')
    __table_args__ = (
        db.UniqueConstraint('course_code', 'module_id', name='uix_course_code_module'),
    )


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    major = db.Column(db.String(100))
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=True)
    college = db.relationship('College')
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'), nullable=True)
    major_ref = db.relationship('Major')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), unique=True, nullable=False)
    student = db.relationship('Student', backref='user', uselist=False)
    is_admin = db.Column(db.Boolean, default=False)


class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), index=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), index=True)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user = db.relationship('User', backref='posts')
    comments = db.relationship(
        'Comment', backref='post', cascade='all, delete-orphan'
    )


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='comments')


class Announcement(db.Model):
    __tablename__ = 'announcement'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = db.relationship('User', backref='announcements')


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# =========================
# 权限与数据库辅助
# =========================
def admin_required(view_func):
    """
    装饰器：限制仅管理员用户可访问视图。

    须已登录且 ``username == ADMIN_USERNAME``，否则 flash 并重定向至进度页。
    """
    @wraps(view_func)
    @login_required
    def wrapped(*args, **kwargs):
        if current_user.username != ADMIN_USERNAME:
            flash('无权限访问此页面', 'danger')
            return redirect(url_for('progress'))
        return view_func(*args, **kwargs)
    return wrapped


def safe_commit(success_msg=None, redirect_to=None):
    """
    提交当前数据库事务。

    Args:
        success_msg: 成功时 flash 的提示文案。
        redirect_to: 失败时重定向目标 URL。

    Returns:
        失败时返回 ``redirect`` 响应，成功返回 ``None``。
    """
    try:
        db.session.commit()
        if success_msg:
            flash(success_msg, 'success')
        return None
    except Exception as exc:
        db.session.rollback()
        flash(f'操作失败：{exc}', 'danger')
        return redirect(redirect_to) if redirect_to else None


# =========================
# 模块树与学分汇总
# =========================
def normalize_module_name(name):
    """
    规范化模块显示名称，兼容导入数据中的前导点或空格。

    Args:
        name: 原始模块名称字符串。

    Returns:
        去除首尾空白及前导 ``.`` 后的名称；空输入原样返回。
    """
    if not name:
        return name
    return name.strip('. ').strip()


def get_descendant_ids(module_id):
    """
    收集某模块的全部后代模块 ID（不含自身）。

    Args:
        module_id: 根模块主键。

    Returns:
        后代模块 id 的集合。
    """
    descendants = set()
    stack = [module_id]
    while stack:
        current = stack.pop()
        children = Module.query.filter_by(parent_id=current).all()
        for child in children:
            if child.id not in descendants:
                descendants.add(child.id)
                stack.append(child.id)
    return descendants


def would_create_cycle(module_id, new_parent_id):
    """
    判断将模块挂到新父节点下是否会产生循环引用。

    Args:
        module_id: 待移动的模块 id。
        new_parent_id: 目标父模块 id；``None`` 表示置顶为根模块。

    Returns:
        ``True`` 表示移动非法（自身或后代作为父节点），否则 ``False``。
    """
    if new_parent_id is None:
        return False
    if new_parent_id == module_id:
        return True
    return new_parent_id in get_descendant_ids(module_id)


def compute_earned_credits(student_id, college_id=None, major_id=None):
    """
    按模块树后序汇总学生已修学分。

    Args:
        student_id: 学生主键。
        college_id: 可选，仅统计指定学院的模块。
        major_id: 可选，仅统计指定专业的模块（优先级高于 college_id）。

    Returns:
        ``dict[int, float]``：键为 ``module.id``，值为该模块及子树已修学分总和
        （直接课程学分 + 所有子模块汇总）。
    """
    enrolled = (
        db.session.query(Course)
        .join(Enrollment)
        .filter(Enrollment.student_id == student_id)
        .all()
    )
    direct = {}
    for course in enrolled:
        if course.module_id:
            direct[course.module_id] = direct.get(course.module_id, 0) + (course.credit or 0)

    all_modules = _get_all_module_rows(college_id, major_id)
    children_map = {}
    for mod in all_modules:
        if mod.parent_id is not None:
            children_map.setdefault(mod.parent_id, []).append(mod.id)

    earned = {}

    def total(module_id):
        if module_id in earned:
            return earned[module_id]
        child_sum = sum(total(cid) for cid in children_map.get(module_id, []))
        earned[module_id] = direct.get(module_id, 0) + child_sum
        return earned[module_id]

    for mod in all_modules:
        total(mod.id)
    return earned


def build_module_options(modules, parent_id=None, level=0, exclude_ids=None):
    """
    构建树形下拉框选项列表。

    Args:
        modules: 全部 ``Module`` 记录（或兼容对象列表）。
        parent_id: 当前层父模块 id；``None`` 表示顶级。
        level: 嵌套深度，用于缩进显示。
        exclude_ids: 需要排除的模块 id 集合。

    Returns:
        ``list[tuple[int, str, int]]``：``(模块id, 显示标签, 层级)``。
    """
    exclude_ids = exclude_ids or set()
    options = []
    for mod in modules:
        if mod.parent_id == parent_id and mod.id not in exclude_ids:
            display = normalize_module_name(mod.name)
            prefix = '　' * level + '└ ' if level > 0 else ''
            options.append((mod.id, f"{prefix}{display}", level))
            options.extend(
                build_module_options(modules, mod.id, level + 1, exclude_ids)
            )
    return options


def build_move_options(all_modules, module_id):
    """
    生成模块移动时可选择的父模块列表。

    Args:
        all_modules: 全部模块记录。
        module_id: 当前被移动模块的 id。

    Returns:
        与 :func:`build_module_options` 相同格式的合法父节点选项。
    """
    forbidden = {module_id} | get_descendant_ids(module_id)
    return build_module_options(all_modules, parent_id=None, exclude_ids=forbidden)


def build_progress_module_tree(all_modules, earned_map):
    """
    构建学分进度页的嵌套模块树。

    Args:
        all_modules: 全部 ``Module`` 记录。
        earned_map: :func:`compute_earned_credits` 的返回值。

    Returns:
        根节点字典列表，每个节点含 ``children`` 及学分统计字段。
        ``parent_id`` 缺失父记录时视为根节点。
    """
    nodes = {}
    for mod in all_modules:
        earned = earned_map.get(mod.id, 0)
        remaining = mod.required_credits - earned
        percent = (
            round(earned / mod.required_credits * 100, 1)
            if mod.required_credits > 0 else 0
        )
        nodes[mod.id] = {
            'id': mod.id,
            'name': normalize_module_name(mod.name),
            'required': mod.required_credits,
            'earned': round(earned, 2),
            'remaining': round(max(remaining, 0), 2),
            'percent': percent,
            'children': [],
        }

    module_ids = set(nodes.keys())
    roots = []
    for mod in all_modules:
        if mod.parent_id is None or mod.parent_id not in module_ids:
            roots.append(nodes[mod.id])
        else:
            nodes[mod.parent_id]['children'].append(nodes[mod.id])

    def sort_children(node):
        node['children'].sort(key=lambda x: x['name'])
        for child in node['children']:
            sort_children(child)

    for root in roots:
        sort_children(root)
    roots.sort(key=lambda x: x['name'])
    return roots


def check_graduation_met(earned_map, all_modules):
    """
    判定是否满足毕业学分要求。

    Args:
        earned_map: 模块 id 到已修学分的映射。
        all_modules: 全部模块记录。

    Returns:
        当且仅当所有 ``parent_id IS NULL`` 的顶级模块均已达标时为 ``True``。
    """
    roots = [m for m in all_modules if m.parent_id is None]
    if not roots:
        return False
    return all(
        earned_map.get(m.id, 0) >= m.required_credits for m in roots
    )


def build_admin_module_tree(all_modules, course_counts):
    """
    构建管理员模块管理页的树形数据。

    Args:
        all_modules: 全部模块记录。
        course_counts: ``module_id -> 课程数量`` 映射。

    Returns:
        根节点列表；节点含 ``move_options``、``can_delete`` 等管理字段。
    """
    nodes = {}
    for mod in all_modules:
        child_count = sum(1 for m in all_modules if m.parent_id == mod.id)
        c_count = course_counts.get(mod.id, 0)
        nodes[mod.id] = {
            'id': mod.id,
            'name': normalize_module_name(mod.name),
            'required': mod.required_credits,
            'child_count': child_count,
            'course_count': c_count,
            'can_delete': child_count == 0 and c_count == 0,
            'move_options': build_move_options(all_modules, mod.id),
            'children': [],
        }

    module_ids = set(nodes.keys())
    roots = []
    for mod in all_modules:
        if mod.parent_id is None or mod.parent_id not in module_ids:
            roots.append(nodes[mod.id])
        else:
            nodes[mod.parent_id]['children'].append(nodes[mod.id])

    def sort_children(node):
        node['children'].sort(key=lambda x: x['name'])
        for child in node['children']:
            sort_children(child)

    for root in roots:
        sort_children(root)
    roots.sort(key=lambda x: x['name'])
    return roots


def module_stats_for_children(parent, earned_map):
    """
    汇总某模块下直接子模块的学分进度行数据。

    Args:
        parent: 父 ``Module`` 实例。
        earned_map: :func:`compute_earned_credits` 的返回值。

    Returns:
        子模块进度字典列表，供 ``submodules.html`` 渲染。
    """
    sub_data = []
    for child in parent.children:
        earned_credits = earned_map.get(child.id, 0)
        remaining = child.required_credits - earned_credits
        percent = (
            round(earned_credits / child.required_credits * 100, 1)
            if child.required_credits > 0 else 0
        )
        sub_data.append({
            'id': child.id,
            'name': normalize_module_name(child.name),
            'required': child.required_credits,
            'earned': round(earned_credits, 2),
            'remaining': round(max(remaining, 0), 2),
            'percent': percent,
        })
    return sub_data


# =========================
# PDF 解析
# =========================
def parse_schedule_pdf(pdf_path):
    """从 PDF 提取课程编号；尽量附带名称与学分。"""
    parsed = {}
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            for line in text.split('\n'):
                line = line.strip()
                if not line:
                    continue
                rich = re.match(
                    r'([A-Z]{2,5}\d{6,})\s+([\u4e00-\u9fa5A-Za-z0-9（）·\-\s]+?)\s+(\d+\.?\d*)\s*$',
                    line,
                )
                if rich:
                    code = rich.group(1)
                    parsed[code] = {
                        'course_code': code,
                        'name': rich.group(2).strip()[:150],
                        'credit': float(rich.group(3)),
                    }
                    continue
                for code in re.findall(r'[A-Z]{2,5}\d{6,}', line):
                    if code not in parsed:
                        parsed[code] = {
                            'course_code': code, 'name': '', 'credit': 0,
                        }
    return list(parsed.values())


def get_module_descendant_ids(module_id):
    """返回模块自身及所有后代模块 id。"""
    ids = {module_id}
    stack = [module_id]
    while stack:
        current = stack.pop()
        for child in Module.query.filter_by(parent_id=current).all():
            if child.id not in ids:
                ids.add(child.id)
                stack.append(child.id)
    return ids


def get_enrolled_course_ids(student_id):
    return {
        row.course_id
        for row in Enrollment.query.filter_by(student_id=student_id).all()
    }


def recommend_courses_for_module(student_id, module_id):
    """模块子树内未修读的课程列表（单次查询）。"""
    module_ids = list(get_module_descendant_ids(module_id))
    if not module_ids:
        return []
    enrolled = get_enrolled_course_ids(student_id)
    query = Course.query.filter(Course.module_id.in_(module_ids))
    if enrolled:
        query = query.filter(~Course.id.in_(enrolled))
    return query.order_by(Course.course_code).all()


def course_to_dict(course, include_module_name=False):
    """序列化课程；默认仅返回列表展示所需字段。"""
    data = {
        'id': course.id,
        'course_code': course.course_code,
        'name': course.name,
        'credit': course.credit,
        'module_id': course.module_id,
    }
    if include_module_name and course.module:
        data['module_name'] = normalize_module_name(course.module.name)
    return data


def merge_unknown_to_session(items):
    """合并未识别课程到 session，供后续手动补全。"""
    store = session.get('unknown_courses') or {}
    for item in items:
        code = item['course_code']
        store[code] = {
            'course_code': code,
            'name': item.get('name') or store.get(code, {}).get('name', ''),
            'credit': item.get('credit') or store.get(code, {}).get('credit', 0),
        }
    session['unknown_courses'] = store
    session.modified = True


def _module_status(earned, remaining):
    if remaining <= 0:
        return 'complete'
    if earned > 0:
        return 'partial'
    return 'none'


def build_progress_api_payload(student_id, use_cache=True, college_id=None, major_id=None):
    """生成进度页图谱与模块水桶数据（精简 JSON + 短期缓存）。"""
    now = time.time()
    cache_key = (student_id, college_id, major_id)
    if use_cache and cache_key in _progress_cache:
        cached_at, payload = _progress_cache[cache_key]
        if now - cached_at < _PROGRESS_CACHE_TTL:
            return payload

    earned_map = compute_earned_credits(student_id, college_id, major_id)
    all_modules = _get_all_module_rows(college_id, major_id)
    tree = build_progress_module_tree(all_modules, earned_map)
    graph_nodes = []
    graph_links = []
    modules_flat = []
    status_colors = {
        'complete': '#34c759',
        'partial': '#ff9500',
        'none': '#ff3b30',
    }

    def walk(nodes, parent_id=None):
        for node in nodes:
            status = _module_status(node['earned'], node['remaining'])
            label = node['name']
            if len(label) > 14:
                label = label[:13] + '…'
            graph_nodes.append({
                'id': str(node['id']),
                'name': node['name'],
                'value': node['required'],
                'required': node['required'],
                'earned': node['earned'],
                'remaining': node['remaining'],
                'percent': node['percent'],
                'status': status,
                'symbolSize': max(36, min(94, node['required'] * 2.3)),
                'itemStyle': {
                    'color': status_colors[status],
                    'borderColor': 'rgba(255,255,255,0.9)',
                    'borderWidth': 2,
                    'shadowBlur': 10,
                    'shadowColor': 'rgba(0,0,0,0.1)',
                },
                'label': {
                    'show': True,
                    'formatter': f'{label}\n{node["percent"]}%',
                    'fontSize': 14,
                    'lineHeight': 18,
                    'color': '#fff',
                },
            })
            # 获取模块的课程列表
            module_courses = Course.query.filter_by(module_id=node['id']).all()
            courses_list = [{
                'id': c.id,
                'course_code': c.course_code,
                'name': c.name,
                'credit': c.credit,
            } for c in module_courses]
            
            modules_flat.append({
                'id': node['id'],
                'name': node['name'],
                'parent_id': parent_id,
                'required': node['required'],
                'earned': node['earned'],
                'remaining': node['remaining'],
                'percent': node['percent'],
                'status': status,
                'courses': courses_list,
                'course_count': len(courses_list),
            })
            if parent_id is not None:
                graph_links.append({
                    'source': str(parent_id),
                    'target': str(node['id']),
                })
            if node['children']:
                walk(node['children'], node['id'])

    walk(tree)
    roots = [m for m in modules_flat if m['parent_id'] is None]
    payload = {
        'graph': {'nodes': graph_nodes, 'links': graph_links},
        'modules': modules_flat,
        'all_met': check_graduation_met(earned_map, all_modules),
        'sun': {
            'required': sum(r['required'] for r in roots) or 160.0,
            'earned': sum(r['earned'] for r in roots),
        },
    }
    _progress_cache[cache_key] = (now, payload)
    return payload


def json_response_cached(data, max_age=30):
    """带 Cache-Control 的 JSON 响应。"""
    resp = jsonify(data)
    resp.headers['Cache-Control'] = f'private, max-age={max_age}'
    return resp


def process_pdf_upload(student, files):
    """处理 PDF 上传，返回插入数与未识别课程列表。"""
    os.makedirs('uploads', exist_ok=True)
    inserted = 0
    unknown_items = []

    for file in files:
        if not file or not file.filename.lower().endswith('.pdf'):
            continue
        path = os.path.join(
            'uploads',
            f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}",
        )
        file.save(path)
        for item in parse_schedule_pdf(path):
            course = Course.query.filter_by(
                course_code=item['course_code']
            ).first()
            if not course:
                unknown_items.append(item)
                continue
            exists = Enrollment.query.filter_by(
                student_id=student.id, course_id=course.id
            ).first()
            if not exists:
                db.session.add(
                    Enrollment(student_id=student.id, course_id=course.id)
                )
                inserted += 1
    return inserted, unknown_items


# =========================
# 路由：首页与认证
# =========================
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('progress'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            flash('请填写用户名和密码', 'warning')
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'danger')
            return redirect(url_for('register'))
        try:
            student = Student(name=username, major='通信工程')
            db.session.add(student)
            db.session.flush()
            user = User(
                username=username,
                password_hash=generate_password_hash(password),
                student_id=student.id,
            )
            db.session.add(user)
            err = safe_commit('注册成功，请登录', redirect_to=url_for('register'))
            if err:
                return err
            return redirect(url_for('login'))
        except Exception as exc:
            db.session.rollback()
            flash(f'注册失败：{exc}', 'danger')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('progress'))
        flash('用户名或密码错误', 'danger')
    return render_template('login.html')


@app.route('/api/auth/login', methods=['POST'])
def login_api():
    """Next.js 前端登录：建立 Flask-Login Session（Set-Cookie）。"""
    data = request.get_json(silent=True) or {}
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''
    if not username or not password:
        return jsonify({
            'success': False,
            'message': '请提供用户名和密码',
        }), 400
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user, remember=True)
        student = user.student
        college = student.college if student and student.college_id else None
        major_ref = student.major_ref if student and student.major_id else None
        return jsonify({
            'success': True,
            'message': '登录成功',
            'user': {
                'id': user.id,
                'username': user.username,
            },
            'student': {
                'id': student.id if student else None,
                'name': student.name if student else '',
            },
            'college': {
                'id': college.id,
                'name': college.name,
                'code': college.code,
            } if college else None,
            'major': {
                'id': major_ref.id,
                'name': major_ref.name,
                'college_id': major_ref.college_id,
            } if major_ref else None,
        })
    return jsonify({
        'success': False,
        'message': '用户名或密码错误',
    }), 401


@app.route('/api/auth/register', methods=['POST'])
def register_api():
    """Next.js 前端注册。"""
    data = request.get_json(silent=True) or {}
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''
    name = (data.get('name') or username).strip()
    college_id = data.get('college_id')
    major_id = data.get('major_id')
    if college_id is not None:
        try:
            college_id = int(college_id)
        except (ValueError, TypeError):
            college_id = None
    if major_id is not None:
        try:
            major_id = int(major_id)
        except (ValueError, TypeError):
            major_id = None
    if not username or not password:
        return jsonify({
            'success': False,
            'message': '请填写用户名和密码',
        }), 400
    if User.query.filter_by(username=username).first():
        return jsonify({
            'success': False,
            'message': '用户名已存在',
        }), 409
    try:
        major_name = '通信工程'
        if major_id:
            mj = db.session.get(Major, major_id)
            if mj:
                major_name = mj.name
        student = Student(
            name=name or username,
            major=major_name,
            college_id=college_id,
            major_id=major_id,
        )
        db.session.add(student)
        db.session.flush()
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            student_id=student.id,
        )
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return jsonify({
            'success': True,
            'message': '注册成功',
            'user': {'id': user.id, 'username': user.username},
        })
    except Exception as exc:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(exc)}), 500


@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout_api():
    logout_user()
    return jsonify({'success': True, 'message': '已退出登录'})


@app.route('/api/auth/me', methods=['GET'])
def me_api():
    if current_user.is_authenticated:
        student = current_user.student
        college = student.college if student and student.college_id else None
        major_ref = student.major_ref if student and student.major_id else None
        return jsonify({
            'authenticated': True,
            'user': {
                'id': current_user.id,
                'username': current_user.username,
            },
            'student': {
                'id': student.id if student else None,
                'name': student.name if student else '',
            },
            'college': {
                'id': college.id,
                'name': college.name,
                'code': college.code,
            } if college else None,
            'major': {
                'id': major_ref.id,
                'name': major_ref.name,
                'college_id': major_ref.college_id,
            } if major_ref else None,
        })
    return jsonify({'authenticated': False}), 401


@app.route('/api/colleges', methods=['GET'])
def api_colleges():
    colleges = College.query.order_by(College.id).all()
    return jsonify({
        'colleges': [
            {'id': c.id, 'name': c.name, 'code': c.code}
            for c in colleges
        ],
    })


@app.route('/api/majors', methods=['GET'])
def api_majors():
    college_id = request.args.get('college_id')
    q = Major.query.order_by(Major.id)
    if college_id:
        try:
            q = q.filter_by(college_id=int(college_id))
        except (ValueError, TypeError):
            pass
    majors = q.all()
    return jsonify({
        'majors': [
            {'id': m.id, 'name': m.name, 'college_id': m.college_id}
            for m in majors
        ],
    })


@app.route('/api/user/college', methods=['POST'])
@login_required
def api_set_user_college():
    data = request.get_json(silent=True) or {}
    college_id = data.get('college_id')
    if college_id is None:
        return jsonify({'success': False, 'message': '请提供学院ID'}), 400
    try:
        college_id = int(college_id)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': '无效的学院ID'}), 400

    college = db.session.get(College, college_id)
    if not college:
        return jsonify({'success': False, 'message': '学院不存在'}), 404

    student = current_user.student
    student.college_id = college_id
    db.session.commit()
    invalidate_progress_cache(student.id)
    return jsonify({
        'success': True,
        'message': '学院已切换',
        'college': {'id': college.id, 'name': college.name, 'code': college.code},
    })


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出登录', 'success')
    return redirect(url_for('login'))


# =========================
# 路由：学分进度与 PDF
# =========================
@app.route('/api/progress_data')
@login_required
def api_progress_data():
    major_id_str = request.args.get('major_id')
    major_id = None
    if major_id_str:
        try:
            major_id = int(major_id_str)
        except (ValueError, TypeError):
            pass
    college_id_str = request.args.get('college_id')
    college_id = None
    if college_id_str:
        try:
            college_id = int(college_id_str)
        except (ValueError, TypeError):
            pass
    if major_id is None and college_id is None and current_user.student.college_id:
        college_id = current_user.student.college_id
    payload = build_progress_api_payload(
        current_user.student.id, college_id=college_id, major_id=major_id
    )
    return json_response_cached(payload, max_age=30)


@app.route('/api/recommend_courses/<int:module_id>')
@login_required
def api_recommend_courses(module_id):
    mod = db.session.get(Module, module_id)
    if not mod:
        return jsonify({'error': '模块不存在'}), 404
    courses = recommend_courses_for_module(
        current_user.student.id, module_id
    )
    return json_response_cached({
        'module': {
            'id': mod.id,
            'name': normalize_module_name(mod.name),
        },
        'courses': [course_to_dict(c) for c in courses],
    }, max_age=15)


@app.route('/api/enroll/<int:course_id>', methods=['POST'])
@login_required
def api_enroll_course(course_id):
    student = current_user.student
    course = db.session.get(Course, course_id)
    if not course:
        return jsonify({'error': '课程不存在'}), 404
    exists = Enrollment.query.filter_by(
        student_id=student.id, course_id=course.id
    ).first()
    if exists:
        return jsonify({'ok': True, 'message': '已在已修列表中'})
    try:
        db.session.add(Enrollment(student_id=student.id, course_id=course.id))
        db.session.commit()
        invalidate_progress_cache(student.id)
        payload = build_progress_api_payload(student.id, use_cache=False)
        return jsonify({
            'ok': True,
            'message': f'已添加 {course.name}',
            'progress': payload,
        })
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': str(exc)}), 500


@app.route('/api/enroll_batch', methods=['POST'])
@login_required
def api_enroll_batch():
    data = request.get_json(silent=True) or {}
    ids = data.get('course_ids', [])
    student = current_user.student
    added = 0
    try:
        enrolled = get_enrolled_course_ids(student.id)
        for cid in ids:
            cid = int(cid)
            if cid in enrolled:
                continue
            if db.session.get(Course, cid):
                db.session.add(
                    Enrollment(student_id=student.id, course_id=cid)
                )
                enrolled.add(cid)
                added += 1
        db.session.commit()
        invalidate_progress_cache(student.id)
        payload = build_progress_api_payload(student.id, use_cache=False)
        return jsonify({
            'ok': True,
            'added': added,
            'message': f'已添加 {added} 门课程',
            'progress': payload,
        })
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': str(exc)}), 500


@app.route('/api/module_options')
@login_required
def api_module_options():
    modules = Module.query.order_by(Module.name).all()
    options = build_module_options(modules)
    return jsonify({
        'options': [
            {'id': oid, 'label': label, 'level': lvl}
            for oid, label, lvl in options
        ],
    })


@app.route('/api/unknown_courses', methods=['GET', 'POST'])
@login_required
def api_unknown_courses():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        items = data.get('courses', [])
        merge_unknown_to_session(items)
    store = session.get('unknown_courses') or {}
    return jsonify({'courses': list(store.values())})


@app.route('/api/add_course_from_user', methods=['POST'])
@login_required
def api_add_course_from_user():
    data = request.get_json(silent=True) or {}
    code = (data.get('course_code') or '').strip()
    name = (data.get('name') or '').strip()
    module_id = data.get('module_id')
    try:
        credit = float(data.get('credit', 0))
    except (TypeError, ValueError):
        return jsonify({'error': '学分格式无效'}), 400

    if not code or not name or not module_id:
        return jsonify({'error': '请填写课程编号、名称和所属模块'}), 400
    if not db.session.get(Module, int(module_id)):
        return jsonify({'error': '所属模块不存在'}), 400

    store = session.get('unknown_courses') or {}
    if code not in store:
        return jsonify({'error': '只能添加待处理列表中的未识别课程'}), 403

    student = current_user.student
    try:
        course = Course.query.filter_by(course_code=code).first()
        if course:
            if not Enrollment.query.filter_by(
                student_id=student.id, course_id=course.id
            ).first():
                db.session.add(
                    Enrollment(student_id=student.id, course_id=course.id)
                )
        else:
            course = Course(
                course_code=code,
                name=name,
                credit=credit,
                module_id=int(module_id),
            )
            db.session.add(course)
            db.session.flush()
            db.session.add(
                Enrollment(student_id=student.id, course_id=course.id)
            )
        store.pop(code, None)
        session['unknown_courses'] = store
        session.modified = True
        db.session.commit()
        invalidate_progress_cache(student.id)
        payload = build_progress_api_payload(student.id, use_cache=False)
        return jsonify({
            'ok': True,
            'message': f'课程 {code} 已加入课程库并记入已修',
            'progress': payload,
            'unknown': list(store.values()),
        })
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': str(exc)}), 500


@app.route('/api/my_courses')
@login_required
def api_my_courses():
    student = current_user.student
    courses = (
        db.session.query(Course)
        .join(Enrollment)
        .filter(Enrollment.student_id == student.id)
        .order_by(Course.course_code)
        .all()
    )
    return jsonify({'courses': [course_to_dict(c) for c in courses]})


@app.route('/api/remove_enrollment', methods=['POST'])
@login_required
def api_remove_enrollment():
    data = request.get_json(silent=True) or {}
    code = (data.get('course_code') or '').strip()
    course = Course.query.filter_by(course_code=code).first()
    if not course:
        return jsonify({'error': '课程不存在'}), 404
    try:
        Enrollment.query.filter_by(
            student_id=current_user.student.id, course_id=course.id
        ).delete()
        sid = current_user.student.id
        db.session.commit()
        invalidate_progress_cache(sid)
        payload = build_progress_api_payload(sid, use_cache=False)
        return jsonify({
            'ok': True,
            'progress': payload,
            'courses': [
                course_to_dict(c) for c in
                db.session.query(Course).join(Enrollment).filter(
                    Enrollment.student_id == sid
                ).all()
            ],
        })
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': str(exc)}), 500


@app.route('/api/upload_pdf', methods=['POST'])
@login_required
def api_upload_pdf():
    student = current_user.student
    files = request.files.getlist('file')
    if not files or files[0].filename == '':
        return jsonify({'error': '请选择 PDF 文件'}), 400
    try:
        inserted, unknown_items = process_pdf_upload(student, files)
        if unknown_items:
            merge_unknown_to_session(unknown_items)
        db.session.commit()
        invalidate_progress_cache(student.id)
        payload = build_progress_api_payload(student.id, use_cache=False)
        store = session.get('unknown_courses') or {}
        return jsonify({
            'ok': True,
            'inserted': inserted,
            'unknown': list(store.values()),
            'message': (
                f'成功添加 {inserted} 门课程'
                + (f'，{len(unknown_items)} 个编号待手动处理'
                   if unknown_items else '')
            ),
            'progress': payload,
        })
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': str(exc)}), 500


# =========================
# 路由：管理员
# =========================
@app.route('/admin/courses', methods=['GET', 'POST'])
@admin_required
def admin_courses():
    if request.method == 'POST' and 'add_course' in request.form:
        course_code = request.form.get('new_course_code', '').strip()
        course_name = request.form.get('new_course_name', '').strip()
        credit_str = request.form.get('new_credit', '').strip()
        module_id = request.form.get('new_module_id', '')

        if not (course_code and course_name and credit_str and module_id):
            flash('请填写完整信息', 'warning')
            return redirect(url_for('admin_courses'))
        try:
            credit = float(credit_str)
        except ValueError:
            flash('学分必须是数字', 'danger')
            return redirect(url_for('admin_courses'))

        if Course.query.filter_by(course_code=course_code).first():
            flash(f'课程编号 {course_code} 已存在', 'danger')
        else:
            db.session.add(Course(
                course_code=course_code,
                name=course_name,
                credit=credit,
                module_id=int(module_id),
            ))
            err = safe_commit(
                f'课程 {course_code} 添加成功',
                redirect_to=url_for('admin_courses'),
            )
            if err:
                return err
        return redirect(url_for('admin_courses'))

    if request.method == 'POST' and 'update_course' in request.form:
        course_id = request.form.get('course_id')
        new_module_id = request.form.get('module_id')
        if not course_id:
            flash('无效请求', 'warning')
            return redirect(url_for('admin_courses'))
        try:
            course = db.session.get(Course, int(course_id))
            if not course:
                flash('课程不存在', 'danger')
            else:
                course.module_id = int(new_module_id) if new_module_id else None
                err = safe_commit(
                    f'课程 {course.course_code} 的模块已更新',
                    redirect_to=url_for('admin_courses'),
                )
                if err:
                    return err
        except (ValueError, TypeError):
            flash('请选择有效模块', 'warning')
        except Exception as exc:
            db.session.rollback()
            flash(f'更新失败：{exc}', 'danger')
        return redirect(url_for('admin_courses'))

    courses = Course.query.order_by(Course.course_code).all()
    for course in courses:
        if course.module:
            path_parts = []
            mod = course.module
            while mod:
                path_parts.append(normalize_module_name(mod.name))
                mod = mod.parent
            course.module_path = ' / '.join(reversed(path_parts))
        else:
            course.module_path = '未分配'

    all_modules = Module.query.order_by(Module.name).all()
    module_options = build_module_options(all_modules)
    return render_template(
        'admin_courses.html',
        courses=courses,
        module_options=module_options,
    )


def _admin_modules_redirect():
    return url_for('admin_modules')


def admin_module_add_root(redirect_to):
    """添加顶级模块。"""
    name = request.form.get('name', '').strip()
    credits = float(request.form.get('required_credits', 0))
    if not name:
        flash('模块名称不能为空', 'warning')
        return None
    db.session.add(Module(name=name, required_credits=credits, parent_id=None))
    return safe_commit(
        f'顶级模块「{normalize_module_name(name)}」已添加',
        redirect_to=redirect_to,
    )


def admin_module_add_child(redirect_to):
    """在指定父模块下添加子模块。"""
    parent_id = int(request.form.get('parent_id'))
    name = request.form.get('name', '').strip()
    credits = float(request.form.get('required_credits', 0))
    parent = db.session.get(Module, parent_id)
    if not parent:
        flash('父模块不存在', 'danger')
        return None
    if not name:
        flash('子模块名称不能为空', 'warning')
        return None
    db.session.add(Module(
        name=name, required_credits=credits, parent_id=parent_id,
    ))
    return safe_commit(
        f'子模块「{name}」已添加到「{normalize_module_name(parent.name)}」下',
        redirect_to=redirect_to,
    )


def admin_module_update(redirect_to):
    """更新模块名称与要求学分。"""
    module_id = int(request.form.get('module_id'))
    name = request.form.get('name', '').strip()
    credits = float(request.form.get('required_credits', 0))
    mod = db.session.get(Module, module_id)
    if not mod:
        flash('模块不存在', 'danger')
        return None
    if not name:
        flash('模块名称不能为空', 'warning')
        return None
    mod.name = name
    mod.required_credits = credits
    return safe_commit('模块已更新', redirect_to=redirect_to)


def admin_module_move(redirect_to):
    """移动模块到新的父节点或置顶。"""
    module_id = int(request.form.get('module_id'))
    raw_parent = request.form.get('new_parent_id', '').strip()
    new_parent_id = int(raw_parent) if raw_parent else None
    mod = db.session.get(Module, module_id)
    if not mod:
        flash('模块不存在', 'danger')
        return None
    if would_create_cycle(module_id, new_parent_id):
        flash('不能将模块移动到自身或其子模块下（会形成循环）', 'danger')
        return None
    mod.parent_id = new_parent_id
    return safe_commit('模块已移动', redirect_to=redirect_to)


def admin_module_delete(redirect_to):
    """删除无子模块且无课程的叶子模块。"""
    module_id = int(request.form.get('module_id'))
    mod = db.session.get(Module, module_id)
    if not mod:
        flash('模块不存在', 'danger')
        return None
    if mod.children:
        flash('该模块仍有子模块，无法删除', 'danger')
        return None
    if Course.query.filter_by(module_id=module_id).first():
        flash('该模块下仍有课程，无法删除', 'danger')
        return None
    db.session.delete(mod)
    return safe_commit('模块已删除', redirect_to=redirect_to)


def process_admin_module_post():
    """
    分发管理员模块管理页的 POST 操作。

    Returns:
        需要立即返回的 ``redirect`` 响应，或 ``None``（表示应刷新列表页）。
    """
    action = request.form.get('action', '')
    redirect_to = _admin_modules_redirect()
    handlers = {
        'add_root': admin_module_add_root,
        'add_child': admin_module_add_child,
        'update': admin_module_update,
        'move': admin_module_move,
        'delete': admin_module_delete,
    }
    handler = handlers.get(action)
    if not handler:
        flash('未知操作', 'warning')
        return redirect(redirect_to)
    try:
        result = handler(redirect_to)
        if result is None:
            invalidate_module_structure_cache()
        return result if result else redirect(redirect_to)
    except ValueError:
        flash('请填写有效的数字', 'danger')
        return redirect(redirect_to)
    except Exception as exc:
        db.session.rollback()
        flash(f'操作失败：{exc}', 'danger')
        return redirect(redirect_to)


@app.route('/admin/modules', methods=['GET', 'POST'])
@admin_required
def admin_modules():
    if request.method == 'POST':
        return process_admin_module_post()

    all_modules = Module.query.all()
    course_counts = dict(
        db.session.query(Course.module_id, func.count(Course.id))
        .group_by(Course.module_id)
        .all()
    )
    module_tree = build_admin_module_tree(all_modules, course_counts)
    return render_template('admin_modules.html', module_tree=module_tree)


# =========================
# 管理员 JSON API
# =========================
def _admin_api_check():
    """检查当前请求是否具备管理员权限。"""
    if not current_user.is_authenticated:
        return jsonify({'error': '未登录'}), 401
    if current_user.username != ADMIN_USERNAME:
        return jsonify({'error': '无权限'}), 403
    return None


@app.route('/api/admin/modules', methods=['GET'])
@login_required
def api_admin_modules():
    err = _admin_api_check()
    if err:
        return err

    modules = Module.query.order_by(Module.name).all()
    return jsonify({
        'modules': [
            {
                'id': m.id,
                'name': m.name,
                'required_credits': m.required_credits,
                'parent_id': m.parent_id,
                'college_id': m.college_id,
                'children_count': len(m.children) if hasattr(m, 'children') else 0,
            }
            for m in modules
        ],
    })


@app.route('/api/admin/modules', methods=['POST'])
@login_required
def api_admin_add_module():
    err = _admin_api_check()
    if err:
        return err

    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify({'error': '模块名称不能为空'}), 400

    try:
        credits = float(data.get('required_credits', 0))
    except (ValueError, TypeError):
        credits = 0

    parent_id = data.get('parent_id')
    if parent_id is not None:
        try:
            parent_id = int(parent_id)
        except (ValueError, TypeError):
            return jsonify({'error': '无效的父模块ID'}), 400
    else:
        parent_id = None

    college_id = data.get('college_id')
    if college_id is not None:
        try:
            college_id = int(college_id)
        except (ValueError, TypeError):
            return jsonify({'error': '无效的学院ID'}), 400
    else:
        college_id = 1

    try:
        mod = Module(name=name, required_credits=credits, parent_id=parent_id, college_id=college_id)
        db.session.add(mod)
        db.session.commit()
        invalidate_module_structure_cache()
        return jsonify({
            'ok': True,
            'module': {
                'id': mod.id,
                'name': mod.name,
                'required_credits': mod.required_credits,
                'parent_id': mod.parent_id,
                'college_id': mod.college_id,
            },
        }), 201
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': str(exc)}), 500


@app.route('/api/admin/modules/<int:module_id>', methods=['PUT'])
@login_required
def api_admin_update_module(module_id):
    err = _admin_api_check()
    if err:
        return err

    mod = db.session.get(Module, module_id)
    if not mod:
        return jsonify({'error': '模块不存在'}), 404

    data = request.get_json(silent=True) or {}
    name = data.get('name')
    if name is not None and not name.strip():
        return jsonify({'error': '模块名称不能为空'}), 400

    try:
        if name is not None:
            mod.name = name.strip()
        if 'required_credits' in data:
            mod.required_credits = float(data['required_credits'])
        if 'parent_id' in data:
            new_parent_id = data['parent_id']
            if new_parent_id is not None:
                new_parent_id = int(new_parent_id)
                if would_create_cycle(module_id, new_parent_id):
                    return jsonify({'error': '不能将模块移动到自身或其子模块下'}), 400
            mod.parent_id = new_parent_id
        if 'college_id' in data:
            mod.college_id = int(data['college_id'])
        db.session.commit()
        invalidate_module_structure_cache()
        return jsonify({'ok': True, 'module': {
            'id': mod.id, 'name': mod.name,
            'required_credits': mod.required_credits,
            'parent_id': mod.parent_id, 'college_id': mod.college_id,
        }})
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': str(exc)}), 500


@app.route('/api/admin/modules/<int:module_id>', methods=['DELETE'])
@login_required
def api_admin_delete_module(module_id):
    err = _admin_api_check()
    if err:
        return err

    mod = db.session.get(Module, module_id)
    if not mod:
        return jsonify({'error': '模块不存在'}), 404
    if mod.children:
        return jsonify({'error': '该模块仍有子模块，无法删除'}), 400
    if Course.query.filter_by(module_id=module_id).first():
        return jsonify({'error': '该模块下仍有课程，无法删除'}), 400

    try:
        db.session.delete(mod)
        db.session.commit()
        invalidate_module_structure_cache()
        return jsonify({'ok': True})
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': str(exc)}), 500


@app.route('/api/admin/courses', methods=['GET'])
@login_required
def api_admin_courses():
    err = _admin_api_check()
    if err:
        return err

    courses = Course.query.order_by(Course.course_code).all()
    result = []
    for c in courses:
        module_path = ''
        if c.module:
            path_parts = []
            mod = c.module
            while mod:
                path_parts.append(normalize_module_name(mod.name))
                mod = mod.parent
            module_path = ' / '.join(reversed(path_parts))
        result.append({
            'id': c.id,
            'course_code': c.course_code,
            'name': c.name,
            'credit': c.credit,
            'module_id': c.module_id,
            'module_path': module_path or '未分配',
        })
    return jsonify({'courses': result})


@app.route('/api/admin/courses', methods=['POST'])
@login_required
def api_admin_add_course():
    err = _admin_api_check()
    if err:
        return err

    data = request.get_json(silent=True) or {}
    course_code = (data.get('course_code') or '').strip()
    course_name = (data.get('name') or '').strip()
    credit = data.get('credit')
    module_id = data.get('module_id')

    if not course_code or not course_name:
        return jsonify({'error': '课程编号和名称不能为空'}), 400
    try:
        credit = float(credit) if credit is not None else 0
    except (ValueError, TypeError):
        return jsonify({'error': '学分必须是数字'}), 400

    if Course.query.filter_by(course_code=course_code).first():
        return jsonify({'error': f'课程编号 {course_code} 已存在'}), 409

    try:
        course = Course(
            course_code=course_code,
            name=course_name,
            credit=credit,
            module_id=int(module_id) if module_id is not None else None,
        )
        db.session.add(course)
        db.session.commit()
        return jsonify({
            'ok': True,
            'course': {
                'id': course.id, 'course_code': course.course_code,
                'name': course.name, 'credit': course.credit,
                'module_id': course.module_id,
            },
        }), 201
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': str(exc)}), 500


@app.route('/api/admin/courses/<int:course_id>', methods=['PUT'])
@login_required
def api_admin_update_course(course_id):
    err = _admin_api_check()
    if err:
        return err

    course = db.session.get(Course, course_id)
    if not course:
        return jsonify({'error': '课程不存在'}), 404

    data = request.get_json(silent=True) or {}
    try:
        if 'module_id' in data:
            course.module_id = int(data['module_id']) if data['module_id'] is not None else None
        if 'name' in data:
            course.name = data['name'].strip()
        if 'course_code' in data:
            course.course_code = data['course_code'].strip()
        if 'credit' in data:
            course.credit = float(data['credit'])
        db.session.commit()
        return jsonify({'ok': True, 'course': {
            'id': course.id, 'course_code': course.course_code,
            'name': course.name, 'credit': course.credit,
            'module_id': course.module_id,
        }})
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': str(exc)}), 500


@app.route('/api/admin/courses/<int:course_id>', methods=['DELETE'])
@login_required
def api_admin_delete_course(course_id):
    err = _admin_api_check()
    if err:
        return err

    course = db.session.get(Course, course_id)
    if not course:
        return jsonify({'error': '课程不存在'}), 404

    try:
        Enrollment.query.filter_by(course_id=course_id).delete()
        db.session.delete(course)
        db.session.commit()
        return jsonify({'ok': True})
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': str(exc)}), 500


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


class SmartPDFParser:
    """智能PDF解析器 - 基于pdf_app的核心算法优化"""
    
    def __init__(self):
        self.modules = []
        self.courses = []
        self.full_text = ""
        self.college_name = ""
        self.major_name = ""
        self.filename = ""
    
    def parse(self, file_stream, filename=""):
        """解析PDF"""
        self.filename = filename
        
        if filename:
            college_from_file, major_from_file = guess_college_and_major_from_filename(filename)
            self.college_name = college_from_file
            self.major_name = major_from_file
        
        with pdfplumber.open(file_stream) as pdf:
            self.full_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
        
        self._extract_college_and_major()
        self._parse_modules_from_pdf()
        self._parse_courses_from_pdf()
        
        return True
    
    def _extract_college_and_major(self):
        """从PDF内容提取学院和专业名称"""
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
                
                if pdf_college and pdf_college != "未知学院":
                    self.college_name = pdf_college
                if pdf_major and pdf_major != "未知专业":
                    self.major_name = pdf_major
                break
    
    def _parse_modules_from_pdf(self):
        """从PDF解析模块 - 支持三种格式：
        1. 主模块：1. 公共基础课程（数字+英文句点）
        2. 子模块：(1) 思政类 18.5 学分（中文括号）
        3. 孙模块：1) 思政必修课（数字+英文右括号）
        """
        # 主模块格式：1. 公共基础课程 [学分]
        pattern1 = r'(\d+)\.\s*([^\n]+?)(?:\s*(\d+(?:\.\d+)?)\s*学分)?'
        
        # 子模块格式：(1) 思政类 18.5 学分（中文括号）
        pattern2 = r'（(\d+)）\s*([^\n]+?)\s*(\d+(?:\.\d+)?)\s*学分'
        
        # 孙模块格式：1) 思政必修课（数字+英文右括号）
        pattern3 = r'(\d+)\)\s*([^\n]+?)(?:\s*(\d+(?:\.\d+)?)\s*学分)?'
        
        # 普通格式：模块名称（XX学分）
        pattern4 = r'([^\n]+?)\s*（(\d+(?:\.\d+)?)学分）'
        
        # 简单格式：模块名称 XX学分
        pattern5 = r'([^\n]+?)\s*(\d+(?:\.\d+)?)\s*学分'
        
        modules = []
        
        for pattern in [pattern1, pattern2, pattern3, pattern4, pattern5]:
            matches = re.findall(pattern, self.full_text)
            for match in matches:
                # 过滤掉太短的模块名称（可能是误匹配）
                if len(match) >= 2 and len(match[1].strip()) >= 2:
                    name = match[1].strip()
                    credits = float(match[2]) if len(match) > 2 and match[2] else 0.0
                    order = int(match[0]) if match[0].isdigit() else len(modules) + 1
                    
                    modules.append({
                        'order': order,
                        'name': name,
                        'credits': credits
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
        
        for name in standard_names:
            found = False
            for parsed in parsed_modules:
                if name in parsed['name'] or parsed['name'] in name:
                    std_modules.append({
                        'name': name,
                        'credits': parsed['credits'],
                        'parent_name': None,
                        'source': 'pdf'
                    })
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
                    'name': name,
                    'credits': default_credits.get(name, 10.0),
                    'parent_name': None,
                    'source': 'default'
                })
        
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
            std_modules.append({
                'name': name,
                'credits': credits,
                'parent_name': parent_name,
                'source': 'default'
            })
        
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
                        'code': code,
                        'name': name,
                        'credit': credit,
                        'module_name': '专业基础课程'
                    })
        
        self.courses = courses
    
    def get_result(self):
        """获取解析结果"""
        return {
            'modules': self.modules,
            'courses': self.courses,
            'college_name': self.college_name,
            'major_name': self.major_name,
            'filename': self.filename
        }


def parse_curriculum_pdf(file_stream, filename=""):
    """智能PDF解析器入口"""
    try:
        parser = SmartPDFParser()
        parser.parse(file_stream, filename)
        return parser.get_result()
    except Exception as e:
        print(f"PDF解析错误: {str(e)}")
        return {'modules': [], 'courses': [], 'error': str(e)}


@app.route('/admin/import_curriculum', methods=['GET', 'POST'])
@admin_required
def import_curriculum():
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'parse':
            if 'file' not in request.files:
                return jsonify({'error': '未上传文件'}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': '未选择文件'}), 400
            
            if not file.filename.lower().endswith('.pdf'):
                return jsonify({'error': '仅支持 PDF 文件'}), 400
            
            try:
                result = parse_curriculum_pdf(file.stream, file.filename)
                if 'error' in result:
                    return jsonify({'error': result['error']}), 400
                return jsonify(result)
            except Exception as e:
                return jsonify({'error': f'解析失败: {str(e)}'}), 500
        
        elif action == 'import':
            data = request.get_json()
            major_id = data.get('major_id')
            college_id = data.get('college_id')
            modules_data = data.get('modules', [])
            courses_data = data.get('courses', [])
            conflict_strategy = data.get('conflict_strategy', 'skip')
            
            if not major_id or not college_id:
                return jsonify({'error': '未选择专业'}), 400
            
            if not modules_data and not courses_data:
                return jsonify({'error': '无数据可导入'}), 400
            
            try:
                db.session.begin()
                
                module_name_to_id = {}
                imported_modules = 0
                imported_courses = 0
                skipped_modules = 0
                skipped_courses = 0
                
                for mod in modules_data:
                    existing = Module.query.filter_by(
                        name=mod['name'],
                        major_id=major_id
                    ).first()
                    
                    if existing:
                        if conflict_strategy == 'skip':
                            skipped_modules += 1
                            module_name_to_id[mod['name']] = existing.id
                            continue
                        elif conflict_strategy == 'overwrite':
                            existing.required_credits = mod['credits']
                            db.session.flush()
                            module_name_to_id[mod['name']] = existing.id
                            continue
                        else:
                            skipped_modules += 1
                            continue
                    
                    parent_id = None
                    if mod.get('parent_name') and mod['parent_name'] in module_name_to_id:
                        parent_id = module_name_to_id[mod['parent_name']]
                    
                    new_module = Module(
                        name=mod['name'],
                        required_credits=mod['credits'],
                        parent_id=parent_id,
                        college_id=college_id,
                        major_id=major_id
                    )
                    db.session.add(new_module)
                    db.session.flush()
                    module_name_to_id[mod['name']] = new_module.id
                    imported_modules += 1
                
                for course in courses_data:
                    module_name = course.get('module_name')
                    if not module_name or module_name not in module_name_to_id:
                        skipped_courses += 1
                        continue
                    
                    existing = Course.query.filter_by(
                        course_code=course['code']
                    ).first()
                    
                    if existing:
                        if conflict_strategy == 'skip':
                            skipped_courses += 1
                            continue
                        elif conflict_strategy == 'overwrite':
                            existing.name = course['name']
                            existing.credit = course['credit']
                            existing.module_id = module_name_to_id[module_name]
                            imported_courses += 1
                            continue
                        else:
                            skipped_courses += 1
                            continue
                    
                    new_course = Course(
                        course_code=course['code'],
                        name=course['name'],
                        credit=course['credit'],
                        module_id=module_name_to_id[module_name]
                    )
                    db.session.add(new_course)
                    imported_courses += 1
                
                db.session.commit()
                
                return jsonify({
                    'ok': True,
                    'imported_modules': imported_modules,
                    'imported_courses': imported_courses,
                    'skipped_modules': skipped_modules,
                    'skipped_courses': skipped_courses
                })
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'导入失败: {str(e)}'}), 500
    
    # GET 请求：渲染页面并传递学院数据
    colleges = College.query.order_by(College.id).all()
    colleges_data = [{'id': c.id, 'name': c.name, 'code': c.code} for c in colleges]
    return render_template('admin_import_curriculum.html', colleges=colleges_data)


# =========================
# 公告栏 API
# =========================
@app.route('/api/announcements', methods=['GET'])
@login_required
def api_get_announcements():
    """获取公告列表（所有用户可见，只返回活跃公告）"""
    active_only = request.args.get('active_only', 'true').lower() == 'true'
    
    query = Announcement.query
    if active_only:
        query = query.filter_by(is_active=True)
    
    announcements = query.order_by(Announcement.created_at.desc()).all()
    
    result = []
    for ann in announcements:
        result.append({
            'id': ann.id,
            'title': ann.title,
            'content': ann.content,
            'is_active': ann.is_active,
            'created_at': ann.created_at.isoformat() if ann.created_at else None,
            'updated_at': ann.updated_at.isoformat() if ann.updated_at else None,
            'username': ann.user.username if ann.user else '',
        })
    
    return jsonify({'announcements': result})


@app.route('/api/announcements/latest', methods=['GET'])
@login_required
def api_get_latest_announcement():
    """获取最新的活跃公告"""
    ann = Announcement.query.filter_by(is_active=True).order_by(Announcement.created_at.desc()).first()
    
    if not ann:
        return jsonify({'announcement': None})
    
    return jsonify({
        'announcement': {
            'id': ann.id,
            'title': ann.title,
            'content': ann.content,
            'is_active': ann.is_active,
            'created_at': ann.created_at.isoformat() if ann.created_at else None,
            'updated_at': ann.updated_at.isoformat() if ann.updated_at else None,
            'username': ann.user.username if ann.user else '',
        }
    })


@app.route('/api/admin/announcements', methods=['GET'])
@login_required
def api_admin_get_announcements():
    """管理员获取所有公告（包括非活跃）"""
    err = _admin_api_check()
    if err:
        return err
    
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    
    result = []
    for ann in announcements:
        result.append({
            'id': ann.id,
            'title': ann.title,
            'content': ann.content,
            'is_active': ann.is_active,
            'created_at': ann.created_at.isoformat() if ann.created_at else None,
            'updated_at': ann.updated_at.isoformat() if ann.updated_at else None,
            'username': ann.user.username if ann.user else '',
        })
    
    return jsonify({'announcements': result})


@app.route('/api/admin/announcements', methods=['POST'])
@login_required
def api_admin_create_announcement():
    """管理员创建公告"""
    err = _admin_api_check()
    if err:
        return err
    
    data = request.get_json(silent=True) or {}
    title = (data.get('title') or '').strip()
    content = (data.get('content') or '').strip()
    
    if not title:
        return jsonify({'error': '公告标题不能为空'}), 400
    if not content:
        return jsonify({'error': '公告内容不能为空'}), 400
    
    try:
        ann = Announcement(
            title=title,
            content=content,
            is_active=True,
            user_id=current_user.id
        )
        db.session.add(ann)
        db.session.commit()
        
        return jsonify({
            'ok': True,
            'announcement': {
                'id': ann.id,
                'title': ann.title,
                'content': ann.content,
                'is_active': ann.is_active,
                'created_at': ann.created_at.isoformat() if ann.created_at else None,
                'updated_at': ann.updated_at.isoformat() if ann.updated_at else None,
            }
        }), 201
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': str(exc)}), 500


@app.route('/api/admin/announcements/<int:ann_id>', methods=['PUT'])
@login_required
def api_admin_update_announcement(ann_id):
    """管理员更新公告"""
    err = _admin_api_check()
    if err:
        return err
    
    ann = db.session.get(Announcement, ann_id)
    if not ann:
        return jsonify({'error': '公告不存在'}), 404
    
    data = request.get_json(silent=True) or {}
    
    try:
        if 'title' in data:
            title = data['title'].strip()
            if not title:
                return jsonify({'error': '公告标题不能为空'}), 400
            ann.title = title
        
        if 'content' in data:
            content = data['content'].strip()
            if not content:
                return jsonify({'error': '公告内容不能为空'}), 400
            ann.content = content
        
        if 'is_active' in data:
            ann.is_active = bool(data['is_active'])
        
        db.session.commit()
        
        return jsonify({
            'ok': True,
            'announcement': {
                'id': ann.id,
                'title': ann.title,
                'content': ann.content,
                'is_active': ann.is_active,
                'created_at': ann.created_at.isoformat() if ann.created_at else None,
                'updated_at': ann.updated_at.isoformat() if ann.updated_at else None,
            }
        })
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': str(exc)}), 500


@app.route('/api/admin/announcements/<int:ann_id>', methods=['DELETE'])
@login_required
def api_admin_delete_announcement(ann_id):
    """管理员删除公告"""
    err = _admin_api_check()
    if err:
        return err
    
    ann = db.session.get(Announcement, ann_id)
    if not ann:
        return jsonify({'error': '公告不存在'}), 404
    
    try:
        db.session.delete(ann)
        db.session.commit()
        return jsonify({'ok': True})
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': str(exc)}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        COLLEGES = [
            ('理学院', 'science'),
            ('微电子学院', 'microelectronics'),
            ('力学与工程科学学院', 'mechanics'),
            ('文学院', 'literature'),
            ('社会学院', 'sociology'),
            ('外国语学院', 'foreign_lang'),
            ('经济学院', 'economics'),
            ('管理学院', 'management'),
            ('文化遗产与信息管理学院', 'cultural_heritage'),
            ('法学院', 'law'),
            ('通信与信息工程学院', 'communication'),
            ('翔英学院', 'xiangying'),
            ('计算机工程与科学学院', 'cs'),
            ('机电工程与自动化学院', 'mechatronics'),
            ('材料科学与工程学院', 'materials'),
            ('环境与化学工程学院', 'env_chem'),
            ('生命科学学院', 'life_science'),
            ('上海美术学院', 'fine_arts'),
            ('上海电影学院', 'film'),
            ('新闻传播学院', 'journalism'),
            ('马克思主义学院', 'marxism'),
            ('国际教育学院', 'intl_edu'),
            ('钱伟长学院', 'qwc'),
            ('悉尼工商学院', 'sydney_business'),
            ('中欧工程技术学院', 'ceeu'),
            ('音乐学院', 'music'),
            ('里斯本学院', 'lisbon'),
            ('未来技术学院', 'future_tech'),
        ]
        if College.query.count() == 0:
            for name, code in COLLEGES:
                db.session.add(College(name=name, code=code))
            db.session.commit()
            print(f'已初始化 {len(COLLEGES)} 个学院')
    app.run(host='0.0.0.0', debug=False, use_reloader=False)
