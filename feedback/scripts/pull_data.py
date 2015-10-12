"""
This script should run daily to:
"""
import arrow
import requests

from feedback.app import create_app
from feedback.surveys.serializers import (
    pic_schema, DataLoader
)
from feedback.surveys.constants import ROUTES
from feedback.dashboard.vendorsurveys import (
    fill_values, filter_improvement, filter_best,
    filter_worst, filter_purpose, filter_role,
    string_to_bool
)

TI_API = 'https://textit.in/api/v1/runs.json?flow_uuid='
TEXTIT_UUID_EN = '0aa9f77b-d775-4bc9-952a-1a6636258841'
TEXTIT_UUID_ES = 'bdb57073-ab32-4c1b-a3a5-25f866b9626b'
TEXTIT_AUTH_KEY = '41a75bc6977c1e0b2b56d53a91a356c7bf47e3e9'

TF_API = 'https://api.typeform.com/v0/form/NNCQGT?key='
TF_KEY = '433dcf9fb24804b47666bf62f83d25dbef2f629d'

TF_LANG_EN = 'list_11278243_choice'
TF_ROLE_EN = 'list_11029984_choice'
TF_ROLE_ES = 'list_11029987_choice'

TF_PURP_EN = 'list_11029985_choice'
TF_PURP_OTHER_EN = 'list_11029985_other'
TF_PURP_ES = 'list_11422502_choice'
TF_PURP_OTHER_ES = 'list_11422502_other'

TF_OPINION_EN = 'opinionscale_11029990'
TF_OPINION_ES = 'opinionscale_11029991'

TF_GETDONE_EN = 'yesno_11029979'
TF_GETDONE_ES = 'yesno_11278208'

TF_BEST_EN = 'list_11277420_choice'
TF_BEST_OTHER_EN = 'list_11277420_other'
TF_WORST_EN = 'list_11277432_choice'
TF_WORST_OTHER_EN = 'list_11277432_other'
TF_BEST_ES = 'list_11277910_choice'
TF_BEST_OTHER_ES = 'list_11277910_other'
TF_WORST_ES = 'list_11277952_choice'
TF_WORST_OTHER_ES = 'list_11277952_other'

TF_IMPROVE_EN = 'list_11277447_choice'
TF_IMPROVE_OTHER_EN = 'list_11277447_other'
TF_IMPROVE_ES = 'list_11278117_choice'
TF_IMPROVE_OTHER_ES = 'list_11278117_other'

TF_COMMENTS_EN = 'textarea_11029995'
TF_COMMENTS_ES = 'textarea_11029999'

TF_ROUTE_EN = 'list_11510353_choice'
TF_ROUTE_ES = 'list_11510726_choice'

TF_FOLLOWUP_EN = 'yesno_11029980'
TF_FOLLOWUP_ES = 'yesno_11029983'
TF_CONTACT_EN = 'textfield_11277574'
TF_CONTACT_ES = 'textfield_11278128'


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
    API = TF_API + TF_KEY + '&completed=true&since=' + str(ts.timestamp)
    response = requests.get(API)

    return response.json()


def get_and_massage_web_data(ts):
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
        if "English" in answers_arr[TF_LANG_EN]:
            obj['lang'] = 'en'
        else:
            obj['lang'] = 'es'

        obj['source_id'] = 'WEB-' + resp['id']

        temp = resp['metadata']['date_submit']
        obj['date_submitted'] = date_to_db(temp)

        obj['get_done'] = fill_values(answers_arr, TF_GETDONE_EN, TF_GETDONE_ES)
        obj['rating'] = int(fill_values(answers_arr, TF_OPINION_EN, TF_OPINION_ES))
        obj['improvement'] = filter_improvement(fill_values(answers_arr, TF_IMPROVE_EN, TF_IMPROVE_ES))
        obj['improvement_other'] = fill_values(answers_arr, TF_IMPROVE_OTHER_EN, TF_IMPROVE_OTHER_ES)
        obj['best'] = filter_best(fill_values(answers_arr, TF_BEST_EN, TF_BEST_ES))
        obj['best_other'] = fill_values(answers_arr, TF_BEST_OTHER_EN, TF_BEST_OTHER_ES)
        obj['worst'] = filter_worst(fill_values(answers_arr, TF_WORST_EN, TF_WORST_ES))
        obj['worst_other'] = fill_values(answers_arr, TF_WORST_OTHER_EN, TF_WORST_OTHER_ES)
        obj['follow_up'] = fill_values(answers_arr, TF_FOLLOWUP_EN, TF_FOLLOWUP_ES)
        obj['contact'] = fill_values(answers_arr, TF_CONTACT_EN, TF_CONTACT_ES)
        obj['more_comments'] = fill_values(answers_arr, TF_COMMENTS_EN, TF_COMMENTS_ES)
        obj['role'] = filter_role(fill_values(answers_arr, TF_ROLE_EN, TF_ROLE_ES))
        obj['purpose'] = filter_purpose(fill_values(answers_arr, TF_PURP_EN, TF_PURP_ES))
        obj['purpose_other'] = fill_values(answers_arr, TF_PURP_OTHER_EN, TF_PURP_OTHER_ES)
        try:
            obj['route'] = ROUTES[fill_values(answers_arr, TF_ROUTE_EN, TF_ROUTE_ES)]
        except KeyError:
            obj['route'] = None

        data.append(obj)
    # print data
    return data


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


def get_and_massage_sms_data(ts):
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
            'role': filter_role(iter['Role']['text']),
            'rating': iter['Satisfaction']['text'],
            'improvement': iter['Improvement']['value'],
            'best': filter_best(iter['Best']['category']),
            'worst': filter_worst(iter['Worst']['category']),
            'follow_up': string_to_bool(iter['Followup Permission']['text']),
            'more_comments': iter['Comments']['text']
        }

        s_obj['date_submitted'] = date_to_db(obj['modified_on'])

        if obj['flow_uuid'] == TEXTIT_UUID_EN:
            s_obj['lang'] = 'en'
        else:
            s_obj['lang'] = 'es'

        try:
            s_obj['purpose'] = iter['Purpose']['value']
        except KeyError:
            s_obj['purpose'] = None

        data.append(s_obj)
    return data


def load_data():
    timestamp = arrow.utcnow()
    timestamp = timestamp.replace(days=-30)

    tf = get_and_massage_web_data(timestamp)
    ti = get_and_massage_sms_data(timestamp)
    data = tf + ti

    loader = DataLoader(pic_schema)

    for row in data:
        loader.slice_and_add(row)

    loader.save_models_or_report_errors()


def run():
    app = create_app()
    with app.app_context():
        load_data()

if __name__ == '__main__':
    run()
