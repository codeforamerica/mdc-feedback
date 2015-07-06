from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from forms import SurveyForm
from wtforms import fields
from pprint import pprint

import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import Survey, Question


@app.route('/surveys')
def surveys():
    errors = []
    results = Survey.query.order_by(Survey.id).all()

    return render_template('surveys.html', errors=errors, results=results)

@app.route('/surveys/add', methods=['GET', 'POST'])
def surveys_add():
    errors = []
    results = {}
    action = '/surveys/add'

    # For dynamic forms, class attributes must be set before any instantiation occurs.
    # you don't have to pass request.form to Flask-WTF; it will load automatically

    class F(SurveyForm):
        pass

    F.question_en = fields.TextField()
    F.question_es = fields.TextField()
    F.question_type = fields.SelectField(choices=[('short_text', 'Short Text')])

    form = F()

    pprint (vars(form))
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
    return render_template('survey-add.html', action=action, errors=errors, form=form, results=results)

# http://stackoverflow.com/questions/30677515/wtform-does-not-entirely-repopulate-form-data-upon-editing-a-model

@app.route('/surveys/edit/<int:survey_id>', methods=['GET', 'POST'])
def surveys_edit(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    # survey_questions = []

    # for question in survey.questions:
    #    survey_questions.append(question.id)

    action = '/surveys/edit/' + `survey_id`
    errors = []

    # For dynamic forms, class attributes must be set before any instantiation occurs.
    # setattr(SurveyForm, 'q1', fields.TextField())

    # form = SurveyForm(obj=survey)
    # form = SurveyForm.append_field('question_en', fields.TextField())(obj=survey)

    class F(SurveyForm):
        pass


    # FIX ME: Make this into a loop and dynamically add in more survey questions

    F.question_en = fields.TextField()
    F.question_es = fields.TextField()
    F.question_type = fields.SelectField(choices=[('short_text', 'Short Text')])

    # FIX ME: TOTALLY CHEATING! This can't be hardcoded obviously.
    survey.question_en = survey.questions[0].question_en
    survey.question_es = survey.questions[0].question_es
    survey.question_type = survey.questions[0].question_type

    form = F(obj=survey)

    if form.validate_on_submit():

        # Write survey metadata to survey database
        try:
            survey.title_en = form.title_en.data
            survey.title_es = form.title_es.data
            survey.description_en = form.description_en.data
            survey.description_es = form.description_es.data

            # FIXME
            survey.questions[0].question_en = form.question_en.data
            survey.questions[0].question_es = form.question_es.data
            survey.questions[0].question_type = form.question_type.data

            db.session.commit()
        except:
            errors.append("Unable to edit to the database.")

        # Iterate on questions


        return redirect('/surveys')

    return render_template('survey-add.html', action=action, errors=errors, form=form)

@app.route('/')
def index():
    errors = []
    results = Survey.query.order_by(Survey.id).all()

    return render_template('index.html', errors=errors, results=results)

if __name__ == '__main__':
    app.run()

