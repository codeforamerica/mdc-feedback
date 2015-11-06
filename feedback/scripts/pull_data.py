"""
This script should run daily to:
"""
import arrow
import requests

from flask import render_template, current_app

from feedback.app import create_app
from feedback.settings import DevelopmentConfig
from feedback.surveys.models import Stakeholder
from feedback.surveys.serializers import (
    pic_schema, DataLoader
)

from feedback.surveys.constants import (
    TF, ROUTES, SURVEY_DAYS, BEST,
    WORST, ROLES, PURPOSE
)
from feedback.dashboard.vendorsurveys import (
    fill_values,
    string_to_bool
)
from feedback.utils import send_email


TI_API = 'https://textit.in/api/v1/runs.json?flow_uuid='
TEXTIT_UUID_EN = '0aa9f77b-d775-4bc9-952a-1a6636258841'
TEXTIT_UUID_ES = 'bdb57073-ab32-4c1b-a3a5-25f866b9626b'
TEXTIT_AUTH_KEY = '41a75bc6977c1e0b2b56d53a91a356c7bf47e3e9'


def date_to_db(str1):
    ''' Takes the string date format of various APIs
    to convert them into a format the postgres is
    okay with. Returns as a string.
    '''
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
    return arrow.get(str1).strftime(DATE_FORMAT)


def call_web(ts):
    ''' Call the WEB API, which in this case is
    Typeform. Accepts an timestamp (Arrow object)
    as an argument, then pulls Return the
    result in json.
    '''
    API = TF['API'] + TF['KEY'] + '&completed=true&since=' + str(ts.timestamp)
    response = requests.get(API)
    print API

    return response.json()


def call_sms(ts):
    ''' Call the SMS API, which in this case is
    TextIt. Accepts an timestamp (Arrow object)
    as an argument, then pulls Return the
    result in json.
    '''
    ts = ts.strftime("%Y-%m-%dT%H:%M:%S.000")
    SMS_API = TI_API + TEXTIT_UUID_ES + ',' + TEXTIT_UUID_EN + '&after=' + ts
    # print 'TEXTIT API', SMS_API

    resp = requests.get(
        SMS_API,
        headers={'Authorization': 'Token ' + TEXTIT_AUTH_KEY}
        )

    return resp.json()


def etl_web_data(ts):
    ''' Take the Typeform API and ETL it to a common
    standard we can do dashboard stats for.

    Returns a list of objects, each object being
    a survey.
    '''
    data = []
    json = call_web(ts)

    for resp in json['responses']:
        answers_arr = resp['answers']

        obj = {'method': 'web'}
        if "English" in answers_arr[TF['LANG_EN']]:
            obj['lang'] = 'en'
        else:
            obj['lang'] = 'es'

        obj['source_id'] = 'WEB-' + resp['id']

        temp = resp['metadata']['date_submit']
        obj['date_submitted'] = date_to_db(temp)

        obj['get_done'] = fill_values(answers_arr, TF['GETDONE_EN'], TF['GETDONE_ES'])
        obj['rating'] = int(fill_values(answers_arr, TF['OPINION_EN'], TF['OPINION_ES']))
        obj['improvement'] = fill_values(answers_arr, TF['IMPROVE_EN'], TF['IMPROVE_ES'])
        obj['best_other'] = fill_values(answers_arr, TF['BEST_OTHER_EN'], TF['BEST_OTHER_ES'])
        obj['worst_other'] = fill_values(
            answers_arr,
            TF['WORST_OTHER_EN'],
            TF['WORST_OTHER_ES'])
        obj['follow_up'] = fill_values(answers_arr, TF['FOLLOWUP_EN'], TF['FOLLOWUP_ES'])
        obj['contact'] = fill_values(answers_arr, TF['CONTACT_EN'], TF['CONTACT_ES'])
        obj['more_comments'] = fill_values(answers_arr, TF['COMMENTS_EN'], TF['COMMENTS_ES'])
        obj['role'] = ROLES[
            fill_values(
                answers_arr,
                TF['ROLE_EN'],
                TF['ROLE_ES'])]
        try:
            obj['purpose'] = PURPOSE[
                fill_values(
                    answers_arr,
                    TF['PURP_EN'],
                    TF['PURP_ES'])]
        except KeyError:
            # None. Set to 6 which is "OTHER"
            obj['purpose'] = 6

        obj['purpose_other'] = fill_values(
            answers_arr,
            TF['PURP_OTHER_EN'],
            TF['PURP_OTHER_ES'])

        try:
            obj['best'] = BEST[
                fill_values(
                    answers_arr,
                    TF['BEST_EN'],
                    TF['BEST_ES'])]
        except KeyError:
            obj['best'] = None

        try:
            obj['worst'] = WORST[
                fill_values(
                    answers_arr,
                    TF['WORST_EN'],
                    TF['WORST_ES'])]
        except KeyError:
            obj['worst'] = None

        try:
            obj['route'] = ROUTES[
                fill_values(
                    answers_arr,
                    TF['ROUTE_EN'],
                    TF['ROUTE_ES'])]
        except KeyError:
            obj['route'] = None

        data.append(obj)
    # print data
    return data


def etl_sms_data(ts):
    ''' Take the Textit API and ETL it to a common
    standard we can do dashboard stats for. Accepts
    a time stamp (Arrow object)

    Returns a list of objects, each object being
    a survey.
    '''
    data = []

    json_result = call_sms(ts)
    # print 'json_result', json_result
    obj_completed = [result for result in json_result['results'] if result['completed']]
    # obj_completed = [result for result in json_result['results']]
    for obj in obj_completed:

        iter = {}
        values_array = obj['values']
        for value in values_array:
            iter[value['label']] = {
                'category': value['category'],
                'value': value['rule_value'],
                'text': value['text']
            }

        s_obj = {
            'source_id': 'SMS-' + str(obj['run']),
            'method': 'sms',
            'route': iter['Section']['text'],
            'get_done': string_to_bool(iter['Tasks']['text']),
            'rating': iter['Satisfaction']['value'],
            'improvement': iter['Improvement']['text'],
            'follow_up': string_to_bool(iter['Followup Permission']['text']),
            'more_comments': iter['Comments']['text']
        }

        if iter['Best']['text'].isdigit():
            s_obj['best'] = iter['Best']['text']
        else:
            s_obj['best_other'] = iter['Best']['text']

        if iter['Worst']['text'].isdigit():
            s_obj['worst'] = iter['Worst']['text']
        else:
            s_obj['worst_other'] = iter['Worst']['text']

        s_obj['date_submitted'] = date_to_db(obj['modified_on'])

        if obj['flow_uuid'] == TEXTIT_UUID_EN:
            s_obj['lang'] = 'en'
        else:
            s_obj['lang'] = 'es'

        try:
            s_obj['purpose'] = iter['Purpose']['value']
        except KeyError:
            s_obj['purpose'] = None

        try:
            s_obj['role'] = iter['Role']['text']
        except KeyError:
            s_obj['role'] = None

        try:
            s_obj['contact'] = iter['Contact Information']['text']
        except KeyError:
            s_obj['contact'] = None

        data.append(s_obj)
    return data


def follow_up(models):
    ''' Inputs a bunch of survey models, go through
    each of them, figuring out if they require
    follow-ups and then e-mail the appropriate
    directors.

    Returns ..?
    '''
    subj = 'New feedback has been posted from the Permitting Inspection Center!'
    from_email = current_app.config.get('ADMIN_EMAIL')
    for survey in models:

        if survey.follow_up and survey.route is not None:
            stakeholder = Stakeholder.query.get(survey.route)
            if stakeholder is None or stakeholder.email_list is None:
                current_app.logger.info(
                    'NOSTAKEHOLDER | Route: {}\nSurvey Submitted Date: {}\nSubject: {}'.format(
                        survey.route_en,
                        survey.date_submitted,
                        subj
                    )
                )
            else:
                send_email(
                    subj,
                    from_email,
                    stakeholder.email_list,
                    render_template(
                        'email/followup_notification.txt',
                        survey=survey
                    ),
                    render_template(
                        'email/followup_notification.html',
                        survey=survey
                    ))


def load_data():
    timestamp = arrow.utcnow()
    timestamp = timestamp.replace(days=-SURVEY_DAYS)

    tf = etl_web_data(timestamp)
    ti = etl_sms_data(timestamp)
    data = tf + ti

    loader = DataLoader(pic_schema)

    for row in data:
        loader.slice_and_add(row)

    db_models = loader.save_models_or_report_errors()
    if db_models is not None:
        follow_up(db_models)


def run():
    app = create_app()
    with app.app_context():
        load_data()

if __name__ == '__main__':
    run()
