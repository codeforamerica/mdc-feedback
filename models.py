import datetime
from app import db
from sqlalchemy.dialects.postgresql import JSON

class Survey(db.Model):
    __tablename__ = 'surveys'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    survey_type = db.Column(db.String(255), nullable=False)
    q1 = db.Column(db.Integer, nullable=False)

    def __init__(self, survey_type, q1):
        self.survey_type = survey_type
        self.q1 = q1

    def __repr__(self):
        return '<id {}>'.format(self.id)
