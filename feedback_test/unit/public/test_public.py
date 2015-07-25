# -*- coding: utf-8 -*-

from mock import Mock, patch
from flask.ext.login import login_user

from feedback_test.unit.test_base import BaseTestCase
from feedback_test.unit.util import insert_a_user
from feedback.user.models import User


class TestLoginAuth(BaseTestCase):
    render_template = True

    def setUp(self):
        super(TestLoginAuth, self).setUp()
        self.email = 'foo@foo.com'
        insert_a_user(email=self.email)

    def test_login_route(self):
        '''
        Test the login route works propertly
        '''
        request = self.client.get('/login')
        self.assert200(request)
        self.assert_template_used('user/login.html')

    @patch('urllib2.urlopen')
    def test_auth_persona_failure(self, urlopen):
        '''
        Test that we reject when persona throws bad statuses to us
        '''
        mock_open = Mock()
        mock_open.read.side_effect = ['{"status": "error"}']
        urlopen.return_value = mock_open

        post = self.client.post('/auth', data=dict(
            assertion='test'
        ))

        self.assert403(post)

    @patch('urllib2.urlopen')
    def test_auth_no_user(self, urlopen):
        '''
        Test that we reject bad email addresses
        '''
        mock_open = Mock()
        mock_open.read.side_effect = ['{"status": "okay", "email": "not_a_valid_email"}']
        urlopen.return_value = mock_open

        post = self.client.post('/auth', data=dict(
            assertion='test'
        ))

        self.assert403(post)

    @patch('urllib2.urlopen')
    def test_logout(self, urlopen):
        '''
        Test that we can logout properly
        '''

        login_user(User.query.all()[0])

        logout = self.client.get('/logout', follow_redirects=True)
        self.assertTrue('You are logged out' in logout.data)
        self.assert_template_used('user/logout.html')

        login_user(User.query.all()[0])
        logout = self.client.post('/logout?persona=True', follow_redirects=True)
        self.assertTrue(logout.data, 'OK')
