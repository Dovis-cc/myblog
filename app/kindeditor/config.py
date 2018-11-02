from flask import Blueprint, request
from utils import random_utils
import config
import json
import os

bp = Blueprint("kindeditor", __name__, url_prefix="/kindeditor")


@bp.route("/upload/", methods=["POST"])
def upload():
    file_type = request.args.get("dir")
    if file_type == "image":  # 用户点击上传单个图片按钮
        img_file = request.files.get("image")
        filename = img_file.filename
        flag = '.' in filename and filename.rsplit('.', 1)[1] in config.ALLOWED_EXTENSIONS
        if flag:
            filename = random_utils.get_random_name()
            img_file.save(config.IMG_PATH+filename+".jpg")
            return json.dumps({
                "error": 0,
                "url": os.path.join("/static/images/post_images/", filename)+".jpg"
            })
        else:
            return json.dumps({
                "error": 1,
                "message": "图片格式错误"
            })
    else:
        return json.dumps({
            "error": 1,
            "message": "请选择图片文件"
        })