from engine import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    in_process = db.Column(db.Boolean, nullable=True, default=False)
    dataOrder = db.Column(db.DateTime(timezone=False), nullable=True)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False)
    success = db.Column(db.Boolean, nullable=False)
    orderid = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False)
