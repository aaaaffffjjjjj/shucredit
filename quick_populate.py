#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速填充学院-专业数据（非交互式）
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from populate_college_majors import CollegeMajorPopulator

populator = CollegeMajorPopulator()
populator.populate_all(clear_first=False)
