 # -*- coding: utf-8 -*-

import arrow
import numpy as np

from flask import (
    Blueprint, render_template
)
from feedback.surveys.models import Survey
from feedback.surveys.constants import ROUTES
from feedback.dashboard.vendorsurveys import (
    get_rating_scale
)

blueprint = Blueprint(
    "reports", __name__,
    url_prefix='/reports',
    template_folder='../templates',
    static_folder="../static"
)


@blueprint.context_processor
def processor():
    ''' Brings functions into the jinja2 templates.
    '''
    def count_field(survey_table, field, value):
        return len([getattr(x, field) for x in survey_table if getattr(x, field) == value])

    def list_all(survey_table, field='best_other'):
        return [getattr(x, field) for x in survey_table if getattr(x, field)]

    return dict(
        get_rating_scale=get_rating_scale,
        count_field=count_field,
        list_all=list_all
    )


@blueprint.route('/overview', methods=['GET'])
def overview():

    last_month = arrow.utcnow().replace(months=-1)
    date_start, date_end = last_month.span('month')
    sect = []

    reports = Survey.query.filter(
        Survey.date_submitted.between(
            date_start.format('YYYY-MM-DD'),
            date_end.format('YYYY-MM-DD')
        ))

    for n in range(1, 15):
        items = reports.filter(Survey.route == n).all()
        sect.append(
            dict(
                label=ROUTES[n],
                count=len(items),
                rating=np.mean([x.rating for x in items if x.rating]),
                getdone=len([x.get_done for x in items if x.get_done is True]),
                follow=len([x.follow_up for x in items if x.follow_up is True])))

    return render_template(
        "reports/overview.html",
        date_header=date_start.format('MMMM, YYYY'),
        surveys=reports.all(),
        section=sect)
