# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""

import json
import urllib

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

from flask import (
    Blueprint, request, render_template, flash,
    current_app, abort, redirect
)

from flask.ext.login import current_user, login_user, login_required, logout_user
from feedback.extensions import login_manager
from feedback.user.models import User
# from feedback.public.forms import LoginForm
# from feedback.user.forms import RegisterForm
from feedback.utils import flash_errors

blueprint = Blueprint('public', __name__, static_folder="../static")


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(email=id).first()


@blueprint.route('/login', methods=['GET'])
def login():
    return render_template("user/login.html", current_user=current_user)


@blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    if request.args.get('persona', None):
        return 'OK'
    else:
        flash('You are logged out.', 'info')
        return render_template('user/logout.html')


@blueprint.route('/auth', methods=['POST'])
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
    current_app.logger.debug('LOGIN: status from persona: {}'.format(response))
    if response.get('status') != 'okay':
        current_app.logger.debug('REJECTEDUSER: User login rejected from persona. Messages: {}'.format(response))
        # abort(403)
        # FIXME - we think abort is FUBARing staging
        return '/login-error'

    next_url = request.args.get('next', None)
    email = response.get('email')
    user = User.query.filter(User.email == email).first()

    domain = email.split('@')[1] if len(email.split('@')) > 1 else None

    if user:
        login_user(user)
        flash('Logged in successfully!', 'alert-success')

        current_app.logger.debug('LOGIN: User {} logged in successfully'.format(user.email))
        # FIXME - I think returning next_url is FUBARing staging. Address this later.
        # return next_url if next_url else '/'
        return '/'

    # FIXME - originally domain == current_app.config.get('CITY_DOMAIN'):
    elif domain is not None:
        user = User.create(email=email)
        login_user(user)

        current_app.logger.debug('NEWUSER: New User {} successfully created'.format(user.email))
        return '/users/profile'

    else:
        current_app.logger.debug('NOTINDB: User {} not in DB -- aborting!'.format(email))
        return '/users/profile'


@blueprint.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User.create(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data,
                        active=True)
        flash("Thank you for registering. You can now log in.", 'success')
        return redirect('/')
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form, title='Register')


@blueprint.route("/admin/",  methods=['GET'])
def admin():
    return render_template("public/admin.html", title='Admin')


@blueprint.route("/create-survey/",  methods=['GET'])
def create_survey():
    return render_template("public/create-survey.html", title='Survey Builder')


@blueprint.route("/saved-survey/",  methods=['GET'])
def save_survey():
    return render_template("public/saved-survey.html", title='Survey Builder')


@blueprint.route("/manage-users/",  methods=['GET'])
def manage_users():
    return render_template("public/manage-users.html", title='Manage Users')
    
@blueprint.route("/violations-detail/",  methods=['GET'])
def violations_detail():
    return render_template("public/violations-detail.html", title='Violations by Type: Detail')
