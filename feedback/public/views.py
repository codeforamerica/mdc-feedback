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
    current_app, abort
)

from flask.ext.login import current_user, login_user, logout_user
from feedback.extensions import login_manager
from feedback.user.models import User

blueprint = Blueprint('public', __name__, static_folder="../static")


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(email=id).first()


@blueprint.route('/login', methods=['GET'])
def login():
    return render_template("user/login.html", current_user=current_user)


@blueprint.route('/logout', methods=['GET', 'POST'])
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
    current_app.logger.debug(
        'LOGIN: status from persona: {}'.format(response))
    if response.get('status') != 'okay':
        current_app.logger.debug(
            'REJECTEDUSER: User login rejected from persona. Messages: {}'.format(response))
        abort(403)

    next_url = request.args.get('next', None)
    email = response.get('email')
    user = User.query.filter(User.email == email).first()

    domain = email.split('@')[1] if len(email.split('@')) > 1 else None

    if user:
        login_user(user)
        flash('Logged in successfully!', 'alert-success')

        current_app.logger.debug(
            'LOGIN: User {} logged in successfully'.format(user.email))
        return next_url if next_url else '/'

    elif domain in current_app.config.get('CITY_DOMAINS'):
        user = User.create(email=email)
        login_user(user)

        current_app.logger.debug(
            'NEWUSER: New User {} successfully created'.format(user.email))
        return '/'

    else:
        current_app.logger.debug(
            'NOTINDB: User {} not in DB -- aborting!'.format(email))
        abort(403)
