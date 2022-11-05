from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True, nullable=False)
    email = db.Column(db.String(100), index=True, nullable=False)
    phone = db.Column(db.String(10), index=True, nullable=False)
    address = db.Column(db.String(100), index=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='user')

class Event(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(80))
    event_desc = db.Column(db.String(500))
    event_image = db.Column(db.String(500)) 
    event_date = db.Column(db.String(10))
    event_time = db.Column(db.String(10))
    event_category = db.Column(db.String(150))
    event_artist = db.Column(db.String)
    event_venue = db.Column(db.String)
    ticket_max = db.Column(db.Integer)
    event_status = db.Column(db.String)
    event_author = db.Column(db.String)
    comments = db.relationship('Comment', backref='eventcomments')
	
    def __repr__(self): #string print method
        return "<Name: {}>".format(self.name)

class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    comment_body = db.Column(db.String(500))
    comment_author = db.Column(db.String, db.ForeignKey('users.username'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
    post_date = db.Column(db.DateTime, default=datetime.now())
    

class Bookings(db.Model):
    __tablename__='bookings'
    booking_id = db.Column(db.Integer, primary_key=True)
    booking_author =  db.Column(db.String, db.ForeignKey('users.username'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
    ticket_qty = db.Column(db.Integer)

    def __repr__(self):
        return "<Comment: {}>".format(self.text)


