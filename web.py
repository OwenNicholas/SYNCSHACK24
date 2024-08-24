import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3

conn = sqlite3.connect(r'instance\users.db')
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
    d = d0[0] + " "+ d0[1]
    start = d0[2] + " "+ d0[3]
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
    #id
    #title
    #fdate
    #fstart
    #fend
    #dow
    id +=1
    sql = '''INSERT OR IGNORE INTO event (eventid, title, date, start, end, dow) 
            VALUES (?, ?, ?, ?, ?, ?);
            '''
    cursor.execute(sql, (id,title,fdate, fstart, fend,dow ))


    print(id)
    print(f"Title: {title}")
    print(fdate)  
    print(fstart) 
    print(fend)
    print(dow)
    print("-" * 40)
conn.commit()
conn.close()