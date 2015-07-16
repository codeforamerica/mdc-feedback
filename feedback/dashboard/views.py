# -*- coding: utf-8 -*-

import datetime
import requests
import json

from flask import (
    Blueprint, render_template, request, flash
)
from flask.ext.login import (
    login_required
)

blueprint = Blueprint(
    "dashboard", __name__,
    template_folder='../templates',
    static_folder="../static"
)

stats = {}

# Get unix timestamp of a week ago
timestamp = datetime.date.today() - datetime.timedelta(7)
unix_time = timestamp.strftime("%s")


API = 'https://api.typeform.com/v0/form/UYZYtI?key='
API_KEY = '433dcf9fb24804b47666bf62f83d25dbef2f629d'

API = API + API_KEY + '&completed=true&since=' + unix_time

response = requests.get(API)
json = response.json()
stats['new_reviews'] = json['stats']['responses']['showing']

total = 0.0
for survey_response in json['responses']:
    # Go through each entry in responses, and pull out opinionscale_7205022 / opinionscale_8228843, whichever is not null. Convert to integer.
    try:
        ans = survey_response['answers']['opinionscale_7205022']
    except KeyError:
        try:
            ans = survey_response['answers']['opinionscale_8228843']
        except KeyError:
            print 'ERROR! one of these opinion scales should show up.'
    total = total + int(ans)
stats['rating'] = total / len(json['responses'])

@blueprint.route("/", methods=["GET", "POST"])
def home():
    return render_template("public/home.html", stats=stats)

@blueprint.route('/dashboard', methods=['GET', 'POST'])
def survey_index():
    form = {}
    return render_template('dashboard/home.html', form=form)

