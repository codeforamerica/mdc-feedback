 # -*- coding: utf-8 -*-

import datetime
import requests

from feedback.utils import utc_to_local

TYPEFORM_API = 'https://api.typeform.com/v0/form/aaz1iK?key='
TYPEFORM_API_KEY = '433dcf9fb24804b47666bf62f83d25dbef2f629d'

TF_OPINION_EN = 'opinionscale_9825055'
TF_OPINION_ES = 'opinionscale_9825056'

TF_BESTWORST_EN = 'textarea_9825061'
TF_BESTWORST_ES = 'textarea_9825064'

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


def fill_typeform_purpose(results):
    '''
    Returns an array of integers for purposes mapped to the possible purposes. If there is a string that means someone typed in a result in the "other" column
    '''
    return_array = []

    if TF_PURP_PERMIT_EN in results or TF_PURP_PERMIT_ES in results:
        return_array.append(1)
    if TF_PURP_INSPECTOR_EN in results or TF_PURP_INSPECTOR_ES in results:
        return_array.append(2)
    if TF_PURP_PLANREVIEW_EN in results or TF_PURP_PLANREVIEW_ES in results:
        return_array.append(3)
    if TF_PURP_VIOLATION_EN in results or TF_PURP_VIOLATION_ES in results:
        return_array.append(4)
    if TF_PURP_CU_ES in results or TF_PURP_CU_ES in results:
        return_array.append(5)
    if TF_PURP_OTHER_EN in results:
        return_array.append(results[TF_PURP_OTHER_EN])
    if TF_PURP_OTHER_ES in results:
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
        iter_obj['date'] = survey_response['metadata']['date_submit']
        iter_obj['firsttime'] = fill_values(answers_arr, 'yesno_9825058', 'yesno_9825060')
        iter_obj['getdone'] = fill_values(answers_arr, 'yesno_9825057', 'yesno_10444681')
        iter_obj['rating'] = fill_values(answers_arr, TF_OPINION_EN, TF_OPINION_ES)
        iter_obj['improvement'] = fill_values(answers_arr, 'textarea_9825062', 'textarea_9825065')
        iter_obj['bestworst'] = fill_values(answers_arr, TF_BESTWORST_EN, TF_BESTWORST_ES)

        # FIXME: THERE'S NO FOLLOW UP IN THE WEB FORM
        iter_obj['followup'] = fill_values(answers_arr, '', '')

        iter_obj['morecomments'] = fill_values(answers_arr, 'textarea_9825063', 'textarea_9825066')
        iter_obj['role'] = fill_values(answers_arr, 'list_9825053_choice', 'list_9825054_choice')
        iter_obj['purpose'] = fill_typeform_purpose(answers_arr)
        survey_table.append(iter_obj)

    return survey_table


def get_typeform_by_meta(json_result):
    web_en = 0
    web_es = 0
    total = 0

    for survey_response in json_result['responses']:
        try:
            ans = survey_response['answers'][TF_OPINION_EN]
            web_en = web_en + 1
        except KeyError:
            try:
                ans = survey_response['answers'][TF_OPINION_ES]
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
