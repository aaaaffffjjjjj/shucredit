#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试通用专业生成脚本
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shucredit_scripts.parsers.universal_major_creator import create_major_data


# 测试配置：光电信息科学与工程专业
test_config = {
    'college_name': '通信与信息工程学院',
    'major_name': '光电信息科学与工程',
    'major_code': 'OE001',
    'direction_modules': [
        ('光电子方向', 4.0, '专业方向模块'),
        ('信息光电子方向', 4.0, '专业方向模块'),
        ('显示技术方向', 2.0, '专业方向模块'),
    ],
}


if __name__ == '__main__':
    print("="*80)
    print("🧪 测试通用专业数据生成器")
    print("="*80)
    
    create_major_data(test_config)
