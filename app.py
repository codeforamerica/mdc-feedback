import requests
import time

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import Survey

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}

    results = Survey.query.all()
    print(results)


    hardcoded_api = 'https://api.typeform.com/v0/form/UYZYtI?key=433dcf9fb24804b47666bf62f83d25dbef2f629d&completed=true'
    if request.method == 'POST':
        print('POST method')
        now = time.ctime(int(time.time()))
        r = requests.get(hardcoded_api)
        r_json = r.json()


        for i in r_json['responses']:

            try:
                # TO DO: Add lang to models.py

                '''
                quiz_id=i['id'],
                list_choice_1=i['answers']['list_7649733_choice'],
                list_choice_2=i['answers']['list_7205097_choice'],
                textfield_1=i['answers']['textfield_7205223'],
                textarea_1=i['answers']['textarea_7205107'],
                textarea_2=i['answers']['textarea_7205102'],
                opinionscale_1=i['answers']['opinionscale_7205022']

                print "start"
                print "{0}, {1}, {2}, {3}, {4}, {5}, {6}".format(quiz_id, list_choice_1, list_choice_2, textfield_1, textarea_1, textarea_2, opinionscale_1)
                print "end"
                '''

                survey = Survey(
                    lang='en',
                    quiz_id=i['id'],
                    list_choice_1=i['answers']['list_7649733_choice'],
                    list_choice_2=i['answers']['list_7205097_choice'],
                    textfield_1=i['answers']['textfield_7205223'],
                    textarea_1=i['answers']['textarea_7205107'],
                    textarea_2=i['answers']['textarea_7205102'],
                    opinionscale_1=i['answers']['opinionscale_7205022']
                )
                db.session.add(survey)
                db.session.commit()

                print "[row committed]"
            except:
                print "[row exception]"
                errors.append("Unable to add item to database.")

            # for j in i['answers']:
            #     print j

    return render_template('index.html', errors=errors, results=results)

if __name__ == '__main__':
    app.run()

