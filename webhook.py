from flask import Flask
import pandas as pd
from flask_assistant import Assistant, ask, tell
import logging
from datetime import datetime, timedelta
from numpy import gradient
from sklearn import linear_model
#import person
entries = {}

feelings = {
    0: "Very Bad",
    1: "Bad",
    2: "Fine",
    3: "Good",
    4: "Very Good"
}

app = Flask(__name__)
assist = Assistant(app, route = '/', project_id = 'daily-refresh-a7879')

@assist.action('greeting')
def greet_and_start():
    speech = "Hey! Are you male or female?"
    return ask(speech)

@assist.action('give-gender')
def ask_for_color(gender):
    if gender == 'male':
        gender_msg = 'sup bro'
    elif gender == 'female':
        gender_msg = 'haay gurl'
    else:
        gender_msg = 'waddup fam'
    speech = gender_msg + ' What\'s your favorite color?'
    return ask(speech)

@assist.action('give-color', mapping = {'color': 'sys.color'})
def ask_for_seasin(color):
    speech = "Ok, {} is an okay color I guess".format(color)
    return ask(speech)

@assist.action('feeling')
def respond_feels(feeling):
    if feeling == "Very Good":
        speech = 'That is fantastic news!'
        entries[datetime.today()] = 4

    elif feeling == "Good":
        speech = 'Thats great! Adding for {}'.format(datetime.today())
        entries[datetime.today()] = 3

    elif feeling == 'Fine':
        speech = 'Thank you for telling me. Adding for {}'.format(datetime.today())
        entries[datetime.today()] = 2

    elif feeling == 'Bad':
        speech = 'Thanks for telling me. Adding for {}'.format(datetime.today())
        entries[datetime.today()] = 1

    elif feeling == 'Very Bad':
        speech = 'I am here for you. Adding for {}'.format(datetime.today())
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
    try:
        emo_score = ceil(sum(relevant_entries)/len(relevant_entries))
    except(e):
        print(e)
        return ask("I don't have any entries for you. How are you feeling?")

    if get_slope(relevant_entries) > 0:
        speech = 'Great job, Your week has gotten better!'
    
    else:
        speech = "On average, you have felt {} this week".format(feelings[emo_score])

    print(speech)
    return tell(speech)

def make_fake_data():
    return

def get_slope(some_list):
    running = []
    for i, item in enumerate(some_list):
        if(i+1 < len(some_list)):
            running.append(some_list[i + 1] - item)
    return mean(item)    

if __name__ == '__main__':
    app.run(debug = True)
    logging.getLogger('flask_assistant').setLevel(logging.DEBUG)
