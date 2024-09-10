from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    phnno = db.Column(db.Integer)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    
class BusRoute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    busNumber = db.Column(db.String(255), nullable=False)
    source = db.Column(db.String(255), nullable=False)
    destination = db.Column(db.String(255), nullable=False)
    stops = db.Column(db.String(1000))  # Adjust the length as needed



