from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'app_user'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password