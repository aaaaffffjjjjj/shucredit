#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的学院-专业数据填充脚本
基于 https://bksy.shu.edu.cn/info/1400/312134.htm
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, College, Major, Module, Course

# ==========================================
# 完整的学院和专业数据（来自网页）
# ==========================================
COLLEGE_MAJOR_DATA = {
    '人文社科大类': {
        'code': 'RW',
        'majors': [
            ('人文社科大类', 'RW001'),
        ]
    },
    '经济管理大类': {
        'code': 'JG',
        'majors': [
            ('经济管理大类', 'JG001'),
        ]
    },
    '理学工学Ⅰ类': {
        'code': 'LG1',
        'majors': [
            ('理学工学Ⅰ类', 'LG1001'),
        ]
    },
    '理学工学Ⅱ类': {
        'code': 'LG2',
        'majors': [
            ('理学工学Ⅱ类', 'LG2001'),
        ]
    },
    '理学工学Ⅲ类': {
        'code': 'LG3',
        'majors': [
            ('理学工学Ⅲ类', 'LG3001'),
        ]
    },
    '理学院': {
        'code': 'science',
        'majors': [
            ('数学与应用数学（直招）', 'SX001'),
            ('数学与应用数学', 'SX002'),
            ('信息与计算科学', 'XX001'),
            ('应用物理学', 'WX001'),
            ('电子信息科学与技术', 'DZ001'),
            ('应用化学', 'HX001'),
        ]
    },
    '微电子学院': {
        'code': 'microelectronics',
        'majors': [
            ('微电子科学与工程', 'WDZ001'),
        ]
    },
    '力学与工程科学学院': {
        'code': 'mechanics',
        'majors': [
            ('理论与应用力学', 'LX001'),
            ('土木工程', 'TM001'),
        ]
    },
    '文学院': {
        'code': 'literature',
        'majors': [
            ('汉语言文学', 'HY001'),
            ('汉语国际教育', 'HG001'),
            ('历史学', 'LS001'),
        ]
    },
    '社会学院': {
        'code': 'sociology',
        'majors': [
            ('社会学（直招）', 'SH001'),
            ('社会学', 'SH002'),
            ('社会工作', 'SG001'),
            ('社会工作（第二学士学位）', 'SG002'),
        ]
    },
    '外国语学院': {
        'code': 'foreign_lang',
        'majors': [
            ('英语', 'YY001'),
            ('日语', 'RY001'),
            ('法语', 'FY001'),
        ]
    },
    '经济学院': {
        'code': 'economics',
        'majors': [
            ('经济学', 'JJ001'),
            ('金融学', 'JR001'),
            ('国际经济与贸易', 'GM001'),
        ]
    },
    '管理学院': {
        'code': 'management',
        'majors': [
            ('信息管理与信息系统', 'XG001'),
            ('工程管理', 'GG001'),
            ('管理科学', 'GK001'),
            ('工商管理', 'GS001'),
            ('物流管理', 'WG001'),
            ('人力资源管理', 'RL001'),
            ('会计学（直招）', 'KJ001'),
            ('会计学', 'KJ002'),
            ('财务管理', 'CW001'),
        ]
    },
    '文化遗产与信息管理学院': {
        'code': 'cultural_heritage',
        'majors': [
            ('档案学', 'DA001'),
            ('信息资源管理', 'XZ001'),
            ('考古学', 'KG001'),
        ]
    },
    '法学院': {
        'code': 'law',
        'majors': [
            ('法学', 'FX001'),
            ('知识产权', 'ZS001'),
            ('知识产权（第二学士学位）', 'ZS002'),
        ]
    },
    '通信与信息工程学院': {
        'code': 'communication',
        'majors': [
            ('通信工程', 'TX001'),
            ('电子信息工程', 'DZ002'),
            ('光电信息科学与工程', 'GD001'),
            ('数据科学与大数据技术', 'SJ001'),
        ]
    },
    '翔英学院': {
        'code': 'xiangying',
        'majors': [
            ('通信工程（翔英班）', 'TX002'),
            ('电子信息工程（翔英班）', 'DZ003'),
        ]
    },
    '计算机工程与科学学院': {
        'code': 'cs',
        'majors': [
            ('计算机科学与技术（直招）', 'JSJ001'),
            ('计算机科学与技术', 'JSJ002'),
            ('智能科学与技术（直招）', 'ZN001'),
            ('智能科学与技术', 'ZN002'),
            ('网络空间安全（直招）', 'WL001'),
            ('网络空间安全', 'WL002'),
            ('人工智能（直招）', 'RG001'),
            ('人工智能', 'RG002'),
        ]
    },
    '机电工程与自动化学院': {
        'code': 'mechatronics',
        'majors': [
            ('工业工程', 'GY001'),
            ('机械设计制造及其自动化', 'JX001'),
            ('智能制造工程', 'ZZ001'),
            ('测控技术与仪器', 'CK001'),
            ('机械电子工程', 'JD001'),
            ('机器人工程', 'JQ001'),
            ('电气工程及其自动化', 'DQ001'),
            ('自动化', 'ZD001'),
        ]
    },
    '材料科学与工程学院': {
        'code': 'materials',
        'majors': [
            ('冶金工程', 'YJ001'),
            ('"冶金工程"+"信息管理与信息系统"双学位', 'YJ002'),
            ('金属材料工程（卓越工程师）', 'JS001'),
            ('高分子材料与工程', 'GF001'),
            ('电子科学与技术', 'DK001'),
            ('无机非金属材料工程（卓越工程师）', 'WF001'),
            ('新能源材料与器件', 'XN001'),
        ]
    },
    '环境与化学工程学院': {
        'code': 'env_chem',
        'majors': [
            ('环境工程', 'HJ001'),
            ('化学工程与工艺', 'HG002'),
        ]
    },
    '生命科学学院': {
        'code': 'life_science',
        'majors': [
            ('生物工程', 'SW001'),
            ('食品科学与工程', 'SP001'),
            ('生物制药', 'SZ001'),
            ('生物医学工程', 'SY001'),
        ]
    },
    '上海美术学院': {
        'code': 'fine_arts',
        'majors': [
            ('中国画', 'GH001'),
            ('绘画（油画）', 'HH001'),
            ('绘画（版画）', 'HB001'),
            ('美术学', 'MS001'),
            ('雕塑', 'DS001'),
            ('视觉传达设计', 'SC001'),
            ('环境设计', 'HS001'),
            ('艺术与科技', 'YK001'),
            ('数字媒体艺术', 'SM001'),
            ('建筑学', 'JZ001'),
            ('城乡规划', 'CX001'),
            ('实验艺术', 'SY001'),
            ('艺术设计学', 'YS001'),
            ('产品设计', 'CS001'),
            ('工艺美术', 'GM002'),
            ('城市设计', 'CS002'),
            ('艺术管理', 'YG001'),
            ('书法学', 'SF001'),
        ]
    },
    '上海电影学院': {
        'code': 'film',
        'majors': [
            ('数字媒体技术（卓越工程师）', 'SM002'),
            ('广播电视编导', 'GB001'),
            ('动画', 'DH001'),
            ('表演', 'BY001'),
            ('影视摄影与制作', 'YS001'),
            ('电影制作', 'DY001'),
            ('戏剧影视导演', 'XD001'),
            ('戏剧影视文学', 'XW001'),
            ('戏剧影视美术设计', 'XM001'),
        ]
    },
    '新闻传播学院': {
        'code': 'journalism',
        'majors': [
            ('广播电视学', 'GX001'),
            ('新闻学', 'XW001'),
            ('广告学', 'GG001'),
            ('会展', 'HZ001'),
            ('网络与新媒体', 'WX001'),
        ]
    },
    '马克思主义学院': {
        'code': 'marxism',
        'majors': [
            ('思想政治教育', 'SZ001'),
            ('哲学', 'ZX001'),
        ]
    },
    '国际教育学院': {
        'code': 'intl_edu',
        'majors': [
            ('汉语言（国际生）', 'HY002'),
            ('汉语国际教育（国际生）', 'HG002'),
        ]
    },
    '钱伟长学院': {
        'code': 'qwc',
        'majors': [
            ('材料设计科学与工程', 'CS003'),
            ('理论与应用力学', 'LX002'),
            ('数学与应用数学', 'SX003'),
            ('应用物理学', 'WX002'),
            ('应用化学', 'HX002'),
            ('生物工程', 'SW002'),
        ]
    },
    '悉尼工商学院': {
        'code': 'sydney_business',
        'majors': [
            ('国际经济与贸易', 'GM002'),
            ('工商管理', 'GS002'),
            ('信息管理与信息系统', 'XG002'),
            ('金融学', 'JR002'),
        ]
    },
    '中欧工程技术学院': {
        'code': 'ceeu',
        'majors': [
            ('材料科学与工程', 'CL001'),
            ('机械工程', 'JX002'),
            ('信息工程', 'XG003'),
        ]
    },
    '音乐学院': {
        'code': 'music',
        'majors': [
            ('音乐学', 'YY002'),
            ('音乐表演', 'YB001'),
        ]
    },
    '里斯本学院': {
        'code': 'lisbon',
        'majors': [
            ('土木工程', 'TM002'),
            ('电气工程及其自动化', 'DQ002'),
            ('环境工程', 'HJ002'),
        ]
    },
    '未来技术学院': {
        'code': 'future_tech',
        'majors': [
            ('人工智能', 'RG003'),
            ('机器人工程', 'JQ002'),
            ('机械电子工程', 'JD002'),
        ]
    },
}

# ==========================================
# 通用模块模板（各专业可以基于此修改）
# ==========================================
DEFAULT_MODULES = [
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
    
    ('专业基础课程', 50.0, None),
    ('专业必修课程', 30.0, None),
    ('专业选修课程', 10.0, None),
]

class CollegeMajorPopulator:
    """学院-专业数据填充器"""
    
    def __init__(self):
        self.module_map = {}
    
    def clear_all_data(self):
        """清空所有数据（谨慎使用）"""
        print("\n⚠️  正在清空所有数据...")
        Course.query.delete()
        Module.query.delete()
        Major.query.delete()
        db.session.commit()
        print("✅ 数据已清空")
    
    def get_or_create_college(self, college_name, college_code):
        """获取或创建学院"""
        college = College.query.filter_by(name=college_name).first()
        if not college:
            college = College(name=college_name, code=college_code)
            db.session.add(college)
            db.session.commit()
            print(f"  📚 创建学院: {college_name} (ID: {college.id})")
        return college
    
    def get_or_create_major(self, college, major_name, major_code):
        """获取或创建专业"""
        major = Major.query.filter_by(college_id=college.id, name=major_name).first()
        if not major:
            major = Major(name=major_name, code=major_code, college_id=college.id)
            db.session.add(major)
            db.session.commit()
            print(f"    🎓 创建专业: {major_name} (ID: {major.id})")
        return major
    
    def populate_major_modules(self, major, modules=None):
        """为专业填充模块"""
        modules = modules or DEFAULT_MODULES
        self.module_map = {}
        
        for mod_name, credits, parent_name in modules:
            parent_id = self.module_map.get(parent_name) if parent_name else None
            
            module = Module(
                name=mod_name,
                required_credits=credits,
                parent_id=parent_id,
                college_id=major.college_id,
                major_id=major.id
            )
            db.session.add(module)
            db.session.flush()
            self.module_map[mod_name] = module.id
        
        db.session.commit()
        print(f"    ✅ 插入 {len(modules)} 个模块")
    
    def populate_all(self, clear_first=False):
        """填充所有学院和专业"""
        print("="*80)
        print("🏗️  填充完整的学院-专业体系")
        print("="*80)
        
        try:
            with app.app_context():
                if clear_first:
                    self.clear_all_data()
                
                for college_name, college_info in COLLEGE_MAJOR_DATA.items():
                    print(f"\n{'='*60}")
                    print(f"处理学院: {college_name}")
                    print(f"{'='*60}")
                    
                    college = self.get_or_create_college(college_name, college_info['code'])
                    
                    for major_name, major_code in college_info['majors']:
                        major = self.get_or_create_major(college, major_name, major_code)
                        self.populate_major_modules(major)
                
                # 统计结果
                print("\n" + "="*80)
                print("🎉 填充完成！统计结果:")
                print("="*80)
                
                college_count = College.query.count()
                major_count = Major.query.count()
                module_count = Module.query.count()
                
                print(f"\n📊 统计:")
                print(f"  学院: {college_count} 个")
                print(f"  专业: {major_count} 个")
                print(f"  模块: {module_count} 个")
                
                # 列出学院专业
                print(f"\n📋 学院-专业列表:")
                for college in College.query.order_by(College.id).all():
                    major_list = [m.name for m in college.majors]
                    print(f"  {college.name} ({len(major_list)} 个专业)")
                    for i, major in enumerate(major_list, 1):
                        print(f"    {i}. {major}")
                
                return True
                
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║           上海大学完整学院-专业体系数据填充脚本                       ║
║  来源: https://bksy.shu.edu.cn/info/1400/312134.htm                ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    populator = CollegeMajorPopulator()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'clear':
            confirm = input("\n⚠️  确认要清空所有数据并重新填充？(yes/no): ").strip().lower()
            if confirm == 'yes':
                populator.populate_all(clear_first=True)
        else:
            print("未知参数")
    else:
        print("""
选项:
  python populate_college_majors.py          - 增量填充（不清空）
  python populate_college_majors.py clear    - 清空所有数据并重新填充
        """)
        
        choice = input("\n选择操作 (1.增量填充 2.清空并重新填充): ").strip()
        
        if choice == '2':
            confirm = input("\n⚠️  确认要清空所有数据并重新填充？(yes/no): ").strip().lower()
            if confirm == 'yes':
                populator.populate_all(clear_first=True)
        else:
            populator.populate_all(clear_first=False)

if __name__ == '__main__':
    main()
