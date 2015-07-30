# -*- coding: utf-8 -*-
from feedback.database import (
    Column, db, Model
)

# https://pythonhosted.org/Flask-SQLAlchemy/models.html
class Survey(Model):
    __tablename__ = 'survey'

    id = Column(db.Integer, primary_key=True, index=True)
    title_en = Column(db.String(255))
    title_es = Column(db.String(255))
    description_en = Column(db.String(255))
    description_es = Column(db.String(255))
    questions = db.relationship('Question', backref='survey')

    def __init__(self, title_en, title_es, description_en, description_es):
        self.title_en = title_en
        self.title_es = title_es
        self.description_en = description_en
        self.description_es = description_es

    def __repr__(self):
        return '<Survey {0}: {1}>'.format(self.id, self.title_en)

class Question(Model):
    __tablename__ = 'question'

    id = Column(db.Integer, primary_key=True, index=True)
    question_en = Column(db.String(255))
    question_es = Column(db.String(255))
    question_type = Column(db.String(255))
    survey_id = Column(db.Integer, db.ForeignKey('survey.id'))

    def __init__(self, question_en, question_es, question_type, survey_id):
        self.question_en = question_en
        self.question_es = question_es
        self.question_type = question_type
        self.survey_id = survey_id

    def __repr__(self):
        return '<Question {0}, {1}>'.format(self.id, self.survey_id)
