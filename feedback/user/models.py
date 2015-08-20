# -*- coding: utf-8 -*-
import datetime as dt

from flask_login import UserMixin
from feedback.database import (
    Column, Model, db, ReferenceCol, SurrogatePK
)


class Role(SurrogatePK, Model):
    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('User', lazy='dynamic', backref='role')

    def __repr__(self):
        return '<Role({name})>'.format(name=self.name)

    def __unicode__(self):
        return self.name


class User(Model, UserMixin):
    __tablename__ = 'user'

    email = db.Column(db.String(80), primary_key=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    full_name = db.Column(db.String(60), nullable=True)
    active = db.Column(db.Boolean(), default=True)
    role_id = ReferenceCol('roles', ondelete='SET NULL', nullable=True)

    @property
    def __repr__(self):
        return '<User({email!r})>'.format(email=self.email)

    def get_id(self):
        return self.email

    def print_pretty_name(self):
        if self.full_name:
            return self.full_name
        else:
            return self.email
