from app import app
from models.user import db, User

def create_initial_users():
    with app.app_context():
        # 检查是否已存在用户
        if User.query.first() is None:
            # 创建管理员用户
            admin = User(username='admin_user', password='admin_pass', role='admin')
            # 创建经理用户
            manager = User(username='manager_user', password='manager_pass', role='manager')
            # 创建客服用户
            service = User(username='service_user', password='service_pass', role='service')
            
            db.session.add(admin)
            db.session.add(manager)
            db.session.add(service)
            db.session.commit()
            print("初始用户创建成功！")
        else:
            print("用户已存在，跳过创建。")

if __name__ == '__main__':
    create_initial_users() 