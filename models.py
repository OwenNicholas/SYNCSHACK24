from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    q1 = db.Column(db.String(150))
    q2 = db.Column(db.String(150))
    q3 = db.Column(db.String(150))
    q4 = db.Column(db.String(150))
    q5 = db.Column(db.String(150))
    sent_requests = db.relationship('FriendRequest', foreign_keys='FriendRequest.sender_id', backref='sender', lazy='dynamic')
    received_requests = db.relationship('FriendRequest', foreign_keys='FriendRequest.receiver_id', backref='receiver', lazy='dynamic')

class FriendRequest(db.Model):
    __tablename__ = 'friend_requests'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class Friendship(db.Model):
    __tablename__ = 'friendships'
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class UserEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start = db.Column(db.Time, nullable=False)
    end = db.Column(db.Time, nullable=False)
    dow = db.Column(db.String(20), nullable=False)

    user = db.relationship('User', backref=db.backref('events', lazy=True))






