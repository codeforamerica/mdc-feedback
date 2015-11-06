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
    SQLALCHEMY_DATABASE_URI = os_env.get('DATABASE_URL')
    BROWSERID_URL = os_env.get('BROWSERID_URL')
    SERVER_NAME = os_env.get('BROWSERID_URL')
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    ADMIN_EMAIL = os_env.get('ADMIN_EMAIL', 'ehsiung@codeforamerica.org')
    CITY_DOMAINS = ['miamidade.gov', 'codeforamerica.org']
    MAIL_USERNAME = os_env.get('MAIL_USERNAME')
    MAIL_PASSWORD = os_env.get('MAIL_PASSWORD')
    MAIL_SERVER = os_env.get('MAIL_SERVER')
    MAIL_DEFAULT_SENDER = os_env.get('MAIL_DEFAULT_SENDER', 'no-reply@miamidade.gov')
    FEEDBACK_SENDER = os_env.get('FEEDBACK_SENDER', 'feedbackbot@miamidade.gov')
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True


class ProductionConfig(Config):
    ENV = 'prod'
    DEBUG = False
    BROWSERID_URL = os_env.get('BROWSERID_URL', 'http://mdc-feedback.herokuapp.com/')


class StagingConfig(Config):
    ENV = 'stage'
    DEVELOPMENT = True
    DEBUG = True
    MAIL_USERNAME = os_env.get('SENDGRID_USERNAME')
    MAIL_PASSWORD = os_env.get('SENDGRID_PASSWORD')
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_MAX_EMAILS = 100


class DevelopmentConfig(Config):
    ENV = 'dev'
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = os_env.get('DATABASE_URL', 'postgresql://localhost/feedback_dev')
    DEBUG = True
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets
    BROWSERID_URL = os_env.get('BROWSERID_URL', 'http://localhost:9000')
    MAIL_SERVER = 'smtp.gmail.com'  # Use gmail in dev: https://support.google.com/mail/answer/1173270?hl=en
    ADMIN_EMAIL = os_env.get('ADMIN_EMAIL', 'mdcfeedbackdev@gmail.com')
    MAIL_USERNAME = 'mdcfeedbackdev@gmail.com'
    MAIL_PASSWORD = 'miamidade305'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_SUPPRESS_SEND = True


class TestingConfig(Config):
    ADMIN_EMAIL = 'foo@foo.com'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os_env.get('TEST_DATABASE_URL', 'postgresql://localhost/feedback_test')
    MAIL_SUPPRESS_SEND = True
