# -*- coding: utf-8 -*-

import pprint

from flask import (
    Blueprint, render_template, redirect,
    url_for, flash
)

from flask.ext.login import login_required


from wtforms import fields

from feedback.extensions import login_manager
from feedback.utils import flash_errors

from feedback.surveys.models import Survey
from feedback.surveys.forms import SurveyForm

blueprint = Blueprint('surveys', __name__, url_prefix='/surveys', static_folder="../static")

@blueprint.route('/')
@login_required
def survey_index():
    surveys = Survey.query.all()
    return render_template("surveys/survey-home.html", surveys=surveys)

@blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # For dynamic forms, class attributes must be set before any instantiation occurs.
    # you don't have to pass request.form to Flask-WTF; it will load automatically

    class F(SurveyForm):
        pass

    F.question_en = fields.TextField()
    F.question_es = fields.TextField()
    F.question_type = fields.SelectField(choices=[('short_text', 'Short Text')])
    form = F()

    if form.validate_on_submit():
        new_survey = Survey.create(
                        title_en = form.title_en.data,
                        title_es = form.title_es.data,
                        description_en = form.description_en.data,
                        description_es = form.description_es.data)
        flash("New survey created", 'success')
        return redirect(url_for('surveys.survey_index'))
    else:
        flash_errors(form)

    return render_template("surveys/survey-form.html", form=form)

@blueprint.route('/<int:survey_id>/edit', methods=['GET', 'POST'])
@login_required
def survey_edit(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    errors = []

    class F(SurveyForm):
        pass

    form = F(obj=survey)
    return render_template('surveys/survey-form.html', form=form)

