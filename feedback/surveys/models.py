# -*- coding: utf-8 -*-
from feedback.database import (
    Column, db, Model
)


class Survey(Model):
    ''' Survey model is the now the base for the PIC
    feedback survey. This is the result of ETLs from
    both Typeform and TextIt, both English and Spanish
    versions. We've decided to do it this way also
    because there now needs to be a record to save every
    time a form is filled.
    '''
    __tablename__ = 'survey'

    id = Column(db.Integer, primary_key=True, index=True)
    source_id = Column(db.String(50), nullable=False)
    lang = Column(db.String(2), nullable=False, default='en')
    method = Column(db.String(3), nullable=False)
    date_submitted = Column(db.DateTime, nullable=False, index=True)
    role = Column(db.Integer, nullable=False)
    purpose = Column(db.Integer, nullable=False)
    purpose_other = Column(db.String(200), nullable=True)
    route = Column(db.Integer, nullable=True)
    rating = Column(db.Integer, nullable=False)
    get_done = Column(db.Boolean(), default=False)
    best = Column(db.Integer, nullable=True)
    best_other = Column(db.String(200), nullable=True)
    worst = Column(db.Integer, nullable=True)
    worst_other = Column(db.String(200), nullable=True)
    improvement = Column(db.Integer, nullable=True)
    improvement_other = Column(db.String(200), nullable=True)
    follow_up = Column(db.Boolean(), default=False)
    contact = Column(db.String(50), nullable=True)
    more_comments = Column(db.String(2000), nullable=True)

    def __repr__(self):
        return '<Survey(id:{0} tracking:{1})>'.format(self.id, self.source_id)
