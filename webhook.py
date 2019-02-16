from flask import Flask
import pandas as pd
from flask_assistant import Assistant, ask, tell
import logging
from datetime import datetime, timedelta
from numpy import gradient
from sklearn import linear_model
import math
import random
from flask_socketio import SocketIO
#import person
entries = {}

feelings = {
    0: "very bad",
    1: "bad",
    2: "quite alright",
    3: "good",
    4: "very good"
}

app = Flask(__name__)
assist = Assistant(app, route = '/', project_id = 'daily-refresh-a7879')

@assist.action('feeling')
def respond_feels(feeling):
    if feeling == "Very Good":
        speech = 'That is fantastic news!'
        entries[datetime.today()] = 4

    elif feeling == "Good":
        speech = 'Thats great!'
        entries[datetime.today()] = 3

    elif feeling == 'Fine':
        speech = 'Thank you for telling me.'
        entries[datetime.today()] = 2

    elif feeling == 'Bad':
        speech = 'Thanks for telling me. Adding for {}'
        entries[datetime.today()] = 1

    elif feeling == 'Very Bad':
        speech = 'I am here for you. Adding for {}'
        entries[datetime.today()] = 0

    else:
        speech = "Sorry, I didn't get that. How are you feeling today?"
        return ask(speech)
    for k in entries:
        print(entries[k])

    return ask(speech)

@assist.action('summary')
def give_summary():
    relevant_entries = [entries[k] for k in entries if datetime.now() - k <= timedelta(days = 7)]
    if get_slope(relevant_entries) > 0:
        speech = 'Great job, Your week has gotten better!'
    
    else:
        if(len(relevant_entries) == 0):
            return ask("I have no entries for you. How are you feeling?")

        emo_score = math.ceil(sum(relevant_entries)/len(relevant_entries))
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

        emo_score = math.ceil(sum(relevant_entries)/len(relevant_entries))
        speech = "On average, you have felt {} this month".format((feelings[emo_score]))

    print(speech)
    return tell(speech)

@assist.action('year')
def yearly_summary():
    relevant_entries = [entries[k] for k in entries if datetime.now() - k <= timedelta(days = 365)]
    if get_slope(relevant_entries) > 0:
        speech = 'Great job, Your year has gotten better!'
    
    else:
        if(len(relevant_entries) == 0):
            return ask("I have no entries for you. How are you feeling?")

        emo_score = math.ceil(sum(relevant_entries)/len(relevant_entries))
        speech = "On average, you have felt {} this year.".format((feelings[emo_score]))

    print(speech)
    return tell(speech)
def make_fake_data():
    for i in range(365):
        entries[datetime.today() - timedelta(days = i)] = random.randint(0, 4)

def get_slope(some_list):
    running = []
    for i, item in enumerate(some_list):
        if(i+1 < len(some_list)):
            running.append(some_list[i + 1] - item)
    return sum(running)/len(running)    

if __name__ == '__main__':
    make_fake_data()
    app.run(debug = True)
    logging.getLogger('flask_assistant').setLevel(logging.DEBUG)
