from flask import Blueprint, render_template, views, request, session, redirect, url_for, g, jsonify
from .models import User, Permission, Role, FriendLink, TitleImage, ChildCategory, ParentCategory, Post, Comment
from .forms import (LoginForm, FindPasswordForm, ResetpwdForm, AddUserForm, UpdataUserForm,
                    AddRoleForm, AddFlForm, AddTimageForm, PostForm)
from werkzeug.datastructures import CombinedMultiDict
from .decorators import login_requried, permission_requried
from utils import my_restful, random_utils, cache
from flask_mail import Message
from exts import mail, db
import config
from tasks import send_mail

bp = Blueprint("cms", __name__, url_prefix="/cms")

@bp.route("/")
@login_requried
def index():
    return render_template("cms/index.html")

@bp.route("/captcha/")
def captcha():
    email = request.args.get("email")
    user = User.query.filter_by(email=email).first()
    if user:
        temp_captcha = random_utils.get_email_captcha()
        send_mail.delay(subject='[倚栏听风个人博客] 重置密码',
                        recipients=[email],
                        sender=("倚栏听风", "1254353037@qq.com"),
                        body="您正在重置密码，邮箱验证码是：%s，10分钟内有效，请尽快完成更改。" % temp_captcha)
        cache.set(email, temp_captcha)
        return my_restful.result(200, "验证码发送成功")
    else:
        return my_restful.result(400, "没有找到该账号")

@bp.route("/logout/")
@login_requried
def logout():
    del session["user_id"]
    return redirect(url_for("cms.login"))

@bp.route("/profile/")
@login_requried
def profile():
    return render_template("cms/profile.html")

@bp.route("/navimages/")
@login_requried
@permission_requried(Permission.b)
def navimages():
    error = request.args.get("error")
    t_images = TitleImage.query.order_by(TitleImage.priority).all()
    return render_template("cms/navimages.html", images=t_images, error=error)

@bp.route("/add_timage/", methods=["POST"])
@login_requried
@permission_requried(Permission.b)
def add_timage():
    form = AddTimageForm(request.form)
    if form.validate():
        img = request.files.get("link")
        if not img:
            return redirect(url_for("cms.navimages", error="请选择图片"))
        # 检查图片是否合法
        img_name = img.filename
        allowed_extention = config.ALLOWED_EXTENSIONS
        flag = '.' in img_name and img_name.rsplit('.', 1)[1] in allowed_extention
        if not flag:
            return redirect(url_for("cms.navimages", error="图片格式错误"))
        img_name = random_utils.get_random_name()
        base_path = config.BASE_PATH
        path = base_path+img_name+".jpg"
        img.save(path)
        # 存入数据库
        link = "/static/images/t_images/{}.jpg".format(img_name)
        desc = form.desc.data
        href = form.href.data
        priority = form.priority.data
        t_image = TitleImage(link=link, desc=desc, href=href, priority=priority)
        db.session.add(t_image)
        db.session.commit()
        return redirect(url_for("cms.navimages"))
    else:
        error = form.get_error()
        return redirect(url_for("cms.navimages", error=error))

@bp.route("/delete_timage/")
@login_requried
@permission_requried(Permission.b)
def delete_timage():
    id = request.args.get("id")
    timage = TitleImage.query.filter_by(id=id).first()
    if timage:
        db.session.delete(timage)
        db.session.commit()
        return my_restful.result(200, "删除成功")
    else:
        return my_restful.result(400, "没有找到此题图")

@bp.route("/update_timage/", methods=["POST"])
@login_requried
@permission_requried(Permission.b)
def update_timage():
    form = AddTimageForm(request.form)
    if form.validate():
        id = request.form.get("timage_id")
        desc = form.desc.data
        priority = form.priority.data
        href = form.href.data
        timage = TitleImage.query.filter_by(id=id).first()
        print(timage)
        if timage:
            timage.href = href
            timage.priority = priority
            timage.desc = desc
            db.session.commit()
            return my_restful.result(200, "添加成功")
        else:
            return my_restful.result(400, "没有找到该题图")
    else:
        error = form.get_error()
        return my_restful.result(400, error)

@bp.route("/friendlink/")
@login_requried
@permission_requried(Permission.b)
def friendlink():
    fls = FriendLink.query.order_by(FriendLink.priority).all()
    return render_template("cms/friendlink.html", fls=fls)

@bp.route("/add_friendlink/", methods=["POST"])
@login_requried
@permission_requried(Permission.b)
def add_friendlink():
    form = AddFlForm(request.form)
    if form.validate():
        name = form.name.data
        link = form.link.data
        priority = form.priority.data
        remark = form.remark.data
        fl = FriendLink(name=name, link=link, priority=priority, remark=remark)
        db.session.add(fl)
        db.session.commit()
        return my_restful.result(200, "添加成功")
    else:
        error = form.get_error()
        return my_restful.result(400, error)

@bp.route("/delete_fl/")
@login_requried
@permission_requried(Permission.b)
def delete_fl():
    id = request.args.get("fl_id")
    fl = FriendLink.query.filter_by(id=id).first()
    if fl:
        db.session.delete(fl)
        db.session.commit()
        return my_restful.result(200, "删除成功")
    else:
        return my_restful.result(400, "没有找到该友链")

@bp.route("/update_fl/", methods=["POST"])
@login_requried
@permission_requried(Permission.b)
def update_fl():
    form = AddFlForm(request.form)
    if form.validate():
        id = request.form.get("fl_id")
        name = form.name.data
        link = form.link.data
        priority = form.priority.data
        remark = form.remark.data
        fl = FriendLink.query.filter_by(id=id).first()
        if fl:
            fl.name = name
            fl.link = link
            fl.priority = priority
            fl.remark = remark
            db.session.commit()
            return my_restful.result(200, "修该成功")
        else:
            return my_restful.result(400, "没有该友链")
    else:
        error = form.get_error()
        return my_restful.result(400, error)

@bp.route("/message/")
@login_requried
@permission_requried(Permission.b)
def message():
    per_page = 10
    page = request.args.get("page", type=int, default=1)
    cate_id = request.args.get("cate_id")
    if cate_id:
        paginate = Post.query.filter_by(cate_id=cate_id).\
            order_by(Post.post_date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    else:
        paginate = Post.query.order_by(Post.post_date.desc()).paginate(page=page, per_page=per_page,
                                                                       error_out=False)
    cates = ChildCategory.query.all()
    return render_template("cms/messages.html", paginate=paginate, cates=cates)

@bp.route("/delete_post/")
@login_requried
@permission_requried(Permission.b)
def delete_post():
    post_id = request.args.get("post_id")
    if post_id:
        post = Post.query.filter_by(id=post_id).first()
        if post:
            db.session.delete(post)
            db.session.commit()
            return my_restful.result(200, "删除成功")
        else:
            return my_restful.result(300, "没有找到这篇文章")
    else:
        return my_restful.result(400, "没有找到这篇文章")

@bp.route("/comment/")
@login_requried
@permission_requried(Permission.b)
def comment():
    per_page = 10
    page = request.args.get("page", type=int, default=1)
    paginate = Comment.query.order_by(Comment.add_time.desc()).paginate(page, per_page=per_page, error_out=False)
    cates = ChildCategory.query.all()
    return render_template("cms/comments.html", cates=cates, paginate=paginate)

@bp.route("/category/<name>")
@login_requried
@permission_requried(Permission.b)
def category(name):
    parents = ParentCategory.query.all()
    if name == "child":
        per_page = 10
        page = request.args.get("page", type=int, default=1)
        paginate = ChildCategory.query.paginate(page, per_page=per_page, error_out=False)
        return render_template("cms/category_child.html", params={"name": name}, paginate=paginate, parents=parents)
    elif name == "parent":
        return render_template("cms/category_parent.html", parents=parents)

@bp.route("/add_parent_cate/", methods=["POST"])
@login_requried
@permission_requried(Permission.b)
def add_parent_cate():
    name = request.form.get("name")
    if name:
        parent = ParentCategory(name=name)
        db.session.add(parent)
        db.session.commit()
        return my_restful.result(200, "添加成功")
    else:
        return my_restful.result(400, "请输入名称")

@bp.route("/add_child_cate/", methods=["POST"])
@login_requried
@permission_requried(Permission.b)
def add_child_cate():
    name = request.form.get("name")
    parent_id = request.form.get("parent_id")
    if name:
        child = ChildCategory(name=name, parent_id=parent_id)
        db.session.add(child)
        db.session.commit()
        return my_restful.result(200, "添加成功")
    else:
        return my_restful.result(400, "请输入姓名")

@bp.route("/delete_parent_cate/")
@login_requried
@permission_requried(Permission.b)
def delete_parent_cate():
    parent_id = request.args.get("parent_id")
    parent = ParentCategory.query.filter_by(id=parent_id).first()
    if parent:
        db.session.delete(parent)
        db.session.commit()
        return my_restful.result(200, "删除成功")
    else:
        return my_restful.result(400, "没有找到该分类")

@bp.route("/delete_child_cate/")
@login_requried
@permission_requried(Permission.b)
def delete_child_cate():
    child_id = request.args.get("child_id")
    child = ChildCategory.query.filter_by(id=child_id).first()
    if child:
        db.session.delete(child)
        db.session.commit()
        return my_restful.result(200, "删除成功")
    else:
        return my_restful.result(400, "没有找到该分类")

@bp.route("/update_parent_cate/", methods=["POST"])
@login_requried
@permission_requried(Permission.b)
def update_parent_cate():
    name = request.form.get("name")
    parent_id = request.form.get("parent_id")
    if name and parent_id:
        parent = ParentCategory.query.filter_by(id=parent_id).first()
        parent.name = name
        db.session.commit()
        return my_restful.result(200, "编辑成功")
    else:
        return my_restful.result(400, "请输入名称")

@bp.route("/update_child_cate/", methods=["POST"])
@login_requried
@permission_requried(Permission.b)
def update_child_cate():
    name = request.form.get("name")
    parent_id = request.form.get("parent_id")
    child_id = request.form.get("child_id")
    if name and parent_id:
        child = ChildCategory.query.filter_by(id=child_id).first()
        child.name = name
        child.parent_id = parent_id
        db.session.commit()
        return my_restful.result(200, "编辑成功")
    else:
        return my_restful.result(400, "请输入名称")

@bp.route("/usermanage/")
@login_requried
@permission_requried(Permission.d)
def usermanage():
    per_page = 10
    page = request.args.get("page", type=int, default=1)
    paginate = User.query.paginate(page=page, per_page=per_page, error_out=False)
    roles = Role.query.all()
    return render_template("cms/usermanage.html", paginate=paginate, roles=roles)

@bp.route("/delete_user/")
@login_requried
@permission_requried(Permission.d)
def delete_user():
    user_id = request.args.get("user_id")
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return my_restful.result(200, "删除成功")

@bp.route("/add_user/", methods=["POST"])
@login_requried
@permission_requried(Permission.d)
def add_user():
    form = AddUserForm(request.form)
    if form.validate():
        email = form.email.data
        password = form.password.data
        remark = form.remark.data
        role_name = form.role.data
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email, password=password, remark=remark, role_name=role_name)
            db.session.add(user)
            db.session.commit()
            return my_restful.result(200, "用户添加成功")
        else:
            return my_restful.result(400, "该邮箱已被使用")
    else:
        error = form.get_error()
        return my_restful.result(400, error)

@bp.route("/update_user/", methods=["POST"])
@login_requried
@permission_requried(Permission.d)
def update_user():
    form = UpdataUserForm(request.form)
    if form.validate():
        user_id = request.form.get("user_id")
        remark = form.remark.data
        role_name = form.role.data
        user = User.query.filter_by(id=user_id).first()
        user.remark = remark
        user.role_name = role_name
        db.session.commit()
        return my_restful.result(200, "编辑成功")
    else:
        error = form.get_error()
        return my_restful.result(400, error)

@bp.route("/lahei/")
@login_requried
@permission_requried(Permission.d)
def lahei():
    user_id = request.args.get("user_id")
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.status = 0
        db.session.commit()
        return my_restful.result(200, "已拉黑")
    else:
        return my_restful.result(400, "没有找到该用户")

@bp.route("/keyong/")
@login_requried
@permission_requried(Permission.d)
def keyong():
    user_id = request.args.get("user_id")
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.status = 1
        db.session.commit()
        return my_restful.result(200, "已激活")
    else:
        return my_restful.result(400, "没有找到该用户")

@bp.route("/rolemanage/")
@login_requried
@permission_requried(Permission.d)
def rolemanage():
    roles = Role.query.order_by(Role.permission.desc()).all()
    return render_template("cms/rolemanage.html", roles=roles)

@bp.route("/add_role/", methods=["POST"])
@login_requried
@permission_requried(Permission.d)
def add_role():
    form = AddRoleForm(request.form)
    if form.validate():
        name = form.name.data
        permission = form.permission.data
        desc = form.desc.data
        role = Role.query.filter_by(name=name).first()
        if not role:
            role = Role(name=name, permission=permission, desc=desc)
            db.session.add(role)
            db.session.commit()
            return my_restful.result(200, "角色添加成功")
        else:
            return my_restful.result(400, "该角色已存在")
    else:
        error = form.get_error()
        return my_restful.result(400, error)

@bp.route("/delete_role/")
@login_requried
@permission_requried(Permission.d)
def delete_role():
    name = request.args.get("name")
    role = Role.query.filter_by(name=name).first()
    if role:
        db.session.delete(role)
        db.session.commit()
        return my_restful.result(200, "删除成功")
    else:
        return my_restful.result(400, "没有此角色")

class Login(views.MethodView):
    def get(self):
        return render_template("cms/login.html")

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            rememberme = request.form.get("rememberme")
            user = User.query.filter_by(email=email).first()
            if user:
                if user.status == 1:
                    if user.check_password(password):
                        session["user_id"] = user.id
                        if rememberme == "1":
                            session.permanent = True
                        return my_restful.result(200, "登录成功")
                    else:
                        return my_restful.result(400, "密码错误")
                else:
                    return my_restful.result(401, "该账号已被列入黑名单，请联系博主解封")
            else:
                return my_restful.result(400, "没有此用户")
        else:
            error = form.get_error()
            return my_restful.result(400, error)

class FindPassword(views.MethodView):
    def get(self):
        return render_template("cms/find_pwd.html")

    def post(self):
        form = FindPasswordForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user:
                user.password = password
                db.session.commit()  # 注意：修改数据后要提交
                return my_restful.result(200, "重置密码成功")
            else:
                return my_restful.result(400, "没有找到此用户")
        else:
            error = form.get_error()
            return my_restful.result(400, error)

class Resetpwd(views.MethodView):
    decorators = [login_requried]

    def get(self):
        return render_template("cms/resetpwd.html")

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            if g.user.check_password(oldpwd):
                g.user.password = newpwd
                db.session.commit()
                return my_restful.result(200, "修改成功")
            else:
                return my_restful.result(400, "旧密码错误")
        else:
            error = form.get_error()
            return my_restful.result(400, error)

class PostmMessage(views.MethodView):
    decorators = [login_requried]
    def get(self):
        childs = ChildCategory.query.all()
        return render_template("cms/post.html", childs=childs)

    def post(self):
        form = PostForm(CombinedMultiDict((request.form, request.files)))
        if form.validate():
            title = form.title.data
            content = form.content.data
            cate_id = form.cate_id.data
            file = form.img_file.data
            if file:
                filename = random_utils.get_random_name()
                file.save(config.IMG_PATH+filename+".jpg")
                img_link = "/static/images/post_images/"+filename+".jpg"
            else:
                img_link = "/static/images/post_images/default.jpg"
            post = Post(title=title, content=content, img_link=img_link, cate_id=cate_id, author_id=session["user_id"])
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("main.view", post_id=post.id))
        else:
            return form.get_error()


bp.add_url_rule("/login/", view_func=Login.as_view("login"))
bp.add_url_rule("/findpassword/", view_func=FindPassword.as_view("find_password"))
bp.add_url_rule("/resetpwd/", view_func=Resetpwd.as_view("resetpwd"))
bp.add_url_rule("/post/", view_func=PostmMessage.as_view("post"))


