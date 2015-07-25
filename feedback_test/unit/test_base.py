# -*- coding: utf-8 -*-

from mock import Mock, patch
from flask.ext.testing import TestCase

from feedback.settings import TestingConfig
from feedback.app import create_app as _create_app, db

class BaseTestCase(TestCase):
    '''
    A base test case that boots our app
    '''
    def create_app(self):
        return _create_app(TestingConfig)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.get_engine(self.app).dispose()

    def assertTemplatesUsed(self, names, tmpl_name_attribute='name'):
        '''
        Subclass assertTemplateUsed from the flask-testing TestCase to
        allow for multiple templates
        '''
        if isinstance(names, basestring):
            names = [names]

        used_templates = []

        for template, context in self.templates:
            if getattr(template, tmpl_name_attribute) in names:
                return True

            used_templates.append(template.name)

        raise AssertionError("template %s not used. Templates were used: %s" % (names, ' '.join(used_templates)))

    assert_template_used = assertTemplatesUsed

    @patch('urllib2.urlopen')
    def login_user(self, user, urlopen):
        _email = user.email if user else 'foo@foo.com'
        mock_open = Mock()
        mock_open.read.side_effect = ['{"status": "okay", "email": "' + _email + '"}']
        urlopen.return_value = mock_open

        self.client.post('/public/auth', data=dict(
            assertion='test'
        ))

    def logout_user(self):
        self.client.post('/public/logout')
