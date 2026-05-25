"""
初始化数据库并创建默认管理员账户
运行方式: python init_db.py
"""
from app import app, db, User, Student, generate_password_hash

def init_database():
    with app.app_context():
        db.create_all()
        print('数据库表已创建')

        if not User.query.filter_by(username='admin').first():
            student = Student(name='管理员', major='系统管理')
            db.session.add(student)
            db.session.flush()

            admin_user = User(
                username='admin',
                password_hash=generate_password_hash('admin'),
                student_id=student.id,
            )
            db.session.add(admin_user)
            db.session.commit()
            print('默认管理员账户已创建: admin / admin')
        else:
            print('管理员账户已存在')

if __name__ == '__main__':
    init_database()
