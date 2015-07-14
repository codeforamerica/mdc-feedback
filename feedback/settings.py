import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    BROWSERID_URL = 'http://localhost:5000'


class ProductionConfig(Config):
    ENV = 'prod'
    DEBUG = False
    BROWSERID_URL = 'http://mdc-feedback.heroku.com/'

class StagingConfig(Config):
    ENV = 'stage'
    DEVELOPMENT = True
    DEBUG = True
    BROWSERID_URL = 'http://mdc-feedback-stage.heroku.com'


class DevelopmentConfig(Config):
    ENV = 'dev'
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/feedback_test"
