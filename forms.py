from flask_wtf import Form
from wtforms import fields

class SurveyForm(Form):
    title_en = fields.TextField()
    title_es = fields.TextField()
    description_en = fields.TextField()
    description_es = fields.TextField()
