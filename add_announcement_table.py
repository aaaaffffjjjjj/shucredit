from app import app, db, Announcement, User

with app.app_context():
    # 创建表
    db.create_all()
    print("公告表创建成功")
    
    # 检查是否已有测试数据
    if not Announcement.query.first():
        # 添加一条测试公告
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            test_announcement = Announcement(
                title='欢迎使用学分管理系统',
                content='这是一个公告示例。管理员可以在这里发布重要通知。',
                is_active=True,
                user_id=admin_user.id
            )
            db.session.add(test_announcement)
            db.session.commit()
            print("已添加测试公告")
        else:
            print("未找到admin用户，跳过测试数据添加")
    else:
        print("公告表已有数据，跳过测试数据添加")