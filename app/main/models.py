from exts import db
import shortuuid
from datetime import datetime

class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.String(30), primary_key=True, default=shortuuid.uuid)
    nickname = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    add_time = db.Column(db.DateTime, default=datetime.now)
    prev_id = db.Column(db.String(30), db.ForeignKey("message.id"))

    prev = db.relationship("Message", remote_side=[id], uselist=False, backref=db.backref("nexts"))

