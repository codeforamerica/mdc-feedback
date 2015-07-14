# -*- coding: utf-8 -*-
import datetime as dt

from flask_login import UserMixin
from feedback.database import db

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    email = db.Column(db.String(80), primary_key=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    active = db.Column(db.Boolean(), default=True)

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __repr__(self):
        return '<User({email!r})>'.format(email=self.email)

    def get_id(self):
        return self.email
