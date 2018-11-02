from .view import bp
from .models import Role, User, FriendLink, TitleImage, ParentCategory, ChildCategory, Post, Comment

# 一定要将hooks文件导入进来，与主文件相关联
import app.cms.hooks