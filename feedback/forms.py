from flask_wtf import Form
from wtforms import fields

class SurveyForm(Form):
    @classmethod
    # Always use cls for the first argument to class methods.
    def append_field(cls, name, field):
        setattr(cls, name, field)
        return cls

    title_en = fields.TextField()
    title_es = fields.TextField()
    description_en = fields.TextField()
    description_es = fields.TextField()

class ProfileForm(Form):
    first_name = fields.TextField()
    last_name = fields.TextField()
