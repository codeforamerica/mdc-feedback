# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template

from feedback.settings import ProductionConfig, DevelopmentConfig
from feedback.assets import assets
from feedback.extensions import (
    db,
    login_manager,
    migrate
)
# from feedback.utils import thispage

from feedback import public, user

def create_app(config_object=ProductionConfig):
    """An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    assets.init_app(app)
    '''
    bcrypt.init_app(app)
    cache.init_app(app)
    debug_toolbar.init_app(app)
    '''
    return None

def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    # app.jinja_env.globals['thispage'] = thispage
    return None

def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)

        return render_template("{0}.html".format(error_code))

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
