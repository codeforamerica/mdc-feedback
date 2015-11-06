# -*- coding: utf-8 -*-
# DO NOT DELETE
import StringIO
import csv

import datetime
today = datetime.date.today()

from flask import (
    Blueprint,
    make_response
)

from flask.ext.login import login_required

from sqlalchemy import desc

from feedback.surveys.models import Survey


blueprint = Blueprint(
    'surveys',
    __name__,
    url_prefix='/surveys',
    static_folder="../static")


@blueprint.route('/download')
@login_required
def to_csv():
    csvList = []
    csvList.append([
        'date_submitted',
        'method',
        'language',
        'route',
        'rating',
        'role',
        'get_done',
        'purpose',
        'best',
        'worst',
        'improvement',
        'follow_up',
        'contact',
        'more_comments'])

    survey_models = Survey.query.order_by(desc(Survey.date_submitted)).all()
    for survey_model in survey_models:
        csvList.append([
            survey_model.date_submitted,
            survey_model.method,
            survey_model.lang,
            survey_model.route_en,
            survey_model.rating,
            survey_model.role_en,
            survey_model.get_done,
            survey_model.purpose_en,
            survey_model.best_en,
            survey_model.worst_en,
            survey_model.improvement,
            survey_model.follow_up,
            survey_model.contact,
            survey_model.more_comments])

    strIO = StringIO.StringIO()
    writer = csv.writer(strIO)
    writer.writerows(csvList)

    output = make_response(strIO.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output
