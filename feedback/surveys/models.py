# -*- coding: utf-8 -*-
from feedback.database import (
    Column, db, Model
)
from feedback.surveys.constants import (
    ROLES, PURPOSE, ROUTES,
    BEST, WORST
)


class Monthly(Model):
    ''' The monthly report model - this only contains
    one field: a string of e-mails separated by commas
    if necessary.
    '''
    __tablename__ = 'monthly-report'

    id = Column(db.Integer, primary_key=True, index=True)
    email_list = Column(db.String(200), nullable=True)

    def __repr__(self):
        return '<Monthly(id:{0}, emails:{1})>'.format(
            self.id,
            self.email_list)


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
        try:
            return ROLES[self.role]
        except KeyError:
            return self.route

    @property
    def route_en(self):
        try:
            return ROUTES[self.route]
        except KeyError:
            return self.route

    @property
    def best_en(self):
        return get_en(
            self.best,
            self.best_other,
            BEST)

    @property
    def worst_en(self):
        return get_en(
            self.worst,
            self.worst_other,
            WORST)

    @property
    def purpose_en(self):
        return get_en(
            self.purpose,
            self.purpose_other,
            PURPOSE)

    def __repr__(self):
        return '<Survey(id:{0} tracking:{1})>'.format(self.id, self.source_id)


def get_en(x, x_other, X_DICT):
    if x_other is None:
        try:
            return X_DICT[x]
        except KeyError:
            return x
    else:
        return x_other
