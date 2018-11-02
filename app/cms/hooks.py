# 一定要将hooks文件导入进来，与主文件相关联
from flask import session, g
from .view import bp
from .models import User, Permission

@bp.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        g.user = user

@bp.context_processor
def context_processor():
    return {"Permission": Permission}