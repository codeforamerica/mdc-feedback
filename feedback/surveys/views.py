# -*- coding: utf-8 -*-

import pprint

from flask import (
    Blueprint, render_template, redirect,
    url_for, flash, request
)
from feedback.database import db

from flask.ext.login import login_required

from feedback.surveys.constants import ROUTES
from feedback.surveys.models import Stakeholder


blueprint = Blueprint(
    'surveys',
    __name__,
    url_prefix='/surveys',
    static_folder="../static")


def process_stakeholders_form(form):
    print form
    for i in range(1, 15):
        label = ROUTES[i]
        key = 'field-route-' + str(i)
        value = request.form[key]
        # FIXME: I'd validate these values later. Value contains a list of e-mails.

        stakeholder = db.session.query(Stakeholder).filter_by(label=label).first()
        if not stakeholder:
            stakeholder = Stakeholder(
                label=label
            )

        stakeholder.email_list = value
        # And from here I want to either GET or CREATE.
        db.session.add(stakeholder)
    db.session.commit()


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def survey_index():
    # from here figure out if you posted the form
    if request.method == 'POST':
        process_stakeholders_form(request.form)

    stakeholders = Stakeholder.query.all()
    return render_template(
        "surveys/edit-stakeholders.html",
        routes=ROUTES,
        stakeholders=stakeholders)
