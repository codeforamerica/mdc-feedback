import datetime
from app import db
from sqlalchemy.dialects.postgresql import JSON

# https://pythonhosted.org/Flask-SQLAlchemy/models.html

class Survey(db.Model):
    __tablename__ = 'surveys'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    lang = db.Column(db.String(2), nullable=False)
    quiz_id = db.Column(db.Integer)
    list_choice_1 = db.Column(db.String(255))
    list_choice_2 = db.Column(db.String(255))
    textfield_1 = db.Column(db.String(255))
    textarea_1 = db.Column(db.Text)
    textarea_2 = db.Column(db.Text)
    opinionscale_1 = db.Column(db.Integer)

    def __init__(self, lang, quiz_id, list_choice_1, list_choice_2, textfield_1, textarea_1, textarea_2, opinionscale_1):
        self.lang = lang
        self.quiz_id = quiz_id
        self.list_choice_1 = list_choice_1
        self.list_choice_2 = list_choice_2
        self.textfield_1 = textfield_1
        self.textarea_1 = textarea_1
        self.textarea_2 = textarea_2
        self.opinionscale_1 = opinionscale_1

    def __repr__(self):
        return '<id {}>'.format(self.id)
