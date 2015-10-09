 # -*- coding: utf-8 -*-

from pprint import pprint

import datetime
import requests

from feedback.extensions import db, cache
from feedback.utils import utc_to_local
from feedback.surveys.serializers import pic_schema
from feedback.surveys.models import Survey
from feedback.surveys.constants import ROUTES, ROLES

from collections import Counter

import numpy as np

TYPEFORM_API = 'https://api.typeform.com/v0/form/NNCQGT?key='
TYPEFORM_API_KEY = '433dcf9fb24804b47666bf62f83d25dbef2f629d'

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

TEXTIT_API = 'https://textit.in/api/v1/runs.json?flow_uuid='
TEXTIT_UUID_EN = '0aa9f77b-d775-4bc9-952a-1a6636258841'
TEXTIT_UUID_ES = 'bdb57073-ab32-4c1b-a3a5-25f866b9626b'
TEXTIT_AUTH_KEY = '41a75bc6977c1e0b2b56d53a91a356c7bf47e3e9'


def string_to_bool(arg):
    arg = arg.lower()
    arg = arg[0]
    valid = {'y': True, 's': True, 'n': False}
    if arg in valid:
        return valid[arg]
    else:
        return None


def roles_const_to_string(arg):
    return ROLES[str(arg)]


def fill_values(array, en, es):
    try:
        if not array[en]:
            if not array[es]:
                return None
            else:
                return array[es]
        else:
            return array[en]
    except KeyError:
        try:
            if not array[es]:
                return None
            else:
                return array[es]
        except KeyError:
            return None


def fill_values_other(array, en, es, en_other, es_other):
    if not array[en] and not array[en_other]:
        if not array[es]:
            if not array[es_other]:
                return None
            else:
                return array[es_other]
        else:
            return array[es]
    else:
        if not array[en]:
            return array[en_other]
        else:
            return array[en]


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

    response2 = requests.get(
        SMS_API,
        headers={'Authorization': 'Token ' + TEXTIT_AUTH_KEY}
        )

    json_result = response2.json()
    # print 'json', json_result
    return json_result


def task_textit(json_result):
    '''
    Take the textit API result and do ETLs to get
    the responses in an easy to digest format.
    '''

    textit_surveys = []

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

        temp = obj['modified_on']
        temp = datetime.datetime.strptime(temp, '%Y-%m-%dT%H:%M:%S.%fZ')
        date_object = utc_to_local(temp)
        s_obj['date_submitted'] = obj['modified_on']

        if obj['flow_uuid'] == TEXTIT_UUID_EN:
            s_obj['lang'] = 'en'
        else:
            s_obj['lang'] = 'es'

        try:
            s_obj['purpose'] = iter['Purpose']['value']
        except KeyError:
            s_obj['purpose'] = None

        textit_data = slice_data(pic_schema, s_obj)
        textit_surveys.append(textit_data)

    textit_surveys, errors = pic_schema.load(
        textit_surveys,
        many=True,
        session=db.session)

    if errors:
        print errors

    db.session.add_all(textit_surveys)
    db.session.commit()


def parse_textit(survey_table, json_result):
    '''
    Take the textit API result and do ETLs to get
    the responses in an easy to digest format.
    Returns an object:
        survey_table
    '''

    textit_surveys = []

    print 'json_result', json_result
    obj_completed = [result for result in json_result['results'] if result['completed']]
    # obj_completed = [result for result in json_result['results']]
    for obj in obj_completed:

        iter = {}
        values_array = obj['values']
        for value in values_array:
            iter[value['label']] = {'category': value['category'], 'value': value['rule_value'], 'text': value['text']}

        iter_obj = {
            'id': 'SMS-' + str(obj['run']),
            'method': 'sms',
            'route': iter['Section']['text'],
            'getdone': iter['Tasks']['text'],
            'role': filter_role(iter['Role']['text']),
            'rating': iter['Satisfaction']['text'],
            'improvement': iter['Improvement']['text'],
            'best': filter_best(iter['Best']['text']),
            'worst': filter_worst(iter['Worst']['text']),
            'followup': iter['Followup Permission']['category'],
            'morecomments': iter['Comments']['text']
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

        temp = obj['modified_on']
        temp = datetime.datetime.strptime(temp, '%Y-%m-%dT%H:%M:%S.%fZ')
        date_object = utc_to_local(temp)
        iter_obj['date'] = date_object.strftime("%m-%d")
        s_obj['date_submitted'] = obj['modified_on']

        if obj['flow_uuid'] == TEXTIT_UUID_EN:
            iter_obj['lang'] = 'en'
            s_obj['lang'] = 'en'
        else:
            iter_obj['lang'] = 'es'
            s_obj['lang'] = 'es'

        try:
            iter_obj['purpose'] = iter['Purpose']['text']
            s_obj['purpose'] = iter['Purpose']['value']
        except KeyError:
            iter_obj['purpose'] = ''

        textit_data = slice_data(pic_schema, s_obj)
        textit_surveys.append(textit_data)
        survey_table.append(iter_obj)

    textit_surveys, errors = pic_schema.load(textit_surveys, many=True, session=db.session)
    if errors:
        print errors

    db.session.add_all(textit_surveys)
    db.session.commit()

    return survey_table


def filter_role(arg1):
    '''
    The role returns int. This is a filter that converts into integers for filter_table in the prase functions. Will try to find the first number if it's mixed e.g. "Number 5"
    Returns an integer or False if it doesn't know what to do with itself.
    '''
    if arg1.isdigit():
        return int(arg1)
    else:
        arg1 = arg1.lower()
        if arg1 in ['contractor', 'contratista']:
            return 1
        if arg1 in ['architect / engineer', 'arquitecto / ingeniero']:
            return 2
        if arg1 in ['permit consultant', 'consultor de permiso']:
            return 3
        if arg1 in ['homeowner', u'due\xf1o/a de casa']:
            return 4
        if arg1 in ['business owner', u'due\xf1o/a de negocio']:
            return 5
        return [int(s) for s in arg1.split() if s.isdigit()][0]


def filter_purpose(arg1):
    ''' Take the hardcoded answers in English and Spanish and change them to constants.
    If there is a completely different purpose, it's a long form and return it as is. (We change to constants for graphic purposes.)
    '''
    if arg1 is None:
        return False
    if arg1.isdigit():
        return int(arg1)
    else:
        arg1 = arg1.lower()
        if 'permit' in arg1 or 'permiso' in arg1:
            return 1
        if 'inspector' in arg1:
            return 2
        if 'reviewer' in arg1 or 'revisador' in arg1:
            return 3
        if 'violation' in arg1 or 'gravamen' in arg1:
            return 4
        if 'certificate' in arg1 or 'certificado' in arg1:
            return 5
        try:
            return [int(s) for s in arg1.split() if s.isdigit()][0]
        except IndexError:
            return arg1


def filter_best(arg1):
    arg1 = str(arg1)
    if arg1.isdigit():
        return {
            '1': 'Getting questions answered and explained',
            '2': 'Finishing tasks quickly',
            '3': 'Courteous staff'
        }.get(arg1, '')
    else:
        arg1 = arg1.lower()
        if 'questions' in arg1 or 'permiso' in arg1:
            return 1
        if 'tasks' in arg1:
            return 2
        if 'staff' in arg1 or 'revisador' in arg1:
            return 3
        if arg1.startswith('4 '):
            return arg1[2:]
        return None
    return arg1


def filter_worst(arg1):
    arg1 = str(arg1)
    if arg1.isdigit():
        return {
            '1': 'Long wait time',
            '2': 'Repeated visits for the same issue',
            '3': 'Not being familiar to how the process works'
        }.get(arg1, '')
    else:
        arg1 = arg1.lower()
        if 'wait' in arg1 or 'permiso' in arg1:
            return 1
        if 'visits' in arg1:
            return 2
        if 'process' in arg1 or 'revisador' in arg1:
            return 3
        if arg1.startswith('4 '):
            return arg1[2:]
        return None
    return arg1


def filter_improvement(arg1):
    arg1 = str(arg1)
    if arg1.isdigit():
        return {
            '1': 'Shorter lines',
            '2': 'More services available online',
            '3': 'Simplifying the processes'
        }.get(arg1, '')
    else:
        arg1 = arg1.lower()
        if 'lines' in arg1 or 'cortas' in arg1:
            return 1
        if 'services' in arg1 or 'servicios' in arg1:
            return 2
        if 'processes' in arg1 or 'procesos' in arg1:
            return 3
        if arg1.startswith('4 '):
            return arg1[2:]
        return None
    return arg1


def task_typeform(json_result):

    typeform_surveys = []

    for survey_response in json_result['responses']:
        obj = {'method': 'web'}

        answers_arr = survey_response['answers']
        if "English" in answers_arr[TF_LANG_EN]:
            obj['lang'] = 'en'
        else:
            obj['lang'] = 'es'

        obj['source_id'] = 'WEB-' + survey_response['id']

        temp = survey_response['metadata']['date_submit']
        temp = datetime.datetime.strptime(temp, '%Y-%m-%d %H:%M:%S')
        date_object = utc_to_local(temp)
        obj['date_submitted'] = survey_response['metadata']['date_submit']

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

        typeform_data = slice_data(pic_schema, obj)
        typeform_surveys.append(typeform_data)

    typeform_surveys, errors = pic_schema.load(typeform_surveys, many=True, session=db.session)
    if errors:
        print errors

    db.session.add_all(typeform_surveys)
    db.session.commit()

    return survey_table


def parse_typeform(survey_table, json_result):

    typeform_surveys = []

    for survey_response in json_result['responses']:
        iter_obj = {'method': 'web'}
        obj = {'method': 'web'}

        answers_arr = survey_response['answers']

        if "English" in answers_arr[TF_LANG_EN]:
            iter_obj['lang'] = 'en'
            obj['lang'] = 'en'
        else:
            iter_obj['lang'] = 'es'
            obj['lang'] = 'es'

        iter_obj['id'] = 'WEB-' + survey_response['id']
        obj['source_id'] = 'WEB-' + survey_response['id']

        temp = survey_response['metadata']['date_submit']
        temp = datetime.datetime.strptime(temp, '%Y-%m-%d %H:%M:%S')
        date_object = utc_to_local(temp)
        iter_obj['date'] = date_object.strftime("%m-%d")
        obj['date_submitted'] = survey_response['metadata']['date_submit']

        iter_obj['getdone'] = fill_values(answers_arr, TF_GETDONE_EN, TF_GETDONE_ES)
        obj['get_done'] = fill_values(answers_arr, TF_GETDONE_EN, TF_GETDONE_ES)

        iter_obj['rating'] = fill_values(answers_arr, TF_OPINION_EN, TF_OPINION_ES)
        obj['rating'] = int(fill_values(answers_arr, TF_OPINION_EN, TF_OPINION_ES))

        iter_obj['improvement'] = fill_values(answers_arr, TF_IMPROVE_EN, TF_IMPROVE_ES)
        obj['improvement'] = filter_improvement(fill_values(answers_arr, TF_IMPROVE_EN, TF_IMPROVE_ES))
        obj['improvement_other'] = fill_values(answers_arr, TF_IMPROVE_OTHER_EN, TF_IMPROVE_OTHER_ES)

        iter_obj['best'] = filter_best(fill_values_other(answers_arr, TF_BEST_EN, TF_BEST_ES, TF_BEST_OTHER_EN, TF_BEST_OTHER_ES))
        obj['best'] = filter_best(fill_values(answers_arr, TF_BEST_EN, TF_BEST_ES))
        obj['best_other'] = fill_values(answers_arr, TF_BEST_OTHER_EN, TF_BEST_OTHER_ES)

        iter_obj['worst'] = filter_worst(fill_values_other(answers_arr, TF_WORST_EN, TF_WORST_ES, TF_WORST_OTHER_EN, TF_WORST_OTHER_ES))
        obj['worst'] = filter_worst(fill_values(answers_arr, TF_WORST_EN, TF_WORST_ES))
        obj['worst_other'] = fill_values(answers_arr, TF_WORST_OTHER_EN, TF_WORST_OTHER_ES)

        iter_obj['followup'] = fill_values(answers_arr, TF_FOLLOWUP_EN, TF_FOLLOWUP_ES)
        obj['follow_up'] = fill_values(answers_arr, TF_FOLLOWUP_EN, TF_FOLLOWUP_ES)

        iter_obj['contact'] = fill_values(answers_arr, TF_CONTACT_EN, TF_CONTACT_ES)
        obj['contact'] = fill_values(answers_arr, TF_CONTACT_EN, TF_CONTACT_ES)

        iter_obj['morecomments'] = fill_values(answers_arr, TF_COMMENTS_EN, TF_COMMENTS_ES)
        obj['more_comments'] = fill_values(answers_arr, TF_COMMENTS_EN, TF_COMMENTS_ES)

        iter_obj['role'] = filter_role(fill_values(answers_arr, TF_ROLE_EN, TF_ROLE_ES))
        obj['role'] = filter_role(fill_values(answers_arr, TF_ROLE_EN, TF_ROLE_ES))

        iter_obj['purpose'] = filter_purpose(fill_values_other(answers_arr, TF_PURP_EN, TF_PURP_ES, TF_PURP_OTHER_EN, TF_PURP_OTHER_ES))
        obj['purpose'] = filter_purpose(fill_values(answers_arr, TF_PURP_EN, TF_PURP_ES))
        obj['purpose_other'] = fill_values(answers_arr, TF_PURP_OTHER_EN, TF_PURP_OTHER_ES)

        # print fill_values(answers_arr, TF_ROUTE_EN, TF_ROUTE_ES)
        iter_obj['route'] = fill_values(answers_arr, TF_ROUTE_EN, TF_ROUTE_ES)
        try:
            obj['route'] = ROUTES[fill_values(answers_arr, TF_ROUTE_EN, TF_ROUTE_ES)]
        except KeyError:
            obj['route'] = None

        typeform_data = slice_data(pic_schema, obj)
        typeform_surveys.append(typeform_data)
        #find_record = Survey.query.filter_by(source_id=typeform_data['source_id']).first()
        #if find_record is None:
        #    typeform_surveys.append(typeform_data)
        #
        survey_table.append(iter_obj)

    typeform_surveys, errors = pic_schema.load(typeform_surveys, many=True, session=db.session)
    if errors:
        print errors

    db.session.add_all(typeform_surveys)
    db.session.commit()

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
    i = [str(x['purpose']) for x in survey_table if x['purpose']]
    return Counter(i).most_common()


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
    # print role, arr
    return np.mean(arr)


def get_rating_by_purpose(survey_table, purpose):
    arr = [x['rating'] for x in survey_table if str(purpose) == str(x['purpose'])]
    arr = [int(x) for x in arr if x.isdigit()]
    return np.mean(arr)


def slice_data(schema, data):
    keys = []
    for name, field in schema.fields.items():
        if field.load_from:
            keys.append(field.load_from)
        else:
            keys.append(name)
    sliced = {k:data[k] for k in keys if k in data}
    return sliced


@cache.memoize(timeout=3600)
def get_all_survey_responses(days):
    survey_table = []
    timestamp = datetime.date.today() - datetime.timedelta(days)

    # TYPEFORM API CALLS
    json_result = make_typeform_call(timestamp)
    # print json_result
    survey_table = parse_typeform(survey_table, json_result)

    # TEXTIT API CALLS
    sms_result = make_textit_call(timestamp)
    survey_table = parse_textit(survey_table, sms_result)

    # print survey_table
    return survey_table
