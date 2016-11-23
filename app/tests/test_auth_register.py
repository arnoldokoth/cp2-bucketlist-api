import json
import unittest

from test_setup import TestSetup


class TestAuthRegister(TestSetup):
    # Endpoint: /auth/register -> POST
    def test_registration_without_username_and_password(self):
        credentials = {}
        response = self.app.post('/auth/register',
                                 data=json.dumps(credentials),
                                 content_type='application/json')
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'Username/Password Not Provided!')

    def test_registration_without_username(self):
        credentials = {'password': 'thepassword'}
        response = self.app.post('/auth/register',
                                 data=json.dumps(credentials),
                                 content_type='application/json')
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'Username/Password Not Provided!')

    def test_registration_without_password(self):
        credentials = {'username': 'theuser'}
        response = self.app.post('/auth/register',
                                 data=json.dumps(credentials),
                                 content_type='application/json')
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'Username/Password Not Provided!')

    def test_duplicate_user_registration(self):
        credentials = {'username': 'testuser', 'password': 'testpassword'}
        response = self.app.post('/auth/register',
                                 data=json.dumps(credentials),
                                 content_type='application/json')
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'User already exists!')

    def test_successful_user_registration(self):
        credentials = {'username': 'user_one', 'password': 'password_one'}
        response = self.app.post('/auth/register',
                                 data=json.dumps(credentials),
                                 content_type='application/json')
        self.assertEqual(str(json.loads(response.get_data())['user']),
                         credentials['username'])
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'login endpoint: localhost:5000/auth/login')
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
