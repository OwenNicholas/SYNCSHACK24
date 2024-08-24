
from flask import Flask, render_template, request, redirect, url_for, session  # Include session here
from flask_bcrypt import Bcrypt
from models import db, User
import sqlite3
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
app.secret_key = 'f9c6254ef57f4bccfc7f9684566b615c' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Needed for flashing messages

db.init_app(app)
bcrypt = Bcrypt(app)

# Create the database and tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Capture the password from the form
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):

            session['user_id'] = user.id  # Store the user's ID in the session
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']  # Capture the username from the form
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:

            new_user = User(email=email, password=hashed_password, q1='', q2='', q3='', q4='', q5='')
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id  # Store user id in session
            return redirect(url_for('question', q_number=1))  # Redirect to the first question
        else:
            flash('User already exists', 'danger')
            return redirect(url_for('signup'))
    return render_template('signup.html')

@app.route('/question/<int:q_number>', methods=['GET', 'POST'])
def question(q_number):
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Ensure user is logged in

    user_id = session['user_id']
    user = User.query.get(user_id)

    if request.method == 'POST':
        answer = request.form.get('answer')
        print(f"Captured answer for question {q_number}: {answer}")

        if q_number == 1:
            user.q1 = answer
        elif q_number == 2:
            user.q2 = answer
        elif q_number == 3:
            user.q3 = answer
        elif q_number == 4:
            user.q4 = answer  
        elif q_number == 5:
            user.q5 = answer
        
        db.session.commit()

        if q_number < 5:
            return redirect(url_for('question', q_number=q_number+1))
        else:
            return render_template('thank_you.html')  # Or another page after the last question

    # Dynamically render question from the main templates directory
    try:
        return render_template(f'q{q_number}.html')
    except Exception:
        return "Question not found", 404

db_path = 'instance/users.db'
output_html_path = 'templates/event.html'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('SELECT * FROM event')
events = cursor.fetchall()
conn.close()

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('event.html')
html_content = template.render(events=events)

with open(output_html_path, 'w') as file:
    file.write(html_content)

print(f'HTML file generated: {output_html_path}')

if __name__ == '__main__':
    app.run(debug=True)

