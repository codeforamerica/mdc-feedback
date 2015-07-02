from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from forms import SurveyForm

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

    # you don't have to pass request.form to Flask-WTF; it will load automatically
    form = SurveyForm()

    if form.validate_on_submit():

        # Write survey metadata to survey database
        try:
            survey = Survey(
                title_en = form.title_en.data,
                title_es = form.title_es.data,
                description_en = form.description_en.data,
                description_es = form.description_es.data
            )
            db.session.add(survey)
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

    action = '/surveys/edit/' + `survey_id`
    errors = []

    form = SurveyForm(obj=survey)
    if form.validate_on_submit():

        # Write survey metadata to survey database
        try:
            survey.title_en = form.title_en.data
            survey.title_es = form.title_es.data
            survey.description_en = form.description_en.data
            survey.description_es = form.description_es.data

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

