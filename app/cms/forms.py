from wtforms import Form, StringField, IntegerField
from wtforms.validators import Email, Regexp, Length, EqualTo, InputRequired, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from utils.base_form import BaseForm
from utils import cache

class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="邮箱格式不正确")])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z]{6,12}", message="密码格式不正确")])

class FindPasswordForm(BaseForm):
    email = StringField(validators=[Email(message="邮箱格式不正确"),
                                    InputRequired(message="请输入邮箱")])
    captcha = StringField(validators=[Length(min=6, max=6, message="验证码长度不正确"),
                                      InputRequired(message="请输入验证码")])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z]{6,12}", message="密码格式不正确"),
                                       InputRequired(message="请输入新密码")])
    repassword = StringField(validators=[EqualTo("password", message="两次密码不一致"),
                                         InputRequired(message="请确认新密码")])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        real_captcha = cache.get(email)
        if not real_captcha or real_captcha != captcha:
            raise ValidationError("验证码错误")

class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Regexp(r"[0-9a-zA-Z]{6,12}", message="密码格式不正确")])
    newpwd = StringField(validators=[Regexp(r"[0-9a-zA-Z]{6,12}", message="密码格式不正确")])
    renewpwd = StringField(validators=[Regexp(r"[0-9a-zA-Z]{6,12}", message="密码格式不正确"),
                                       EqualTo("newpwd", message="两次密码不一致")])

class AddUserForm(BaseForm):
    email = StringField(validators=[Email(message="邮箱格式不正确"), InputRequired(message="请输入邮箱")])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z]{6,12}", message="密码格式不正确"),
                                       InputRequired(message="请输入密码")])
    remark = StringField(validators=[InputRequired(message="请输入备注")])
    role = StringField(validators=[InputRequired(message="请选择角色")])

class UpdataUserForm(BaseForm):
    remark = StringField(validators=[InputRequired(message="请输入备注")])
    role = StringField(validators=[InputRequired(message="请选择角色")])

class AddRoleForm(BaseForm):
    name = StringField(validators=[InputRequired(message="请输入角色名称")])
    permission = IntegerField(validators=[InputRequired(message="请选择角色权限")])
    desc = StringField(validators=[InputRequired(message="请输入角色描述")])

class AddFlForm(BaseForm):
    name = StringField(validators=[InputRequired(message="请输入角色名称")])
    link = StringField(validators=[InputRequired(message="请输入友链地址")])
    priority = IntegerField(validators=[InputRequired(message="请输入优先级")])
    remark = StringField(validators=[InputRequired(message="请输入备注")])

class AddTimageForm(BaseForm):
    desc = StringField(validators=[InputRequired(message="请输入描述信息")])
    href = StringField(validators=[InputRequired(message="请输入跳转链接")])
    priority = IntegerField(validators=[InputRequired(message="请输入优先级")])

class PostForm(BaseForm):
    title = StringField(validators=[InputRequired(message="请输入文章标题"),
                                    Length(max=100, message="文章标题过长")])
    content = StringField(validators=[InputRequired(message="文章内容不能为空")])
    img_file = FileField(validators=[FileAllowed(['jpg', 'png'], message="文件只能是图片")])
    cate_id = IntegerField()