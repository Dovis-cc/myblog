from exts import db
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash
import shortuuid

class Permission(object):
    a = 0b00000001  # 个人信息、发帖
    b = 0b00000011  # 个人信息、发帖、管理帖子相关
    c = 0b00000111  # 个人信息、发帖、管理帖子相关、管理用户
    d = 0b11111111  # 所有权限

class Role(db.Model):
    __tablename__ = "role"
    name = db.Column(db.String(10), nullable=False, primary_key=True)
    desc = db.Column(db.String(50), nullable=False)
    permission = db.Column(db.Integer, default=Permission.a)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    remark = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    join_time = db.Column(db.Date, default=date.today)
    status = db.Column(db.Integer, default=1)
    role_name = db.Column(db.String(10), db.ForeignKey("role.name"), nullable=False)

    role = db.relationship("Role", backref=db.backref("users"))

    # 涉及到外键时不能用此方法
    # def __init__(self, *args, **kwargs):
    #     if "password" in kwargs:
    #         self.password = kwargs.get("password")
    #         kwargs.pop("password")
    #     super(User, self).__init__(*args, **kwargs)
    def __init__(self, email, password, role_name, remark):
        self.email = email
        self.password = password
        self.role_name = role_name
        self.remark = remark

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)  # 只能用“self._password”

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

    def have_permission(self, permission):
        return self.role.permission & permission == permission

class FriendLink(db.Model):
    __tablename__ = "friendlink"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    link = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    join_time = db.Column(db.Date, default=date.today)
    remark = db.Column(db.String(50), nullable=False)

class TitleImage(db.Model):
    __tablename__ = "titleimage"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(30), nullable=False)
    href = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    join_time = db.Column(db.Date, default=date.today)

class ParentCategory(db.Model):
    __tablename__ = "parent_cate"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)

class ChildCategory(db.Model):
    __tablename__ = "child_cate"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("parent_cate.id"))

    parent = db.relationship("ParentCategory", backref=db.backref("childs"))

class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.String(30), primary_key=True, default=shortuuid.uuid)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    img_link = db.Column(db.String(100), nullable=False)
    view = db.Column(db.Integer, default=0)
    star = db.Column(db.Integer, default=0)
    post_date = db.Column(db.Date, default=date.today())
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    cate_id = db.Column(db.Integer, db.ForeignKey("child_cate.id"), nullable=False)

    category = db.relationship("ChildCategory", backref=db.backref("posts"))
    author = db.relationship("User", backref=db.backref("posts"))

class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.String(30), primary_key=True, default=shortuuid.uuid)
    nickname = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    add_time = db.Column(db.DateTime, default=datetime.now)
    post_id = db.Column(db.String(30), db.ForeignKey("post.id"))

    post = db.relationship("Post", backref=db.backref("comments"))