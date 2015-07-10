from flask import Flask, render_template, request, redirect, url_for, current_app, abort, flash
from flask.ext.sqlalchemy import SQLAlchemy
from forms import SurveyForm, ProfileForm
from wtforms import fields
from pprint import pprint
from flask.ext.login import login_user, logout_user, login_required
from flask_login import LoginManager, current_user
from utils import thispage

import urllib
import urllib2
import os
import requests
import json

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import Survey, Question, User

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(email=id).first()

app.jinja_env.globals['thispage'] = thispage

@app.route('/login', methods=['GET'])
def login():
    return render_template("users/login.html", current_user=current_user)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    if request.args.get('persona', None):
        return 'OK'
    else:
        flash('Logged out successfully!', 'alert-success')
        return render_template('users/logout.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    form = ProfileForm(
        first_name=current_user.first_name,
        last_name=current_user.last_name
    )

    if form.validate_on_submit():

        user = User.query.get(current_user.email)
        data = request.form

        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        db.session.commit()

        flash('Updated your profile!', 'alert-success')
        data = data.to_dict().pop('csrf_token', None)
        print ('PROFILE UPDATE: Updated profile for {email} with {data}'.format(
            email=user.email, data=data
        ))

        return redirect(url_for('profile'))

    return render_template('users/profile.html', form=form, user=current_user)

@app.route('/auth', methods=['POST'])
def auth():
    '''
    Endpoint from AJAX request for authentication from persona
    '''

    data = urllib.urlencode({
        'assertion': request.form.get('assertion'),
        'audience': current_app.config.get('BROWSERID_URL')
    })
    req = urllib2.Request('https://verifier.login.persona.org/verify', data)

    response = json.loads(urllib2.urlopen(req).read())
    if response.get('status') != 'okay':
        print('REJECTEDUSER: User login rejected from persona. Messages: {}'.format(response))
        abort(403)

    next_url = request.args.get('next', None)
    email = response.get('email')
    user = User.query.filter(User.email == email).first()

    domain = email.split('@')[1] if len(email.split('@')) > 1 else None

    if user:
        login_user(user)
        flash('Logged in successfully!', 'alert-success')

        print('LOGIN: User {} logged in successfully'.format(user.email))
        return next_url if next_url else '/'
    else:
        user = User.create(email=email)
        login_user(user)

        print('NEWUSER: New User {} successfully created'.format(user.email))
        return '/users/profile'

    # FIXME - unhook this, set CITY_DOMAIN to miamidade.gov
    '''
    elif domain == current_app.config.get('CITY_DOMAIN'):
        user = User.create(email=email)
        login_user(user)

        print('NEWUSER: New User {} successfully created'.format(user.email))
        return '/users/profile'

    else:
        print('NOTINDB: User {} not in DB -- aborting!'.format(email))
        abort(403)
    '''

@app.route('/surveys')
def surveys():
    errors = []
    results = Survey.query.order_by(Survey.id).all()

    return render_template('surveys.html', errors=errors, results=results)

@app.route('/surveys/add', methods=['GET', 'POST'])
@login_required
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
    return render_template('survey-add.html', action=action, errors=errors, form=form, results=results)

# http://stackoverflow.com/questions/30677515/wtform-does-not-entirely-repopulate-form-data-upon-editing-a-model

@app.route('/surveys/edit/<int:survey_id>', methods=['GET', 'POST'])
@login_required
def surveys_edit(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    # survey_questions = []

    # for question in survey.questions:
    #    survey_questions.append(question.id)

    action = '/surveys/edit/' + str(survey_id)
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

@app.route('/surveys/run/<int:survey_id>')
def surveys_run(survey_id):
    return render_template('trigger.html')

@app.route('/')
def index():
    # API = 'https://api.typeform.com/v0/form/UYZYtI?key=433dcf9fb24804b47666bf62f83d25dbef2f629d&completed=true'
    # response = requests.get(API)
    # json = response.json()
    # print json['stats']['responses']
    errors = []
    return render_template('index.html', errors=errors)

if __name__ == '__main__':
    app.run()

