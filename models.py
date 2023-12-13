from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "app_user"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    vip = db.Column(db.Boolean, default = False)
    battle_scars = db.Column(db.Integer, default = 0)
    posts = db.relationship("Post", backref="user", lazy=True)  # add relationship


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("app_user.user_id"))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, onupdate=datetime.utcnow)
    replies_count = db.Column(db.Integer, default=0)
    views_count = db.Column(db.Integer, default=0)


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("app_user.user_id"), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="replies")
    post = db.relationship("Post", backref="replies")
