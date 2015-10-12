 # -*- coding: utf-8 -*-

from feedback.extensions import cache

from feedback.surveys.constants import ROLES
from feedback.surveys.models import Survey

from collections import Counter

import numpy as np


def string_to_bool(arg):
    if arg[0].lower() in ['s', 'y', '1']:
        return True
    if arg[0].lower() == 'n':
        return False
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
            return array[es]
        except KeyError:
            return None


def filter_role(arg1):
    '''
    The role returns int. This is a filter that converts
    into integers for filter_table in the prase functions.
    Will try to find the first number if it's mixed e.g.
    "Number 5"
    Returns an integer or False if it doesn't know what
    to do with itself.
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
    ''' Take the hardcoded answers in English and Spanish
    and change them to constants. If there is a completely
    different purpose, it's a long form and return it as
    is. (We change to constants for graphic purposes.)
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


def get_surveys_by_role(survey_table):
    valid_roles = [x.role for x in survey_table]
    return Counter(valid_roles).most_common()


def get_surveys_by_completion(survey_table):
    items = [x.get_done for x in survey_table]
    return {
        "yes": items.count(True),
        "total": len(items)
    }


def get_surveys_by_purpose(survey_table):
    i = [str(x.purpose) for x in survey_table if x.purpose]
    #FIXME: THIS DOESN'T ADDRESS THE ISSUE OF "OTHER".
    return Counter(i).most_common()


def get_rating_scale(survey_table):
    ''' Given the table of all the responses,
    find the values of all roles.
    '''
    return np.mean([x.rating for x in survey_table])


def get_rating_by_lang(survey_table, lang='en'):
    return np.mean([x.rating for x in survey_table if x.lang == lang])


def get_rating_by_role(survey_table, role):
    return np.mean([x.rating for x in survey_table if x.role == role])


def get_rating_by_purpose(survey_table, purpose):
    arr = [x.rating for x in survey_table if str(purpose) == str(x.purpose)]
    return np.mean(arr)


@cache.memoize(timeout=3600)
def get_all_survey_responses(days):

    surveys = Survey.query.all()

    return surveys
