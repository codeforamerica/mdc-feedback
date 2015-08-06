# -*- coding: utf-8 -*-

import datetime
import requests
import json
import pprint

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

json_obj = {}
stats = {}
total = 0.0
sms_total = 0.0
web_en = 0
web_es = 0
sms_en = 0
sms_es = 0

# Get unix timestamp of a week ago
timestamp = datetime.date.today() - datetime.timedelta(7)
unix_time = timestamp.strftime("%s")

API = 'https://api.typeform.com/v0/form/UYZYtI?key='
API_KEY = '433dcf9fb24804b47666bf62f83d25dbef2f629d'

API = API + API_KEY + '&completed=true&since=' + unix_time

response = requests.get(API)
json_result = response.json()

web_completed_responses = int(json_result['stats']['responses']['showing'])

for survey_response in json_result['responses']:
    # Go through each entry in responses, and pull out opinionscale_7205022 / opinionscale_8228843, whichever is not null. Convert to integer.
    try:
        ans = survey_response['answers']['opinionscale_7205022']
        web_en = web_en + 1
    except KeyError:
        try:
            ans = survey_response['answers']['opinionscale_8228843']
            web_es = web_es + 1
        except KeyError:
            # print 'ERROR! one of these opinion scales should show up.'
            pass
    total = total + int(ans)



# TEXTIT API CALLS

'''
Each survey is called a "flow". For now, we will hardcode two particular flows
from textit so we can wrap our heads around how this works.
'''

TEXTIT_UUID_EN = 'cd8cd1b5-ab4c-4c85-b623-9f28c56cc753'
TEXTIT_UUID_ES = 'abc55a5c-2d4a-468f-ae76-a5a1e31865e0'
SMS_KEY = '41a75bc6977c1e0b2b56d53a91a356c7bf47e3e9'
sms_query_date = timestamp.strftime("%Y-%m-%dT%H:%M:%S.000")

SMS_API = 'https://textit.in/api/v1/runs.json?flow_uuid=' + TEXTIT_UUID_ES + ',' + TEXTIT_UUID_EN + '&after=' + sms_query_date

response2 = requests.get(SMS_API, headers={'Authorization': 'Token ' + SMS_KEY})

json_result = response2.json()
sms_total_responses = json_result['count']

obj_completed = [result for result in json_result['results'] if result['completed'] == True]
sms_completed_responses = len(obj_completed)

for obj in obj_completed:
    if obj['flow_uuid'] == TEXTIT_UUID_EN:
        sms_en = sms_en + 1
    else:
        sms_es = sms_es + 1

    # filter for the node ID of the opinion scale,
    # which is 8b04d9e3-9bdb-4b1b-b258-aaa3c7062083
    opinion_node = [result for result in obj['values'] if result['node'] == '8b04d9e3-9bdb-4b1b-b258-aaa3c7062083']
    try:
        sms_total = sms_total + float(opinion_node[0]['value'])
    except IndexError:
        pass

try:
  rating = (total + sms_total) / (web_completed_responses + sms_completed_responses)
except ZeroDivisionError:
  rating = 0
stats['rating'] = "{0:.2f}".format(rating)
stats['new_reviews'] = web_completed_responses + sms_completed_responses

stats['web_en'] = web_en
stats['web_es'] = web_es
stats['sms_en'] = sms_en
stats['sms_es'] = sms_es

sample_graph = {
  "datetime": {
    "data": [
      "2014-01",
      "2014-02",
      "2014-03",
      "2014-04",
      "2014-05",
      "2014-06"
    ]
  },
  "series": [
    {
      "data": [
        71173,
        57624,
        64851,
        60486,
        60500,
        62908
      ]
    }
  ]
}

json_obj['test'] = json.dumps(sample_graph)

@blueprint.route("/", methods=["GET", "POST"])
def home():
    today = datetime.date.today()
    return render_template(
                "public/home.html",
                date=today.strftime('%B %d, %Y'),
                stats=stats,
                json_obj=json_obj
            )

@blueprint.route('/dashboard', methods=['GET', 'POST'])
def survey_index():
    form = {}
    return render_template('dashboard/home.html', form=form)

