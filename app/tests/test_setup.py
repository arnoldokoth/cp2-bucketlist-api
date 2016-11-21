import json
import unittest
from app.app import app, db


class TestSetup(unittest.TestCase):

    def setUp(self):
        # Create Test User
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tests/tests.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        self.app = app.test_client()
        db.create_all()
        credentials = {'username': 'testuser', 'password': 'testpassword'}
        self.app.post('/auth/register', data=json.dumps(credentials),
                      content_type='application/json')

        response = self.app.post('/auth/login',
                                 data=json.dumps(credentials),
                                 content_type='application/json')
        token = json.loads(response.get_data().decode())['token']
        self.headers = {
            'Authorization': 'Token ' + token
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
