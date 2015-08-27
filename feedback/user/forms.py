# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms.fields import TextField, RadioField
from wtforms.validators import Email


class UserForm(Form):
    full_name = TextField()
    email = TextField(validators=[Email()], default='No email provided')
    role_id = RadioField('Permissions', choices=[
                         ('1', 'Superuser <span class="small">Can edit everything.</span>'),
                         ('2', 'User <span class="small">Can do everything but manage users</span>')])
