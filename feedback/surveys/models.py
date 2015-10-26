# -*- coding: utf-8 -*-
from feedback.database import (
    Column, db, Model
)
from feedback.surveys.constants import (
    ROLES, PURPOSE, ROUTES,
    BEST, WORST
)


class Stakeholder(Model):
    ''' Stakeholder model - each field contains a
    string of e-mails separated by commas.
    '''
    __tablename__ = 'stakeholders'

    id = Column(db.Integer, primary_key=True, index=True)
    email_list = Column(db.String(200), nullable=True)
    label = Column(db.String(50), unique=True, nullable=True)

    def __repr__(self):
        return '<Stakeholder(id:{0})>'.format(self.id)


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
    purpose_other = Column(db.String(500), nullable=True)
    route = Column(db.Integer, nullable=True)
    rating = Column(db.Integer, nullable=False)
    get_done = Column(db.Boolean(), default=False)
    best = Column(db.Integer, nullable=True)
    best_other = Column(db.String(500), nullable=True)
    worst = Column(db.Integer, nullable=True)
    worst_other = Column(db.String(500), nullable=True)
    improvement = Column(db.String(500), nullable=True)
    follow_up = Column(db.Boolean(), default=False)
    contact = Column(db.String(500), nullable=True)
    more_comments = Column(db.String(2000), nullable=True)

    @property
    def role_en(self):
        return ROLES[self.role]

    @property
    def route_en(self):
        try:
            return ROUTES[self.route]
        except KeyError:
            return self.route

    @property
    def best_en(self):
        if self.best_other is None:
            return BEST[self.best]
        else:
            return self.best_other

    @property
    def worst_en(self):
        if self.worst_other is None:
            return WORST[self.worst]
        else:
            return self.worst_other

    @property
    def purpose_en(self):
        if self.purpose_other is None:
            return PURPOSE[self.purpose]
        else:
            return self.purpose_other

    def __repr__(self):
        return '<Survey(id:{0} tracking:{1})>'.format(self.id, self.source_id)
