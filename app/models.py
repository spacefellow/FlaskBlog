from config import db
from datetime import datetime
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String, nullable=False, unique=True)
    posts = db.relationship('Post', cascade="all, delete-orphan", backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    intro = db.Column(db.String(300))
    text = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_name = db.Column(db.String(80), db.ForeignKey('user.username'))

    def __repr__(self):
        return '<Post %r>' % self.post_id
