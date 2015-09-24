 # -*- coding: utf-8 -*-

import datetime
import requests

from feedback.extensions import cache
from feedback.utils import utc_to_local
from collections import Counter
import numpy as np


TYPEFORM_API = 'https://api.typeform.com/v0/form/aaz1iK?key='
TYPEFORM_API_KEY = '433dcf9fb24804b47666bf62f83d25dbef2f629d'

TF_OPINION_EN = 'opinionscale_9825055'
TF_OPINION_ES = 'opinionscale_9825056'

TF_BESTWORST_EN = 'textarea_9825061'
TF_BESTWORST_ES = 'textarea_9825064'

TF_1STTIME_EN = 'yesno_9825058'
TF_1STTIME_ES = 'yesno_9825060'
TF_GETDONE_EN = 'yesno_9825057'
TF_GETDONE_ES = 'yesno_10444681'

TF_IMPROVE_EN = 'textarea_9825062'
TF_IMPROVE_ES = 'textarea_9825065'

TF_COMMENTS_EN = 'textarea_9825063'
TF_COMMENTS_ES = 'textarea_9825066'
TF_ROLE_EN = 'list_9825053_choice'
TF_ROLE_ES = 'list_9825054_choice'

TF_PURP_PERMIT_EN = 'list_10432251_choice_12738830'
TF_PURP_INSPECTOR_EN = 'list_10432251_choice_12738831'
TF_PURP_PLANREVIEW_EN = 'list_10432251_choice_12738832'
TF_PURP_VIOLATION_EN = 'list_10432251_choice_12738833'
TF_PURP_CU_EN = 'list_10432251_choice_12738834'
TF_PURP_OTHER_EN = 'list_10432251_other'

TF_PURP_PERMIT_ES = 'list_10444324_choice_12758795'
TF_PURP_INSPECTOR_ES = 'list_10444324_choice_12758796'
TF_PURP_PLANREVIEW_ES = 'list_10444324_choice_12758797'
TF_PURP_VIOLATION_ES = 'list_10444324_choice_12758798'
TF_PURP_CU_ES = 'list_10444324_choice_12758799'
TF_PURP_OTHER_ES = 'list_10444324_other'

TEXTIT_API = 'https://textit.in/api/v1/runs.json?flow_uuid='
TEXTIT_UUID_EN = '920cec13-ffc0-4fe9-92c3-1cced2073498'
TEXTIT_UUID_ES = '7001c507-1c9e-46dd-aea3-603b986c3d89'
TEXTIT_AUTH_KEY = '41a75bc6977c1e0b2b56d53a91a356c7bf47e3e9'
TEXTIT_UUID_OPINION = '53249739-7b72-43c2-9463-e4cd4963a408'


def fill_values(array, arg1, arg2):
    try:
        if array[arg1]:
            return array[arg1]
        else:
            return array[arg2]
    except KeyError:
        try:
            if array[arg2]:
                return array[arg2]
        except KeyError:
            return ''


def fill_purpose(array, arg1, arg2):
    # if TF_PURP_PERMIT_EN in results or TF_PURP_PERMIT_ES in results:
    try:
        if not array[arg1]:
            return False
        else:
            return array[arg1]
    except KeyError:
        if not array[arg2]:
            return False
        else:
            return array[arg2]


def make_typeform_call(timestamp):
    '''
    Takes in the timestamp in unix form
    Returns the JSON of the actual API. Let's just start simple.
    '''
    unix_time = timestamp.strftime("%s")

    API = TYPEFORM_API + TYPEFORM_API_KEY + '&completed=true&since=' + unix_time
    # print 'TYPEFORM API', API

    response = requests.get(API)
    json_result = response.json()
    return json_result


def make_textit_call(timestamp):
    '''
    Takes in the timestamp in unix form
    Returns the JSON of the actual API.
    '''
    sms_query_date = timestamp.strftime("%Y-%m-%dT00:00:00.000")

    SMS_API = TEXTIT_API + TEXTIT_UUID_ES + ',' + TEXTIT_UUID_EN + '&after=' + sms_query_date
    # print 'TEXTIT API', SMS_API

    response2 = requests.get(SMS_API, headers={'Authorization': 'Token ' + TEXTIT_AUTH_KEY})

    json_result = response2.json()
    # print json_result
    return json_result


def parse_textit(survey_table, json_result):
    '''
    Take the textit API result and do ETLs to get
    the responses in an easy to digest format.
    Returns an object:
        survey_table
    '''
    # print 'json_result', json_result
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
            'role': filter_role(iter['Role']['text']),
            'rating': iter['Experience Rating']['text'],
            'improvement': iter['Improvement']['text'],
            'bestworst': iter['Best and Worst']['text'],
            'followup': iter['Followup Permission']['category'],
            'morecomments': iter['Comments']['text']
        }

        temp = obj['modified_on']
        temp = datetime.datetime.strptime(temp, '%Y-%m-%dT%H:%M:%S.%fZ')
        date_object = utc_to_local(temp)
        iter_obj['date'] = date_object.strftime("%m-%d")

        if obj['flow_uuid'] == TEXTIT_UUID_EN:
            iter_obj['lang'] = 'en'
        else:
            iter_obj['lang'] = 'es'

        try:
            iter_obj['purpose'] = [int(iter['Purpose']['text'])]
        except KeyError:
            iter_obj['purpose'] = []

        survey_table.append(iter_obj)

    return survey_table


def filter_role(arg1):
    '''
    The role returns either a string (both EN/ES) or a int depending on the API. This is a filter that converms them into integers for filter_table in the prase functions. Will try to find the first number if it's mixed e.g. "Number 5"
    Returns an integer or False if it doesn't know what to do with itself.
    '''
    if arg1.isdigit():
        return int(arg1)
    else:
        arg1 = arg1.lower()
        if arg1 in ['contractor', 'contratista']:
            return 1
        if arg1 in ['architect', 'arquitecto']:
            return 2
        if arg1 in ['permit consultant', 'consultor de permiso']:
            return 3
        if arg1 in ['homeowner', u'due\xf1o/a de casa']:
            return 4
        if arg1 in ['business owner', u'due\xf1o/a de negocio']:
            return 5
        return [int(s) for s in arg1.split() if s.isdigit()][0]


def fill_typeform_purpose(results):
    '''
    Returns an array of integers for purposes mapped to the possible purposes. If there is a string that means someone typed in a result in the "other" column
    '''
    return_array = []

    if fill_purpose(results, TF_PURP_PERMIT_EN, TF_PURP_PERMIT_ES):
        return_array.append(1)
    if fill_purpose(results, TF_PURP_INSPECTOR_EN, TF_PURP_INSPECTOR_ES):
        return_array.append(2)
    if fill_purpose(results, TF_PURP_PLANREVIEW_EN, TF_PURP_PLANREVIEW_ES):
        return_array.append(3)
    if fill_purpose(results, TF_PURP_VIOLATION_EN, TF_PURP_VIOLATION_ES):
        return_array.append(4)
    if fill_purpose(results, TF_PURP_CU_EN, TF_PURP_CU_ES):
        return_array.append(5)

    if results[TF_PURP_OTHER_EN]:
        return_array.append(results[TF_PURP_OTHER_EN])
    if results[TF_PURP_OTHER_ES]:
        return_array.append(results[TF_PURP_OTHER_ES])

    return return_array


def parse_typeform(survey_table, json_result):

    for survey_response in json_result['responses']:
        iter_obj = {'method': 'web'}
        answers_arr = survey_response['answers']

        # LANGUAGE CHOICE LOGIC JUMP = 'list_9825052_choice'
        if "English" in answers_arr['list_9825052_choice']:
            iter_obj['lang'] = 'en'
        else:
            iter_obj['lang'] = 'es'

        iter_obj['id'] = 'WEB-' + survey_response['id']

        temp = survey_response['metadata']['date_submit']
        temp = datetime.datetime.strptime(temp, '%Y-%m-%d %H:%M:%S')
        date_object = utc_to_local(temp)
        iter_obj['date'] = date_object.strftime("%m-%d")

        iter_obj['firsttime'] = fill_values(answers_arr, TF_1STTIME_EN, TF_1STTIME_ES)
        iter_obj['getdone'] = fill_values(answers_arr, TF_GETDONE_EN, TF_GETDONE_ES)
        iter_obj['rating'] = fill_values(answers_arr, TF_OPINION_EN, TF_OPINION_ES)
        iter_obj['improvement'] = fill_values(answers_arr, TF_IMPROVE_EN, TF_IMPROVE_ES)
        iter_obj['bestworst'] = fill_values(answers_arr, TF_BESTWORST_EN, TF_BESTWORST_ES)

        # FIXME: THERE'S NO FOLLOW UP IN THE WEB FORM
        iter_obj['followup'] = fill_values(answers_arr, '', '')

        iter_obj['morecomments'] = fill_values(answers_arr, TF_COMMENTS_EN, TF_COMMENTS_ES)
        iter_obj['role'] = filter_role(fill_values(answers_arr, TF_ROLE_EN, TF_ROLE_ES))
        iter_obj['purpose'] = fill_typeform_purpose(answers_arr)
        survey_table.append(iter_obj)

    return survey_table


def get_surveys_by_role(survey_table):
    valid_roles = [x['role'] for x in survey_table]
    return Counter(valid_roles).most_common()


def get_surveys_by_completion(survey_table):
    items = [x['getdone'] for x in survey_table]
    return {
        "yes": items.count('Yes') + items.count('1'),
        "total": len(items)
    }


def get_surveys_by_purpose(survey_table):
    i = [x['purpose'] for x in survey_table if x['purpose']]

    # flattens list. See:http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
    items = sum(i, [])

    return Counter(items).most_common()


def get_rating_scale(survey_table):
    '''
    Given the table of all the responses, find the values of all roles.
    '''
    arr = [int(x['rating']) for x in survey_table if x['rating'].isdigit()]
    return np.mean(arr)


def get_rating_by_lang(survey_table, lang='en'):
    arr = [int(x['rating']) for x in survey_table if x['rating'].isdigit() and x['lang'] == lang]
    return np.mean(arr)


def get_rating_by_role(survey_table, role):
    arr = [int(x['rating']) for x in survey_table if x['rating'].isdigit() and x['role'] == role]
    print role, arr
    return np.mean(arr)


def get_rating_by_purpose(survey_table, purpose):
    arr = [x['rating'] for x in survey_table if purpose in x['purpose']]
    arr = [int(x) for x in arr if x.isdigit()]
    return np.mean(arr)


@cache.memoize(timeout=3600)
def get_all_survey_responses(days):
    survey_table = []
    timestamp = datetime.date.today() - datetime.timedelta(days)

    # TYPEFORM API CALLS
    json_result = make_typeform_call(timestamp)
    survey_table = parse_typeform(survey_table, json_result)

    # TEXTIT API CALLS
    sms_result = make_textit_call(timestamp)
    survey_table = parse_textit(survey_table, sms_result)

    # print survey_table
    return survey_table
