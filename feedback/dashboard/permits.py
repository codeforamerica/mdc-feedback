 # -*- coding: utf-8 -*-

import datetime
import requests
import numpy as np


def json_to_dateobj(jsondate):
    '''
    Take a string of format 2015-07-29T00:00:00 and return a datetime obj
    '''
    return datetime.datetime.strptime(jsondate, '%Y-%m-%dT%H:%M:%S')


def lifespan_api_call(arg1=0, arg2=30, property_type='c'):
    '''
    Run the API call between arg1 days ago and arg2 days ago.
    property_type should either be 'r', 'h' or 'c'. If it's an 'h',
    we take out the residential_commercial clause and we'll check
    if it's an owner/builder, if "contractor_name" = 'OWNER.'
    Defaults to 'c'
    Return the integer mean lifespan.
    '''
    days_0 = (datetime.date.today() - datetime.timedelta(arg1)).strftime("%Y-%m-%d")
    days_30 = (datetime.date.today() - datetime.timedelta(arg2)).strftime("%Y-%m-%d")

    API = 'https://opendata.miamidade.gov/resource/kw55-e2dj.json?$where=co_cc_date%20%3E=%20%27' + days_30 + '%27%20AND%20co_cc_date%20<%20%27' + days_0 + '%27%20AND%20'
    if property_type == 'h':
        API = API + 'contractor_name=%27OWNER%27'
    else:
        API = API + 'residential_commercial%20=%20%27' + property_type + '%27'
    API = API + '&$order=co_cc_date%20desc'
    response = requests.get(API)
    json_result = response.json()
    lifespan_array = []
    application_to_permit_array = []

    for resp in json_result:
        start_date = json_to_dateobj(resp['application_date'])
        permit_date = json_to_dateobj(resp['permit_issued_date'])

        end_date = json_to_dateobj(resp['co_cc_date'])

        lifespan_array.append((end_date-start_date).days)
        application_to_permit_array.append((permit_date-start_date).days)
        # permit_to_close_array.append((end_date-permit_date).days)

    # print np.mean(lifespan_array), np.mean(application_to_permit_array), np.mean(permit_to_close_array)
    return np.mean(lifespan_array), np.mean(application_to_permit_array)


def get_avg_cost(property_type='c'):
    '''
    property_type should either be 'r', 'h' or 'c'. Defaults to 'c'.
    Returns an integer
    '''
    API = 'https://opendata.miamidade.gov/resource/kw55-e2dj.json?$select=AVG(permit_total_fee)&$where='
    if property_type == 'h':
        API = API + 'contractor_name=%27OWNER%27'
    else:
        API = API + 'residential_commercial%20=%20%27' + property_type + '%27'
    API = API + '%20and%20co_cc_date%20IS%20NULL'

    response = requests.get(API)
    result = response.json()
    return result[0]['avg_permit_total_fee']


def get_permit_types(arg1=0, arg2=30):
    '''
    This should print out the pie chart of all permit types.
    Defaults from 0 to 30 days but you can change it in
    arg1 and arg2. The entire JSON should be printed out
    so that the graph can be created in JS.
    '''
    days_0 = (datetime.date.today() - datetime.timedelta(arg1)).strftime("%Y-%m-%d")
    days_30 = (datetime.date.today() - datetime.timedelta(arg2)).strftime("%Y-%m-%d")

    API = 'https://opendata.miamidade.gov/resource/kw55-e2dj.json?$select=permit_type,%20count(*)&$group=permit_type&$where=application_date%20%3E=%20%27' + days_30 + '%27%20AND%20application_date%20<%20%27' + days_0 + '%27'
    response = requests.get(API)
    json_result = response.json()
    return json_result


def get_lifespan(property_type='c'):
    '''
    property_type should either be 'r', 'h' or 'c'. Defaults to 'c'.
    Returns an object:
        val = the current lifespace
        yoy = the year over year increase or decrease (100 to -100)
    '''

    lifespan_now, waittime_now = lifespan_api_call(0, 30, property_type)
    lifespan_then, waittime_then = lifespan_api_call(30, 60, property_type)
    yoy = ((lifespan_now-lifespan_then)/lifespan_then)*100

    # print lifespan_now, lifespan_then, yoy
    return {
        'val': int(lifespan_now),
        'waittime': waittime_now * 0.03333333,
        'yoy': yoy
    }
