 # -*- coding: utf-8 -*-

import datetime
import requests
import json
import pprint
import pytz

from flask import (
    Blueprint, render_template, request, flash
)
from flask.ext.login import (
    login_required
)
from tzlocal import get_localzone

blueprint = Blueprint(
    "dashboard", __name__,
    template_folder='../templates',
    static_folder="../static"
)

TYPEFORM_API = 'https://api.typeform.com/v0/form/UYZYtI?key='
TYPEFORM_API_KEY = '433dcf9fb24804b47666bf62f83d25dbef2f629d'

TEXTIT_API = 'https://textit.in/api/v1/runs.json?flow_uuid='
TEXTIT_UUID_EN = 'cd8cd1b5-ab4c-4c85-b623-9f28c56cc753'
TEXTIT_UUID_ES = 'abc55a5c-2d4a-468f-ae76-a5a1e31865e0'
TEXTIT_AUTH_KEY = '41a75bc6977c1e0b2b56d53a91a356c7bf47e3e9'


json_obj = {}
stats = {}
total = 0.0
sms_total = 0.0
sms_en = 0
sms_es = 0
surveys_by_date = {}
surveys_date_array = []
surveys_value_array = []

local_tz = get_localzone()

def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt) # .normalize might be unnecessary

def make_typeform_call(timestamp):
    '''
    Takes in the timestamp in unix form
    Returns the JSON of the actual API. Let's just start simple.
    '''
    unix_time = timestamp.strftime("%s")

    API = TYPEFORM_API + TYPEFORM_API_KEY + '&completed=true&since=' + unix_time

    response = requests.get(API)
    json_result = response.json()
    return json_result

def get_typeform_by_meta(json_result):
    web_en = 0
    web_es = 0
    total = 0

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
    return {
        "en": web_en,
        "es": web_es,
        "total": total,
        "completed": int(json_result['stats']['responses']['showing'])
    }

def get_textit_by_meta(json_result):
    sms_en = 0
    sms_es = 0
    sms_total = 0

    obj_completed = [result for result in json_result['results'] if result['completed'] == True]
    sms_completed_responses = len(obj_completed)

    for obj in obj_completed:
        if obj['flow_uuid'] == TEXTIT_UUID_EN:
            sms_en += 1
        else:
            sms_es += 1

        # filter for the node ID of the opinion scale,
        # which is 8b04d9e3-9bdb-4b1b-b258-aaa3c7062083
        opinion_node = [result for result in obj['values'] if result['node'] == '8b04d9e3-9bdb-4b1b-b258-aaa3c7062083']
        try:
            sms_total = sms_total + float(opinion_node[0]['value'])
        except IndexError:
            pass

    return {
        "en": sms_en,
        "es": sms_es,
        "total": sms_total,
        "completed": sms_completed_responses
    }

def get_typeform_by_date(json_result, surveys_by_date):
    for survey_response in json_result['responses']:

        # Iterate through the metadata. In the API there is a date_land field in the format of "2015-08-04 22:13:38". Parse this into our surveys_by_date array and increase these by 1.
        date_object = datetime.datetime.strptime(
                        survey_response['metadata']['date_submit'],
                        '%Y-%m-%d %H:%M:%S'
                        )
        surveys_by_date[date_object.strftime("%m-%d")] += 1
    return surveys_by_date

def get_textit_by_date(json_result, surveys_by_date):
    obj_completed = [result for result in json_result['results'] if result['completed'] == True]

    for obj in obj_completed:
        # obj['created_on'] "2015-08-03T16:51:48.661Z"
        date_object = datetime.datetime.strptime(
                        obj['created_on'],
                        '%Y-%m-%dT%H:%M:%S.%fZ'
                        )

        # http://stackoverflow.com/questions/4563272/how-to-convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-stand
        date_object = utc_to_local(date_object)
        try:
            surveys_by_date[date_object.strftime("%m-%d")] += 1
        except KeyError:
            pass

    return surveys_by_date

def make_textit_call(timestamp):
    '''
    Takes in the timestamp in unix form
    Returns the JSON of the actual API.
    '''
    sms_query_date = timestamp.strftime("%Y-%m-%dT%H:%M:%S.000")

    SMS_API = TEXTIT_API + TEXTIT_UUID_ES + ',' + TEXTIT_UUID_EN + '&after=' + sms_query_date

    response2 = requests.get(SMS_API, headers={'Authorization': 'Token ' + TEXTIT_AUTH_KEY})

    json_result = response2.json()
    return json_result

for i in range(7, -1, -1):
    time_i = (datetime.date.today() - datetime.timedelta(i))
    date_index = time_i.strftime("%m-%d")
    surveys_by_date[date_index] = 0
    surveys_date_array.append(date_index)

# Get unix timestamp of a week ago
timestamp = datetime.date.today() - datetime.timedelta(7)
json_result = make_typeform_call(timestamp)
# print get_typeform_by_meta(json_result)
# print get_typeform_by_date(json_result, surveys_by_date)

web_meta = get_typeform_by_meta(json_result)
web_date = get_typeform_by_date(json_result, surveys_by_date)

# TEXTIT API CALLS
'''
Each survey is called a "flow". For now, we will hardcode two particular flows
from textit so we can wrap our heads around how this works.
'''
sms_result = make_textit_call(timestamp)
sms_meta = get_textit_by_meta(sms_result)
sms_date = get_textit_by_date(sms_result, surveys_by_date)

# ANALYTICS CODE

try:
  rating = (web_meta['total'] + sms_meta['total']) / (web_meta['completed'] + sms_meta['completed'])
except ZeroDivisionError:
  rating = 0

for i in range(7, -1, -1):
    time_i = (datetime.date.today() - datetime.timedelta(i))
    date_index = time_i.strftime("%m-%d")
    surveys_value_array.append(surveys_by_date[date_index])


dashboard_collection = [
    {
        "id": "graph",
        "title": "Surveys Submitted - Last 7 Days",
        "data": {
            "new_reviews": web_meta['completed'] + sms_meta['completed'],
            "graph": {
                "datetime": {
                    "data": surveys_date_array
                },
                "series": [
                    {
                        "data": surveys_value_array
                    }
                ]
            }
        }
    },
    {
        "title": "Satisfaction Rating - Last 7 Days",
        "data": "{0:.2f}".format(rating)
    },
    {
        "title": "Survey Type - Last 7 Days",
        "data": {
            "web_en": web_meta['en'],
            "web_es": web_meta['es'],
            "sms_en": sms_meta['en'],
            "sms_es": sms_meta['es']
        },
        "labels": {
            "web_en": "Web (EN)",
            "web_es": "Web (ES)",
            "sms_en": "SMS (EN)",
            "sms_es": "SMS (ES)"
        }
    }
]

json_obj['test'] = json.dumps(dashboard_obj[0]['data']['graph'])
json_obj['surveys_type'] = json.dumps(dashboard_obj[2])

@blueprint.route("/", methods=["GET", "POST"])
def home():
    today = datetime.date.today()
    return render_template(
                "public/home.html",
                date=today.strftime('%B %d, %Y'),
                stats=stats,
                json_obj=json_obj,
                dash_obj=dashboard_collection,
                title='Dashboard'	#sophia added
            )

@blueprint.route('/dashboard', methods=['GET', 'POST'])
def survey_index():
    form = {}
    return render_template('dashboard/home.html', form=form)

