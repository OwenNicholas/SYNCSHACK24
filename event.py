import sqlite3
from jinja2 import Environment, FileSystemLoader

db_path = 'instance/users.db'
html_template_path = 'templates/event_template.html'
output_html_path = 'templates/event.html'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('SELECT * FROM event')
events = cursor.fetchall()

conn.close()

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('event_template.html')

html_content = template.render(events=events)

with open(output_html_path, 'w') as file:
    file.write(html_content)

print(f'HTML file generated: {output_html_path}')