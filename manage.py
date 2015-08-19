#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os

from flask_script import Manager, Shell, Server
from flask_migrate import MigrateCommand

from feedback.app import create_app
from feedback.database import db
from feedback.settings import DevelopmentConfig, ProductionConfig, StagingConfig, TestingConfig

if os.environ.get("CPCO_ENV") == 'prod':
    app = create_app(ProductionConfig)
else:
    app = create_app(DevelopmentConfig)

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
@manager.option('-r', '--role', dest='role', default=None)
def seed_user(email, role):
    '''
    Creates a new user in the database.
    '''
    from feedback.users.models import User
    seed_email = email if email else app.config.get('SEED_EMAIL')
    user_exists = User.query.filter(User.email == seed_email).first()
    if user_exists:
        print 'User {email} already exists'.format(email=seed_email)
    else:
        try:
            new_user = User.create(
                email=seed_email,
                created_at=datetime.datetime.utcnow(),
                role_id=role
            )
            db.session.add(new_user)
            db.session.commit()
            print 'User {email} successfully created!'.format(email=seed_email)
        except Exception, e:
            print 'Something went wrong: {exception}'.format(exception=e.message)
    return


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
