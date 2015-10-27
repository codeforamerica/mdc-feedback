# -*- coding: utf-8 -*-


from flask import (
    redirect, flash, request
)
from flask_login import current_user
from functools import wraps


def requires_roles(*roles):
    '''
    Takes in a list of roles and checks whether the user
    has access to those role
    '''
    def check_roles(view_function):
        @wraps(view_function)
        def decorated_function(*args, **kwargs):

            if not current_user.role or current_user.role.name not in roles:
                flash('You do not have sufficent permissions to do that!', 'alert-danger')
                return redirect(request.args.get('next') or '/')
            return view_function(*args, **kwargs)
        return decorated_function
    return check_roles
