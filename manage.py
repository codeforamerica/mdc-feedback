#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask_script import Manager, Shell, Server
from flask_migrate import MigrateCommand

from feedback.app import create_app
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
    return { 'app': app }

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
