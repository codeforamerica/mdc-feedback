 # -*- coding: utf-8 -*-

import datetime
import json

from flask import (
    Blueprint, render_template
)

from feedback.dashboard.vendorsurveys import (
    parse_textit, get_textit_by_meta, get_textit_by_date,
    make_typeform_call, make_textit_call, parse_typeform,
    get_typeform_by_meta, get_typeform_by_date
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

SURVEY_DAYS = 31

for i in range(SURVEY_DAYS, -1, -1):
    time_i = (datetime.date.today() - datetime.timedelta(i))
    date_index = time_i.strftime("%m-%d")
    surveys_by_date[date_index] = 0
    surveys_date_array.append(date_index)

# Get unix timestamp of a week ago
timestamp = datetime.date.today() - datetime.timedelta(SURVEY_DAYS)
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

for i in range(SURVEY_DAYS, -1, -1):
    time_i = (datetime.date.today() - datetime.timedelta(i))
    date_index = time_i.strftime("%m-%d")
    surveys_value_array.append(surveys_by_date[date_index])

dashboard_collection = [
    {
        "id": "graph",
        "title": "Surveys Submitted - Last {0} Days".format(SURVEY_DAYS),
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
        "title": "Satisfaction Rating - Last {0} Days".format(SURVEY_DAYS),
        "data": "{0:.2f}".format(rating)
    },
    {
        "title": "Survey Type - Last {0} Days".format(SURVEY_DAYS),
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
    return render_template("public/home.html", api=api_health(), date=today.strftime('%B %d, %Y'), stats=stats, json_obj=json_obj, dash_obj=dashboard_collection, resp_obj=survey_table, title='Dashboard')


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


@blueprint.route("/choose-survey/", methods=['GET'])
def choose_survey():
    return render_template("public/choose-survey.html", title="Choose a survey")
