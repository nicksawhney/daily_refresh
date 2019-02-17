from flask import Flask
import pandas as pd
from flask_assistant import Assistant, ask, tell
import logging
from datetime import datetime, timedelta
from numpy import gradient
from sklearn import linear_model
import math
import random
from flask_socketio import SocketIO, emit
import json
from statistics import median
import csv

entries = {}
feelings = {
    0: "very bad",
    1: "bad",
    2: "quite alright",
    3: "good",
    4: "very good"
}

#initialize server
app = Flask(__name__)
assist = Assistant(app, route = '/', project_id = 'daily-refresh-a7879')
socketio = SocketIO(app)

#respond to user feeling and log feeling and time
@assist.action('feeling')
def respond_feels(feeling):
    if feeling == "Very Good":
        speech = 'That is fantastic news!'
        entries[datetime.today()] = 4

    elif feeling == "Good":
        speech = 'Thats great!'
        entries[datetime.today()] = 3

    elif feeling == 'Fine':
        speech = 'Thanks for telling me.'
        entries[datetime.today()] = 2

    elif feeling == 'Bad':
        speech = 'Thank you for telling me'
        entries[datetime.today()] = 1

    elif feeling == 'Very Bad':
        speech = 'Thank you for telling me.'
        entries[datetime.today()] = 0

    else:
        speech = "Sorry, I didn't get that. How are you feeling today?"
        return ask(speech)

    return ask(speech)

#below are various summaries of mental health. If there has been an improvement, user is notified of progress, otherwise median feeling is given
@assist.action('summary')
def give_summary():
    relevant_entries = [entries[k] for k in entries if datetime.now() - k <= timedelta(days = 7)]
    if get_slope(relevant_entries) > 0:
        speech = 'Great job, Your week has gotten better!'
    
    else:
        if(len(relevant_entries) == 0):
            return ask("I have no entries for you. How are you feeling?")

        emo_score = median(relevant_entries)
        speech = "On average, you have felt {} this week".format((feelings[emo_score]))

    print(speech)
    return tell(speech)

@assist.action('month')
def montly_summary():
    relevant_entries = [entries[k] for k in entries if datetime.now() - k <= timedelta(days = 30)]
    if get_slope(relevant_entries) > 0:
        speech = 'Great job, Your month has gotten better!'
    
    else:
        if(len(relevant_entries) == 0):
            return ask("I have no entries for you. How are you feeling?")

        emo_score = median(relevant_entries)
        speech = "On average, you have felt {} this month".format((feelings[emo_score]))

    return tell(speech)

@assist.action('year')
def yearly_summary():
    relevant_entries = [entries[k] for k in entries if datetime.now() - k <= timedelta(days = 365)]
    if get_slope(relevant_entries) > 0:
        speech = 'Great job, Your year has gotten better!'
    
    else:
        if(len(relevant_entries) == 0):
            return ask("I have no entries for you. How are you feeling?")

        emo_score = median(relevant_entries)
        speech = "On average, you have felt {} this year.".format((feelings[emo_score]))

    print(speech)
    return tell(speech)

@assist.action('two month')
def yearly_summary():
    relevant_entries = [entries[k] for k in entries if datetime.now() - k <= timedelta(days = 60)]
    if get_slope(relevant_entries) > 0:
        speech = 'Great job, You\'ve felt better over the last 2 months!'
    
    else:
        if(len(relevant_entries) == 0):
            return ask("I have no entries for you. How are you feeling?")

        emo_score = median(relevant_entries)
        speech = "On average, you have felt {} this and last month.".format((feelings[emo_score]))

    print(speech)
    return tell(speech)

@assist.action('two week')
def yearly_summary():
    relevant_entries = [entries[k] for k in entries if datetime.now() - k <= timedelta(days = 14)]
    if get_slope(relevant_entries) > 0:
        speech = 'Great job, You\'ve felt better over the last 2 weeks!'
    
    else:
        if(len(relevant_entries) == 0):
            return ask("I have no entries for you. How are you feeling?")

        emo_score = median(relevant_entries)
        speech = "On average, you have felt {} this year.".format((feelings[emo_score]))

    print(speech)
    return tell(speech)

#for HackNYU demo
def make_demo_data():
    for i in range(365):
        entries[datetime.today() - timedelta(days = i)] = random.randint(0, 4)

#For detecting improvement
def get_slope(some_list):
    running = []
    for i, item in enumerate(some_list):
        if(i+1 < len(some_list)):
            running.append(some_list[i + 1] - item)
    return sum(running)/len(running)    

#Send data to frontend website
@socketio.on('connect')
def send_data():
    emit('health tracking data', {str(k.date()): v for k, v in entries.items()})


if __name__ == '__main__':
    make_demo_data()
    socketio.run(app, debug = True)
    logging.getLogger('flask_assistant').setLevel(logging.DEBUG)

    #TODO: individual users, frontend login, automatic emailing of data to therapist
