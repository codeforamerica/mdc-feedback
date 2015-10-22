 # -*- coding: utf-8 -*-

import math
import datetime
import requests
import requests_cache
import numpy as np

from feedback.extensions import cache
from dateutil.relativedelta import *


requests_cache.install_cache()

API_URL = 'https://opendata.miamidade.gov/resource/vvjq-pfmc.json'
VIOLATIONS_URL = 'https://opendata.miamidade.gov/resource/tzia-umkx.json'
DATA311_URL = 'https://opendata.miamidade.gov/resource/dj6j-qg5t.json'


PERMITS_API_URL = API_URL + '?%24select=date_trunc_ym(permit_issued_date)%20as%20month,count(*)%20as%20total&%24group=month&%24order=month%20desc&%24limit=12&$where=starts_with(process_number,%27C%27)%20AND%20master_permit_number=0%20AND%20category1%20not%20in(%270092%27,%20%270095%27,%20%270096%27,%20%270103%27,%20%270107%27)%20AND%20permit_type=%27BLDG%27&%24offset=1'

VIOLATIONS_API_URL = VIOLATIONS_URL + '?$select=date_trunc_ym(ticket_created_date_time)%20AS%20month,%20count(*)%20AS%20total&$group=month&$order=month%20desc&$limit=12&$offset=1'
VIOLATIONS_LOCATIONS_API_URL = VIOLATIONS_URL + '?$where=ticket_created_date_time%20%3E%20%272015-01-01%27'
VIOLATIONS_BY_TYPE_API_URL = DATA311_URL + '?&case_owner=Regulatory_and_Economic_Resources&$select=issue_type,%20count(*)%20AS%20total&$group=issue_type&$where=ticket_created_date_time%20%3E=%20%272015-01-01%27'

p_days_30 = (datetime.date.today() - datetime.timedelta(30)).strftime("%Y-%m-%d")
p_month = datetime.datetime.now() - relativedelta(months=1)
p_month = p_month.strftime("%Y-%m-01")

VIOLATIONS_LAST_30 = VIOLATIONS_URL + '?$select=issue_type%2C%20street_address%2C%20city%2C%20ticket_status%2C%20location%2C%20method_received%2C%20ticket_last_updated_date_time%2C%20ticket_closed_date_time&$where=ticket_created_date_time%3E%27' + p_days_30 + '%27&$limit=50000'

VIOLATIONS_PREV_MONTH = VIOLATIONS_URL + '?$select=issue_type%2C%20street_address%2C%20city%2C%20ticket_status%2C%20location%2C%20method_received%2C%20ticket_last_updated_date_time%2C%20ticket_closed_date_time&$where=ticket_created_date_time%3E%27' + p_month + '%27&$limit=50000'


def api_health():
    '''
    Run the API to see if its even working.
    If it is, pass 1.
    If the county did a bad import, pass -1.
    If Socrata is down, the HTTP result code. (404, 500, etc)
    '''
    OK = 1
    COUNTY_EMPTY_DATA = -1

    r = requests.get(API_URL)
    if r.status_code == requests.codes.ok:
        json = r.json()
        if len(json[0]) == 0:
            # print 'EMPTY'
            return COUNTY_EMPTY_DATA
        else:
            # print 'OK'
            return OK
    else:
        # print 'socrataerr', r.status_code
        return r.status_code


def json_to_dateobj(jsondate):
    '''
    Take a string of format 2015-07-29T00:00:00 and return a datetime obj
    '''
    return datetime.datetime.strptime(jsondate, '%Y-%m-%dT%H:%M:%S.000')


@cache.memoize(timeout=86400)
def dump_socrata_api(datatype='p'):

    ''' For performance issues, have Sophia's AJAX calls
    get called on the server side instead.
    '''

    data_table = {
        'p': PERMITS_API_URL,
        'v': VIOLATIONS_API_URL,
        'vl': VIOLATIONS_LAST_30,
        'vm': VIOLATIONS_PREV_MONTH,
        'vt': VIOLATIONS_BY_TYPE_API_URL
    }
    response = requests.get(data_table.get(datatype))
    return response.json()


@cache.memoize(timeout=86400)
def lifespan_api_call(arg1=0, arg2=30, property_type='c'):
    '''
    Run the API call between arg1 days ago and arg2 days ago.
    property_type should either be 'r', 'h' or 'c'. If it's an 'h',
    we take out the residential_commercial clause and we'll check
    if it's an owner/builder, if "contractor_name" = 'OWNER.'
    Defaults to 'c'
    Return the integer mean lifespan.
    If the return value is -1 the API is down.
    '''
    days_0 = (datetime.date.today() - datetime.timedelta(arg1)).strftime("%Y-%m-%d")
    days_30 = (datetime.date.today() - datetime.timedelta(arg2)).strftime("%Y-%m-%d")

    API = API_URL + '?$where=category1%20not%20in(%270092%27,%20%270095%27,%20%270096%27,%20%270103%27,%20%270107%27)%20AND%20starts_with(process_number,%20%27C%27)%20AND%20master_permit_number=0%20AND%20permit_type=%27BLDG%27%20AND%20permit_issued_date%20%3E=%20%27' + days_30 + '%27%20AND%20permit_issued_date%20<%20%27' + days_0 + '%27%20AND%20'
    if property_type == 'h':
        API = API + 'contractor_name=%27OWNER%27'
    else:
        API = API + 'residential_commercial%20=%20%27' + property_type.upper() + '%27'
    API = API + '&$order=permit_issued_date%20desc'
    # print API
    response = requests.get(API)
    json_result = response.json()

    lifespan_array = []

    for resp in json_result:
        start_date = json_to_dateobj(resp['application_date'])
        permit_date = json_to_dateobj(resp['permit_issued_date'])

        lifespan_array.append((permit_date-start_date).days)
        # permit_to_close_array.append((end_date-permit_date).days)

    result1 = np.mean(lifespan_array)
    max_val = np.amax(lifespan_array)
    min_val = np.amin(lifespan_array)

    if not math.isnan(result1):
        return result1, max_val, min_val
    else:
        return -1, 0, 0


@cache.memoize(timeout=86400)
def get_permit_types(arg1=0, arg2=30):
    '''
    This should print out the pie chart of all permit types.
    Defaults from 0 to 30 days but you can change it in
    arg1 and arg2. The entire JSON should be printed out
    so that the graph can be created in JS.
    '''
    days_0 = (datetime.date.today() - datetime.timedelta(arg1)).strftime("%Y-%m-%d")
    days_30 = (datetime.date.today() - datetime.timedelta(arg2)).strftime("%Y-%m-%d")

    API = API_URL + '?$select=permit_type,%20count(*)&$group=permit_type&$where=permit_issued_date%20%3E=%20%27' + days_30 + '%27%20AND%20permit_issued_date%20<%20%27' + days_0 + '%27'
    response = requests.get(API)
    json_result = response.json()
    return json_result


@cache.memoize(timeout=86400)
def get_lifespan(property_type='c'):
    '''
    property_type should either be 'r', 'h' or 'c'. Defaults to 'c'.
    Returns an object:
        val = the current lifespace
        min = the mini
    '''
    lifespan_now, max_val, min_val = lifespan_api_call(0, 30, property_type)

    return {
        'val': int(lifespan_now),
        'max': max_val,
        'min': min_val
    }


@cache.memoize(timeout=86400)
def trade(arg1=30, arg2='PLUM'):
    days = (datetime.date.today() - datetime.timedelta(arg1)).strftime("%Y-%m-%d")

    API = API_URL + '?$select=count(*)%20as%20total&$where=application_date%3C%27' + days + '%27%20AND%20permit_type=%27' + arg2 + '%27'
    resp = requests.get(API)
    resp = resp.json()
    print API, resp
    total = float(resp[0]['total'])

    API = API_URL + '?$select=count(*)%20as%20total&&$where=application_date%3C%27' + days + '%27%20AND%20application_date=permit_issued_date&permit_type=%27' + arg2 + '%27'
    resp = requests.get(API)
    resp = resp.json()
    print API, resp
    sameday = float(resp[0]['total'])

    return {
        'total': total,
        'sameday': sameday,
        'percent': (sameday/total)*100
    }


@cache.memoize(timeout=86400)
def api_count_call(arg1=0, arg2=30, field=''):
    days_0 = (datetime.date.today() - datetime.timedelta(arg1)).strftime("%Y-%m-%d")
    days_30 = (datetime.date.today() - datetime.timedelta(arg2)).strftime("%Y-%m-%d")

    API = API_URL + '?$select=count(*)%20as%20total&$where=category1%20not%20in(%270092%27,%20%270095%27,%20%270096%27,%20%270103%27,%20%270107%27)%20AND%20starts_with(process_number,%20%27C%27)%20AND%20permit_type=%27BLDG%27%20AND%20master_permit_number=0%20AND%20' + field + '%20%3E%20%27' + days_30 + '%27%20AND%20' + field + '%20<%20%27' + days_0 + '%27'
    # print API
    response = requests.get(API)
    json_result = response.json()
    total = float(json_result[0]['total'])
    return total


@cache.memoize(timeout=86400)
def get_master_permit_counts(arg1):
    '''
    Run the API call of all master permits where
    date field arg1 is checked between 0-30 days
    ago and the same period a year previous.
    Returns an object:
        val = the current count
        yoy = the percentage increase or decrease
                  (100 to -100)
    '''
    now = api_count_call(0, 30, arg1)

    return {
        'val': int(now),
        'yoy': None
    }
