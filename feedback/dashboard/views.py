 # -*- coding: utf-8 -*-

import datetime
import json
import pytz

from flask import (
    Blueprint, render_template
)
from tzlocal import get_localzone

from feedback.dashboard.vendorsurveys import (
    make_typeform_call, make_textit_call, parse_typeform,
    get_typeform_by_meta
)

from feedback.dashboard.permits import (
    api_health, get_lifespan, get_avg_cost,
    get_permit_types,
    get_master_permit_counts
)

blueprint = Blueprint(
    "dashboard", __name__,
    template_folder='../templates',
    static_folder="../static"
)

TEXTIT_UUID_EN = '920cec13-ffc0-4fe9-92c3-1cced2073498'
TEXTIT_UUID_OPINION = '53249739-7b72-43c2-9463-e4cd4963a408'


json_obj = {}
stats = {}
total = 0.0
sms_total = 0.0
sms_en = 0
sms_es = 0
surveys_by_date = {}
surveys_date_array = []
surveys_value_array = []

survey_table = []

local_tz = get_localzone()


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)  # .normalize might be unnecessary


def parse_textit(survey_table, json_result):
    '''
    Take the textit API result and do ETLs to get
    the responses in an easy to digest format.
    Returns an object:
        survey_table
    '''

    obj_completed = [result for result in json_result['results'] if result['completed']]
    for obj in obj_completed:

        iter = {}
        values_array = obj['values']
        for value in values_array:
            iter[value['label']] = {'category': value['category'], 'text': value['text']}

        iter_obj = {
            'id': 'SMS-' + str(obj['run']),
            'method': 'sms',
            'firsttime': iter['First Time']['category'],
            'getdone': iter['Get it Done']['text'],
            'role': iter['Role']['text'],
            'rating': iter['Experience Rating']['text'],
            'improvement': iter['Improvement']['text'],
            'bestworst': iter['Best and Worst']['text'],
            'followup': iter['Followup Permission']['category'],
            'morecomments': iter['Comments']['text']
        }

        temp = obj['modified_on']
        temp = datetime.datetime.strptime(temp, '%Y-%m-%dT%H:%M:%S.%fZ')
        date_object = utc_to_local(temp)
        iter_obj['date'] = date_object.strftime("%Y-%m-%d %H:%M:%S")

        if obj['flow_uuid'] == TEXTIT_UUID_EN:
            iter_obj['lang'] = 'en'
        else:
            iter_obj['lang'] = 'es'

        try:
            iter_obj['purpose'] = iter['Purpose']['text']
        except KeyError:
            iter_obj['purpose'] = ''

        survey_table.append(iter_obj)

    return survey_table


def get_textit_by_meta(json_result):
    sms_en = 0
    sms_es = 0
    sms_total = 0

    obj_completed = [result for result in json_result['results'] if result['completed']]
    sms_completed_responses = len(obj_completed)

    for obj in obj_completed:
        if obj['flow_uuid'] == TEXTIT_UUID_EN:
            sms_en += 1
        else:
            sms_es += 1

        # filter for the node ID of the opinion scale,
        # which is 0a77d0af-2685-4d8d-b4be-732e376f2f85
        values_array = obj['values']
        # print values_array
        iter = {}

        for value in values_array:
            iter[value['label']] = {'category': value['category'], 'text': value['text']}
            # print value['label'], '/', value['category'], '/', value['text']

            if value['node'] == TEXTIT_UUID_OPINION and value['category'] == '1 - 7':
                try:
                    sms_total = sms_total + float(value['value'])
                except IndexError:
                    pass
        # print iter

    return {
        "en": sms_en,
        "es": sms_es,
        "total": sms_total,
        "completed": sms_completed_responses
    }


def get_typeform_by_date(json_result, surveys_by_date):
    for survey_response in json_result['responses']:
        # Iterate through the metadata. In the API there is a date_land field in the format of "2015-08-04 22:13:38". Parse this into our surveys_by_date array and increase these by 1.
        date_object = datetime.datetime.strptime(survey_response['metadata']['date_submit'], '%Y-%m-%d %H:%M:%S')
        surveys_by_date[date_object.strftime("%m-%d")] += 1
    return surveys_by_date


def get_textit_by_date(json_result, surveys_by_date):
    for result in json_result['results']:
        if result['completed']:
            obj = result['modified_on']
            obj = datetime.datetime.strptime(obj, '%Y-%m-%dT%H:%M:%S.%fZ')
            date_object = utc_to_local(obj)
            try:
                surveys_by_date[date_object.strftime("%m-%d")] += 1
            except KeyError:
                pass
    return surveys_by_date


for i in range(7, -1, -1):
    time_i = (datetime.date.today() - datetime.timedelta(i))
    date_index = time_i.strftime("%m-%d")
    surveys_by_date[date_index] = 0
    surveys_date_array.append(date_index)

# Get unix timestamp of a week ago
timestamp = datetime.date.today() - datetime.timedelta(7)
json_result = make_typeform_call(timestamp)
survey_table = parse_typeform(survey_table, json_result)

web_meta = get_typeform_by_meta(json_result)
web_date = get_typeform_by_date(json_result, surveys_by_date)

# TEXTIT API CALLS
'''
Each survey is called a "flow". For now, we will hardcode two particular flows
from textit so we can wrap our heads around how this works.
'''
sms_result = make_textit_call(timestamp)
survey_table = parse_textit(survey_table, sms_result)

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
    },
    {
        "title": "Average time from application date to permit issuance, Commercial Permits, Last 30 Days",
        "data": get_lifespan('c')
    },
    {
        "title": "Average time from application date to permit issuance, Residential Permits, Last 30 Days",
        "data": get_lifespan('r')
    },
    {
        "title": "Average time from application date to permit issuance, Owner/Builder Permits, Last 30 Days",
        "data": get_lifespan('h')
    },
    {
        "title": "Avg Cost of an Open Commercial Permit",
        "data": float(get_avg_cost('c'))
    },
    {
        "title": "Avg Cost of an Open Residential Permit",
        "data": float(get_avg_cost('r'))
    },
    {
        "title": "Avg Cost of an Owner/Builder Permit",
        "data": float(get_avg_cost('h'))
    },
    {
        "title": "Permits & sub-permits issued by type, Last 30 Days",
        "data": get_permit_types()
    },
    {
        "title": "Average age of an Open Permit (in Days)",
        "data": -1
    },
    {
        "title": "Master Permits Issued, Last 30 Days",
        "data": get_master_permit_counts('permit_issued_date')
    }
]

json_obj['test'] = json.dumps(dashboard_collection[0]['data']['graph'])
json_obj['surveys_type'] = json.dumps(dashboard_collection[2])
json_obj['permits_type'] = json.dumps(dashboard_collection[9])
json_obj['app_answers'] = json.dumps(survey_table)


@blueprint.route("/", methods=["GET", "POST"])
def home():
    today = datetime.date.today()
    return render_template("public/home.html", api=api_health(), date=today.strftime('%B %d, %Y'), stats=stats, json_obj=json_obj, dash_obj=dashboard_collection, title='Dashboard')


@blueprint.route('/dashboard', methods=['GET', 'POST'])
def survey_index():
    form = {}
    return render_template('dashboard/home.html', form=form)


@blueprint.route('/dashboard/feedback/', methods=['GET'])
def survey_detail():
    return render_template("dashboard/survey-detail.html", resp_obj=survey_table, title='Permitting & Inspection Center User Survey Metrics: Detail')


@blueprint.route("/dashboard/violations/",  methods=['GET'])
def violations_detail():
    return render_template("public/violations-detail.html", title='Violations by Type: Detail')


@blueprint.route("/edit-public/",  methods=['GET'])
def edit_public():
    return render_template("public/edit-public.html", stats=stats, json_obj=json_obj, dash_obj=dashboard_collection, title='Dashboard Editor - Public')


@blueprint.route("/edit-internal/",  methods=['GET'])
def edit_internal():
    return render_template("public/edit-internal.html", stats=stats, json_obj=json_obj, dash_obj=dashboard_collection, title='Dashboard Editor - Internal')
