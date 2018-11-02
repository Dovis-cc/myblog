from wtforms import Form, StringField
from wtforms.validators import Regexp, InputRequired, Length, Email
from utils.base_form import BaseForm


class MessageForm(BaseForm):
    message = StringField(validators=[InputRequired("还没输入评论信息呢")])
    nickname = StringField(validators=[Length(max=10, message="昵称最长为10个字符"), InputRequired(message="请输入昵称")])
    email = StringField(validators=[Email(message="请填写正确的邮箱")])

class CommentForm(BaseForm):
    post_id = StringField()
    nickname = StringField(validators=[InputRequired(message="请输入昵称")])
    email = StringField(validators=[InputRequired(message="请输入邮箱")])
    content = StringField(validators=[InputRequired(message="请输入内容")])