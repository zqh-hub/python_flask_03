from exts import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(12), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    is_delete = db.Column(db.BOOLEAN, default=False)
    ctime = db.Column(db.DateTime, default=datetime.now)

    def __str__(self):
        return self.username
