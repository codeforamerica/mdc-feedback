# -*- coding: utf-8 -*-

from flask import (
    Blueprint, render_template, redirect,
    url_for, flash
)
from flask.ext.login import (
    login_required
)
from feedback.user.models import User
from feedback.decorators import requires_roles

blueprint = Blueprint(
    "user", __name__, url_prefix='/users',
    template_folder='../templates',
    static_folder="../static"
)


@blueprint.route('/delete/<id>', methods=['POST'])
@requires_roles('superadmin')
def user_delete(id):
    user = User.query.get(id)
    user.delete()
    flash('Deleted a profile.', 'alert-success')
    return redirect(url_for('user.user_manage'))


@blueprint.route('/manage', methods=['GET', 'POST'])
@requires_roles('superadmin')
def user_manage():
    users = User.query.order_by(User.role_id).all()
    return render_template("user/manage.html", users=users, title='Manage Users')


@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('users/profile.html', user=current_user)
