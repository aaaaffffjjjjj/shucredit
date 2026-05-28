# 上海大学培养方案PDF解析器 - 完整指南

## 🎉 概述

我们成功改进了PDF解析功能！现在工具包支持：

1. **真正解析PDF内容** - 提取模块、课程等信息
2. **自动识别专业方向** - 根据专业名称确定方向
3. **完整的数据库导入** - 一键解析并导入
4. **预配置专业支持** - 内置多个常用专业

---

## 📦 新增文件

### 核心解析器
| 文件 | 说明 |
|------|------|
| `shupdf_parser_final.py` | ✅ **最终版PDF解析器** - 推荐使用 |
| `universal_pdf_parser.py` | 备用的完整解析器 |
| `universal_parser_final.py` | 旧版（保留参考） |

### 测试和辅助文件
| 文件 | 说明 |
|------|------|
| `create_preconfigured_majors.py` | 预配置专业批量创建 |
| `universal_major_creator.py` | 通用专业创建（无需PDF） |

---

## 🚀 快速开始

### 方式1：使用最终版解析器（推荐）

```python
from shucredit_scripts.parsers.shupdf_parser_final import SHUPDFParserFinal

# 创建解析器
parser = SHUPDFParserFinal(
    college_name='通信与信息工程学院',
    major_name='通信工程',
    major_code='TE001'
)

# 解析PDF
pdf_path = r'e:\wodeaishiyan\2025通信工程.pdf'
if parser.parse(pdf_path):
    # 打印结果
    parser.print_summary()
    
    # 导入数据库
    parser.import_db()
```

### 方式2：命令行直接使用

```bash
cd e:\nbainbshuda\shucredit-1\shucredit_scripts\parsers
python shupdf_parser_final.py
```

---

## 📊 预配置的专业

工具包内置支持以下专业（自动识别方向）：

| 学院 | 专业 | 方向 |
|------|------|------|
| 通信与信息工程学院 | 通信工程 | 通信方向、光通信方向、AI方向 |
| 通信与信息工程学院 | 电子信息工程 | 信号处理方向、嵌入式系统方向、智能硬件方向 |
| 微电子学院 | 微电子科学与工程 | 集成电路微纳电子学方向、制造工程方向、设计方向 |
| 计算机工程与科学学院 | 计算机科学与技术 | 软件工程方向、人工智能方向、网络安全方向 |

---

## 🔧 自定义专业

### 基本配置

```python
# 创建解析器时会自动使用标准结构
parser = SHUPDFParserFinal(
    college_name='你的学院',
    major_name='你的专业',
    major_code='专业代码'
)

# 解析PDF
parser.parse(pdf_path)
```

### 完全自定义（不使用PDF）

如果不需要解析PDF，可以使用通用创建器：

```python
from shucredit_scripts.parsers.universal_major_creator import create_major_data

config = {
    'college_name': '学院名称',
    'major_name': '专业名称',
    'major_code': '专业代码',
    'direction_modules': [
        ('方向1名称', 4.0, '专业方向模块'),
        ('方向2名称', 4.0, '专业方向模块'),
        ('方向3名称', 2.0, '专业方向模块'),
    ]
}

create_major_data(config)
```

---

## 📁 模块结构说明

解析器会自动构建完整的模块结构：

```
公共基础课程 (67.5)
├── 思政类 (18.5)
├── 军体类 (9.0)
├── 大学英语 (8.0)
├── 人工智能类 (5.0)
├── 国家安全教育 (1.0)
└── 自然科学类 (26.0)

通识课程 (8.0)
├── 核心通识课 (2.0)
├── 跨类通识课 (2.0)
└── 其他通识课 (4.0)

专业基础课程 (52.0)
专业必修课程 (18.5)
专业选修课程 (4.0)
├── 专业选修子模块1 (2.0)
└── 专业选修子模块2 (2.0)

个性化教育课程 (10.0)
└── 综合工程实践能力培养模块 (10.0)

专业方向模块 (10.0)
├── 方向1 (4.0)
├── 方向2 (4.0)
└── 方向3 (2.0)
```

---

## 📚 课程处理

### 自动包含的核心课程

解析器会自动插入完整的公共基础课程：

- 思政类（7门课）
- 军体类（4门课）
- 人工智能类（2门课）
- 国家安全教育（1门课）
- 自然科学类（9门课）

### PDF课程提取

从PDF中提取课程时，会：
1. 识别课程代码
2. 提取课程名和学分
3. 避免重复
4. 自动分配模块

---

## 🎯 完整示例：解析并导入通信工程

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整示例：解析2025通信工程.pdf并导入
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shucredit_scripts.parsers.shupdf_parser_final import SHUPDFParserFinal


def main():
    print("="*80)
    print("📄 解析2025通信工程培养方案")
    print("="*80)
    
    # 1. 创建解析器
    parser = SHUPDFParserFinal(
        college_name='通信与信息工程学院',
        major_name='通信工程',
        major_code='TE001'
    )
    
    # 2. 解析PDF
    pdf_path = r'e:\wodeaishiyan\2025通信工程.pdf'
    if not parser.parse(pdf_path):
        print("❌ 解析失败！")
        return
    
    # 3. 打印结果
    parser.print_summary()
    
    # 4. 导入数据库
    print("\n" + "="*80)
    parser.import_db()
    
    print("\n" + "="*80)
    print("✅ 全部完成！")
    print("="*80)


if __name__ == '__main__':
    main()
```

---

## 💡 高级用法

### 批量导入多个专业

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shucredit_scripts.parsers.shupdf_parser_final import SHUPDFParserFinal


majors = [
    {
        'college': '通信与信息工程学院',
        'name': '通信工程',
        'code': 'TE001',
        'pdf': r'e:\wodeaishiyan\2025通信工程.pdf'
    },
    {
        'college': '通信与信息工程学院',
        'name': '电子信息工程',
        'code': 'EIE001',
        'pdf': r'e:\wodeaishiyan\2025电子信息工程.pdf'
    },
    {
        'college': '微电子学院',
        'name': '微电子科学与工程',
        'code': 'ME001',
        'pdf': r'e:\wodeaishiyan\2025微电子科学与工程.pdf'
    }
]


for major_cfg in majors:
    print(f"\n" + "="*80)
    print(f"🎯 处理: {major_cfg['name']}")
    print("="*80)
    
    parser = SHUPDFParserFinal(
        college_name=major_cfg['college'],
        major_name=major_cfg['name'],
        major_code=major_cfg['code']
    )
    
    if parser.parse(major_cfg['pdf']):
        parser.import_db()
```

---

## ⚠️ 注意事项

### 1. PDF格式

- PDF必须是上海大学标准培养方案格式
- 如果格式差异太大，解析可能不完整
- 此时建议使用 `universal_major_creator.py` 手动配置

### 2. 课程重复

- 课程代码是唯一的
- 如果课程已存在，会自动跳过
- 不会报错，只是不重复添加

### 3. 模块ID

- 解析器会从1开始分配模块ID
- 如果已有数据，会先清空

---

## 📞 故障排除

### 问题：找不到pdfplumber

```bash
pip install pdfplumber
```

### 问题：数据库导入错误

确保：
1. 已运行 `init_db.py`
2. app.py 没有语法错误
3. 数据库连接正常

### 问题：解析内容不完整

1. 检查PDF是否正确
2. 查看输出的调试信息
3. 可以使用 `simple_pdf_test.py` 仅做分析

---

## 📝 更新日志

### v2.0 - 改进版PDF解析（当前）
- ✅ 真正解析PDF内容
- ✅ 自动识别模块和课程
- ✅ 完整的模块结构
- ✅ 预配置专业支持
- ✅ 一键数据库导入

### v1.0 - 初始版
- 基础解析框架
- 手动配置模式

---

## 🎓 总结

现在工具包已完全支持：

1. **PDF解析** - 从培养方案PDF提取数据
2. **智能识别** - 自动确定专业方向
3. **完整导入** - 一键解析并导入数据库
4. **灵活配置** - 支持手动配置和自动解析

所有脚本都已集成到工具包中，方便使用！
