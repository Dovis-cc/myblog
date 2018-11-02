from flask import Flask
from app.main import bp as main_bp
from app.cms import bp as cms_bp
from app.kindeditor import bp as kindeditor_bp
import config
from exts import db, mail
from flask_wtf import CSRFProtect

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(cms_bp)
    app.register_blueprint(kindeditor_bp)

    CSRFProtect(app)
    mail.init_app(app)
    return app
app = create_app()


if __name__ == '__main__':
    app.run()
