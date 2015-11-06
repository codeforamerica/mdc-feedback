# -*- coding: utf-8 -*-

import re

import datetime
today = datetime.date.today()

from flask import (
    Blueprint, render_template, redirect,
    url_for, request, flash, current_app
)
from flask.ext.login import (
    current_user, login_required
)

from feedback.database import db, get_object_or_404

from feedback.user.models import User
from feedback.user.forms import UserForm
from feedback.decorators import requires_roles

from feedback.surveys.constants import ROUTES
from feedback.surveys.models import Stakeholder
from feedback.reports.models import Monthly

blueprint = Blueprint(
    "user", __name__, url_prefix='/users',
    template_folder='../templates',
    static_folder="../static"
)


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
            stakeholder = Stakeholder.query.filter_by(label=label).first()
            if not stakeholder:
                stakeholder = Stakeholder(
                    label=label,
                    email_list=value
                )
            else:
                stakeholder.update(email_list=value)
            db.session.add(stakeholder)
        else:
            errors = True
            db.session.rollback()

    if not errors:
        db.session.commit()
        flash("Your settings have been saved!", "alert-success")

    return redirect(url_for('user.user_manage'))


@blueprint.route('/create', methods=['GET', 'POST'])
@requires_roles('admin')
def user_create():
    form = UserForm()
    if form.validate_on_submit():
        current_app.logger.info(
            'USER CREATED with email {}'.format(form.email.data)
        )
        User.create(
            email=form.email.data,
            full_name=form.full_name.data,
            role_id=form.role_id.data)

        flash('Created a new profile.', 'alert-success')
        return redirect(url_for('user.user_manage'))
    else:
        return render_template(
            'user/add-edit.html',
            form=form,
            date=today.strftime('%B %d, %Y'),
            form_action=url_for('user.user_create'),
            title='Add User',
            action='Add User')


@blueprint.route('/edit/<id>', methods=['GET', 'POST'])
@requires_roles('admin')
def user_edit(id):
    user = get_object_or_404(User, User.id == id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.update(
            full_name=form.full_name.data,
            email=form.email.data,
            role_id=form.role_id.data
        )
        flash('Profile changes saved.', 'alert-success')
        current_app.logger.info(
            'url_for of user.user_mange is: {}'.format(url_for('user.user_manage')))

        return redirect(url_for('user.user_manage'))
    else:
        return render_template(
            'user/add-edit.html',
            form=form,
            date=today.strftime('%B %d, %Y'),
            form_action=url_for('user.user_edit', id=id),
            title='Edit User',
            action='Save Changes')


@blueprint.route('/delete/<id>', methods=['POST'])
@requires_roles('admin')
def user_delete(id):
    current_app.logger.info(
        'USER DELETED with email {}'.format(id)
    )
    user = get_object_or_404(User, User.id == id)
    user.delete()
    flash('Profile successfully deleted.', 'alert-success')
    return redirect(url_for('user.user_manage'))


def set_form():
    form = UserForm()
    users = User.query.order_by(User.role_id).all()
    stakeholders = Stakeholder.query.order_by(Stakeholder.id).all()
    monthly_admins = Monthly.query.first()

    return render_template(
        "user/manage.html",
        current_user=current_user,
        users=users,
        date=today.strftime('%B %d, %Y'),
        routes=ROUTES,
        form=form,
        stakeholders=stakeholders,
        monthly=monthly_admins,
        title='Manage Users')


@blueprint.route('/manage', methods=['GET', 'POST'])
@requires_roles('admin')
def user_manage():

    if request.method == 'POST':
        return process_stakeholders_form(request.form)
    return set_form()


@blueprint.route('/monthly/manage', methods=['POST'])
@requires_roles('admin')
def monthly_manage():
    errors = False

    if request.method == 'POST':
        value = request.form['monthly-report-field']
        if is_valid_email_list(value):
            stakeholder = Monthly.query.first()
            if not stakeholder:
                stakeholder = Monthly(
                    email_list=value
                )
            else:
                stakeholder.update(email_list=value)
            db.session.add(stakeholder)
        else:
            errors = True

        if not errors:
            db.session.commit()
            flash("Your settings have been saved!", "alert-success")

        return redirect(url_for('user.user_manage'))

    return set_form()


@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template(
        'users/profile.html',
        current_user=current_user)
