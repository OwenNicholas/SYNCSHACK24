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








