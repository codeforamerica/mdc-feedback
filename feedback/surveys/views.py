# -*- coding: utf-8 -*-

from flask import (
    Blueprint, render_template
)

from flask.ext.login import login_required

from feedback.surveys.forms import SurveyForm

from wtforms import fields

from feedback.extensions import login_manager
from feedback.surveys.models import Survey

blueprint = Blueprint('surveys', __name__, url_prefix='/surveys', static_folder="../static")

@blueprint.route('/')
@login_required
def survey_index():
    surveys = Survey.query.all()
    return render_template("surveys/survey-home.html", surveys=surveys)

@blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    errors = []
    results = {}
    action = 'surveys.create'


    # For dynamic forms, class attributes must be set before any instantiation occurs.
    # you don't have to pass request.form to Flask-WTF; it will load automatically

    class F(SurveyForm):
        pass

    F.question_en = fields.TextField()
    F.question_es = fields.TextField()
    F.question_type = fields.SelectField(choices=[('short_text', 'Short Text')])

    form = F()

    # pprint (vars(form))
    if form.validate_on_submit():

        # Write survey metadata to survey database
        try:
            survey = Survey(
                title_en = form.title_en.data,
                title_es = form.title_es.data,
                description_en = form.description_en.data,
                description_es = form.description_es.data
            )

            # Maybe it's something like
            # begin loop
            #   survey.questions.append(question)
            # (Taken from http://techarena51.com/index.php/one-to-many-relationships-with-flask-sqlalchemy/)

            db.session.add(survey)
            db.session.flush()

            question = Question(
                question_en = form.question_en.data,
                question_es = form.question_es.data,
                question_type = form.question_type.data,
                survey_id = survey.id
            )
            survey.questions.append(question)

            '''
            for field in form:
                print field.name

                # FIXME: This is totally wrong. This should be one iteration
                if field.name.startswith("q"):
                    print "attempting to write to question table"
                    print form.question_en.data, form.question_es.data, form.question_type.data, survey.id
                    question = Question(
                        question_en = form.question_en.data,
                        question_es = form.question_es.data,
                        question_type = form.question_type.data,
                        survey_id = survey.id
                    )
                    survey.questions.append(question)
            '''

            db.session.commit()
        except:
            errors.append("Unable to add to the database.")

        # Iterate on questions
        return redirect('/surveys')

    return render_template("surveys/survey-form.html", action=action,
                           errors=errors, form=form, results=results)

@blueprint.route('/<int:survey_id>/edit', methods=['POST'])
@login_required
def survey_edit(survey_id):
    pass
