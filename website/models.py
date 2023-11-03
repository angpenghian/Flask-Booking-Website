from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import UniqueConstraint

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    account_type = db.Column(db.String(150))
    notes = db.relationship('Note')
    rooms = db.relationship('Rooms')

class Rooms(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True))
    room_name = db.Column(db.String(150))
    room_size = db.Column(db.String(150))
    room_price = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    checkout = db.Column(db.Boolean, default=False)
    
    __table_args__ = (UniqueConstraint('date', 'room_name', name='_date_room_name_uc'),)