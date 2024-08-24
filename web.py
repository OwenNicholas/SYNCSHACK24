import requests
from bs4 import BeautifulSoup

url = 'https://usu.edu.au/events/'
response = requests.get(url)
response.raise_for_status() 
soup = BeautifulSoup(response.text, 'html.parser')

events = soup.find_all('div', class_='EventCard-module--EventCard--3dc8c')

eventsdata = []

for card in events:
    date_span = card.find('span', class_='EventCard-module--date--d8888')
    date = date_span.get_text(strip=True) if date_span else 'No date available'
    
    title_h3 = card.find('h3', class_='EventCard-module--name--c1353')
    title = title_h3.get_text(strip=True) if title_h3 else 'No title available'
    
    print(f"Title: {title}")
    print(f"Date: {date}")
    print("-" * 40)