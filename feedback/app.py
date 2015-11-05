# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""

import sys
import logging
import os

from flask import Flask, render_template
from werkzeug.utils import import_string

from feedback.settings import (
    ProductionConfig, StagingConfig, DevelopmentConfig
)
from feedback.assets import assets, test_assets
from feedback.extensions import (
    db, ma, login_manager,
    migrate, debug_toolbar,
    cache, mail
)
from feedback.utils import thispage

from feedback import (
    public, user,
    dashboard, surveys,
    reports
)

login_manager.login_view = "public.login"


def create_app():
    """An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/
    :param config: The configuration object to use.
    """
    #print os.environ
    config_string = os.environ['CONFIG']
    if isinstance(config_string, basestring):
        config = import_string(config_string)
    else:
        config = config_string

    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_jinja_extensions(app)

    @app.before_first_request
    def before_first_request():
        config_string = os.environ['CONFIG']
        register_logging(app, config_string)

    # import pdb; pdb.set_trace()

    return app


def register_extensions(app):
    test_assets.init_app(app) if app.config.get('TESTING') else assets.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    debug_toolbar.init_app(app)
    mail.init_app(app)
    return None


def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(dashboard.views.blueprint)
    app.register_blueprint(surveys.views.blueprint)
    app.register_blueprint(reports.views.blueprint)
    return None


def register_jinja_extensions(app):
    app.jinja_env.globals['thispage'] = thispage
    return None


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        app.logger.exception(error)

        return render_template("errors/{0}.html".format(error_code)), error_code

    for errcode in [401, 403, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_logging(app, config_string):
    if 'staging' in config_string.lower():
        app.logger.removeHandler(app.logger.handlers[0])

        app.logger.setLevel(logging.DEBUG)
        stdout = logging.StreamHandler(sys.stdout)
        stdout.setFormatter(logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s in %(module)s [%(pathname)s:%(lineno)d]: %(message)s'))
        app.logger.addHandler(stdout)

    elif 'test' in config_string.lower():
        app.logger.setLevel(logging.CRITICAL)

    else:
        # log to console for dev
        app.logger.setLevel(logging.DEBUG)

    return None
