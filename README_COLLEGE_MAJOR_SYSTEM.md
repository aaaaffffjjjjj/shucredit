# 上海大学学院-专业系统

## 🎉 完成总结

已成功创建完整的学院-专业层级系统，基于 https://bksy.shu.edu.cn/info/1400/312134.htm

## 📊 系统统计

| 层级 | 数量 |
|------|------|
| 学院 | 35 个 |
| 专业 | 134 个 |
| 模块 | 1938 个 |

## 📁 关键文件

- `populate_college_majors.py` - 完整的学院-专业数据填充脚本
- `populate_colleges.py` - 旧版填充脚本（保留参考）
- `quick_populate.py` - 快速填充脚本（非交互式）
- `migrations/002_add_major_support.sql` - 数据库迁移脚本

## 🛠️ 数据库变更

### 新增表
- `major` - 专业表
  - id (主键)
  - name (专业名称)
  - code (专业代码)
  - college_id (所属学院 ID，外键)

### 修改表
- `module` - 模块表
  - 新增 `major_id` (外键，指向专业)
  - `college_id` 改为可空（为了兼容）

## 📋 学院列表

1. 人文社科大类
2. 经济管理大类
3. 理学工学Ⅰ类
4. 理学工学Ⅱ类
5. 理学工学Ⅲ类
6. 理学院
7. 微电子学院
8. 力学与工程科学学院
9. 文学院
10. 社会学院
11. 外国语学院
12. 经济学院
13. 管理学院
14. 文化遗产与信息管理学院
15. 法学院
16. 通信与信息工程学院
17. 翔英学院
18. 计算机工程与科学学院
19. 机电工程与自动化学院
20. 材料科学与工程学院
21. 环境与化学工程学院
22. 生命科学学院
23. 上海美术学院
24. 上海电影学院
25. 新闻传播学院
26. 马克思主义学院
27. 国际教育学院
28. 钱伟长学院
29. 悉尼工商学院
30. 中欧工程技术学院
31. 音乐学院
32. 里斯本学院
33. 未来技术学院

## 🚀 使用方法

### 查看数据
```python
from app import app, db, College, Major, Module

with app.app_context():
    # 查询所有学院
    colleges = College.query.all()
    
    # 查询学院的专业
    for college in colleges:
        print(f"\n{college.name}:")
        for major in college.majors:
            print(f"  - {major.name}")
            
    # 查询专业的模块
    major = Major.query.filter_by(name='通信工程').first()
    if major:
        print(f"\n{major.name} 的模块:")
        for module in major.modules:
            parent_name = module.parent.name if module.parent else '根模块'
            print(f"  - {module.name} ({module.required_credits} 学分) - {parent_name}")
```

### 重新填充数据
```bash
# 增量填充（不清空）
python populate_college_majors.py

# 清空并重新填充
python populate_college_majors.py clear
```

## 📌 下一步建议

1. 更新前端，添加专业选择功能
2. 为特定专业添加完整课程数据
3. 实现 API 接口支持专业筛选
