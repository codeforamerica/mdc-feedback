 # -*- coding: utf-8 -*-

from feedback.extensions import cache
from feedback.surveys.models import Survey

from collections import Counter

from sqlalchemy import desc

import numpy as np


def string_to_bool(arg):
    if arg[0].lower() in ['s', 'y', '1']:
        return True
    if arg[0].lower() == 'n':
        return False
    return None


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

    surveys = Survey.query.order_by(desc(Survey.date_submitted)).all()
    return surveys
