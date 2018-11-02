import os

DEBUG = False

# session加密的盐
SECRET_KEY = os.urandom(24)

# 上传图片相关
# 首页题图
BASE_PATH = os.path.dirname(__file__)+"/static/images/t_images/"
# 文章图片
IMG_PATH = os.path.dirname(__file__)+"/static/images/post_images/"
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

# 数据库相关配置
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:000000@127.0.0.1:3306/myblog?charset=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 邮箱相关配置
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
# MAIL_USE_TLS = True 587
MAIL_USE_SSL = True  #465
# MAIL_DEBUG : default app.debug
MAIL_USERNAME = "1254353037@qq.com"
MAIL_PASSWORD = "zreznapycwochbgi"
# MAIL_DEFAULT_SENDER = "1254353037@qq.com"  # 配置的方式给出默认发送者

# ueditor上传图片
UEDITOR_UPLOAD_PATH = os.path.dirname(__file__)+"/static/images/post_images/"

# celery相关配置
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"

