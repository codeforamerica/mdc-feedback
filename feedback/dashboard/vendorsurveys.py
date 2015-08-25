 # -*- coding: utf-8 -*-

import requests
from flask import current_app

TYPEFORM_API = 'https://api.typeform.com/v0/form/UYZYtI?key='
TYPEFORM_API_KEY = '433dcf9fb24804b47666bf62f83d25dbef2f629d'

TEXTIT_API = 'https://textit.in/api/v1/runs.json?flow_uuid='
TEXTIT_UUID_EN = 'cd8cd1b5-ab4c-4c85-b623-9f28c56cc753'
TEXTIT_UUID_ES = 'abc55a5c-2d4a-468f-ae76-a5a1e31865e0'
TEXTIT_AUTH_KEY = '41a75bc6977c1e0b2b56d53a91a356c7bf47e3e9'


def make_typeform_call(timestamp):
    '''
    Takes in the timestamp in unix form
    Returns the JSON of the actual API. Let's just start simple.
    '''
    unix_time = timestamp.strftime("%s")

    API = TYPEFORM_API + TYPEFORM_API_KEY + '&completed=true&since=' + unix_time
    current_app.logger.debug('TYPEFORM API: {}'.format(API))

    response = requests.get(API)
    json_result = response.json()
    return json_result


def make_textit_call(timestamp):
    '''
    Takes in the timestamp in unix form
    Returns the JSON of the actual API.
    '''
    sms_query_date = timestamp.strftime("%Y-%m-%dT%H:%M:%S.000")

    SMS_API = TEXTIT_API + TEXTIT_UUID_ES + ',' + TEXTIT_UUID_EN + '&after=' + sms_query_date
    current_app.logger.debug('TEXTIT API: {}'.format(SMS_API))

    response2 = requests.get(SMS_API, headers={'Authorization': 'Token ' + TEXTIT_AUTH_KEY})

    json_result = response2.json()
    # print json_result
    return json_result
