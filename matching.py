from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    q1 = db.Column(db.String(100))
    q2 = db.Column(db.String(100))
    q3 = db.Column(db.String(100))
    q4 = db.Column(db.String(100))

def calculate_match(user1, user2):
    match_count = 0
    total_questions = 4

    if user1.q1 == user2.q1:
        match_count += 1
    if user1.q2 == user2.q2:
        match_count += 1
    if user1.q3 == user2.q3:
        match_count += 1
    if user1.q4 == user2.q4:
        match_count += 1

    match_percentage = (match_count / total_questions) * 100
    return match_percentage

def get_matches(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return None

    users = User.query.all()
    matches = []

    for other_user in users:
        if other_user.username != user.username:
            match_percentage = calculate_match(user, other_user)
            matches.append({
                'username': other_user.username,
                'match_percentage': match_percentage
            })

    matches.sort(key=lambda x: x['match_percentage'], reverse=True)
    return matches
