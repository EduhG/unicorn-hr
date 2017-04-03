from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)
    full_name = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(100), nullable=False)
