from datetime import datetime

from ext import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(12), nullable=False)
    pwd = db.Column(db.String(12), unique=True)
    ctime = db.Column(db.DateTime, default=datetime.now)

    def __str__(self):
        return self.name
