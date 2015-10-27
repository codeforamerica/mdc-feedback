# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms.fields import TextField, RadioField
from wtforms.validators import Email


class UserForm(Form):
    full_name = TextField()
    email = TextField(
        validators=[Email()],
        default='No email provided')
    role_id = RadioField('Permissions', choices=[
        ('2', 'Regular users <span class="small">can view the main dashboard, a table view of all surveys (including open-ended questions) and access to the detail view to link to a particular survey if necessary. They are limited to e-mail addresses with a miamidade.gov domain.</span>'),
        ('1', 'Admins <span class="small">have the ability to do what logged in users can do, plus edit section stakeholder e-mails, download bulk data in csv format and change the permissions of other users.</span>')])

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.user = None
