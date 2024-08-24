from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__)

@app.route('/events', methods=['GET'])
def events():
    # Get the date from the query parameter
    filter_date = request.args.get('date')
    
    # Connect to the database
    db_path = os.path.join('instance', 'users.db')
    
    if not os.path.exists(db_path):
        return "Database file not found.", 500
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    if filter_date:
        # Filter events based on the input date
        query = '''
        SELECT * FROM event
        WHERE date = ?
        '''
        cursor.execute(query, (filter_date,))
    else:
        # Retrieve all events if no date is provided
        query = 'SELECT * FROM event'
        cursor.execute(query)
    
    events = cursor.fetchall()
    conn.close()
    
    # Render the template with the filtered events
    return render_template('event.html', events=events)

if __name__ == '__main__':
    app.run(debug=True)