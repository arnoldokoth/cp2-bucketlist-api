import unittest

from app.models.models import User, BucketList, BucketListItems
from app.app import db, app


class TestSetup(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tests/tests.db'
        # Create a Test Client
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
