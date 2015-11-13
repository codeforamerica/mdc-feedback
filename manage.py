#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os

from flask import current_app
from flask_script import Manager, Shell, Server
from flask_migrate import MigrateCommand

from feedback.app import create_app
from feedback.database import db
from feedback.settings import (
    DevelopmentConfig, ProductionConfig,
    StagingConfig, TestingConfig
)
from feedback.surveys.constants import ROUTES


app = create_app()
HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {
        'app': app
    }


@manager.option('-e', '--email', dest='email', default=None)
@manager.option('-s', '--section', dest='section', default=None)
def seed_stakeholder(email, section):
    ''' Creates a new stakeholder.
    '''
    from feedback.surveys.models import Stakeholder
    seed_email = email if email else app.config.get('SEED_EMAIL')
    try:
        section_title = ROUTES[int(section)]
        stakeholder_exists = Stakeholder.query.filter(Stakeholder.id == int(section)).first()
        if stakeholder_exists:
            current_app.logger.info(
                'Stakeholder for Section {0} ({1}) already exists'.format(
                    section,
                    section_title))
        else:
            new_stakeholder = Stakeholder.create(
                email_list=seed_email,
                id=int(section),
                label=ROUTES[int(section)]
            )
            db.session.add(new_stakeholder)
            db.session.commit()
            current_app.logger.info(
                'Stakeholder for Section {0} successfully created!'.format(
                    section_title))
    except Exception, e:
        current_app.logger.error(
            'Something went wrong: {exception}'.format(exception=e.message))
    return


@manager.option('-e', '--email', dest='email', default=None)
@manager.option('-r', '--role', dest='role', default=None)
def seed_user(email, role):
    '''
    Creates a new user in the database.
    '''
    from feedback.user.models import User
    seed_email = email if email else app.config.get('SEED_EMAIL')
    user_exists = User.query.filter(User.email == seed_email).first()
    if user_exists:
        current_app.logger.info(
            'User {email} already exists'.format(email=seed_email))
    else:
        try:
            new_user = User.create(
                email=seed_email,
                created_at=datetime.datetime.utcnow(),
                role_id=int(role)
            )
            db.session.add(new_user)
            db.session.commit()
            current_app.logger.info(
                'User {email} successfully created!'.format(
                    email=seed_email))
        except Exception, e:
            current_app.logger.error(
                'Something went wrong: {exception}'.format(exception=e.message))
    return


@manager.command
def seed_roles():
    from feedback.user.models import Role

    try:
        db.session.add(Role.create(name='admin'))
        db.session.add(Role.create(name='user'))
        db.session.commit()
    except Exception, e:
        current_app.logger.error(
            'SEEDERROR | Error: {}'.format(
                e
            )
        )
        return False


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code

manager.add_command('server', Server(port=os.environ.get('PORT', 9000)))
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
