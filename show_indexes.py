import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from sqlalchemy import text

with app.app_context():
    print("检查 Course 表的索引...")

    with db.engine.connect() as conn:
        result = conn.execute(text("SHOW INDEX FROM course"))
        for row in result:
            print(f"  Index: {row[2]}, Column: {row[4]}, Non_unique: {row[1]}")

    print("\n检查表结构...")
    result = conn.execute(text("DESCRIBE course"))
    for row in result:
        print(f"  {row[0]}: {row[1]} - Extra: {row[5]}")