# -*- coding: utf-8 -*-

from flask import (
    Blueprint, render_template, request, flash
)
from flask.ext.login import (
    login_required
)

blueprint = Blueprint(
    "user", __name__, url_prefix='/users',
    template_folder='../templates',
    static_folder="../static"
)

@blueprint.route('/profile', methods=['GET', 'POST'])
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

