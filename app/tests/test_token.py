import unittest

from test_setup import TestSetup


class TestToken(TestSetup):

    def test_manipulated_token(self):
        self.headers['Authorization'] += "sdfklsd"
        response = self.app.get('/bucketlists',
                                content_type='application/json',
                                headers=self.headers)
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
