 # -*- coding: utf-8 -*-

import datetime
import json

from flask import (
    Blueprint, render_template
)

from feedback.dashboard.vendorsurveys import (
    get_rating_scale, get_surveys_by_role,
    get_surveys_by_completion, get_surveys_by_purpose,
    get_all_survey_responses, get_rating_by_lang,
    get_rating_by_purpose, get_rating_by_role,
    roles_const_to_string
)

from feedback.dashboard.permits import (
    api_health, get_lifespan,
    get_permit_types,
    get_master_permit_counts,
    dump_socrata_api
)

blueprint = Blueprint(
    "dashboard", __name__,
    template_folder='../templates',
    static_folder="../static"
)

SURVEY_DAYS = 30


@blueprint.route("/", methods=["GET", "POST"])
def home():

    json_obj = {}

    surveys_by_date = {}
    surveys_date_array = []
    surveys_value_array = []

    for i in range(SURVEY_DAYS, -1, -1):
        time_i = (datetime.date.today() - datetime.timedelta(i))
        date_index = time_i.strftime("%m-%d")
        surveys_by_date[date_index] = 0
        surveys_date_array.append(date_index)

    survey_table = get_all_survey_responses(SURVEY_DAYS)

    sms_rows = [x['lang'] for x in survey_table if x['method'] == 'sms']
    web_rows = [x['lang'] for x in survey_table if x['method'] == 'web']

    # ANALYTICS CODE
    for i in range(SURVEY_DAYS, -1, -1):
        time_i = (datetime.date.today() - datetime.timedelta(i))
        date_index = time_i.strftime("%m-%d")
        surveys_value_array.append(len([x for x in survey_table if x['date'] == date_index]))

    dashboard_collection = [
        {
            "id": "graph",
            "title": "Surveys Submitted - Last {0} Days".format(SURVEY_DAYS),
            "data": {
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
            "data": "{0:.2f}".format(get_rating_scale(survey_table))
        },
        {
            "title": "Survey Type - Last {0} Days".format(SURVEY_DAYS),
            "data": {
                "web_en": web_rows.count('en'),
                "web_es": web_rows.count('es'),
                "sms_en": sms_rows.count('en'),
                "sms_es": sms_rows.count('es')
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
            "title": "(UNUSED) Avg Cost of an Open Commercial Permit",
            "data": 0
        },
        {
            "title": "(UNUSED) Avg Cost of an Open Residential Permit",
            "data": 0
        },
        {
            "title": "(UNUSED) Avg Cost of an Owner/Builder Permit",
            "data": 0
        },
        {
            "title": "Permits & sub-permits issued by type, Last 30 Days",
            "data": get_permit_types()
        },
        {
            "title": "Surveys by Survey Role",
            "data": get_surveys_by_role(survey_table)
        },
        {
            "title": "Master Permits Issued, Last 30 Days",
            "data": get_master_permit_counts('permit_issued_date')
        },
        {
            "title": "How many completions?",
            "data": get_surveys_by_completion(survey_table)
        },
        {
            "title": "Purpose",
            "data": get_surveys_by_purpose(survey_table)
        },
        {
            "title": "Ratings",
            "data": {
                "en": get_rating_by_lang(survey_table, 'en'),
                "es": get_rating_by_lang(survey_table, 'es'),
                "p1": get_rating_by_purpose(survey_table, 1),
                "p2": get_rating_by_purpose(survey_table, 2),
                "p3": get_rating_by_purpose(survey_table, 3),
                "p4": get_rating_by_purpose(survey_table, 4),
                "p5": get_rating_by_purpose(survey_table, 5),
                "r1": get_rating_by_role(survey_table, 1),
                "r2": get_rating_by_role(survey_table, 2),
                "r3": get_rating_by_role(survey_table, 3),
                "r4": get_rating_by_role(survey_table, 4),
                "r5": get_rating_by_role(survey_table, 5)
            }
        }
    ]

    json_obj['test'] = json.dumps(dashboard_collection[0]['data']['graph'])
    json_obj['surveys_type'] = json.dumps(dashboard_collection[2])
    json_obj['permits_type'] = json.dumps(dashboard_collection[9])
    json_obj['survey_role'] = json.dumps(dashboard_collection[10])
    json_obj['survey_complete'] = json.dumps(dashboard_collection[12])
    json_obj['survey_purpose'] = json.dumps(dashboard_collection[13])
    json_obj['app_answers'] = json.dumps(survey_table)
    json_obj['permits_rawjson'] = json.dumps(dump_socrata_api('p'))
    json_obj['violations_rawjson'] = json.dumps(dump_socrata_api('v'))

    today = datetime.date.today()
    return render_template(
        "public/home.html",
        api=api_health(),
        date=today.strftime('%B %d, %Y'),
        json_obj=json_obj,
        dash_obj=dashboard_collection,
        resp_obj=survey_table,
        title='Dashboard'
        )


@blueprint.route('/dashboard', methods=['GET', 'POST'])
def survey_index():
    form = {}
    return render_template('dashboard/home.html', form=form)


@blueprint.route('/dashboard/feedback/', methods=['GET'])
def all_surveys():
    def followup_to_str(arg1):
        try:
            return arg1['base']
        except TypeError:
            if arg1.isdigit():
                if arg1 == '1':
                    return 'Yes'
                else:
                    return 'No'
            else:
                return arg1

        return arg1

    def purpose_to_str(arg1):
        if arg1.isdigit():
            return {
                '1': 'Apply for a permit',
                '2': 'Meet with an Inspector',
                '3': 'Meet with a Plan Reviewer',
                '4': 'Find out about a violation or lien on your property',
                '5': 'Obtain a certificate of use and/or occupancy'
            }.get(arg1, '')
        else:
            if arg1.startswith('6 '):
                return arg1[2:]
        return arg1

    survey_table = get_all_survey_responses(SURVEY_DAYS)
    for row in survey_table:
        row['role'] = roles_const_to_string(row['role'])
        row['followup'] = followup_to_str(row['followup'])
        row['purpose'] = purpose_to_str(str(row['purpose']))
    return render_template(
        "dashboard/all-surveys.html",
        resp_obj=survey_table,
        title='Permitting & Inspection Center User Survey Metrics: Detail'
    )


@blueprint.route('/dashboard/feedback/<id>', methods=['GET'])
def survey_detail(id):
    survey_table = get_all_survey_responses(SURVEY_DAYS)
    survey_table = [x for x in survey_table if x['id'] == id]
    return render_template("dashboard/survey-detail.html", resp_obj=survey_table, title='Permitting & Inspection Center User Survey Metrics: Detail')


@blueprint.route("/dashboard/violations/",  methods=['GET'])
def violations_detail():
    return render_template("public/violations-detail.html", title='Violations by Type: Detail')


@blueprint.route("/edit-public/",  methods=['GET'])
def edit_public():
    return render_template("public/edit-public.html", title='Dashboard Editor - Public')


@blueprint.route("/edit-internal/",  methods=['GET'])
def edit_internal():
    return render_template("public/edit-internal.html", title='Dashboard Editor - Internal')


@blueprint.route("/choose-survey/", methods=['GET'])
def choose_survey():
    return render_template("public/choose-survey.html", title="Choose a survey")
