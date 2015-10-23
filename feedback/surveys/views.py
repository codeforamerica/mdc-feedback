# -*- coding: utf-8 -*-

import re

from flask import (
    Blueprint, render_template,
    flash, request, redirect, url_for
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


def is_valid_email_list(value):

    value = [item.strip() for item in value.split(',') if item.strip()]
    email_list = list(set(value))

    for item in email_list:
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", item):
            flash("{0} is not a valid e-mail address.".format(item), "alert-danger")
            return False
    return True


def process_stakeholders_form(form):
    errors = False

    for i in range(1, 15):
        label = ROUTES[i]
        key = 'field-route-' + str(i)
        value = request.form[key]

        if is_valid_email_list(value):
            stakeholder = db.session.query(Stakeholder).filter_by(label=label).first()
            if not stakeholder:
                stakeholder = Stakeholder(
                    label=label,
                    email_list=value
                )
            else:
                stakeholder.update(
                    email_list=value
                )
            db.session.add(stakeholder)
        else:
            errors = True
            db.session.rollback()

    if not errors:
        db.session.commit()
        flash("Your settings have been saved.", "alert-success")
        return redirect(url_for('dashboard.home'))
    else:
        return redirect(url_for('surveys.survey_index'))


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def survey_index():
    # from here figure out if you posted the form
    if request.method == 'POST':
        return process_stakeholders_form(request.form)

    stakeholders = Stakeholder.query.order_by(Stakeholder.id).all()
    return render_template(
        "surveys/edit-stakeholders.html",
        routes=ROUTES,
        stakeholders=stakeholders)
