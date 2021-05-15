from __future__ import print_function
import streamlit as st
import pandas as pd
import numpy as np
import time 
import schedule
import datetime
from datetime import datetime
import random
import pytz
IST = pytz.timezone('Asia/Kolkata')
import requests, json
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from newsapi import NewsApiClient
import streamlit.components.v1 as components
from credentials import weather_key, news_api, task_list_key

st.title("Smart Mirror")


"""
Hello there! What would you like to do today?
"""
st.info("Open Sidebar")
weather = st.sidebar.button('Show weather')
tasks = st.sidebar.button("Schedule")
songs = st.sidebar.button("Random Trap songs YouTube")
worktravel = st.sidebar.button("Estimated travel time to work")
news = st.sidebar.button("News")


def weatherr():
	api_key = credentials.weather_key
	base_url = "http://api.openweathermap.org/data/2.5/weather?"
	city_name = "zirakpur"
	complete_url = base_url + "appid=" + api_key + "&q=" + city_name
	response = requests.get(complete_url)
	x = response.json()
	if x["cod"] != "404":
		y = x["main"]
		current_temperature = y["temp"]-273.15
		current_pressure = y["pressure"]
		current_humidiy = y["humidity"]
		z = x["weather"]
		weather_description = z[0]["description"]

		return(current_temperature,current_pressure,current_humidiy,weather_description)

	else:
		return("City Not Found")
def taskss():
	SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
	creds = None
	if os.path.exists('Google_calendar_events.json'):
		creds = Credentials.from_authorized_user_file('Google_calendar_events.json', SCOPES)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		with open('Google_calendar_events.json', 'w') as token:
			token.write(creds.to_json())

	service = build('calendar', 'v3', credentials=creds)
	now = datetime.datetime.utcnow().isoformat() + 'Z'
	events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
	events = events_result.get('items', [])
	list1 = []
	if not events:
		st.balloons()
		return "No upcoming calendar events found"
	for event in events:
		start = event['start'].get('dateTime', event['start'].get('date'))
		new_row = {'Creator':event['creator']['email'],'Start':start, 'Summary':event['summary']}
		list1.append(new_row)
		new_row = {}
	df = pd.DataFrame(list1)
	
	return df





def taskss1():
	SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']
	creds = None
	if os.path.exists('token.json'):
		creds = Credentials.from_authorized_user_file('token.json', SCOPES)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
        		'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		with open('token.json', 'w') as token:
			token.write(creds.to_json())
	service = build('tasks', 'v1', credentials=creds)
	results = service.tasks().list(credentials.task_list_key,maxResults=10).execute()
	items = results.get('items', [])
	if not items:
		return 'No tasks found.'
	else:
		task_list = []
		for item in items:
			task_list.append(item['title'])
		df1 = pd.DataFrame(task_list,columns = ['Task List'])
		return df1


def worktravell():
	url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=Vancouver+BC|Seattle&destinations=San+Francisco|Victoria+BC&mode=bicycling&language=fr-FR&key=AIzaSyBhZy09wLTrHDuWkoKoYgw5Htmx0iFYbwA'
	r = requests.get(url)
	x = r.json()
	return x

def newss():
	newsapi = NewsApiClient(credentials.news_api)
	top_headlines = newsapi.get_top_headlines(language='en',
                                          country='in',page_size=10)
	news_list = []
	for i in range(10):
		news_list.append(top_headlines['articles'][i]['title'])
	df_news = pd.DataFrame(news_list,columns = ['Top News'])
	
	return df_news
	
def songss():
	links = ['https://www.youtube.com/watch?v=s8XIgR5OGJc', 'https://www.youtube.com/watch?v=knfrxj0T5NY', 'https://www.youtube.com/watch?v=T7K0pZ9tGi4', 'https://www.youtube.com/watch?v=pVLmZMjxfjw', 'https://www.youtube.com/watch?v=ntLop32pYd0', 'https://www.youtube.com/watch?v=mKzLoZFz8PE', 'https://www.youtube.com/watch?v=0t2tjNqGyJI', 'https://www.youtube.com/watch?v=5hEh9LiSzow', ' https://www.youtube.com/watch?v=vZv9-TWdBJM', ' https://www.youtube.com/watch?v=WIXjHt8KmUc', ' https://www.youtube.com/watch?v=DArzZ3RvejU', ' https://www.youtube.com/watch?v=qK_NeRZOdq4', ' https://www.youtube.com/watch?v=v8B5AOljhsY', ' https://www.youtube.com/watch?v=KlL4xXwRF9U', ' https://www.youtube.com/watch?v=IQTzlGLvCAU', ' https://www.youtube.com/watch?v=qo6ygYSxwEY', ' https://www.youtube.com/watch?v=kwW0IAkwIWc', ' https://www.youtube.com/watch?v=9PB30JUOncw', ' https://www.youtube.com/watch?v=mIUKGKwBRk8', ' https://www.youtube.com/watch?v=I8mS8Pfgros', ' https://www.youtube.com/watch?v=3_-a9nVZYjk', ' https://www.youtube.com/watch?v=aSJpnjmqGkY', ' https://www.youtube.com/watch?v=LdQjndOvNn4', ' https://www.youtube.com/watch?v=BsGnMpSVixg', ' https://www.youtube.com/watch?v=Ewr86bQB8Lc', ' https://www.youtube.com/watch?v=vBdnfyfBSKg', ' https://www.youtube.com/watch?v=Vyzi-7N58ww', ' https://www.youtube.com/watch?v=kfE0y1IV8Bc', ' https://www.youtube.com/watch?v=mBHTXQo65p8', ' https://www.youtube.com/watch?v=Obt-vLEJ8jo', ' https://www.youtube.com/watch?v=gl4PNq6A4BU', ' https://www.youtube.com/watch?v=GHC8Hwq9Eag', ' https://www.youtube.com/watch?v=huxX0DmElNU', ' https://www.youtube.com/watch?v=S-l6a34mwWw', ' https://www.youtube.com/watch?v=i33DB6R8YUY', ' https://www.youtube.com/watch?v=-mSRraXCY9w', ' https://www.youtube.com/watch?v=2BkWNqWvFHs', ' https://www.youtube.com/watch?v=U8T6wocw4so', ' https://www.youtube.com/watch?v=-9T5fLmn7rY', ' https://www.youtube.com/watch?v=Axq1FHwFMrQ', ' https://www.youtube.com/watch?v=PMUt0lShZfs', ' https://www.youtube.com/watch?v=o5ENzs8Czm0', ' https://www.youtube.com/watch?v=EZt6mZ-Te1U', ' https://www.youtube.com/watch?v=vPxf8m93GgY', ' https://www.youtube.com/watch?v=fHYA3x9p1hk', ' https://www.youtube.com/watch?v=xlDLd8MBkeE', ' https://www.youtube.com/watch?v=IT_c3fFW3VM', ' https://www.youtube.com/watch?v=Fw0R0b2r6pE', ' https://www.youtube.com/watch?v=DhCp22tIiTc', ' https://www.youtube.com/watch?v=hf4IxNNiqbU', ' https://www.youtube.com/watch?v=ktw8hcSq2mc', ' https://www.youtube.com/watch?v=9gZfHu3sdGY', ' https://www.youtube.com/watch?v=jD0asf_uxKA', ' https://www.youtube.com/watch?v=a5PwMONNGMw', ' https://www.youtube.com/watch?v=czd0Er-_qI8', ' https://www.youtube.com/watch?v=HRRruUdE-9o', ' https://www.youtube.com/watch?v=6zW5reS2rBI', ' https://www.youtube.com/watch?v=QcTRc0biGwo', ' https://www.youtube.com/watch?v=kho6vC6S3kY', ' https://www.youtube.com/watch?v=6WbZIoCtBmk', ' https://www.youtube.com/watch?v=PPMW_355CUs', ' https://www.youtube.com/watch?v=YfRLJQlpMNw', ' https://www.youtube.com/watch?v=Zp2fz99lIAs', ' https://www.youtube.com/watch?v=GnQcMBzhr8E', ' https://www.youtube.com/watch?v=ugpvZ61CnD8', ' https://www.youtube.com/watch?v=oz6kKB8wlj8', ' https://www.youtube.com/watch?v=M2hW6jgomwo', ' https://www.youtube.com/watch?v=jg5UfYCnmO0', ' https://www.youtube.com/watch?v=18obFY29_T8', ' https://www.youtube.com/watch?v=xXvJuVcI5mU', ' https://www.youtube.com/watch?v=Kx1QIlGmhPo', ' https://www.youtube.com/watch?v=IX_L9RWjU_8', ' https://www.youtube.com/watch?v=1C48SaP4FMc', ' https://www.youtube.com/watch?v=zUueYq54Foc', ' https://www.youtube.com/watch?v=d-1csddl0VU', ' https://www.youtube.com/watch?v=FJWRtYPzHy0', ' https://www.youtube.com/watch?v=6xTr5S88pk8', ' https://www.youtube.com/watch?v=DRmHjDzVbRs', ' https://www.youtube.com/watch?v=3t_eU3tdy2g', ' https://www.youtube.com/watch?v=pxR2A7NApYI', ' https://www.youtube.com/watch?v=e7nkA7Ue5yg', ' https://www.youtube.com/watch?v=PV737QlqwLA', ' https://www.youtube.com/watch?v=tyrUaI4KBRk', ' https://www.youtube.com/watch?v=EmI6b8xFSX4', ' https://www.youtube.com/watch?v=aho6XmpSgk4', ' https://www.youtube.com/watch?v=dbTFGcknEcM', ' https://www.youtube.com/watch?v=u7cy4RFsyM8', ' https://www.youtube.com/watch?v=-JWewEsf-X0', ' https://www.youtube.com/watch?v=zlbSFU1UCcQ', ' https://www.youtube.com/watch?v=MOCUaLO__kw', ' https://www.youtube.com/watch?v=prLgYc1gRm0', ' https://www.youtube.com/watch?v=PJ8IBPpzToc', ' https://www.youtube.com/watch?v=i-t6TW0d1Ag']
	random_link = random.choice(links)
	return random_link

weatherrr = weatherr()
tasksss = taskss()
taskssss = taskss1()
worktravelll = worktravell()
newsss = newss()
songsss = songss()


if weather:
	b = st.empty()
	c = st.empty()

	st.write((" Temperature (in celcius unit) = " +
                    str(weatherrr[0])))
	st.write(("Atmospheric Pressure (in hPa unit) = " +
                    str(weatherrr[1])))
	st.write(("Humidity (in %) = " +
                    str(weatherrr[2])))
	st.write(("Description = " +
                    str(weatherrr[3])))

	while True:
		e = datetime.datetime.now()
		b.text( "Today's date:  = %s/%s/%s" % (e.day, e.month, e.year))
		c.text("The time is now: = %s:%s:%s" % (e.hour, e.minute, e.second))
		time.sleep(1)
		if tasks or songs or worktravel:
			break

if tasks:
	tasksss
	taskssss
		
if songs:
	url = str(songsss)
	url = url.replace(" ","")
	st.video(url)

if worktravel:
	worktravelll

if news:
	newsss


