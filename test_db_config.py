import os
from dotenv import load_dotenv
import pymysql

print("="*60)
print("🔍 测试数据库配置")
print("="*60)

# 测试 .env 加载
print("\n1. 加载 .env 文件...")
try:
    load_dotenv()
    print("   ✅ .env 已加载")
except Exception as e:
    print(f"   ❌ 加载失败: {e}")

# 检查环境变量
print("\n2. 检查环境变量...")
env_vars = ['MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_HOST', 'MYSQL_PORT', 'MYSQL_DB']
for var in env_vars:
    value = os.environ.get(var)
    print(f"   {var}: {value if value else 'NOT SET'}")

# 尝试直接连接
print("\n3. 测试数据库连接...")
try:
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='24567@Zzy',
        database='student_system',
        charset='utf8mb4'
    )
    print("   ✅ 连接成功!")
    
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM module")
    module_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM course")
    course_count = cursor.fetchone()[0]
    
    print(f"\n   当前数据:")
    print(f"   模块数: {module_count}")
    print(f"   课程数: {course_count}")
    
    cursor.close()
    connection.close()
    
    print("\n" + "="*60)
    print("✅ 测试完成!")
    print("="*60)
    
except Exception as e:
    print(f"   ❌ 连接失败: {e}")
    import traceback
    traceback.print_exc()
