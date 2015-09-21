 # -*- coding: utf-8 -*-

import requests

TYPEFORM_API = 'https://api.typeform.com/v0/form/aaz1iK?key='
TYPEFORM_API_KEY = '433dcf9fb24804b47666bf62f83d25dbef2f629d'

TF_OPINION_EN = 'opinionscale_9825055'
TF_OPINION_ES = 'opinionscale_9825056'

TF_BESTWORST_EN = 'textarea_9825061'
TF_BESTWORST_ES = 'textarea_9825064'

TF_ROLE_CONTRACTOR_EN = 'list_10432251_choice_12738830'
TF_ROLE_ARCHITECT_EN = 'list_10432251_choice_12738831'
TF_ROLE_PERMITCONSULT_EN = 'list_10432251_choice_12738832'
TF_ROLE_HOMEOWNER_EN = 'list_10432251_choice_12738833'
TF_ROLE_BIZOWNER_EN = 'list_10432251_choice_12738834'
TF_ROLE_OTHER_EN = 'list_10432251_other'

TF_ROLE_CONTRACTOR_ES = 'list_10444324_choice_12758795'
TF_ROLE_ARCHITECT_ES = 'list_10444324_choice_12758796'
TF_ROLE_PERMITCONSULT_ES = 'list_10444324_choice_12758797'
TF_ROLE_HOMEOWNER_ES = 'list_10444324_choice_12758798'
TF_ROLE_BIZOWNER_ES = 'list_10444324_choice_12758799'
TF_ROLE_OTHER_ES = 'list_10444324_other'

TEXTIT_API = 'https://textit.in/api/v1/runs.json?flow_uuid='
TEXTIT_UUID_EN = '920cec13-ffc0-4fe9-92c3-1cced2073498'
TEXTIT_UUID_ES = '7001c507-1c9e-46dd-aea3-603b986c3d89'
TEXTIT_AUTH_KEY = '41a75bc6977c1e0b2b56d53a91a356c7bf47e3e9'


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


def fill_typeform_purpose(results):
    '''
    Returns an array of integers for purposes mapped to the possible purposes. If there is a string that means someone typed in a result in the "other" column
    '''
    return_array = []

    if TF_ROLE_CONTRACTOR_EN in results or TF_ROLE_CONTRACTOR_ES in results:
        return_array.append(1)
    if TF_ROLE_ARCHITECT_EN in results or TF_ROLE_ARCHITECT_ES in results:
        return_array.append(2)
    if TF_ROLE_PERMITCONSULT_EN in results or TF_ROLE_PERMITCONSULT_ES in results:
        return_array.append(3)
    if TF_ROLE_HOMEOWNER_EN in results or TF_ROLE_HOMEOWNER_ES in results:
        return_array.append(4)
    if TF_ROLE_BIZOWNER_EN in results or TF_ROLE_BIZOWNER_ES in results:
        return_array.append(5)
    if TF_ROLE_OTHER_EN in results:
        return_array.append(results[TF_ROLE_OTHER_EN])
    if TF_ROLE_OTHER_ES in results:
        return_array.append(results[TF_ROLE_OTHER_ES])

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
