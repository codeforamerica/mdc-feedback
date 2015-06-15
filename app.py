import requests
import time

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import Survey

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    errors = []

    hardcoded_api = 'https://api.typeform.com/v0/form/UYZYtI?key=433dcf9fb24804b47666bf62f83d25dbef2f629d&completed=true'
    if request.method == 'POST':
        print('POST method')
        now = time.ctime(int(time.time()))
        r = requests.get(hardcoded_api)
        r_json = r.json()

        for i in r_json['responses']:

            try:
                # TO DO: Add lang to models.py

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
            except:
                errors.append("Unable to add item to database.")

            # for j in i['answers']:
            #     print j

    return render_template('admin.html', errors=errors)

@app.route('/')
def index():
    errors = []
    results = {}

    results = Survey.query.all()

    return render_template('index.html', errors=errors, results=results)

if __name__ == '__main__':
    app.run()

