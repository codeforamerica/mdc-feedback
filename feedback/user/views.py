# -*- coding: utf-8 -*-

from flask import (
    Blueprint, render_template, redirect,
    url_for, flash, current_app
)
from flask.ext.login import (
    current_user, login_required
)
from feedback.user.models import User
from feedback.user.forms import UserForm
from feedback.decorators import requires_roles

blueprint = Blueprint(
    "user", __name__, url_prefix='/users',
    template_folder='../templates',
    static_folder="../static"
)


@blueprint.route('/create', methods=['POST'])
@requires_roles('superadmin')
def user_create():
    form = UserForm()
    if form.validate_on_submit():
        current_app.logger.info(
            'USER CREATED with email {}'.format(form.email.data)
        )
        User.create(email=form.email.data,
                    full_name=form.full_name.data,
                    role_id=form.role_id.data)

    flash('Created a new profile.', 'alert-success')
    return redirect(url_for('user.user_manage'))


@blueprint.route('/delete/<id>', methods=['POST'])
@requires_roles('superadmin')
def user_delete(id):
    current_app.logger.info(
        'USER DELETED with email {}'.format(id)
    )
    user = User.query.get(id)
    user.delete()
    flash('Deleted a profile.', 'alert-success')
    return redirect(url_for('user.user_manage'))


@blueprint.route('/manage', methods=['GET', 'POST'])
@requires_roles('superadmin', 'admin')
def user_manage():
    form = UserForm()
    users = User.query.order_by(User.role_id).all()
    return render_template("user/manage.html", current_user=current_user, users=users, form=form, title='Manage Users')


@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('users/profile.html', current_user=current_user)
