# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""

import json
import urllib
import urllib2

from flask import (
    Blueprint, request, render_template, flash, url_for,
    current_app, redirect, session
)

from flask.ext.login import current_user, login_user, login_required, logout_user
from feedback.extensions import login_manager
from feedback.user.models import User
from feedback.public.forms import LoginForm
# from feedback.user.forms import RegisterForm
from feedback.utils import flash_errors
from feedback.database import db

blueprint = Blueprint('public', __name__, static_folder="../static")

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(email=id).first()


@blueprint.route("/", methods=["GET", "POST"])
def home():
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", 'success')
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route('/login/', methods=['GET'])
def login():
    return render_template("user/login.html", current_user=current_user)


@blueprint.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    if request.args.get('persona', None):
        return 'OK'
    else:
        flash('You are logged out.', 'info')
        return redirect(url_for('public.home'))

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


@blueprint.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User.create(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data,
                        active=True)
        flash("Thank you for registering. You can now log in.", 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route("/about/")
def about():
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)
