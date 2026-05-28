from app import app, db, User

with app.app_context():
    # 添加 is_admin 字段
    try:
        with db.engine.connect() as conn:
            conn.execute(db.text('ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT FALSE'))
            conn.commit()
        print("成功添加 is_admin 字段")
    except Exception as e:
        print(f"字段可能已存在: {e}")
    
    # 设置 admin 用户为管理员
    admin = User.query.filter_by(username='admin').first()
    if admin:
        admin.is_admin = True
        db.session.commit()
        print("成功设置 admin 用户为管理员")
    else:
        print("未找到 admin 用户")