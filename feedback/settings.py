# -*- coding: utf-8 -*-
import os

os_env = os.environ

class Config(object):
    DEBUG = False
    TESTING = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    BROWSERID_URL = 'http://localhost:9000'
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.


class ProductionConfig(Config):
    ENV = 'prod'
    DEBUG = False
    BROWSERID_URL = 'http://mdc-feedback.herokuapp.com/'

class StagingConfig(Config):
    ENV = 'stage'
    DEVELOPMENT = True
    DEBUG = True
    BROWSERID_URL = 'http://mdc-feedback-stage.heroku.com'


class DevelopmentConfig(Config):
    ENV = 'dev'
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = os_env.get('DATABASE_URL','postgresql://localhost/feedback_dev')
    DEBUG = True
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    BROWSERID_URL = 'http://localhost:9000'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os_env.get('TEST_DATABASE_URL','postgresql://localhost/feedback_test')
