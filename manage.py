from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.cms import (Role, User, FriendLink, TitleImage, ParentCategory,
                     ChildCategory, Post)
from app.main import Message
from exts import db
from myblog import app

manager = Manager(app)
Migrate(app, db)

manager.add_command("db", MigrateCommand)

@manager.option("-n", "--name", dest="name")
@manager.option("-d", "--desc", dest="desc")
@manager.option("-p", "--permission", dest="permission")
def add_role(name, desc, permission):
    role = Role.query.filter_by(name=name).first()
    if role:
        print("该角色已存在")
    else:
        role = Role(name=name, desc=desc, permission=permission)
        db.session.add(role)
        db.session.commit()

@manager.option("-e", "--email", dest="email")
@manager.option("-p", "--password", dest="password")
@manager.option("-r", "--role_name", dest="role_name")
@manager.option("-n", "--remark", dest="remark")
def add_user(email, password, role_name, remark):
    user = User.query.filter_by(email=email).first()
    if user:
        print("邮箱已被使用")
    else:
        user = User(email=email, password=password, role_name=role_name, remark=remark)
        db.session.add(user)
        db.session.commit()

@manager.option("-n", "--name", dest="name")
@manager.option("-l", "--link", dest="link")
@manager.option("-p", "--priority", dest="priority")
def add_friendlink(name, link, priority):
    fl = FriendLink(name=name, link=link, priority=priority)
    db.session.add(fl)
    db.session.commit()


# manager要调用run()函数
if __name__ == "__main__":
    manager.run()