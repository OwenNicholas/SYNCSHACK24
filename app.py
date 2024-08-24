from flask import Flask, render_template, request, redirect, url_for, session, flash  # Include session here
from flask_bcrypt import Bcrypt
from models import db, User
import sqlite3
import os


import sqlite3
from jinja2 import Environment, FileSystemLoader


app = Flask(__name__)
app.secret_key = 'f9c6254ef57f4bccfc7f9684566b615c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
bcrypt = Bcrypt(app)


# Create the database and tables
with app.app_context():
   db.create_all()


@app.route('/', methods=['GET', 'POST'])  # Use '/' for the login route
def login():
   if request.method == 'POST':
       username = request.form['username']
       password = request.form['password']
       user = User.query.filter_by(username=username).first()
       if user and bcrypt.check_password_hash(user.password, password):
           session['user_id'] = user.id
           session['username'] = user.username 
           return redirect(url_for('profile'))  # Redirect to the profile page after login
       else:
           error_message = 'Invalid username or password'  # Set error message if login fails
           return render_template('index.html', error_message=error_message)  # Pass error message to template
   return render_template('index.html')  # Render index.html for the login page




@app.route('/signup', methods=['GET', 'POST'])
def signup():
   error_message = None  # Initialize the error message
   if request.method == 'POST':
       username = request.form['username']  # Capture the username from the form
       password = request.form['password']
       hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
       existing_user = User.query.filter_by(username=username).first()
       if not existing_user:
           new_user = User(username=username, password=hashed_password, q1='', q2='', q3='', q4='', q5='')
           db.session.add(new_user)
           db.session.commit()
           session['user_id'] = new_user.id  # Store user id in session
           return redirect(url_for('question', q_number=1))  # Redirect to the first question
       else:
           error_message = 'User already exists'  # Set the error message
   return render_template('signup.html', error_message=error_message)  # Pass the error message to the template


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
           return render_template('profile.html')  # Or another page after the last question


   try:
       return render_template(f'q{q_number}.html')
   except Exception:
       return "Question not found", 404


@app.route('/profile')
def profile():
   if 'user_id' not in session:
       return redirect(url_for('login'))
  
   user_id = session['user_id']
   user = User.query.get(user_id)
  
   return render_template('profile.html', username=user.username, description=user.q5)




@app.route('/events_list')
def events_list():
   return redirect(url_for('events'))

@app.route('/events', methods=['GET'])
def events():
    # Get the date from the query parameter
    filter_date = request.args.get('event_date')  # Ensure parameter name matches HTML form

    # Print the filter date for debugging purposes
    #print(f"Filter date received: {filter_date}")

    # Connect to the database
    db_path = os.path.abspath(os.path.join('instance', 'users.db'))

    if not os.path.exists(db_path):
        print("Database file not found.")  # Debugging output
        return "Database file not found.", 500

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        if filter_date:
            # Filter events based on the input date
            query = '''
            SELECT * FROM event
            WHERE date = ?
            '''
            cursor.execute(query, (filter_date,))
            events = cursor.fetchall()
            print(f"Events found: {events}")  # Debugging output
        else:
            # Retrieve all events if no date is provided
            query = 'SELECT * FROM event'
            cursor.execute(query)
            events = cursor.fetchall()
            print("No date filter applied, displaying all events.")  # Debugging output

        conn.close()

        # Render the template with the filtered events
        if events:
            return render_template('event_template.html', events=events)
        else:
            return render_template('event_template.html', events=[], message="No events found for the selected date.")

    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return "Database connection error", 500


@app.route('/sign_out')
def sign_out():
   session.pop('user_id', None)
   return redirect(url_for('login'))


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login')) 

    user_id = session['user_id']
    user = User.query.get(user_id)

    if request.method == 'POST':
        new_username = request.form['username']
        new_description = request.form['description']

        # Update the user's username and description
        user.username = new_username
        user.q5 = new_description
        db.session.commit()

        return redirect(url_for('profile'))

    # Render the edit profile form with the current values
    return render_template('edit_profile.html', username=user.username, description=user.q5)



@app.route('/friends_list')
def some_function():
   # Correctly generate the URL with the 'username' parameter
   return redirect(url_for('friends_list', username='some_username'))




def calculate_match(user1, user2):
   match_count = 0
   total_questions = 5


   if user1.q1 == user2.q1:
       match_count += 1
   if user1.q2 == user2.q2:
       match_count += 1
   if user1.q3 == user2.q3:
       match_count += 1
   if user1.q4 == user2.q4:
       match_count += 1
   if user1.q5 == user2.q5:
       match_count += 1


   match_percentage = (match_count / total_questions) * 100
   return match_percentage


def get_matches(current_user):
   users = User.query.all()
   matches = []


   for other_user in users:
       if other_user.username != current_user.username:
           match_percentage = calculate_match(current_user, other_user)
           matches.append({
               'username': other_user.username,
               'match_percentage': match_percentage
           })


   matches.sort(key=lambda x: x['match_percentage'], reverse=True)
   return matches


@app.route('/friends_list/<username>')
def friends_list(username):
   user = User.query.filter_by(username=username).first()
   if not user:
       return "User not found.", 404
  
   matches = get_matches(user)
   return render_template('friends_list.html', matches=matches, username=username)




'''
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
'''








if __name__ == '__main__':
   app.run(host='127.0.0.1', port=5001, debug=True)
