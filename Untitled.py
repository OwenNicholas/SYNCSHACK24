#!/usr/bin/env python
# coding: utf-8

# In[9]:


import requests
from bs4 import BeautifulSoup

# URL of the page you want to scrape
base_url = 'https://usu.edu.au/events/'

# Send HTTP request to the URL
response = requests.get(url) 

def get_html(base_url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.text
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'An error occurred: {err}')


if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')



# In[16]:


events = soup.find_all('div', class_='EventCard-module--EventCard--3dc8c')
events


# In[8]:


# Function to extract event details
def get_event_details(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    # Find all event card divs
    event_cards = soup.find_all('div', class_='EventCard-module--EventCard--3dc8c')
    
    event_details = []
    
    for card in event_cards:
        # Find the link within the event card
        link = card.find('a', class_='EventCard-module--link--6562a')
        if link and 'href' in link.attrs:
            # Construct the full URL for the event detail page
            event_url = base_url + link['href']
            event_html = get_html(event_url)
            event_soup = BeautifulSoup(event_html, 'html.parser')
            
            # Extract the event date and other details from the event detail page
            # You will need to adjust the selectors based on the actual HTML structure
            date = event_soup.find('p', class_='event-date').text.strip()
            name = event_soup.find('h1', class_='event-name').text.strip()
            # ... other details
            
            event_details.append({'name': name, 'date': date})
    
    return event_details

# Main function to scrape the events
def scrape_events():
    main_page_html = get_html(base_url + '/events/')
    if main_page_html:
        events = get_event_details(main_page_html)
        # Do something with the extracted event details
        # For example, print them or save to a file
        for event in events:
            print(event)

# Run the scraper
scrape_events()


# In[13]:


#response.text
soup


# In[14]:


{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import requests\n",
    "from bs4 import BeautifulSoup\n",
    "\n",
    "url = 'https://usu.edu.au/events/'\n",
    "response = requests.get(url)\n",
    "response.raise_for_status() \n",
    "soup = BeautifulSoup(response.text, 'html.parser')\n",
    "\n",
    "# Find all <div> elements with class 'event'\n",
    "events = soup.find_all('div', class_='EventCard-module--EventCard--3dc8c')\n",
    "\n",
    "# Print the complete HTML of each event\n",
    "for event in events:\n",
    "    print(event.prettify())\n",
    "    print(\"-\" * 100)"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}


# In[31]:


import pandas as pd 
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
    
    
  
    eventsdata.append({'title': title, 'date': date})
df = pd.DataFrame(eventsdata)
df
     


# In[27]:


import pandas as pd   
eventsdata.append({'title': title, 'date': date})
df = pd.DataFrame(eventsdata)
df


# In[37]:


#Importing relevant packages/libraries for the analysis
import pandas as pd
get_ipython().system('pip install geopandas')
get_ipython().system('pip install geoalchemy2')
import geopandas as gpd
from shapely.geometry import Point, Polygon, MultiPolygon
from geoalchemy2 import Geometry, WKTElement
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
get_ipython().system('pip install psycopg2-binary')
import psycopg2
import psycopg2.extras
import json
import os
import pandas as pd

#Setting up & establishing Postgres connection
credentials = "Credentials.json"

def pgconnect(credential_filepath, db_schema="public"):
    with open(credential_filepath) as f:
        db_conn_dict = json.load(f)
        host       = db_conn_dict['host']
        db_user    = db_conn_dict['user']
        db_pw      = db_conn_dict['password']
        default_db = db_conn_dict['user']
        port       = db_conn_dict['port']
        try:
            db = create_engine(f'postgresql+psycopg2://{db_user}:{db_pw}@{host}:{port}/{default_db}', echo=False)
            conn = db.connect()
            print('Connected successfully.')
        except Exception as e:
            print("Unable to connect to the database.")
            print(e)
            db, conn = None, None
        return db,conn

def query(conn, sqlcmd, args=None, df=True):
    result = pd.DataFrame() if df else None
    try:
        if df:
            result = pd.read_sql_query(sqlcmd, conn, params=args)
        else:
            result = conn.execute(text(sqlcmd), args).fetchall()
            result = result[0] if len(result) == 1 else result
    except Exception as e:
        print("Error encountered: ", e, sep='\n')
    return result


# In[36]:


db, conn = pgconnect(credentials)


# In[41]:


df.to_sql("events", conn, if_exists='append', index=False)

