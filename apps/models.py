from datetime import date

from werkzeug.security import generate_password_hash, check_password_hash

from apps import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    join_date = db.Column(db.Date, default=date.today)

    @property
    def password(self):
        raise AttributeError('密码不能访问')

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def verify_password(self, value):
        return check_password_hash(self.password_hash, value)

    def __repr__(self):
        return self.username
