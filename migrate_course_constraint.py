import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from sqlalchemy import text

with app.app_context():
    print("开始迁移 Course 表结构...")

    try:
        # 1. 删除 course_code 的唯一索引 ix_course_course_code
        print("1. 删除 course_code 的唯一索引 ix_course_course_code...")
        with db.engine.connect() as conn:
            conn.execute(text("DROP INDEX ix_course_course_code ON course"))
            print("   已删除 ix_course_course_code 索引")
            conn.commit()

        # 2. 创建组合唯一索引 (course_code, module_id)
        print("2. 创建组合唯一索引 (course_code, module_id)...")
        with db.engine.connect() as conn:
            conn.execute(text("""
                ALTER TABLE course
                ADD CONSTRAINT uix_course_code_module
                UNIQUE (course_code, module_id)
            """))
            print("   已创建组合唯一索引 uix_course_code_module")
            conn.commit()

        print("\n迁移完成！")

    except Exception as e:
        print(f"\n迁移出错: {e}")