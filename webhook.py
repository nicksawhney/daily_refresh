from flask import Flask
import pandas as pd
from flask_assistant import Assistant, ask, tell
import logging

app = Flask(__name__)
assist = Assistant(app, route = '/')

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
    if feeling == "":
        speech = "Sorry, I didn't get that."

    elif feeling == "Very Good":
        speech = 'That is fantastic news!'

    elif feeling == "Good":
        speech = 'Thats great!'

    elif feeling == 'Fine':
        speech = 'Thank you for telling me'

    elif feeling == 'Bad':
        speech = 'Thanks for telling me'

    elif feeling == 'Very Bad':
        speech = 'I am here for you'

    return ask(speech)




if __name__ == '__main__':
    app.run(debug = True)
    logging.getLogger('flask_assistant').setLevel(logging.DEBUG)
