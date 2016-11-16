import json
import unittest

from test_setup import TestSetup


class TestAuthLogin(TestSetup):

    # Endpoint: /auth/login -> POST
    def test_login_without_username_and_password(self):
        credentials = {}
        response = self.app.post('/auth/login',
                                 data=json.dumps(credentials),
                                 content_type='application/json')
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'Username/Password Not Provided!')

    def test_login_without_username(self):
        credentials = {'password': 'testpassword'}
        response = self.app.post('/auth/login',
                                 data=json.dumps(credentials),
                                 content_type='application/json')
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'Username/Password Not Provided!')

    def test_login_without_password(self):
        credentials = {'username': 'testuser'}
        response = self.app.post('/auth/login',
                                 data=json.dumps(credentials),
                                 content_type='application/json')
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'Username/Password Not Provided!')

    def test_successful_user_login(self):
        credentials = {'username': 'testuser', 'password': 'testpassword'}
        response = self.app.post('/auth/login',
                                 data=json.dumps(credentials),
                                 content_type='application/json')
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'Hello, {0}'.format(credentials['username']))

if __name__ == '__main__':
    unittest.main()
