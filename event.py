from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Redirect to the /events route directly
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

if __name__ == '__main__':
    app.run(debug=True)