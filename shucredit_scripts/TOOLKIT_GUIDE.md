# 工具包完整使用指南

## 🎉 欢迎使用！

这个工具包提供了一整套上海大学学分系统的专业数据管理功能，支持快速创建和管理各个专业的数据。

---

## 📁 工具包结构

```
shucredit_scripts/
├── core/                          # 核心脚本
├── migrations/                    # 数据库迁移脚本
├── parsers/                       # PDF解析和专业数据生成脚本
│   ├── universal_major_creator.py   # ✨ 通用专业数据生成器（重点！）
│   ├── create_preconfigured_majors.py # 预配置专业批量创建
│   └── ...
├── utils/                         # 工具脚本
├── quick_start.py                 # 快速初始化脚本
├── check_all_majors.py            # 查看所有专业数据脚本
└── TOOLKIT_GUIDE.md               # 本文档
```

---

## ✨ 特色功能：通用专业数据生成器

### 快速开始

#### 1. 简单配置即可创建任意专业

```python
from parsers.universal_major_creator import create_major_data

# 配置你的专业
config = {
    'college_name': '你的学院',
    'major_name': '你的专业',
    'major_code': '专业代码',
    'direction_modules': [
        ('方向1名称', 4.0, '专业方向模块'),
        ('方向2名称', 4.0, '专业方向模块'),
        ('方向3名称', 2.0, '专业方向模块'),
    ],
}

# 一键生成
create_major_data(config)
```

#### 2. 运行预配置的专业

```bash
cd shucredit_scripts/parsers
python create_preconfigured_majors.py
```

---

## 📖 使用详解

### 一、快速初始化系统

```bash
# 方式1：快速一键初始化（推荐）
cd e:\nbainbshuda\shucredit-1
python shucredit_scripts/quick_start.py
```

### 二、使用通用专业生成器

#### 示例 1：创建计算机科学与技术专业

```python
from shucredit_scripts.parsers.universal_major_creator import create_major_data

config = {
    'college_name': '计算机工程与科学学院',
    'major_name': '计算机科学与技术',
    'major_code': 'CS001',
    'direction_modules': [
        ('软件工程方向', 4.0, '专业方向模块'),
        ('人工智能方向', 4.0, '专业方向模块'),
        ('网络安全方向', 2.0, '专业方向模块'),
    ],
}

create_major_data(config)
```

#### 示例 2：创建机械工程专业

```python
from shucredit_scripts.parsers.universal_major_creator import create_major_data

config = {
    'college_name': '机电工程与自动化学院',
    'major_name': '机械工程',
    'major_code': 'ME001',
    'direction_modules': [
        ('智能制造方向', 4.0, '专业方向模块'),
        ('机器人工程方向', 4.0, '专业方向模块'),
        ('智能设计方向', 2.0, '专业方向模块'),
    ],
}

create_major_data(config)
```

#### 示例 3：创建材料科学与工程专业

```python
from shucredit_scripts.parsers.universal_major_creator import create_major_data

config = {
    'college_name': '材料科学与工程学院',
    'major_name': '材料科学与工程',
    'major_code': 'MSE001',
    'direction_modules': [
        ('金属材料方向', 4.0, '专业方向模块'),
        ('高分子材料方向', 4.0, '专业方向模块'),
        ('新能源材料方向', 2.0, '专业方向模块'),
    ],
}

create_major_data(config)
```

### 三、查看当前所有数据

```bash
python shucredit_scripts/check_all_majors.py
```

---

## 📋 配置参数说明

### `major_config` 字典的可用参数

| 参数名 | 是否必填 | 说明 | 示例 |
|--------|----------|------|------|
| `college_name` | ✅ 是 | 学院名称 | "通信与信息工程学院" |
| `major_name` | ✅ 是 | 专业名称 | "通信工程" |
| `major_code` | ❌ 否 | 专业代码 | "TE001" |
| `college_code` | ❌ 否 | 学院代码 | "CIE" |
| `direction_modules` | ❌ 否 | 专业方向模块列表 | 见下文 |
| `modules` | ❌ 否 | 自定义模块列表 | 见下文 |
| `courses` | ❌ 否 | 自定义课程列表 | 见下文 |

### `direction_modules` 格式说明

专业方向模块通常是3个，总共10学分（4+4+2）：

```python
'direction_modules': [
    ('方向名称', 4.0, '专业方向模块'),  # 第一个方向
    ('方向名称', 4.0, '专业方向模块'),  # 第二个方向
    ('方向名称', 2.0, '专业方向模块'),  # 第三个方向
]
```

### `create_major_data()` 函数参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `major_config` | 专业配置字典（见上） | 必填 |
| `use_template` | 是否使用通用模块模板（公共基础课程等） | `True` |

---

## 📦 预配置的专业列表

工具包预配置了以下专业（在 `create_preconfigured_majors.py` 中）：

| 学院 | 专业 | 代码 |
|------|------|------|
| 通信与信息工程学院 | 通信工程 | TE001 |
| 通信与信息工程学院 | 电子信息工程 | EIE001 |
| 微电子学院 | 微电子科学与工程 | ME001 |
| 计算机工程与科学学院 | 计算机科学与技术 | CS001 |
| 机电工程与自动化学院 | 机械工程 | ME002 |
| 材料科学与工程学院 | 材料科学与工程 | MSE001 |

使用方法：
```bash
cd shucredit_scripts/parsers
python create_preconfigured_majors.py
```

---

## 📊 自动包含的内容

当使用 `use_template=True` 时，会自动包含以下内容：

### 自动包含的模块
- 公共基础课程（67.5学分）
  - 思政类（18.5）
  - 军体类（9.0）
  - 大学英语（8.0）
  - 人工智能类（5.0）
  - 国家安全教育（1.0）
  - 自然科学类（26.0）
- 通识课程（8.0学分）
  - 核心通识课（2.0）
  - 跨类通识课（2.0）
  - 其他通识课（4.0）
- 专业基础课程（52.0学分）
- 专业必修课程（18.5学分）
- 专业选修课程（4.0学分）
  - 专业选修子模块1（2.0）
  - 专业选修子模块2（2.0）
- 个性化教育课程（10.0学分）
  - 综合工程实践能力培养模块（10.0）
- 专业方向模块（10.0学分，由你配置）

### 自动包含的课程
- 完整的思政类课程
- 军体类课程
- 大学英语（模板未包含，可自行添加）
- 人工智能类课程
- 国家安全教育课程
- 完整的自然科学类课程（高等数学、物理、化学等）

---

## 🔧 进阶使用

### 完全自定义（不使用模板）

```python
from shucredit_scripts.parsers.universal_major_creator import create_major_data

my_modules = [
    ('我的根模块1', 50.0, None),
    ('我的根模块2', 30.0, None),
    ('子模块1', 20.0, '我的根模块1'),
    ('子模块2', 30.0, '我的根模块1'),
]

config = {
    'college_name': '我的学院',
    'major_name': '我的专业',
    'modules': my_modules,
    # 你也可以添加 direction_modules、courses 等
}

create_major_data(config, use_template=False)
```

### 添加自定义课程

```python
from shucredit_scripts.parsers.universal_major_creator import create_major_data

my_courses = [
    ('课程代码1', '课程名称1', 3.0, '模块名称1'),
    ('课程代码2', '课程名称2', 2.0, '模块名称2'),
]

config = {
    'college_name': '你的学院',
    'major_name': '你的专业',
    'direction_modules': [ ... ],
    'courses': my_courses,
}

create_major_data(config)
```

### 添加额外的自定义模块

```python
from shucredit_scripts.parsers.universal_major_creator import create_major_data

extra_modules = [
    ('我的额外模块', 5.0, None),
    ('我的额外子模块', 5.0, '我的额外模块'),
]

config = {
    'college_name': '你的学院',
    'major_name': '你的专业',
    'direction_modules': [ ... ],
    'modules': extra_modules,
}

create_major_data(config)
```

---

## 📚 工具包的其他功能

### 核心脚本（core/）

| 脚本 | 功能 |
|------|------|
| `init_db.py` | 初始化数据库和管理员账户 |
| `populate_college_majors.py` | 填充完整的35个学院和134个专业 |

### 数据库迁移（migrations/）

这些脚本用于更新数据库结构（如需要）。

### 其他解析器（parsers/）

| 脚本 | 功能 |
|------|------|
| `universal_parser_final.py` | 旧版通用解析器（通信工程模板） |
| `reset_shucredit_db.py` | 通信工程专业数据库重置 |
| `create_microelectronics_db.py` | 微电子专业数据库生成 |

---

## 📝 常见问题

### Q1：课程代码重复报错？

A：课程代码有唯一性约束，如出现重复，脚本会自动跳过该课程并继续。你可以：
- 检查是否重复创建了同一专业
- 修改课程代码使其唯一

### Q2：如何查看当前数据库中的所有数据？

A：运行：
```bash
python shucredit_scripts/check_all_majors.py
```

### Q3：如何清空并重新开始？

A：使用 `quick_start.py` 或自行调用 `db.drop_all()` 和 `db.create_all()`。

### Q4：可以在 Jupyter Notebook 中使用吗？

A：可以！只需正确设置路径并导入相关模块即可。

---

## 🎯 下一步建议

1. 运行 `quick_start.py` 初始化系统
2. 尝试使用通用专业生成器创建1-2个专业
3. 查看 `check_all_majors.py` 的输出
4. 根据你的需要进行自定义配置

---

## 📄 许可证

本工具包仅供学习和研究使用。

---

## 💡 联系与反馈

如有问题或建议，欢迎通过代码仓库提交 Issue！
