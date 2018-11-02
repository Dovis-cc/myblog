from flask import Blueprint, render_template, request, redirect
from app.cms import TitleImage, FriendLink, ParentCategory, ChildCategory, Post, Comment
from .models import Message
from .forms import MessageForm, CommentForm
from utils import my_restful, cache
from exts import db

bp = Blueprint("main", __name__)

@bp.route('/')
def index():
    title_images = TitleImage.query.order_by(TitleImage.priority).limit(3).all()
    friendlinks = FriendLink.query.order_by(FriendLink.priority).all()
    childs = ChildCategory.query.all()
    hot_post = Post.query.order_by(Post.view.desc()).limit(5)
    per_page = 10
    page = request.args.get("page", type=int, default=1)
    paginate = Post.query.order_by(Post.post_date.desc()).paginate(page=page, per_page=per_page,
                                                                   error_out=False)
    data = {"title_images": title_images,
            "friendlinks": friendlinks,
            "childs": childs,
            "hot_post": hot_post,
            "paginate": paginate}
    return render_template("main/index.html", data=data)

@bp.route("/learnlist/")
def learnlist():
    friendlinks = FriendLink.query.order_by(FriendLink.priority).all()
    parent = ParentCategory.query.filter_by(name="学无止境").first()
    childs = []
    if parent:
        childs = parent.childs
    cate_id = []
    for child in childs:
        cate_id.append(child.id)
    base_post_list = Post.query.filter(Post.cate_id.in_(cate_id))
    per_page = 10
    page = request.args.get("page", type=int, default=1)  # 当前页
    paginate = base_post_list.order_by(Post.post_date.desc()).paginate(page=page, per_page=per_page,
                                                                       error_out=False)
    hot_post = base_post_list.order_by(Post.view.desc()).limit(5)
    data = {"hot_post": hot_post,
            "childs": childs,
            "friendlinks": friendlinks,
            "paginate": paginate}
    return render_template("main/learnlist.html", data=data)

@bp.route("/lifelist/")
def lifelist():
    friendlinks = FriendLink.query.order_by(FriendLink.priority).all()
    parent = ParentCategory.query.filter_by(name="生活随笔").first()
    childs = []
    if parent:
        childs = parent.childs
    cate_id = []
    for child in childs:
        cate_id.append(child.id)
    base_post_list = Post.query.filter(Post.cate_id.in_(cate_id))
    hot_post = base_post_list.order_by(Post.view.desc()).limit(5)
    per_page = 10
    page = request.args.get("page", type=int, default=1)
    paginate = base_post_list.order_by(Post.post_date.desc()).paginate(page=page, per_page=per_page,
                                                                       error_out=False)
    data = {"paginate": paginate,
            "hot_post": hot_post,
            "childs": childs,
            "friendlinks": friendlinks,
            }
    return render_template("main/lifelist.html", data=data)

@bp.route("/aboutme/")
def aboutme():
    return render_template("main/aboutme.html")

@bp.route("/message/")
def message():
    per_page = 10
    page = request.args.get("page", type=int, default=1)
    paginate = Message.query.order_by(Message.add_time.desc()).paginate(page=page, per_page=per_page,
                                                                        error_out=False)
    return render_template("main/message.html", paginate=paginate)

@bp.route("/add_message/", methods=["POST"])
def add_message():
    form = MessageForm(request.form)
    if form.validate():
        content = form.message.data
        nickname = form.nickname.data
        email = form.email.data
        message = Message(content=content, nickname=nickname, email=email)
        db.session.add(message)
        db.session.commit()
        return my_restful.result(200, "吐槽成功")
    else:
        error = form.get_error()
        return my_restful.result(400, error)

@bp.route("/reply_message/", methods=["POST"])
def reply_message():
    form = MessageForm(request.form)
    prev_id = request.form.get("prev_id")
    if form.validate():
        if prev_id:
            prev = Message.query.filter_by(id=prev_id).first()
            if prev:
                content = form.message.data
                nickname = form.nickname.data
                email = form.email.data
                message = Message(content=content, nickname=nickname, email=email)
                message.prev = prev
                db.session.add(message)
                db.session.commit()
                return my_restful.result(200, "回复成功")
            else:
                return my_restful.result(400, "没有找到要回复的评论")
        else:
            return my_restful.result(400, "没有找到要回复的评论")
    else:
        error = form.get_error()
        return my_restful.result(400, error)

@bp.route("/view/<post_id>")
def view(post_id):
    childs = ChildCategory.query.all()
    hot_post = Post.query.order_by(Post.view.desc()).limit(5)
    friendlinks = FriendLink.query.order_by(FriendLink.priority).all()
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.add_time.desc()).all()
    data = {"childs": childs,
            "hot_post": hot_post,
            "friendlinks": friendlinks,
            "comments": comments
            }
    post = Post.query.filter_by(id=post_id).first()
    post.view = post.view + 1
    db.session.commit()
    return render_template("main/view.html", post=post, data=data)

@bp.route("/tags/<int:tag_id>")
def tags(tag_id):
    base_post_list = Post.query.filter_by(cate_id=tag_id)
    childs = ChildCategory.query.all()
    per_page = 10
    page = request.args.get("page", type=int, default=1)
    paginate = base_post_list.order_by(Post.post_date.desc()).paginate(page=page, per_page=per_page,
                                                                       error_out=False)
    hot_post = base_post_list.order_by(Post.view.desc()).limit(5)
    friendlinks = FriendLink.query.order_by(FriendLink.priority).all()
    data = {"childs": childs,
            "hot_post": hot_post,
            "friendlinks": friendlinks,
            "paginate": paginate,
            "endpoint": ".tags",
            "params": {"tag_id": tag_id}}
    return render_template("main/postlist.html", data=data)

@bp.route("/to_star/")
def to_star():
    ip_address = request.remote_addr
    post_id = request.args.get("post_id")
    cache_key = ip_address + post_id
    cache_value = cache.get(cache_key)
    if cache_value:
        return my_restful.result(400, "您已经点过赞了")
    post = Post.query.filter_by(id=post_id).first()
    if post:
        post.star = post.star+1
        db.session.commit()
        cache.set(cache_key, "like", 60*30)
        return my_restful.result(200, "感谢点赞", data={"star": post.star})
    else:
        return my_restful.result(400, "没有找到这篇文章")

@bp.route("/comment/", methods=["POST"])
def comment():
    form = CommentForm(request.form)
    if form.validate():
        post_id = form.post_id.data
        nickname = form.nickname.data
        email = form.email.data
        content = form.content.data
        comment = Comment(nickname=nickname, email=email, content=content, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        return my_restful.result(200, "评论发表成功")
    else:
        return my_restful.result(400, form.get_error())

@bp.route("/search/")
def search():
    to_return = request.referrer
    key = request.args.get("key")
    if key:
        friendlinks = FriendLink.query.order_by(FriendLink.priority).all()
        title_images = TitleImage.query.order_by(TitleImage.priority).limit(3).all()
        childs = ChildCategory.query.all()
        per_page = 10
        page = request.args.get("page", type=int, default=1)
        paginate = Post.query.filter(Post.title.like("%"+key+"%")).order_by(Post.post_date.desc()).paginate(page=page, per_page=per_page,
                                                                                                             error_out=False)
        hot_post = Post.query.order_by(Post.view.desc()).limit(5)
        data = {"title_images": title_images,
                "friendlinks": friendlinks,
                "childs": childs,
                "paginate": paginate,
                "endpoint": ".search",
                "params": {"key": key},
                "hot_post": hot_post}
        return render_template("main/postlist.html", data=data)
    else:
        return redirect(to_return)
