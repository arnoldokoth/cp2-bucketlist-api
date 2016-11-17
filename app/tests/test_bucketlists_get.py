import json
import unittest

from test_setup import TestSetup


class TestBucketListsGet(TestSetup):

    # Endpoint: /bucketlists -> GET
    def test_get_bucket_list_without_creation(self):
        response = self.app.get('/bucketlists',
                                content_type='application/json',
                                headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'no bucketlist found')

    def test_invalid_page_value_in_get_url(self):
        response = self.app.get('/bucketlists?page=sdnkfs',
                                content_type='application/json',
                                headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'Invalid Page Value')

    def test_invalid_limit_value_in_get_url(self):
        response = self.app.get('/bucketlists?limit=sdnkfs',
                                content_type='application/json',
                                headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'Invalid Limit Value')

    # Endpoint: /bucketlists/<int:bucketlist_id> -> GET
    def test_get_with_invalid_url(self):
        response = self.app.get('/bucketlists/nkjn',
                                content_type='application/json',
                                headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'You entered an invalid URL')

    def test_get_bucketlist_with_inexistent_bucketlist_id(self):
        response = self.app.get('/bucketlists/1000',
                                content_type='application/json',
                                headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'bucket list not found')

if __name__ == '__main__':
    unittest.main()
