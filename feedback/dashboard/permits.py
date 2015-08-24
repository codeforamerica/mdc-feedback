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
    property_type should either be 'r' or 'c'. Defaults to 'c'
    Return the integer mean lifespan.
    '''
    days_0 = (datetime.date.today() - datetime.timedelta(arg1)).strftime("%Y-%m-%d")
    days_30 = (datetime.date.today() - datetime.timedelta(arg2)).strftime("%Y-%m-%d")

    API = 'https://opendata.miamidade.gov/resource/kw55-e2dj.json?$where=co_cc_date%20%3E=%20%27' + days_30 + '%27%20AND%20co_cc_date%20<%20%27' + days_0 + '%27%20AND%20residential_commercial%20=%20%27' + property_type + '%27&$order=co_cc_date%20desc'
    response = requests.get(API)
    json_result = response.json()
    lifespan_array = []

    for resp in json_result:
        start_date = json_to_dateobj(resp['application_date'])
        end_date = json_to_dateobj(resp['co_cc_date'])
        # print resp['permit_number'], resp['application_date'], resp['co_cc_date'], (end_date-start_date).days
        lifespan_array.append((end_date-start_date).days)

    # print np.mean(lifespan_array), np.median(lifespan_array)
    return np.mean(lifespan_array)


def get_lifespan(property_type='c'):
    '''
    property_type should either be 'r' or 'c'. Defaults to 'c'.
    Returns an object:
        val = the current lifespace
        yoy = the year over year increase or decrease (100 to -100)
    '''

    lifespan_now = lifespan_api_call(0, 30, property_type)
    lifespan_then = lifespan_api_call(30, 60, property_type)
    yoy = ((lifespan_now-lifespan_then)/lifespan_then)*100

    # print lifespan_now, lifespan_then, yoy
    return {
        'val': int(lifespan_now),
        'yoy': yoy
    }
