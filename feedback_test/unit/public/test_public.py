# -*- coding: utf-8 -*-

from mock import Mock, patch
from flask.ext.login import login_user

from feedback_test.unit.test_base import BaseTestCase
from feedback_test.unit.util import insert_a_user


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
