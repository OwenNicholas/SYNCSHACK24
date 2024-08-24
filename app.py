from flask import Flask, render_template, request, redirect, url_for, session, flash  # Include session here
from flask_bcrypt import Bcrypt
from models import db, User, FriendRequest, Friendship, UserEvent
import sqlite3
import os
from datetime import datetime, date, time

import requests
from bs4 import BeautifulSoup
from datetime import datetime

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
                error_message = 'Invalid username or password'
                return render_template('index.html', error_message=error_message)
    return render_template('index.html')


def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None



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
    current_user = get_current_user()  # Function to get the logged-in user
    if not current_user:
        return redirect(url_for('login'))
    
    # Get friend requests and accepted friends
    friend_requests = FriendRequest.query.filter_by(receiver_id=current_user.id, status='pending').all()
    friends = []

    friendships = Friendship.query.filter(
        (Friendship.user1_id == current_user.id) | (Friendship.user2_id == current_user.id)
    ).all()

    for friendship in friendships:
        friend_id = friendship.user1_id if friendship.user1_id != current_user.id else friendship.user2_id
        friend = User.query.get(friend_id)
        if friend:
            friends.append(friend)

    # Pass the data to the template
    return render_template(
        'profile.html', 
        friend_requests=friend_requests, 
        friends=friends, 
        username=current_user.username, 
        user_description=current_user.q5
    )
    

@app.route('/events_list')
def events_list():
   return redirect(url_for('events'))

@app.route('/events', methods=['GET'])
def events():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    current_user = User.query.get(user_id)


    # Get the date from the query parameter
    filter_date = request.args.get('event_date')  # Ensure parameter name matches HTML form

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
        else:
            # Retrieve all events if no date is provided
            query = 'SELECT * FROM event'
            cursor.execute(query)
            events = cursor.fetchall()
        
        conn.close()

        # Fetch the list of event IDs that the user has already joined
        joined_events = UserEvent.query.filter_by(user_id=user_id).all()
        joined_event_ids = {event.event_id for event in joined_events}  # Create a set of joined event IDs

        users = User.query.all()
        matches = []

        friends_ids = set()
        friendships = Friendship.query.filter(
            (Friendship.user1_id == current_user.id) | (Friendship.user2_id == current_user.id)
        ).all()

        for friendship in friendships:
            if friendship.user1_id == current_user.id:
                friends_ids.add(friendship.user2_id)
            else:
                friends_ids.add(friendship.user1_id)

        for other_user in users:
            if other_user.id != current_user.id and other_user.id not in friends_ids:
                match_percentage = calculate_match(current_user, other_user)
                matches.append({
                    'username': other_user.username,
                    'match_percentage': match_percentage,
                    'id': other_user.id  # Ensure that 'id' is included here
                })

        matches.sort(key=lambda x: x['match_percentage'], reverse=True)
        return matches



        # Render the template with the filtered events and joined event IDs
        return render_template('event_template.html', events=events, joined_event_ids=joined_event_ids)

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

   # Fetch IDs of all friends
    friends_ids = set()
    friendships = Friendship.query.filter(
        (Friendship.user1_id == current_user.id) | (Friendship.user2_id == current_user.id)
    ).all()
    for friendship in friendships:
        if friendship.user1_id == current_user.id:
            friends_ids.add(friendship.user2_id)
        else:
            friends_ids.add(friendship.user1_id)

    # Exclude current user's own ID and friends' IDs
    for other_user in users:
        if other_user.id != current_user.id and other_user.id not in friends_ids:
            match_percentage = calculate_match(current_user, other_user)
            matches.append({
                'username': other_user.username,
                'match_percentage': match_percentage,
                'id': other_user.id  # Ensure that 'id' is included here
            })

    matches.sort(key=lambda x: x['match_percentage'], reverse=True)
    return matches

    def get_current_user():
        user_id = session.get('user_id')
        if user_id:
            return User.query.get(user_id)
        return None


@app.route('/friends_list/<username>')
def friends_list(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return "User not found.", 404

    matches = get_matches(user)
    # Check existing requests for each match
    for match in matches:
        existing_request = FriendRequest.query.filter_by(sender_id=user.id, receiver_id=match['id']).first()
        if existing_request:
            match['requested'] = True
        else:
            match['requested'] = False
    return render_template('friends_list.html', matches=matches, username=username)



# Route to send friend request
@app.route('/send_friend_request/<int:receiver_id>', methods=['POST'])
def send_friend_request(receiver_id):
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('login'))

    # Check if the current user has already sent a friend request to the receiver
    existing_request = FriendRequest.query.filter_by(sender_id=current_user.id, receiver_id=receiver_id).first()

    # Check if there is a mutual pending friend request
    mutual_request = FriendRequest.query.filter_by(sender_id=receiver_id, receiver_id=current_user.id, status='pending').first()

    if mutual_request:
        # If a mutual request exists, create a friendship
        new_friendship = Friendship(user1_id=current_user.id, user2_id=receiver_id)
        db.session.add(new_friendship)

        # Update both friend requests to 'accepted'
        mutual_request.status = 'accepted'
        if existing_request:
            existing_request.status = 'accepted'
        else:
            # If current user hadn't sent a request, create one and set it as 'accepted'
            existing_request = FriendRequest(sender_id=current_user.id, receiver_id=receiver_id, status='accepted')
            db.session.add(existing_request)

        db.session.commit()
        flash("You are now friends with the user!")
    else:
        # If no mutual request, create a new pending friend request if it doesn't exist already
        if not existing_request:
            new_request = FriendRequest(sender_id=current_user.id, receiver_id=receiver_id, status='pending')
            db.session.add(new_request)
            db.session.commit()
            flash("Friend request sent!")
        else:
            flash("Friend request already sent.")

    return redirect(url_for('friends_list', username=current_user.username))



@app.route('/respond_friend_request/<int:request_id>/<response>')
def respond_friend_request(request_id, response):
    friend_request = FriendRequest.query.get(request_id)
    current_user = get_current_user()  # Assume this function gets the currently logged-in user

    if friend_request and friend_request.receiver_id == current_user.id:
        if response == 'accept':
            friend_request.status = 'accepted'
            db.session.commit()
            # Add to friendships
            new_friendship = Friendship(user1_id=friend_request.sender_id, user2_id=friend_request.receiver_id)
            db.session.add(new_friendship)
            db.session.commit()
            flash("Friend request accepted.")
        elif response == 'decline':
            friend_request.status = 'declined'
            db.session.commit()
            flash("Friend request declined.")

    return redirect(url_for('profile'))



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

def scrape_and_store_events():
    conn = sqlite3.connect(r'instance/users.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event (
        eventid INTEGER PRIMARY KEY,
        title VARCHAR(100),
        date DATE,
        start TIME,
        end TIME,
        dow VARCHAR(20)
    );
    ''')

    url = 'https://usu.edu.au/events/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    events = soup.find_all('div', class_='EventCard-module--EventCard--3dc8c')

    eventsdata = []
    id = 0
    for card in events:
        date_span = card.find('span', class_='EventCard-module--date--d8888')
        date = date_span.get_text(strip=True)
        test1 = date.split("-")
        if len(test1) == 2:
            test2 = test1[1].split("to")
        elif len(test1) == 1:
            test2 = test1[0].split("to")
        d0 = test2[0].split()
        d = d0[0] + " " + d0[1]
        start = d0[2] + " " + d0[3]
        end = test2[1].strip()
        y = 2024
        date_str = f"{d} {y}"
        date_format_in = "%d %b %Y"
        date_obj = datetime.strptime(date_str, date_format_in)
        fdate = date_obj.strftime("%Y-%m-%d")
        time_format_in = "%I:%M %p"
        time_format_out = "%H:%M"

        def convert_time(time_str):
            time_obj = datetime.strptime(time_str, time_format_in)
            return time_obj.strftime(time_format_out)

        fstart = convert_time(start)
        fend = convert_time(end)

        date_obj = datetime.strptime(fdate, "%Y-%m-%d")

        dow = date_obj.strftime("%A")

        title_h3 = card.find('h3', class_='EventCard-module--name--c1353')
        title = title_h3.get_text(strip=True)

        allowed_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

        filtered_characters = []

        for char in title:
            if char in allowed_characters:
                filtered_characters.append(char)

        result = ''.join(filtered_characters)

        id += 1
        sql = '''INSERT OR IGNORE INTO event (eventid, title, date, start, end, dow) 
                VALUES (?, ?, ?, ?, ?, ?);
                '''
        cursor.execute(sql, (id, result, fdate, fstart, fend, dow))

    conn.commit()
    conn.close()

@app.route('/join_event/<int:event_id>', methods=['POST'])
def join_event(event_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    # Check if the user has already joined the event
    existing_event = UserEvent.query.filter_by(user_id=user_id, event_id=event_id).first()
    if existing_event:
        flash('You have already joined this event.')
        return redirect(url_for('events'))

    # Fetch event details from the SQLite database using a raw SQL query
    db_path = os.path.abspath(os.path.join('instance', 'users.db'))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM event WHERE eventid = ?', (event_id,))
    event = cursor.fetchone()
    conn.close()

    if not event:
        return "Event not found", 404

    # Convert date and time
    event_date = datetime.strptime(event[2], "%Y-%m-%d").date()
    start_time = datetime.strptime(event[3], "%H:%M").time()
    end_time = datetime.strptime(event[4], "%H:%M").time()

    # Create a new UserEvent instance
    user_event = UserEvent(
        user_id=user_id,
        event_id=event[0],
        title=event[1],
        date=event_date,
        start=start_time,
        end=end_time,
        dow=event[5]
    )

    # Add and commit to the database
    db.session.add(user_event)
    db.session.commit()

    flash('You have successfully joined the event.')
    return redirect(url_for('events'))








if __name__ == '__main__':
    with app.app_context():
        scrape_and_store_events()
    app.run(host='127.0.0.1', port=5001, debug=True)
