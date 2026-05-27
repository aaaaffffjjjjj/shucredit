#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
预配置专业批量创建脚本
包含多个常用专业的配置，一键创建
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from universal_major_creator import create_major_data


# 预配置的专业列表
PRECONFIGURED_MAJORS = [
    {
        'college_name': '通信与信息工程学院',
        'major_name': '通信工程',
        'major_code': 'TE001',
        'direction_modules': [
            ('通信方向', 4.0, '专业方向模块'),
            ('光通信方向', 4.0, '专业方向模块'),
            ('AI方向', 2.0, '专业方向模块'),
        ],
    },
    {
        'college_name': '通信与信息工程学院',
        'major_name': '电子信息工程',
        'major_code': 'EIE001',
        'direction_modules': [
            ('信号处理方向', 4.0, '专业方向模块'),
            ('嵌入式系统方向', 4.0, '专业方向模块'),
            ('智能硬件方向', 2.0, '专业方向模块'),
        ],
    },
    {
        'college_name': '微电子学院',
        'major_name': '微电子科学与工程',
        'major_code': 'ME001',
        'direction_modules': [
            ('集成电路微纳电子学方向', 4.0, '专业方向模块'),
            ('集成电路制造工程方向', 4.0, '专业方向模块'),
            ('集成电路设计方向', 2.0, '专业方向模块'),
        ],
    },
    {
        'college_name': '计算机工程与科学学院',
        'major_name': '计算机科学与技术',
        'major_code': 'CS001',
        'direction_modules': [
            ('软件工程方向', 4.0, '专业方向模块'),
            ('人工智能方向', 4.0, '专业方向模块'),
            ('网络安全方向', 2.0, '专业方向模块'),
        ],
    },
    {
        'college_name': '机电工程与自动化学院',
        'major_name': '机械工程',
        'major_code': 'ME002',
        'direction_modules': [
            ('智能制造方向', 4.0, '专业方向模块'),
            ('机器人工程方向', 4.0, '专业方向模块'),
            ('智能设计方向', 2.0, '专业方向模块'),
        ],
    },
    {
        'college_name': '材料科学与工程学院',
        'major_name': '材料科学与工程',
        'major_code': 'MSE001',
        'direction_modules': [
            ('金属材料方向', 4.0, '专业方向模块'),
            ('高分子材料方向', 4.0, '专业方向模块'),
            ('新能源材料方向', 2.0, '专业方向模块'),
        ],
    },
]


def main():
    print("="*80)
    print("🏗️  批量创建预配置专业")
    print("="*80)
    
    print(f"\n📋 可用的预配置专业 ({len(PRECONFIGURED_MAJORS)} 个)：")
    for i, config in enumerate(PRECONFIGURED_MAJORS, 1):
        print(f"  {i}. {config['college_name']} - {config['major_name']}")
    
    print("\n" + "="*80)
    print("请选择操作：")
    print("  1. 创建所有专业")
    print("  2. 选择单个专业创建")
    choice = input("\n请输入选项 (1 或 2): ").strip()
    
    if choice == '1':
        print("\n" + "="*80)
        print(f"🚀 开始创建所有 {len(PRECONFIGURED_MAJORS)} 个专业...")
        print("="*80)
        
        for i, config in enumerate(PRECONFIGURED_MAJORS, 1):
            print(f"\n\n" + "="*80)
            print(f"[{i}/{len(PRECONFIGURED_MAJORS)}] 处理：{config['major_name']}")
            print("="*80)
            create_major_data(config)
        
        print("\n" + "="*80)
        print("✅ 所有专业创建完成！")
        print("="*80)
        
    elif choice == '2':
        choice = input(f"\n请输入要创建的专业编号 (1-{len(PRECONFIGURED_MAJORS)}): ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(PRECONFIGURED_MAJORS):
                config = PRECONFIGURED_MAJORS[idx]
                create_major_data(config)
            else:
                print("❌ 无效的编号！")
        except ValueError:
            print("❌ 请输入有效的数字！")
    else:
        print("❌ 无效的选项！")


if __name__ == '__main__':
    main()
