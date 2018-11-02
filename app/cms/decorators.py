from flask import session, redirect, url_for,g
from functools import wraps

# 登陆验证
def login_requried(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if "user_id" in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("cms.login"))
    return inner

# 权限验证
def permission_requried(permission):
    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user = g.user
            if user.have_permission(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for("cms.index"))
        return inner
    return outer

