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
    events = db.Column(db.Text)








