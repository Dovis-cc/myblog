from celery import Celery
from flask import Flask
from flask_mail import Message
from exts import mail
import config

app = Flask(__name__)
app.config.from_object(config)
mail.init_app(app)

def make_celery():
    celery = Celery(app.import_name,
                    backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery()

@celery.task
def send_mail(subject, sender, recipients, body):
    """异步发送邮件
    """
    message = Message(subject=subject, sender=sender, recipients=recipients, body=body)
    mail.send(message)